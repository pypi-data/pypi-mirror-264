# Pyro-Velocity

<div align="center" style="margin-left: auto; margin-right: auto; max-width: 540px; overflow-x: auto;">
<img
    src="https://raw.githubusercontent.com/pinellolab/pyrovelocity/beta/docs/_static/logo.png"
    alt="Pyro-Velocity logo"
    style="width: 300px; max-width: 90%; height: auto;"
    role="img">

𝒫robabilistic modeling of RNA velocity ⬱

|         |                                                                                                                                                           |
| ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CI/CD   | [![CID][cid-badge]][cid-link] [![codecov][codecov-badge]][codecov-link] [![pre-commit.ci status][precommit-badge]][precommit-link]                        |
| Docs    | [![Cloudflare Pages][cloudflare-badge]][cloudflare-link] [![Preprint][preprint-badge]][preprint-link]                                                     |
| Package | [![PyPI - Version][pypi-badge]][pypi-link] [![Conda-forge badge][conda-forge-badge]][anaconda-link] [![Docker image][docker-badge]][docker-link]          |
| Meta    | [![flyte-badge]][flyte-link] [![code style][black-badge]][black-link] [![License - MIT][license-badge]][license-link] [![Tuple][tuple-badge]][tuple-link] |

[cid-badge]: https://github.com/pinellolab/pyrovelocity/actions/workflows/cid.yaml/badge.svg?branch=master
[cid-link]: https://github.com/pinellolab/pyrovelocity/actions/workflows/cid.yaml
[precommit-badge]: https://results.pre-commit.ci/badge/github/pinellolab/pyrovelocity/main.svg
[precommit-link]: https://results.pre-commit.ci/latest/github/pinellolab/pyrovelocity/main
[flyte-badge]: https://img.shields.io/badge/flyte-carrier-gray.svg?color=7552A2&logo=data:image/svg%2bxml;base64,PHN2ZyBpZD0iTGF5ZXJfMSIgZGF0YS1uYW1lPSJMYXllciAxIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB2aWV3Qm94PSIwIDAgMzYwIDMzMy40ODM3OSI+PGRlZnM+PHN0eWxlPi5jbHMtMXtmaWxsOnVybCgjbGluZWFyLWdyYWRpZW50KTt9PC9zdHlsZT48bGluZWFyR3JhZGllbnQgaWQ9ImxpbmVhci1ncmFkaWVudCIgeDE9IjYuMTkzNjUiIHkxPSIxNjcuMzQ3NDUiIHgyPSIzNTIiIHkyPSIxNjcuMzQ3NDUiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj48c3RvcCBvZmZzZXQ9IjAiIHN0b3AtY29sb3I9IiNlNWM5ZDMiLz48c3RvcCBvZmZzZXQ9IjAuMzMiIHN0b3AtY29sb3I9IiNiMzg1ZGYiLz48c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiM2ZjJhZWYiLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48cGF0aCBjbGFzcz0iY2xzLTEiIGQ9Ik05MC45NjQ3NSwxNzAuODEzMzRjNy42Mjc3Ny0xOC4xMjcsMTEuNTEwNDctMzYuNzc2NTUsMTUuMDA2NC01NS40OTI4OSw1Ljk2MDM3LTMxLjkxMDIsOS45OS02NC4wMzIzLDguNjM2MjEtOTYuNTk0NzUtLjI1NzIzLTYuMTg3NDIsMS40ODQ5NS04LjQ4NzYzLDguMTQ5My03Ljg1ODIzLDE4LjA0NDY1LDEuNzA0MjUsMzUuOTM3NDYsMy43NjY1Nyw1Mi4xNTksMTIuNjUyODYsNC4yOTQyNSwyLjM1MjQxLDguMDYyNzIsMS4wODk0OSwxMi4xNjgzLS4wNjgxLDMxLjA0ODU5LTguNzU0NCw2Mi41MzI3Mi0xNC42OTE0Niw5NC45NjgyNS0xNC4wMjQ1NiwyMS4zMTQuNDM4Miw0MS45ODQyNSwzLjg3ODkxLDYxLjY0Mzc5LDEyLjcwMjc2LDYuNDI3MjksMi44ODQ3OSw4LjgwODY5LDYuOTg2NDEsOC4yMTY1NywxMy44MS0xLjU5MzM4LDE4LjM2MDg0LTguOTMzNDUsMzQuODE3NTEtMTYuNTU1NzEsNTEuMTgwMzgtMi4wODM3NSw0LjQ3MzEzLTUuMTEzMiwxLjkwMDYzLTcuNjg0MTcuMjc2ODYtMjUuODcwMzMtMTYuMzM4ODYtNTMuNjUxLTI4LjcwMDYzLTgyLjI2NC0zOS4yNTUxNi0yMC4zMDkwNi03LjQ5MTQ2LTQwLjg0NzY4LTE0LjMwOTczLTYzLjA1ODIzLTE3LjcxMjkzLDYuODUzODgsNi43ODE4MiwxMy40NjQwNywxMy44MzI2NiwyMC42MDM1NSwyMC4yOTkxMiwzMS42MDk3OSwyOC42Myw2NC41NTE4NSw1NS40OTQsMTAyLjYyNDMsNzUuMzE3NjQsNC4yMDA1MiwyLjE4NzEyLDUuMjE5NDYsNC40Mjk0MiwyLjMzNzMyLDguNTIyMTMtMTAuNTgzNzQsMTUuMDI5MDgtMjEuNDEwODUsMjkuODczMzEtMzcuMjkwNjQsMzkuODIzMTItNC43MjI4MywyLjk1OTE4LTUuODUyNDYsNy4xNjgzOC03LjAyMjgzLDExLjg0MjItOS4xMDQzMywzNi4zNTkyOS0yMi4zMzIsNzAuOTU1ODEtNDQuMDI1MzEsMTAxLjg2NTA3YTE0MS4zMjU0NSwxNDEuMzI1NDUsMCwwLDEtMzIuNzkzMiwzMy44NDUyMWMtNS44MDIwOSw0LjE5ODExLTEwLjk2OTg0LDQuNjkyLTE2Ljg1MDguMjcxOC0xNC4xOTA0Ny0xMC42NjU4OS0yNC44NjAxOS0yNC40MDA5My0zNC43NTE4NC0zOC44NzctMi43MTgzNy0zLjk3ODMzLS43ODg4Ni02LjE1NjEyLDIuNzA4NC03Ljk1NSwyOC41MTE4My0xNC42NjUyNyw1My44NDQ5NS0zMy45MTk2Nyw3OC4yNjQzNi01NC40NTM3YTQ1Mi44NjksNDUyLjg2OSwwLDAsMCw0Mi41MjQwOS00MC4wNmMtMi44MDMzNy0yLjY3MTQxLTUuMjA3ODItLjcwNTI5LTcuMzA0OC0uMTQ2MTctNDcuMDUyLDEyLjU0NS05Mi4zNzI1NCwyOS4zODkyMS0xMzQuMDQwODIsNTUuMDEwOS01LjY5NTE1LDMuNTAxOTMtOC43MjM0NiwzLjA2NjE2LTExLjQ5OTg1LTMuMzM5MzctNy4wOTI2OC0xNi4zNjM2Ny0xMy42NjczNC0zMi44Njc1MS0xNC43NzQxOS01MC44NjkzNi0uMzYyNjgtNS44OTgxNC0zLjk2ODM2LTkuMDc1NTUtNy41NjI2NC0xMi41Njg0Ni0yNS42NTEyMy0yNC45MjcxNy00Ny45NjEtNTIuMzc0ODMtNjMuNDg0ODYtODQuODQzN0MxMi40MjgyOSw2OC4yNTUsNi44ODkxOSw1MS44MDAxNCw2LjIxMDg5LDMzLjkzMzgxYy0uMjY5LTcuMDg2MDYsMi42MDM2OC0xMS4wMzkyNSw5LjAwMTQ3LTEzLjM0NDlhMTY4LjI0NDkxLDE2OC4yNDQ5MSwwLDAsMSw0Ni4xNTYtOS42ODQxNGM2LjMyMDE1LS40MjE2Miw3Ljg3MzEsMS44MDQzMyw3LjcwNzY4LDcuNTA2NjgtMS4xNjg0MSw0MC4yODA2LDQuOTg5MjMsNzkuNzU1LDEzLjU3NjQ2LDExOC45MjMsMi40NjE1MiwxMS4yMjc0MSw1LjUyNDg2LDIyLjMyMjk0LDguMzEyMjcsMzMuNDc4ODRaTTE3OS40MTM2OSwzOS41MDhDMTY5LjA5Niw5Mi45NjE2MSwxMzYuNjc2ODUsMTMyLjkwNDIxLDEwMC4xMzIxMywxNzAuNTI4MmM0OS44OTE3Ny0yMC4zNzEsOTkuNjI4NTctMTEuMjM1NywxNDkuODI1NDMtMS4zMjA3NkMyMTEuNDQzODcsMTMzLjc1OTY5LDE5My45ODkyNiw4Ny43MTM2MywxNzkuNDEzNjksMzkuNTA4WiIvPjwvc3ZnPg==
[flyte-link]: https://docs.flyte.org
[cloudflare-badge]: https://img.shields.io/badge/Docs-pages-gray.svg?style=flat&logo=cloudflare&color=F26722
[cloudflare-link]: https://docs.pyrovelocity.net
[preprint-badge]: https://img.shields.io/badge/doi-10.1101/2022.09.12.507691v2-B31B1B
[preprint-link]: https://doi.org/10.1101/2022.09.12.507691
[pypi-badge]: https://img.shields.io/pypi/v/pyrovelocity.svg?logo=pypi&label=PyPI&color=F26722&logoColor=F26722
[pypi-link]: https://pypi.org/project/pyrovelocity/
[conda-forge-badge]: https://img.shields.io/conda/vn/conda-forge/pyrovelocity.svg?logo=conda-forge&label=conda-forge&color=F26722
[anaconda-link]: https://anaconda.org/conda-forge/pyrovelocity
[docker-badge]: https://img.shields.io/badge/docker-image-blue?logo=docker
[docker-link]: https://github.com/pinellolab/pyrovelocity/pkgs/container/pyrovelocity
[codecov-badge]: https://codecov.io/gh/pinellolab/pyrovelocity/branch/main/graph/badge.svg
[codecov-link]: https://codecov.io/gh/pinellolab/pyrovelocity
[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[black-link]: https://github.com/psf/black
[license-badge]: https://img.shields.io/badge/license-AGPL%203-gray.svg?color=F26722
[license-link]: https://spdx.org/licenses/
[tuple-badge]: https://img.shields.io/badge/Tuple%20❤️%20OSS-5A67D8?logo=tuple
[tuple-link]: https://tuple.app/github-badge

</div>

<!--
[anaconda-badge]: https://anaconda.org/conda-forge/pyrovelocity/badges/version.svg?style=flat&color=F26722

[![GitHub Pages][gh-pages-badge]][gh-pages-link]
[gh-pages-badge]: https://img.shields.io/github/deployments/pinellolab/pyrovelocity/github-pages?logo=github&label=Docs
[gh-pages-link]: https://pinellolab.github.io/pyrovelocity

[![CML][cml-badge]][cml-link]
[cml-badge]: https://github.com/pinellolab/pyrovelocity/actions/workflows/cml.yml/badge.svg
[cml-link]: https://github.com/pinellolab/pyrovelocity/actions/workflows/cml.yml
-->

---

[Pyro-Velocity](https://docs.pyrovelocity.net) is a library for probabilistic inference in minimal models approximating gene expression dynamics from, possibly multimodal, single-cell sequencing data.
It provides posterior estimates of gene expression parameters, predictive estimates of gene expression states, and local estimates of cell state transition probabilities.
It can be used as a component in frameworks that attempt to retain the ability to propagate uncertainty in predicting: distributions over cell fates from subpopulations of cell states, response to cell state perturbations, or candidate genes or gene modules that correlate with determination of specific cell fates.

---

## Documentation 📒

Please see the [Documentation](https://docs.pyrovelocity.net).

## Changelog 🔀

Changes for each release are listed in the [Changelog](https://docs.pyrovelocity.net/about/changelog).

## Contributing ✨

Please review the [Contributing Guide](https://docs.pyrovelocity.net/about/contributing) for instructions on setting up a development environment and submitting pull requests.

## Community 🏘

If you would like to apply [Pyro-Velocity](https://docs.pyrovelocity.net) in your research, have an idea for a new feature, have a problem using the library, or just want to chat, please feel free to [start a discussion](https://github.com/pinellolab/pyrovelocity/discussions).

If you have a feature request or issue using Pyro-Velocity that may require making changes to the contents of this repository, please [file an issue](https://github.com/pinellolab/pyrovelocity/issues) containing

- a [GitHub permananent link](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-a-permanent-link-to-a-code-snippet) to the location in the repository you think is causing a problem or will require changes, and
- provide a [minimal reproducible example](https://en.wikipedia.org/wiki/Minimal_reproducible_example) of the problem or proposed improvement.

We are always interested in discussions and issues that can help to improve the [Documentation](https://docs.pyrovelocity.net).

## License ⚖️

[AGPL](https://github.com/pinellolab/pyrovelocity/blob/main/LICENSE)
