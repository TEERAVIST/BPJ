import nox
import nox_poetry

# --- Global Nox Options ---
# Set default sessions to run if none are specified on the command line
nox.options.sessions = ["lint", "typecheck", "tests", "coverage", "build","format"]
# Reuse existing virtual environments for speed
nox.options.reuse_existing_virtualenvs = True
# Do not install the project in the session unless explicitly requested
# This is a common nox-poetry setup. If your tests or other sessions
# *do* need your project installed, you can add session.install(".")
# or session.install(".[dev]") as needed.
# For many linting/typechecking tasks, the source files are enough.
# nox.options.install_unmanaged = False

# --- Project Specific Variables ---
SRC_DIR = "src"
PACKAGE = "bpj"
TESTS_DIR = "tests"


# --- Nox Sessions ---

@nox_poetry.session(python=["3.11"])
def format(session):
    """Auto-format code using black."""
    session.install("black")
    session.run("black", SRC_DIR, TESTS_DIR)


@nox_poetry.session(python=["3.11"])
def lint(session: nox_poetry.Session):
    """
    Runs linters (black, flake8) on the codebase.
    """
    # Use session.install() for direct dependencies needed for the session
    session.install("flake8")
    session.run("flake8", SRC_DIR, TESTS_DIR)


@nox_poetry.session(python=["3.11"])
def typecheck(session: nox_poetry.Session):
    """
    Performs static type checking with MyPy.
    """
    session.install("mypy")
    # You might need to install your project and its dependencies for mypy to resolve imports
    # If mypy complains about missing modules, uncomment the line below:
    # session.install(".", "mypy") # Install project and mypy
    session.run("mypy", f"{SRC_DIR}/{PACKAGE}")


@nox_poetry.session(python=["3.11"])
def tests(session: nox_poetry.Session):
    """
    Runs unit tests with pytest.
    """
    # Install the project itself and then pytest.
    # The "." tells nox-poetry to install your project and its main dependencies.
    session.install(".", "pytest")
    session.run("pytest", TESTS_DIR)


@nox_poetry.session(python=["3.11"])
def coverage(session: nox_poetry.Session):
    """
    Runs tests with coverage and generates an XML report.
    """
    # Install the project and testing dependencies
    session.install(".", "pytest", "pytest-cov")
    session.run("pytest", "--cov", f"{SRC_DIR}/{PACKAGE}", "--cov-report=term", "--cov-report=xml", TESTS_DIR)


@nox_poetry.session(python=["3.11"])
def build(session: nox_poetry.Session):
    """
    Builds the project's distributable packages.
    """
    # poetry is typically installed by nox-poetry if needed, but explicit is fine.
    # We don't need to install the project itself with session.install(".") here
    # because 'poetry build' operates directly on the source.
    session.install("poetry") # Ensure poetry is available
    session.run("poetry", "build")


# --- Optional: Session for generating requirements.txt (if you add this later) ---
@nox_poetry.session(python=["3.11"])
def export_deps(session: nox_poetry.Session):
    """
    Exports poetry dependencies to a requirements.txt file.
    This session demonstrates how to fix the `poetry export` command issue.
    """
    session.log(f"Current Poetry version: {session.run('poetry', '--version', external=True)}")

    # Crucial step for Poetry 1.2+ to enable the 'export' command
    session.run("poetry", "self", "add", "poetry-plugin-export", external=True)
    session.log("Installed poetry-plugin-export.")

    # Install your project's dependencies (optional, but good practice if export relies on them)
    # If you only need to export 'dev' group, ensure it's available.
    session.run("poetry", "install", "--with=dev", "--no-root", "--sync", external=True)
    session.log("Installed project dependencies for export.")

    # Now, run the export command
    session.run("poetry", "export", "--format=requirements.txt", "--with=dev", "--without-hashes", external=True)
    session.log("Dependencies exported to requirements.txt")

    # You might want to move/rename the file after export, e.g.:
    # session.run("mv", "requirements.txt", "requirements-dev.txt", external=Tr
