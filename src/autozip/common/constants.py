"""Application-wide constants."""

DEFAULT_LANGUAGE = "es"

SUPPORTED_LANGUAGES = (
    "es",
    "en",
)

DEFAULT_APPEARANCE = "dark"

SUPPORTED_APPEARANCES = (
    "light",
    "dark",
)

APPLICATION_DATA_DIRECTORY_NAME = "AutoZipBackup"

SETTINGS_FILE_NAME = "settings.json"

LOG_DIRECTORY_NAME = "logs"

LOG_FILE_NAME = "autozip.log"

DEFAULT_LOG_MAX_BYTES = 10 * 1024 * 1024

DEFAULT_LOG_BACKUP_COUNT = 10

ZIP_EXTENSION = ".zip"

BACKUP_FILENAME_SEPARATOR = "_"

DATE_TIME_FORMAT = "%Y%m%d_%H%M%S"