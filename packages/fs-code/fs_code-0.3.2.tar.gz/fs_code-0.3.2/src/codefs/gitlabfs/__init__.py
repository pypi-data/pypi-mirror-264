"""
These are read-only filesystems which use the GitLab API to download an archive.

Usage with <a target="_blank" href="https://docs.pyfilesystem.org/en/latest/openers.html">FS URL</a>:

```python
import fs

user_fs = fs.open_fs("gitlab://?user=dAnjou")
readme = user_fs.open("fs-code/main/README.md")
print(readme.read())
```

.. hint::
   You can also access a self-managed GitLab instance. The FS URL would look like this then:
   `gitlab://https://gitlab.example.com?user=USER`

Usage with <a target="_blank" href="https://python-gitlab.readthedocs.io/">python-gitlab</a> client:

```python
from gitlab import Gitlab

user_fs = RepoFS(Gitlab())
readme = user_fs.open("fs-code/main/README.md")
print(readme.read())
```
"""

from abc import abstractmethod, ABCMeta
from io import BytesIO
from typing import Optional, Mapping, MutableMapping, Any, cast

from fs.base import FS
from fs.zipfs import ReadZipFS
from gitlab import Gitlab
from gitlab.v4.objects import Project, Group, User, CurrentUser
from werkzeug.utils import cached_property

from codefs._core import NamespaceFS, AbstractReposFetcher, AbstractArchiveFetcher

__all__ = [
    "UserFS",
    "GroupFS",
]


class UserFS(NamespaceFS):
    """"""

    def __init__(self, client: Gitlab, user: Optional[str] = None):
        """
        Parameters
        ----------
        client : gitlab.Gitlab
            a <a target="_blank" href="https://python-gitlab.readthedocs.io/">python-gitlab</a> client
        user : str, optional
            an optional username; if *not* given, the client needs to be authenticated and the logged-in user is used
        """
        super().__init__(UserReposFetcher(client, user), ArchiveFetcher)


class GroupFS(NamespaceFS):
    """"""

    def __init__(self, client: Gitlab, group: str):
        """
        Parameters
        ----------
        client : gitlab.Gitlab
            a <a target="_blank" href="https://python-gitlab.readthedocs.io/">python-gitlab</a> client
        group : str
            a group name; it might be necessary to authenticate the client
        """
        super().__init__(GroupReposFetcher(client, group), ArchiveFetcher)


class ReposFetcher(AbstractReposFetcher[Project], metaclass=ABCMeta):
    def __init__(self, client: Gitlab) -> None:
        self.client = client
        self._single_cache: MutableMapping[str, Project] = {}
        self._all_cache: MutableMapping[str, Project] = {}

    @cached_property
    @abstractmethod
    def namespace_name(self) -> str:
        raise NotImplementedError

    @cached_property
    @abstractmethod
    def namespace(self) -> Any:
        raise NotImplementedError

    def get_repo(self, name: str) -> Project:
        if name not in self._single_cache.keys():
            if name not in self._all_cache.keys():  # pragma: no cover, because I'm not testing the caching
                self._all_cache[name] = self.client.projects.get(f"{self.namespace_name}/{name}")
            self._single_cache[name] = self._all_cache[name]
        return self._single_cache[name]

    def get_repos(self) -> Mapping[str, Project]:
        if not self._all_cache:  # pragma: no cover, because I'm not testing the caching
            repos = self.namespace.projects.list(all=True)
            self._all_cache = {repo.path: self.client.projects.get(repo.id, lazy=True) for repo in repos}
        return self._all_cache


class UserReposFetcher(ReposFetcher):
    def __init__(self, client: Gitlab, user: Optional[str]) -> None:
        super().__init__(client)
        self._username = user

    @cached_property
    def namespace_name(self) -> str:
        if not self._username:
            self.client.auth()
            self._username = cast(CurrentUser, self.client.user).username  # auth makes sure we have a user
        return cast(str, self._username)

    @cached_property
    def namespace(self) -> User:
        return self.client.users.list(username=self.namespace_name)[0]  # type: ignore


class GroupReposFetcher(ReposFetcher):
    def __init__(self, client: Gitlab, group: str) -> None:
        super().__init__(client)
        self._groupname = group

    @cached_property
    def namespace_name(self) -> str:
        return self._groupname

    @cached_property
    def namespace(self) -> Group:
        return self.client.groups.get(self.namespace_name)


class ArchiveFetcher(AbstractArchiveFetcher):
    def __init__(self, project: Project) -> None:
        self._project = project
        self._cache: Optional[bytes] = None

    def __call__(self, ref: str) -> FS:
        if not self._cache:
            self._cache = cast(
                bytes, self._project.repository_archive(ref if ref != self.DEFAULT_BRANCH else None, format="zip")
            )
        fs = ReadZipFS(BytesIO(self._cache or b""))
        return cast(FS, fs.opendir(fs.listdir("/")[0]))
