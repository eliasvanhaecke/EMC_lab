from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def load_pcb_magnitude(filepath: Path) -> pd.DataFrame:
    """Laad een PCB 2 CSV-bestand en behoud frequentie en db:Trc1_S31."""
    df = pd.read_csv(filepath, sep=";", comment="#").dropna(axis=1, how="all")
    df["freq_ghz"] = pd.to_numeric(df["freq[Hz]"], errors="coerce") / 1e9
    df["db:Trc1_S31"] = pd.to_numeric(df["db:Trc1_S31"], errors="coerce")
    return df[["freq_ghz", "db:Trc1_S31"]].dropna()


def main() -> None:
    base_dir = Path(__file__).resolve().parent

    # Bovenste rij: Near-end 1, 2, 3 | Onderste rij: Far-end 1, 2, 3
    ordered_names = [
        "PCB 2 opstelling 1 Near-end.csv",
        "PCB 2 opstelling 2 Near-end.csv",
        "PCB 2 opstelling 3 Near-end.csv",
        "PCB 2 opstelling 1 Far-end.csv",
        "PCB 2 opstelling 2 Far-end.csv",
        "PCB 2 opstelling 3 Far-end.csv",
    ]

    items = [
        (Path(name).stem, load_pcb_magnitude(base_dir / name))
        for name in ordered_names
        if (base_dir / name).exists()
    ]

    if not items:
        raise FileNotFoundError("Geen PCB 2 CSV-bestanden gevonden.")

    fig, axes = plt.subplots(2, 3, figsize=(16, 8.5), sharex=True, sharey=True)
    axes = axes.flatten()
    colors = ["#1f77b4", "#2ca02c", "#9467bd", "#ff7f0e", "#d62728", "#8c564b"]

    for ax, (title, df), color in zip(axes, items, colors):
        ax.plot(df["freq_ghz"], df["db:Trc1_S31"], color=color, linewidth=1.3)
        ax.set_title(title, fontsize=10.5, fontweight="bold")
        ax.grid(True, linestyle="--", alpha=0.4)

    for ax in axes[3:]:
        ax.set_xlabel("Frequentie (GHz)", fontsize=10)
    for ax in [axes[0], axes[3]]:
        ax.set_ylabel("Magnitude (dB)", fontsize=10)

    fig.suptitle(
        "Magnitude per testopstelling PCB",
        fontsize=13,
        fontweight="bold",
    )
    plt.tight_layout()
    plt.savefig(base_dir / "meeting_pcb_2.png", dpi=220)
    plt.show()


if __name__ == "__main__":
    main()