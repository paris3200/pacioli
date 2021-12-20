"""Nox Sessions."""
import tempfile

import nox
from nox_poetry import session
from nox_poetry.sessions import Session

locations = "src", "tests", "noxfile.py"
nox.options.sessions = "lint", "mypy", "pytype", "safety", "tests"
package = "pacioli"


@session(python=["3.7", "3.8", "3.9", "3.10"])
def tests(session: Session) -> None:
    """Run the test suite."""
    session.install("pytest", "pytest-cov", ".")
    session.run("pytest", "--cov=pacioli")


@session(python=["3.8", "3.9", "3.10"])
def lint(session: Session) -> None:
    """Run the lint session."""
    args = session.posargs or locations
    session.install(
        "flake8",
        "flake8-black",
        "flake8-docstrings",
        "flake8-isort",
    )
    session.run("flake8", *args)


@session(python=["3.9", "3.10"])
def black(session: Session) -> None:
    """Run black session."""
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@session(python=["3.9", "3.10"])
def safety(session: Session) -> None:
    """Run the safety session."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.install("safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


@session(python=["3.9", "3.10"])
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or locations
    session.install("mypy")
    session.run("mypy", *args)


@session(python="3.9")
def pytype(session: Session) -> None:
    """Run the static type checker."""
    args = session.posargs or ["--disable=import-error", *locations]
    session.install("pytype")
    session.run("pytype", *args)


@session(python=["3.9", "3.8"])
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]
    session.run("poetry", "install", "--no-dev", external=True)
    session.install("xdoctest")
    session.run("python", "-m", "xdoctest", package, *args)


@session(python="3.10")
def docs(session: Session) -> None:
    """Build the documentation."""
    session.run("poetry", "install", "--no-dev", external=True)
    session.install("sphinx", "sphinx-autodoc-typehints")
    session.run("sphinx-build", "docs", "docs/_build")


@session(python=["3.9", "3.10"])
def coverage(session: Session) -> None:
    """Upload coverage data."""
    session.install("coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)
