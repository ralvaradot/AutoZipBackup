"""AutoZipBackup application entry point."""

from autozip.application import Application


def main() -> None:
    """Start AutoZipBackup."""
    application = Application()
    application.run()


if __name__ == "__main__":
    main()
    