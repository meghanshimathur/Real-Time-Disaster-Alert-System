import matplotlib.pyplot as plt
import pandas as pd

def plot_disaster_counts(df):
    """
    Bar chart of disaster type frequency
    """
    counts = df["disaster_type"].value_counts()

    plt.figure()
    counts.plot(kind="bar")
    plt.title("Disaster Type Distribution")
    plt.xlabel("Disaster Type")
    plt.ylabel("Count")
    plt.show()


def plot_severity_heatmap(df):
    """
    Heatmap-like visualization using table
    """
    pivot = pd.crosstab(df["disaster_type"], df["severity"])
    print("\nSeverity Heatmap (Table View):\n")
    print(pivot)
