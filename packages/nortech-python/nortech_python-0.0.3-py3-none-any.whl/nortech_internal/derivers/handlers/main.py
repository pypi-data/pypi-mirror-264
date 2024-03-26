import os

from nortech_internal.derivers.services.logger import logger


def main():
    logger.info(f"[COMMIT] {os.getenv('GIT_COMMIT', 'unknown')}")

    RECOVERY_DB_PATH = os.getenv("RECOVERY_DB_PATH")

    if RECOVERY_DB_PATH:
        logger.info(f"Using SQLite recovery with path {RECOVERY_DB_PATH}")

        lost_found_dir = "lost+found"
        dir_list = os.listdir(RECOVERY_DB_PATH)
        if lost_found_dir in dir_list:
            dir_list.remove(lost_found_dir)

        if len(dir_list) == 0:
            try:
                logger.info(
                    f"Initializing SQLite recovery with path {RECOVERY_DB_PATH}"
                )
                os.system(f"python -m bytewax.recovery {RECOVERY_DB_PATH} 4")
            except Exception:
                logger.warn(
                    f"Using SQLite recovery with path {RECOVERY_DB_PATH} already initialized"
                )

        os.system(
            f"python -m bytewax.run nortech_internal.derivers.handlers.flow -r {RECOVERY_DB_PATH}"
        )
    else:
        logger.info("Running without recovery")
        os.system("python -m bytewax.run nortech_internal.derivers.handlers.flow")


if __name__ == "__main__":
    main()
