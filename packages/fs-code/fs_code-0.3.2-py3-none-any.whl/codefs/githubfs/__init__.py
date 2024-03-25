"""
These are read-only filesystems which use the GitHub API to download an archive.

Usage with <a target="_blank" href="https://docs.pyfilesystem.org/en/latest/openers.html">FS URL</a>:

```python
import fs

user_fs = fs.open_fs("github://?user=dAnjou")
readme = user_fs.open("dAnjou/main/README.md")
print(readme.read())
```

.. hint::
   You can also access a self-managed GitHub instance. The FS URL would look like this then:
   `github://https://github.example.com?user=USER`

Usage with <a target="_blank" href="https://pygithub.readthedocs.io/">PyGitHub</a> client:

```python
from github import Github

user_fs = RepoFS(Github())
readme = user_fs.open("dAnjou/main/README.md")
print(readme.read())
```
"""

from abc import ABCMeta, abstractmethod
from io import BytesIO
from typing import Optional, Union, Any, Mapping, MutableMapping, cast

import requests
from fs.base import FS
from fs.zipfs import ReadZipFS
from github import Github
from github.AuthenticatedUser import AuthenticatedUser
from github.NamedUser import NamedUser
from github.Organization import Organization
from github.Repository import Repository
from werkzeug.utils import cached_property

from codefs._core import NamespaceFS, AbstractArchiveFetcher, AbstractReposFetcher

__all__ = [
    "UserFS",
    "OrgFS",
]


class UserFS(NamespaceFS):
    """"""

    def __init__(self, client: Github, user: Optional[str] = None):
        """
        Parameters
        ----------
        client : github.Github
            a <a target="_blank" href="https://pygithub.readthedocs.io/">PyGitHub</a> client
        user : str, optional
            an optional username; if *not* given, the client needs to be authenticated and the logged-in user is used
        """
        super().__init__(UserReposFetcher(client, user), ArchiveFetcher)


class OrgFS(NamespaceFS):
    """"""

    def __init__(self, client: Github, org: str):
        """
        Parameters
        ----------
        client : github.Github
            a <a target="_blank" href="https://pygithub.readthedocs.io/">PyGitHub</a> client
        org : str
            an org name; it might be necessary to authenticate the client
        """
        super().__init__(GroupReposFetcher(client, org), ArchiveFetcher)


class ReposFetcher(AbstractReposFetcher[Repository], metaclass=ABCMeta):
    def __init__(self) -> None:
        self._single_cache: MutableMapping[str, Repository] = {}
        self._all_cache: MutableMapping[str, Repository] = {}

    @cached_property
    @abstractmethod
    def namespace(self) -> Any:
        raise NotImplementedError

    def get_repo(self, name: str) -> Repository:
        if name not in self._single_cache.keys():
            if name not in self._all_cache.keys():  # pragma: no cover, because I'm not testing the caching
                self._all_cache[name] = self.namespace.get_repo(name)
            self._single_cache[name] = self._all_cache[name]
        return self._single_cache[name]

    def get_repos(self) -> Mapping[str, Repository]:
        if not self._all_cache:  # pragma: no cover, because I'm not testing the caching
            self._all_cache = {repo.name: repo for repo in self.namespace.get_repos()}
        return self._all_cache


class UserReposFetcher(ReposFetcher):
    def __init__(self, client: Github, user: Optional[str]) -> None:
        super().__init__()
        self._client = client
        self._username = user

    @cached_property
    def namespace(self) -> Union[AuthenticatedUser, NamedUser]:
        if self._username:
            return self._client.get_user(self._username)
        else:
            return self._client.get_user()


class GroupReposFetcher(ReposFetcher):
    def __init__(self, client: Github, group: str) -> None:
        super().__init__()
        self._client = client
        self._groupname = group

    @cached_property
    def namespace(self) -> Organization:
        return self._client.get_organization(self._groupname)


class ArchiveFetcher(AbstractArchiveFetcher):
    def __init__(self, repo: Repository) -> None:
        self._repo = repo
        self._cache: Optional[bytes] = None

    def __call__(self, ref: str) -> FS:
        if not self._cache:
            if ref == self.DEFAULT_BRANCH:
                ref = self._repo.default_branch
            archive_link = self._repo.get_archive_link("zipball", ref)
            response = requests.get(archive_link)
            self._cache = response.content
        fs = ReadZipFS(BytesIO(self._cache))
        return cast(FS, fs.opendir(fs.listdir("/")[0]))
