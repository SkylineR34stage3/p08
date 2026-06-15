import sys
import os
import site


def main() -> None:
    in_matrix: bool = False

    if sys.prefix == sys.base_prefix:
        print("\nMATRIX STATUS:", "You're still plugged in\n")
    else:
        in_matrix = True
        print("\nMATRIX STATUS:", "Welcome to the construct\n")

    print("Current Python:", sys.executable)
    path = os.environ.get("VIRTUAL_ENV")
    if path:
        print("Virtual Environment:", os.path.basename(path))
        print("Environment Path:", path)
    else:
        print("Virtual Environment:", "None Detected")

    if not in_matrix:
        print("\nWARNING: You're in the global environment!",
              "The machines can see everything you install.",
              "\nTo enter the construct, run:",
              "python -m venv matrix_env",
              "source matrix_env/bin/activate # On Unix",
              r"matrix_env\Scripts\activate # On Windows",
              "\nThen run this program again.", sep="\n")
    else:
        print("\nSUCCESS: You're in an isolated environment!",
              "Safe to install packages without affecting",
              "the global system.",
              "\nPackage installation path:",
              site.getsitepackages()[0], sep="\n")


if __name__ == "__main__":
    main()
