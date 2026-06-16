import sys

try:
    import pandas as pd
    PANDAS_VERSION = pd.__version__
    PANDAS_OK = True
except ImportError:
    PANDAS_OK = False
    PANDAS_VERSION = "NOT INSTALLED"

try:
    import numpy as np
    NUMPY_VERSION = np.__version__
    NUMPY_OK = True
except ImportError:
    NUMPY_OK = False
    NUMPY_VERSION = "NOT INSTALLED"

try:
    import matplotlib as mpl
    MPL_VERSION = mpl.__version__
    MPL_OK = True
except ImportError:
    MPL_OK = False
    MPL_VERSION = "NOT INSTALLED"


def check_dependencies() -> bool:
    print("Checking dependencies:")
    all_ok = True

    if PANDAS_OK:
        print(f"[OK] pandas ({PANDAS_VERSION})",
              "\t- Data manipulation ready")
    else:
        print("[MISSING] pandas - install with:",
              "  pip:    pip install -r requirements.txt",
              "  poetry: poetry install", sep="\n")
        all_ok = False

    if NUMPY_OK:
        print(f"[OK] numpy ({NUMPY_VERSION})",
              "\t- Numerical computation ready")
    else:
        print("[MISSING] numpy - install with:",
              "  pip:    pip install -r requirements.txt",
              "  poetry: poetry install", sep="\n")
        all_ok = False

    if MPL_OK:
        print(f"[OK] matplotlib ({MPL_VERSION})",
              "\t- Visualization ready")
    else:
        print("[MISSING] matplotlib - install with:",
              "  pip:    pip install -r requirements.txt",
              "  poetry: poetry install", sep="\n")
        all_ok = False

    return all_ok


def main() -> None:
    print("\nLOADING STATUS: Loading programs...\n")
    if not check_dependencies():
        print("\nTo install all missing dependencies:")
        print("  pip:    pip install -r requirements.txt")
        print("  poetry: poetry install")
        print("          poetry run python loading.py")
        sys.exit(1)


if __name__ == "__main__":
    main()
