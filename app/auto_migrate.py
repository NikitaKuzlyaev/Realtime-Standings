import logging
import os
import subprocess

logger = logging.getLogger(__name__)


def list_files_in_directory():
    directory = os.getcwd()
    try:
        result = subprocess.run(
            ["ls", directory],
            capture_output=True,
            text=True
        )
        logger.error(result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error while listing files: {e}")


def auto_migrate():
    list_files_in_directory()

    try:
        logger.info("Generating new Alembic migration...")

        subprocess.run(
            ["alembic", "revision", "--autogenerate", "-m", "Auto migration"],
            check=True,
            cwd="app"
        )

        logger.info("Applying migrations...")
        subprocess.run(
            ["alembic", "upgrade", "head"],
            check=True,
            cwd="app"
        )

        logger.info("Migrations applied successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error while applying migrations: {e}")
