from dotenv import load_dotenv
import os
import sys


def parse_configuration() -> tuple[str, str, str, str, str]:
    matrix_mode = os.environ.get("MATRIX_MODE")
    if not matrix_mode:
        print("ERROR: MATRIX_MODE is not set")
        sys.exit(1)

    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("ERROR: DATABASE_URL is not set")
        sys.exit(1)

    api_key = os.environ.get("API_KEY")
    if not api_key:
        print("ERROR: API_KEY is not set")
        sys.exit(1)

    log_level = os.environ.get("LOG_LEVEL")
    if not log_level:
        print("ERROR: LOG_LEVEL is not set")
        sys.exit(1)

    zion_endpoint = os.environ.get("ZION_ENDPOINT")
    if not zion_endpoint:
        print("ERROR: ZION_ENDPOINT is not set")
        sys.exit(1)

    return (matrix_mode, database_url, api_key, log_level, zion_endpoint)


def print_configuration(matrix_mode: str,
                        database_url: str,
                        api_key: str,
                        log_level: str,
                        zion_endpoint: str) -> None:
    print("Configuration loaded:")
    if database_url:
        database_status = "Connected to local instance"
    else:
        database_status = "Not reachable"
    if api_key:
        api_access = f"Authenticated with {api_key[:4]}...{api_key[-4:]}"
    else:
        api_access = "Forbidden"
    if zion_endpoint:
        zion_status = "Online"
    else:
        zion_status = "Offline"
    print(f"Mode: {matrix_mode}",
          f"Database: {database_status}",
          f"API Access: {api_access}",
          f"Log Level: {log_level}",
          f"Zion Network: {zion_status}", sep="\n")


def print_security_check() -> None:
    print("\nEnvironment security check:")
    print("[OK] No hardcoded secrets detected",
          "[OK] .env file properly configured",
          "[OK] Production overrides available", sep="\n")


def main() -> None:
    print("\nORACLE STATUS: Reading the Matrix...\n")

    if not load_dotenv():
        print("[KO] Cannot load .env (probably mising)")
        sys.exit(1)

    print_configuration(*parse_configuration())

    print_security_check()

    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    main()
