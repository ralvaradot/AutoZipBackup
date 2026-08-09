"""AutoZipBackup application entry point."""

from autozip.common.version import get_version_info


def main() -> None:
    """Start the AutoZipBackup application."""
    version_info = get_version_info()

    print(
        f"{version_info['application_name']} "
        f"{version_info['application_version']}"
    )

    print(
        f"Build: {version_info['build_number']}"
    )

    print(
        f"Git Commit: {version_info['git_commit']}"
    )


if __name__ == "__main__":
    main()