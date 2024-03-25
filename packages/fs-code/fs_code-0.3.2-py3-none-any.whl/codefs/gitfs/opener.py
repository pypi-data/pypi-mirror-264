from dulwich.client import get_transport_and_path
from fs.opener import Opener as BaseOpener
from fs.opener.errors import OpenerError, NotWriteable
from fs.opener.parse import ParseResult

from codefs.gitfs import RepoFS


class Opener(BaseOpener):
    protocols = ["gitfs"]

    def open_fs(self, fs_url: str, parse_result: ParseResult, writeable: bool, create: bool, cwd: str) -> RepoFS:
        if writeable or create:
            raise NotWriteable
        try:
            client, path = get_transport_and_path(parse_result.resource)
        except Exception as e:  # todo: no cover, because I can't get it to fail yet
            raise OpenerError(f"failed to create client: {e}")
        return RepoFS(client, path)
