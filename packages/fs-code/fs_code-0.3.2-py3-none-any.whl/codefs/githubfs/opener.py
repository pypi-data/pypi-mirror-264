from typing import Any, Union, Mapping, MutableMapping

from fs.opener import Opener as BaseOpener
from fs.opener.errors import OpenerError, NotWriteable
from fs.opener.parse import ParseResult
from github import Github
from schema import Schema, Or, Optional as Opt, Hook, SchemaError  # type: ignore

from codefs._core import Str, Int, Bool
from codefs.githubfs import UserFS, OrgFS


def _validate_credentials(key: str, data: Mapping[str, str], _: Any) -> None:
    keys = data.keys()
    if key == "token" and ("login" in keys or "password" in keys):
        raise SchemaError("cannot pass login or password when passing token")
    if key == "login" and "password" not in keys:
        raise SchemaError("must pass password when passing login")
    if key == "password" and "login" not in keys:
        raise SchemaError("must pass login when passing password")


class Opener(BaseOpener):
    protocols = ["github"]

    schema = Schema(
        {
            Or("user", "org", only_one=True): Str(),
            Hook("token", handler=_validate_credentials): object,
            Opt("token"): Str(),
            Hook("login", handler=_validate_credentials): object,
            Opt("login"): Str(),
            Hook("password", handler=_validate_credentials): object,
            Opt("password"): Str(),
            Opt("timeout"): Int(),
            Opt("user_agent"): Str(),
            Opt("per_page"): Int(),
            Opt("verify"): Or(Bool(), str),
            Opt("retry"): Int(),
            Opt("pool_size"): Int(),
        }
    )

    def open_fs(
        self, fs_url: str, parse_result: ParseResult, writeable: bool, create: bool, cwd: str
    ) -> Union[UserFS, OrgFS]:
        if writeable or create:
            raise NotWriteable

        try:
            kwargs: MutableMapping[str, Any] = self.schema.validate(parse_result.params)
            user = kwargs.pop("user", None)
            org = kwargs.pop("org", None)
            kwargs["login_or_token"] = (
                kwargs.pop("login", None) if kwargs.pop("password", None) else kwargs.pop("token", None)
            )
            if parse_result.resource:
                kwargs["base_url"] = parse_result.resource
            client = Github(**kwargs)
        except Exception as e:
            raise OpenerError(f"failed to create client: {e}")

        return UserFS(client, user) if user else OrgFS(client, org)
