# fs-code

[![Documentation][docs badge]][docs link]
[![PyPI][pypi badge]][pypi link]
![Pipeline status][pipeline badge]
![3.8 coverage][3.8 coverage badge]
![3.12 coverage][3.12 coverage badge]
[![Code style: black][code style badge]][code style link]

[PyFilesystems](https://www.pyfilesystem.org/) for GitLab, GitHub, and Git.

---

## Installation

```shell
pip install fs-code[gitlabfs]
# or
pip install fs-code[githubfs]
# or
pip install fs-code[gitfs]
# or
pip install fs-code[all]
```

## Usage

### with <a target="_blank" href="https://docs.pyfilesystem.org/en/latest/openers.html">FS URL</a>

```python
import fs

user_fs = fs.open_fs("gitlab://?user=dAnjou")
readme = user_fs.open("fs-code/main/README.md")
print(readme.read())
```

### with class

```python
from gitlab import Gitlab
from codefs.gitlabfs import UserFS

user_fs = UserFS(Gitlab(), user="dAnjou")
readme = user_fs.open("fs-code/main/README.md")
print(readme.read())
```

[docs link]: https://danjou.gitlab.io/fs-code
[docs badge]: https://img.shields.io/badge/%F0%9F%94%8D-documentation-blue
[pypi link]: https://pypi.org/project/fs-code/ 
[pypi badge]: https://img.shields.io/pypi/v/fs-code
[pipeline badge]: https://gitlab.com/dAnjou/fs-code/badges/main/pipeline.svg
[3.8 coverage badge]: https://gitlab.com/dAnjou/fs-code/badges/main/coverage.svg?job=test%3A%20%5B3.8%5D&key_text=3.8+coverage&key_width=90
[3.12 coverage badge]: https://gitlab.com/dAnjou/fs-code/badges/main/coverage.svg?job=test%3A%20%5B3.12%5D&key_text=3.12+coverage&key_width=90
[code style link]: https://github.com/psf/black
[code style badge]: https://img.shields.io/badge/code%20style-black-000000.svg
