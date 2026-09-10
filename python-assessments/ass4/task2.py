import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def load_dataset(filename="Sports_car_prices.csv"):
    if os.path.exists(filename):
        return pd.read_csv(filename)
    url = "https://raw.githubusercontent.com/rkiattisak/Sports-car-prices-dataset/main/Sports%20car%20prices.csv"
    return pd.read_csv(url)


def clean_dataset(df):
    data = df.dropna().drop_duplicates().copy()
    cols = [
        "Horsepower",
        "Torque (lb-ft)",
        "0-60 MPH",
        "Top Speed (mph)",
        "Price (in USD)",
    ]
    for col in cols:
        if col in data.columns:
            cleaned = data[col].astype(str).str.replace(
                r"[$,HP,hp,lb-ft,\s+]", "", regex=True
            )
            data[col] = pd.to_numeric(cleaned, errors="coerce")
    if "Year" in data.columns:
        data["Year"] = pd.to_numeric(data["Year"], errors="coerce")
    return data.dropna(subset=cols)


def compute_statistics(df):
    stats = df.describe().transpose()
    mode_val = df.mode().iloc[0]
    stats["mode"] = mode_val
    stats["range"] = stats["max"] - stats["min"]
    return stats[["mean", "50%", "mode", "std", "min", "max", "range"]]


def avg_price_by_make(df):
    return (
        df.groupby("Make")["Price (in USD)"].mean().sort_values(ascending=False)
    )


def avg_hp_by_year(df):
    valid_year = df.dropna(subset=["Year"])
    return valid_year.groupby("Year")["Horsepower"].mean().sort_index()


def plot_price_vs_hp(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    valid = df.dropna(subset=["Horsepower", "Price (in USD)"])
    ax.scatter(valid["Horsepower"], valid["Price (in USD)"], alpha=0.7)

    z = np.polyfit(valid["Horsepower"], valid["Price (in USD)"], 1)
    p = np.poly1d(z)
    sorted_hp = np.sort(valid["Horsepower"])
    ax.plot(sorted_hp, p(sorted_hp), "r--", label="Regression Line")

    ax.set_title("Price vs Horsepower")
    ax.set_xlabel("Horsepower")
    ax.set_ylabel("Price (in USD)")
    ax.legend()
    plt.tight_layout()
    fig.savefig("price_vs_horsepower.png")
    return fig


def plot_0_60_histogram(df):
    valid = df.dropna(subset=["0-60 MPH"])
    min_t = valid["0-60 MPH"].min()
    max_t = valid["0-60 MPH"].max()
    bins = np.arange(min_t, max_t + 0.5, 0.5)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(valid["0-60 MPH"], bins=bins, color="skyblue", edgecolor="black")
    ax.set_title("Histogram of 0-60 MPH Times")
    ax.set_xlabel("0-60 MPH Time (s)")
    ax.set_ylabel("Count")
    plt.tight_layout()
    fig.savefig("0_60_mph_histogram.png")
    return fig


def filter_expensive_cars(df):
    expensive = df[df["Price (in USD)"] > 500000]
    return expensive.sort_values(by="Horsepower", ascending=False)


def export_cleaned_data(df, filename="cleaned_sports_car_prices.csv"):
    df.to_csv(filename, index=False)
    return filename


if __name__ == "__main__":
    df = load_dataset()
    print("1. First 5 rows:\n", df.head())

    df_clean = clean_dataset(df)
    print("\n2. Cleaned data info:")
    df_clean.info()

    print("\n3. Summary statistics:\n", compute_statistics(df_clean))
    print("\n4. Average price by make:\n", avg_price_by_make(df_clean))
    print("\n5. Average horsepower by year:\n", avg_hp_by_year(df_clean))

    fig1 = plot_price_vs_hp(df_clean)
    print("\n6. Scatter plot created and saved.")

    fig2 = plot_0_60_histogram(df_clean)
    print("7. Histogram created and saved.")

    print(
        "\n8. Cars > $500,000 sorted by horsepower:\n",
        filter_expensive_cars(df_clean).head(),
    )

    out_file = export_cleaned_data(df_clean)
    print(f"\n9. Cleaned dataset saved to {out_file}")

    plt.show()
