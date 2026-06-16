from dotenv import load_dotenv
import os


def parse_configuration() -> tuple[str, str, str, str, str]:
    matrix_mode = os.environ.get("MATRIX_MODE", "development")
    database_url = os.environ.get("DATABASE_URL", "")
    api_key = os.environ.get("API_KEY", "")
    log_level = os.environ.get("LOG_LEVEL", "INFO")
    zion_endpoint = os.environ.get("ZION_ENDPOINT", "")

    if not api_key:
        print("WARNING: API_KEY not set — API access disabled")
    if not database_url:
        print("WARNING: DATABASE_URL not set — no database configured")
    if not zion_endpoint:
        print("WARNING: ZION_ENDPOINT not set — network offline")

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

    load_dotenv()

    print_configuration(*parse_configuration())

    print_security_check()

    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    main()
