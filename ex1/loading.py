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
    import numpy.typing as npt
    NUMPY_VERSION = np.__version__
    NUMPY_OK = True
except ImportError:
    NUMPY_OK = False
    NUMPY_VERSION = "NOT INSTALLED"

try:
    import matplotlib as mpl
    mpl.use("Agg")
    import matplotlib.pyplot as plt
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


def generate_data(n: int) -> "npt.NDArray[np.float64]":
    # repoducibility
    np.random.seed(42)

    # time axis - n points from 0 to 4pi (two full sine cycles)
    t = np.linspace(0, 4 * np.pi, n)

    # base signal - sine wave with amplitude 2
    base = np.sin(t) * 2

    # machine noise - gaussian with std (standart deviation) 0.5
    noise = np.random.randn(n) * 0.5

    # combined signal
    combined = base + noise

    # inject 15 random "glitches" - spikes of +/-4
    glitch_indices = np.random.randint(0, n, 15)
    combined[glitch_indices] += np.random.choice([-1, 1], 15) * 4

    print(f"\nProcessing {n} data point...")

    # stack into a 2D array
    return np.column_stack([t, base, noise, combined])


def analyse_data(data: "npt.NDArray[np.float64]") -> "pd.DataFrame":
    print("Analyzing Matrix data...")

    # create DataFrame from numpy - column names map to the 4 array columns
    df = pd.DataFrame(data,
                      columns=["time", "base_signal", "noise", "combined"])

    # anomaly column - boolean mask where signal deviates too far
    # df["anomaly"] = df["combined"].abs() > 3.0
    df["rolling_mean"] = df["combined"].rolling(window=20).mean()
    rolling_std = df["combined"].rolling(window=20).std()
    z_score = (df["combined"] - df["rolling_mean"]) / rolling_std
    df["anomaly"] = z_score.abs() > 2.5

    anomaly_count = df["anomaly"].sum()
    print(f"  Signal mean:\t{df['combined'].mean():.4f}")
    print(f"  Signal std:\t{df['combined'].std():.4f}")
    print(f"  Anomalies found:\t{anomaly_count}")

    return df


def visualise(df: "pd.DataFrame") -> None:
    print("Generating visualization...")

    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    fig.suptitle("Matrix Signal Analysis", fontsize=14)

    # signal over time with anomalies and rolling mean:
    # raw combined signal
    axes[0].plot(df["time"],
                 df["combined"],
                 color="green",
                 alpha=0.6,
                 label="Signal")

    # rolling mean overlay
    axes[0].plot(df["time"],
                 df["rolling_mean"],
                 color="cyan",
                 linewidth=2,
                 label="Rolling mean")

    # anomalies as red dots
    # boolean indexing to filter only anomaly rows
    anomalies = df[df["anomaly"]]
    axes[0].scatter(anomalies["time"],
                    anomalies["combined"],
                    color="red",
                    zorder=5,
                    label="Anomaly")

    axes[0].set_title("Matrix Code Stream")
    axes[0].set_xlabel("Time")
    axes[0].set_ylabel("Signal Amptitude")
    axes[0].legend()

    # signal distribution histogram:
    axes[1].hist(df["combined"],
                 bins=40,
                 color="green",
                 alpha=0.7,
                 edgecolor="black")
    axes[1].set_title("Signal Distribution")
    axes[1].set_xlabel("Amplitude")
    axes[1].set_ylabel("Frequency")

    # saving and closing
    plt.tight_layout()
    plt.savefig("matrix_analysis.png", dpi=100)
    plt.close()
    print("Results saved to: matrix_analysis.png")


def compare_managers() -> None:
    print("\nPackage manager comparison:",
          "pip\t-> uses requirements.txt | flat list | no lock file",
          "poetry\t-> uses pyproject.toml | dependency graph | poetry.lock",
          sep="\n")


def main() -> None:
    print("\nLOADING STATUS: Loading programs...\n")
    if not check_dependencies():
        print("\nTo install all missing dependencies:")
        print("  pip:    pip install -r requirements.txt")
        print("  poetry: poetry install")
        print("          poetry run python loading.py")
        sys.exit(1)
    data = generate_data(1000)
    df = analyse_data(data)
    visualise(df)
    print("\nAnalysis complete!")
    compare_managers()


if __name__ == "__main__":
    main()
