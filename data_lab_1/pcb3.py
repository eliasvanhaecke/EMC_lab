from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def load_pcb_magnitude(filepath: Path) -> pd.DataFrame:
    """Laad een PCB 3 CSV-bestand en behoud frequentie en db:Trc1_S31."""
    df = pd.read_csv(filepath, sep=";", comment="#").dropna(axis=1, how="all")
    df["freq_ghz"] = pd.to_numeric(df["freq[Hz]"], errors="coerce") / 1e9
    df["db:Trc1_S31"] = pd.to_numeric(df["db:Trc1_S31"], errors="coerce")
    return df[["freq_ghz", "db:Trc1_S31"]].dropna()


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    files = [base_dir / f"PCB 3 opstelling {i}.csv" for i in range(1, 5)]
    datasets = {f.stem: load_pcb_magnitude(f) for f in files if f.exists()}

    if not datasets:
        raise FileNotFoundError(
            "Geen 'PCB 3 opstelling 1.csv' t/m 'PCB 3 opstelling 4.csv' gevonden."
        )

    fig, axes = plt.subplots(2, 2, figsize=(13, 8.5), sharex=True, sharey=True)
    axes = axes.flatten()
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]

    for ax, (name, df), color in zip(axes, datasets.items(), colors):
        ax.plot(df["freq_ghz"], df["db:Trc1_S31"], color=color, linewidth=1.3)
        ax.set_title(name, fontsize=11, fontweight="bold")
        ax.grid(True, linestyle="--", alpha=0.4)

    for ax in axes[2:]:
        ax.set_xlabel("Frequentie (GHz)", fontsize=10)
    for ax in [axes[0], axes[2]]:
        ax.set_ylabel("Magnitude (dB)", fontsize=10)

    fig.suptitle(
        "Magnitude per testopstelling PCB 3",
        fontsize=13,
        fontweight="bold",
    )
    plt.tight_layout()
    plt.savefig(base_dir / "meeting_pcb_3.png", dpi=250)
    plt.show()


if __name__ == "__main__":
    main()