from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def load_vna_data(filepath: Path) -> pd.DataFrame:
    """Laad een VNA CSV-bestand en behoud frequentie, PCB S31 en Antenne S41."""
    df = pd.read_csv(filepath, sep=";", comment="#").dropna(axis=1, how="all")
    df["freq_ghz"] = pd.to_numeric(df["freq[Hz]"], errors="coerce") / 1e9
    df["db:Trc1_S31"] = pd.to_numeric(df["db:Trc1_S31"], errors="coerce")
    df["db:Trc2_S41"] = pd.to_numeric(df["db:Trc2_S41"], errors="coerce")
    return df[["freq_ghz", "db:Trc1_S31", "db:Trc2_S41"]].dropna()


def plot_grid(
    datasets: dict[str, pd.DataFrame],
    column: str,
    suptitle: str,
    output_name: str,
) -> None:
    """Teken een 2x2-grid voor de gekozen magnitude-kolom."""
    fig, axes = plt.subplots(2, 2, figsize=(13, 8.5), sharex=True, sharey=True)
    axes = axes.flatten()
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]

    for ax, (name, df), color in zip(axes, datasets.items(), colors):
        ax.plot(df["freq_ghz"], df[column], color=color, linewidth=1.3)
        ax.set_title(name, fontsize=11, fontweight="bold")
        ax.grid(True, linestyle="--", alpha=0.4)

    for ax in axes[2:]:
        ax.set_xlabel("Frequentie (GHz)", fontsize=10)
    for ax in [axes[0], axes[2]]:
        ax.set_ylabel("Magnitude (dB)", fontsize=10)

    fig.suptitle(suptitle, fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(output_name, dpi=250)


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    files = [base_dir / f"PCB 1 opstelling {i}.csv" for i in range(1, 5)]
    datasets = {f.stem: load_vna_data(f) for f in files if f.exists()}

    if not datasets:
        raise FileNotFoundError(
            "Geen 'PCB 1 opstelling 1.csv' t/m 'PCB 1 opstelling 4.csv' gevonden."
        )

    # 1. Grafiek voor PCB (db:Trc1_S31)
    plot_grid(
        datasets=datasets,
        column="db:Trc1_S31",
        suptitle="Magnitude per testopstelling PCB",
        output_name=str(base_dir / "meeting_pcb_1.png"),
    )

    # 2. Grafiek voor Antenne (db:Trc2_S41)
    antenne_datasets = {
        f"Antenne opstelling {i}": df
        for i, df in enumerate(datasets.values(), start=1)
    }
    plot_grid(
        datasets=antenne_datasets,
        column="db:Trc2_S41",
        suptitle="Magnitude per testopstelling Antenne",
        output_name=str(base_dir / "meeting_antenne_1.png"),
    )

    plt.show()


if __name__ == "__main__":
    main()