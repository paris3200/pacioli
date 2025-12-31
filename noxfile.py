"""Nox Sessions."""

import tempfile

import nox
from nox_poetry import session
from nox_poetry.sessions import Session

locations = "src", "tests", "noxfile.py"
nox.options.sessions = "lint", "mypy", "pytype", "safety", "tests"
package = "pacioli"


@nox.session
def tests(session: Session) -> None:
    """Run the test suite."""
    session.install("pytest", "pytest-cov", ".")
    session.run("pytest", "--cov=pacioli")


@nox.session
def lint(session: Session) -> None:
    """Run the lint session."""
    args = session.posargs or locations
    session.install(
        "flake8",
        "flake8-black",
        "flake8-docstrings",
    )
    session.run("flake8", *args)


@nox.session
def black(session: Session) -> None:
    """Run black session."""
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@nox.session
def safety(session: Session) -> None:
    """Run the safety session."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--with",
            "dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.install("safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


@nox.session
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or locations
    session.install("mypy")
    session.run("mypy", *args)


@nox.session
def pytype(session: Session) -> None:
    """Run the static type checker."""
    args = session.posargs or ["--disable=import-error", *locations]
    session.install("pytype")
    session.run("pytype", *args)


@nox.session
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]
    session.run("poetry", "install", "--without dev", external=True)
    session.install("xdoctest")
    session.run("python", "-m", "xdoctest", package, *args)


@nox.session
def docs(session: Session) -> None:
    """Build the documentation."""
    session.run("poetry", "install", "--without dev", external=True)
    session.install("sphinx", "sphinx-autodoc-typehints")
    session.run("sphinx-build", "docs", "docs/_build")


@nox.session
def coverage(session: Session) -> None:
    """Upload coverage data."""
    session.install("coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)
