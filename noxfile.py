import nox
from nox_poetry import Session, session

nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = ["test"]


@session(python=["3.8"])
def test(s: Session) -> None:
    s.install(".", "pytest", "pytest-cov")
    s.run(
        "python",
        "-m",
        "pytest",
        "--cov=onemodel",
        "--cov-report=html",
        "--cov-report=term",
        "tests",
        *s.posargs,
    )


# For some sessions, set venv_backend="none" to simply execute scripts within
# the existing Poetry environment. This requires that nox is run within `poetry
# shell` or using `poetry run nox ...`.
@session(venv_backend="none")
def fmt(s: Session) -> None:
    s.run("isort", ".")
    s.run("black", ".")


@session(venv_backend="none")
def fmt_check(s: Session) -> None:
    s.run("isort", "--check", ".")
    s.run("black", "--check", ".")


@session(venv_backend="none")
def lint(s: Session) -> None:
    s.run("pflake8")


@session(venv_backend="none")
def type_check(s: Session) -> None:
    s.run("mypy", "src", "tests", "noxfile.py")

