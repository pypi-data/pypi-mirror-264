from typing import Any, Union, Mapping, MutableMapping

from fs.opener import Opener as BaseOpener
from fs.opener.errors import NotWriteable, OpenerError
from fs.opener.parse import ParseResult
from gitlab import Gitlab
from schema import SchemaError, Optional as Opt, Schema, Or, Hook  # type: ignore

from codefs._core import Str, Float, Int, Bool
from codefs.gitlabfs import UserFS, GroupFS


def _validate_credentials(key: str, data: Mapping[str, str], _: Any) -> None:
    keys = data.keys()
    if key in ["private_token", "oauth_token", "job_token"]:
        if "http_username" in keys or "http_password" in keys:
            raise SchemaError(f"cannot pass http_username or http_password when passing {key}")
    if key == "http_username" and "http_password" not in keys:
        raise SchemaError("must pass http_password when passing http_username")
    if key == "http_password" and "http_username" not in keys:
        raise SchemaError("must pass http_username when passing http_password")


class Opener(BaseOpener):
    protocols = ["gitlab"]

    schema = Schema(
        {
            Or("user", "group", only_one=True): Str(),
            Hook("private_token", handler=_validate_credentials): object,
            Opt("private_token"): Str(),
            Hook("oauth_token", handler=_validate_credentials): object,
            Opt("oauth_token"): Str(),
            Hook("job_token", handler=_validate_credentials): object,
            Opt("job_token"): Str(),
            Hook("http_username", handler=_validate_credentials): object,
            Opt("http_username"): Str(),
            Hook("http_password", handler=_validate_credentials): object,
            Opt("http_password"): Str(),
            Opt("timeout"): Float(),
            Opt("user_agent"): Str(),
            Opt("order_by"): Str(),
            Opt("pagination"): Str(),
            Opt("per_page"): Int(),
            Opt("ssl_verify"): Bool(),
            Opt("retry_transient_errors"): Bool(),
        }
    )

    def open_fs(
        self, fs_url: str, parse_result: ParseResult, writeable: bool, create: bool, cwd: str
    ) -> Union[UserFS, GroupFS]:
        if writeable or create:
            raise NotWriteable

        try:
            kwargs: MutableMapping[str, Any] = self.schema.validate(parse_result.params)
            user = kwargs.pop("user", None)
            group = kwargs.pop("group", None)
            if parse_result.resource:
                kwargs["url"] = parse_result.resource
            client = Gitlab(**kwargs)
        except Exception as e:
            raise OpenerError(f"failed to create client: {e}")

        return UserFS(client, user) if user else GroupFS(client, group)
