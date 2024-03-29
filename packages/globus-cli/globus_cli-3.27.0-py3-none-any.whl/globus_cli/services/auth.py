from __future__ import annotations

import typing as t
import uuid

import globus_sdk
import globus_sdk.scopes
from globus_sdk.experimental.scope_parser import Scope


def _is_uuid(s: str) -> bool:
    try:
        uuid.UUID(s)
        return True
    except ValueError:
        return False


class GetIdentitiesKwargs(t.TypedDict, total=False):
    provision: bool
    usernames: str
    ids: str


class CustomAuthClient(globus_sdk.AuthClient):
    def _lookup_identity_field(
        self,
        id_name: str | None = None,
        id_id: str | None = None,
        field: t.Literal["id", "username"] = "id",
        provision: bool = False,
    ) -> str | None:
        assert (id_name or id_id) and not (id_name and id_id)

        kw: GetIdentitiesKwargs = dict(provision=provision)
        if id_name:
            kw["usernames"] = id_name
        elif id_id:
            kw["ids"] = id_id
        else:
            raise NotImplementedError("must provide id or name")

        try:
            value = self.get_identities(**kw)["identities"][0][field]
        # capture any failure to lookup this data, including:
        # - identity doesn't exist (`identities=[]`)
        # - field is missing
        except LookupError:
            return None

        if not isinstance(value, str):
            return None

        return value

    # this method has been added in the latest SDK versions but is not
    # present in the last release
    # this is therefore temporary until an SDK release ships with the change
    # so that CLI testing against SDK main can succeed
    if not hasattr(globus_sdk.AuthClient, "userinfo"):
        userinfo = globus_sdk.AuthClient.oauth2_userinfo

    @t.overload
    def maybe_lookup_identity_id(
        self, identity_name: str, provision: t.Literal[True]
    ) -> str: ...

    @t.overload
    def maybe_lookup_identity_id(
        self, identity_name: str, provision: bool = False
    ) -> str | None: ...

    def maybe_lookup_identity_id(
        self, identity_name: str, provision: bool = False
    ) -> str | None:
        if _is_uuid(identity_name):
            return identity_name
        else:
            return self._lookup_identity_field(
                id_name=identity_name, provision=provision
            )

    def lookup_identity_name(self, identity_id: str) -> str | None:
        return self._lookup_identity_field(id_id=identity_id, field="username")

    def get_consents(self, identity_id: str) -> ConsentForestResponse:
        """
        Get the consent for a given identity_id
        """
        return ConsentForestResponse(
            self.get(f"/v2/api/identities/{identity_id}/consents")
        )


class ConsentForestResponse(globus_sdk.GlobusHTTPResponse):
    @property
    def consents(self) -> list[dict[str, t.Any]]:
        return t.cast("list[dict[str, t.Any]]", self.data["consents"])

    def top_level_consents(self) -> list[dict[str, t.Any]]:
        return [c for c in self.consents if len(c["dependency_path"]) == 1]

    def get_child_consents(self, consent: dict[str, t.Any]) -> list[dict[str, t.Any]]:
        path_length = len(consent["dependency_path"]) + 1
        return [
            c
            for c in self.consents
            if len(c["dependency_path"]) == path_length
            and c["dependency_path"][:-1] == consent["dependency_path"]
        ]

    def contains_scopes(
        self,
        scope_trees: list[Scope] | list[str] | list[globus_sdk.scopes.MutableScope],
    ) -> bool:
        """
        Determine whether or not a user's consents contains the given scope trees.
        """
        scope_trees = _normalize_scope_trees(scope_trees)
        top_level_by_name = _map_consents_by_name(self.top_level_consents())

        for scope in scope_trees:
            if scope.scope_string not in top_level_by_name:
                return False

        trees_to_match = [
            (
                top_level_by_name[s.scope_string],
                s,
            )
            for s in scope_trees
        ]

        while trees_to_match:
            consent, scope = trees_to_match.pop()
            child_consents = _map_consents_by_name(self.get_child_consents(consent))
            for dependency in scope.dependencies:
                if dependency.scope_string not in child_consents:
                    return False
                trees_to_match.append(
                    (child_consents[dependency.scope_string], dependency)
                )
        return True


def _map_consents_by_name(
    consents: list[dict[str, t.Any]]
) -> dict[str, dict[str, t.Any]]:
    return {c["scope_name"]: c for c in consents}


def _normalize_scope_trees(
    scope_trees: list[Scope] | list[str] | list[globus_sdk.scopes.MutableScope],
) -> list[Scope]:
    ret = []
    for scope in scope_trees:
        if isinstance(scope, str):
            ret.extend(Scope.parse(scope))
        elif isinstance(scope, globus_sdk.scopes.MutableScope):
            ret.extend(Scope.parse(str(scope)))
        else:
            ret.append(scope)
    return ret
