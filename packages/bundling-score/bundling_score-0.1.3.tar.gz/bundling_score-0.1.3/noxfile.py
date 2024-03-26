from __future__ import annotations

import shutil
from pathlib import Path
import platform

import nox

nox.options.sessions = ["lint", "coverage"]

private_package_registry = "https://gitlab.college-de-france.fr/api/v4/projects/145/packages/pypi/simple"
python_versions = ["3.9", "3.10"]  # the versions of python used in our team
macosx_deployment_target = "10.9"  # as numpy (25/01/2023)
# maybe to update in the future ?
# try to see the result of pip3 debug --verbose | grep macosx | cut -d"_" -f2 | sort | uniq
# if everybody has more than 10, then we should be able to update the value.


@nox.session(tags=["annotations"], reuse_venv=True)
def mypy(session: nox.Session) -> None:
    """(annotations) Run mypy"""
    session.install("mypy")
    session.run("mypy")


@nox.session(tags=["style", "fix"], reuse_venv=True)
def lint(session: nox.Session) -> None:
    """
    (quality) Run Black and isort.
    """
    # This needs to be installed into the package environment, and is slower
    # than a pre-commit check
    session.install("black")
    session.install("isort")
    session.run("black", "src", *session.posargs)
    session.run("isort", "src", *session.posargs)


@nox.session(tags=["style"], reuse_venv=True)
def flake(session: nox.Session) -> None:
    """(quality) Run Flake8"""
    session.install("pyproject-flake8")
    session.run("pflake8")


@nox.session(tags=["full fix and style"])
def precommit_checks(session: nox.Session) -> None:
    """
    (quality) Run all linters. Will be a bit long the first time only.
    Manual stage : check-manifest
    """
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files")


@nox.session
def tests(session: nox.Session) -> None:
    """
    (test) Run tests.
    """
    session.install(
        ".[test]",
        "-i",
        private_package_registry,
    )
    session.run("pytest", *session.posargs)


@nox.session
def coverage(session: nox.Session) -> None:
    """
    (test) Run tests and show coverage.
    """

    session.posargs.append("--cov=bundling_score")
    session.posargs.append("--cov-report")
    session.posargs.append("html")
    session.posargs.append("--cov-report")
    session.posargs.append("term")
    tests(session)


@nox.session
def profile(session: nox.Session) -> None:
    """
    (profiling) Run scalene. Add "-- program.py". See scalene documentation.
    """
    session.install(".")
    session.install("scalene")
    session.run("scalene", *session.posargs)


@nox.session
def docs(session: nox.Session) -> None:
    """
    (docs) Build the docs. Pass "serve" to serve.
    """

    session.install(
        ".[docs]",
        "-i",
        private_package_registry,
    )
    session.chdir("docs")
    session.run("sphinx-build", "-M", "html", ".", "_build")

    if session.posargs:
        if "serve" in session.posargs:
            print("Launching docs at http://localhost:8000/ - use Ctrl-C to quit")
            session.run("python", "-m", "http.server", "8000", "-d", "_build/html")
        else:
            session.warn("Unsupported argument to docs")


@nox.session(reuse_venv=True)
def check_manifest(session: nox.Session) -> None:
    """(build) Run check-manifest"""
    session.install("check-manifest")
    session.run("check-manifest", "-c", "-v")


DIR = Path(__file__).parent.resolve()


@nox.session(python=python_versions)
def build(session: nox.Session) -> None:
    """
    (build) Build an SDist and wheel, locally.
    """

    build_p = DIR.joinpath("build")
    if build_p.exists():
        shutil.rmtree(build_p)

    session.install("build")
    session.run("python", "-m", "build")

    if "Darwin" in platform.uname().system:
        print("MacOS detected. Trying also to build for minimal version", macosx_deployment_target)
        session.run("python", "-m", "build", "--wheel", env={"MACOSX_DEPLOYMENT_TARGET":macosx_deployment_target})


@nox.session
def publish(session: nox.Session) -> None:
    """Publish the built packages on the gitlab repository. Pass "pypi" to publish on PyPI.
    You must have a gitlab entry in your ~/.pypirc with access tokens for the package registry.
    """
    dist_dir = DIR.joinpath("dist")
    if not dist_dir.exists():
        print(dist_dir.resolve(), "not found, have you built the package ?")
    else:
        sdists = Path("dist").glob("*.tar.gz")
        wheels = Path("dist").glob("*.whl")

        session.install("twine")
        for sdist in sdists:
            session.run("twine", "check", str(sdist), "--strict")
        for wheel in wheels:
            session.run("twine", "check", str(wheel), "--strict")

        if "Darwin" in platform.uname().system and "no-bundle" not in session.posargs:
            print("MacOS detected. Running delocate to bundle external libraries")
            session.install("delocate")
            wheels = Path("dist").glob("*.whl")
            for wheel in wheels:
                session.run("delocate-wheel", str(wheel))

        if session.posargs:
            if "pypi" in session.posargs:
                session.run("twine", "upload", "dist/*")
        else:
            session.run("twine", "upload", "--repository", "gitlab", "dist/*")


@nox.session
def requirements(session: nox.Session) -> None:
    """Generate a requirements.txt file."""
    session.install(
        ".",
        "-i",
        private_package_registry,
    )
    session.install("pipdeptree")
    session.run(
        "sh",
        "-c",
        r"pipdeptree -f --warn silence | grep -E '^[a-zA-Z0-9\-]+' | tee requirements.txt",
    )


@nox.session
def lock_file(session: nox.Session) -> None:
    """Generate a locked-requirements.txt file."""
    session.install(
        ".",
        "-i",
        private_package_registry,
    )
    session.install("pipdeptree")
    session.run("sh", "-c", "pipdeptree -f | tee locked-requirements.txt")


@nox.session(python=False)
def clean(session: nox.Session) -> None:
    """Delete cache folders and files."""
    folders = [
        ".nox",
        "_skbuild",
        "__pycache__",
        ".pytest_cache",
        ".coverage",
        ".mypy_cache",
        "docs/_build",
        "docs/_generate",
    ]
    for folder in folders:
        session.run("rm", "-rf", folder)


@nox.session(reuse_venv=True)
def install_precommit_hooks(session: nox.Session) -> None:
    """(installation) Install the pre-commit hooks."""
    session.install("pre-commit")
    session.run("pre-commit", "install")
