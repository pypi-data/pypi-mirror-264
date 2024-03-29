import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
import seaborn as sns

from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter, MultipleLocator
from scipy.interpolate import interp1d

from hygeoclas.fonts import cambria
from hygeoclas.utils.changeover import rgb_to_matplotlib

def plot_train_validation_curve(trainLosses, validationLosses):
    lenInfo = len(trainLosses)
    if lenInfo == 1:
        return
    elif lenInfo == 2:
        kind = "linear"
    elif lenInfo == 3:
        kind = "quadratic"
    else:
        kind = "cubic"
    _, ax = plt.subplots(1, 1)
    ax.cla()

    xTrainLosses = np.linspace(1, len(trainLosses), len(trainLosses))
    yTrainLosses = trainLosses
    functionTrainLosses = interp1d(xTrainLosses, yTrainLosses, kind=kind)
    xInterpolatedTrainLosses = np.linspace(1, len(trainLosses), num=1000)
    yInterpolatedTrainLosses = functionTrainLosses(xInterpolatedTrainLosses)
    line, = plt.plot(xInterpolatedTrainLosses, yInterpolatedTrainLosses, label="Entrenamiento")
    plt.scatter(xTrainLosses, yTrainLosses, color=line.get_color(), s=20)

    xValidationLosses = np.linspace(1, len(validationLosses), len(validationLosses))
    yValidationLosses = validationLosses
    functionValidationLosses = interp1d(xValidationLosses, yValidationLosses, kind=kind)
    xInterpolatedValidationLosses = np.linspace(1, len(validationLosses), num=1000)
    yInterpolatedValidationLosses = functionValidationLosses(xInterpolatedValidationLosses)
    line, = plt.plot(xInterpolatedValidationLosses, yInterpolatedValidationLosses, label="Validación")
    plt.scatter(xValidationLosses, yValidationLosses, color=line.get_color(), s=20)

    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.set_xlabel("Epoca", fontdict=cambria.labelFont)
    ax.set_ylabel("Error", fontdict=cambria.labelFont)
    plt.legend()
    plt.show()

def plot_database(compressedDatabase: pd.DataFrame, **kwargs) -> None:
    """
    This function generates plots from the data contained in a pandas DataFrame. 
    The plots represent the presence and absence of water in a compressed database.

    Parameters:
    compressedDatabase (pd.DataFrame): A pandas DataFrame containing the data to be plotted.
    **kwargs: Additional arguments for customizing the plots. Possible arguments are:
        - colors (list): A list of two colors for the plots. Default is ["gray", "blue"].
        - numberSize (int): The size of the numbers on the plots. Default is 10.
        - legendFontSize (int): The font size of the legend. Default is 9.
        - legendLabelNames (list): A list of two names for the legend labels. Default is ["NWP", "WP"].
        - fontFamily (str): The font family for the plots. Default is "Cambria".
        - fontSize (int): The font size for the plots. Default is 11.
        - formatterAx1 (str): The format of the y-axis for the first plot. Default is "normal".
        - formatterAx3 (str): The format of the y-axis for the third plot. Default is "normal".
        - saveFigures (bool): If True, saves the plots as .png files. Default is False.
        - savePaths (list): A list of three file paths to save the plots. Default is ["fig1.png", "fig2.png", "fig3.png"].

    Returns:
    None. Displays the plots and, if saveFigures is True, saves the plots at the specified paths.
    """
    
    data = {
        "NWP": compressedDatabase[compressedDatabase["Label"] == 0],
        "WP": compressedDatabase[compressedDatabase["Label"] == 1]
    }

    coefficients = np.arange(1, len(data["WP"].mean()[1:])+1)
    formatters = {
        "normal": FuncFormatter(lambda y, _: "{:.16g}".format(y*1e-0)),
        "kilo": FuncFormatter(lambda y, _: "{:.16g}K".format(y*1e-3)),
        "mega": FuncFormatter(lambda y, _: "{:.16g}M".format(y*1e-6))
    }

    colors = kwargs.get("colors", ["gray", "blue"])
    labelSize = kwargs.get("numberSize", 10)
    legendFontSize = kwargs.get("legendFontSize", 9)
    legendLabelNames = kwargs.get("legendLabelNames", ["NWP", "WP"])

    plt.rcParams["font.family"] = kwargs.get("fontFamily", "Cambria")
    plt.rcParams["font.size"] = kwargs.get("fontSize", 11)
    
    figs = []
    for i, (set, color) in enumerate(zip(["NWP", "WP"], colors)):
        fig, ax = plt.subplots()
        ax.fill_between(coefficients, data[set].min()[1:], data[set].max()[1:], color=color, alpha=0.3)
        ax.plot(coefficients, data[set].mean()[1:], color=color)
        ax.set_xlabel("Coeficiente")
        ax.set_ylabel("Amplitud")
        ax.tick_params(axis="both", which="major", labelsize=labelSize)
        ax.yaxis.set_major_formatter(formatters[kwargs.get(f"formatterAx{i+1}", "normal")])
        sns.despine()
        figs.append(fig)

    fig3, ax = plt.subplots()
    for set, label, color in zip(["NWP", "WP"], legendLabelNames, colors):
        ax.fill_between(coefficients, data[set].min()[1:], data[set].max()[1:], color=color, alpha=0.3, label=label)
    ax.set_xlabel("Coeficiente")
    ax.set_ylabel("Amplitud")
    ax.tick_params(axis="both", which="major", labelsize=labelSize)
    ax.yaxis.set_major_formatter(formatters[kwargs.get("formatterAx3", "normal")])
    legend = ax.legend(frameon=False, fontsize=kwargs.get("legendFontSize", 10), bbox_to_anchor=(1, 1.05))
    for handle in legend.legend_handles:
        handle.set_width(legendFontSize*2.25)
        handle.set_height(legendFontSize/2.75)
    sns.despine()
    figs.append(fig3)

    plt.show()

    if kwargs.get("saveFigures", False):
        savePaths = kwargs.get("savePaths", ["fig1.png", "fig2.png", "fig3.png"])
        for fig, savePath in zip(figs, savePaths):
            fig.savefig(f"{savePath}", dpi=300, bbox_inches="tight")

def plot_database_bars(compressedDatabase: pd.DataFrame, nWPCountFromCompressedDB: int, wPCountFromCompressedDB: int, **kwargs) -> None:
    """
    Generates a bar chart comparing two databases.

    Args:
        compressedDatabase (pd.DataFrame): The compressed database.
        nWPCountFromCompressedDB (int): The number of files for non water presence in the structured database.
        wPCountFromCompressedDB (int): The number of files for water presence in the structured database.

    Kwargs:
        fontFamily (str): The font to use in the chart. Default is "Cambria".
        fontSize (int): The font size to use in the chart. Default is 11.
        saveFigure (bool): If True, saves the chart to a file. Default is False.
        savePath (str): The path where the chart will be saved. Default is "fig.png".

    Returns:
    None. Displays the bar and, if saveFigures is True, saves the bar at the specified paths.
    """
    plt.rcParams["font.family"] = kwargs.get("fontFamily", "Cambria")
    plt.rcParams["font.size"] = kwargs.get("fontSize", 11)

    labels = ("PA", "NPA")

    nWPCount = compressedDatabase["Label"].value_counts().values[0]
    wPCount = compressedDatabase["Label"].value_counts().values[1]
    counts = {
        "Structured DB": np.array([nWPCount, nWPCountFromCompressedDB]),
        "Compressed DB": np.array([wPCount, wPCountFromCompressedDB]),
    }

    white = rgb_to_matplotlib((234, 234, 234))
    black = rgb_to_matplotlib((67, 67, 67))
    blue = rgb_to_matplotlib((72, 139, 202))
    colors = {
        "Structured DB": [white, white], 
        "Compressed DB": [blue, black],
    }

    fig, ax = plt.subplots(figsize=(3,1))
    for i, label in enumerate(labels):
        for databaseName, count in counts.items():
            p = ax.barh(label, count[i], height=0.9, label=databaseName if i == 0 else "", color=colors[databaseName][i], edgecolor="black", linewidth=1.5)

    legendElements1 = [Patch(facecolor=white, edgecolor="black", label="Structured DB")]
    legendElements2 = [Patch(facecolor=black, edgecolor="black", label="Compressed DB (NPA)"),
                       Patch(facecolor=blue, edgecolor="black", label="Compressed DB (PA)")]

    legend1 = ax.legend(handles=legendElements1, loc="upper right", bbox_to_anchor=(0.4, -0.25), frameon=False, fontsize=9)
    ax.legend(handles=legendElements2, loc="upper right", bbox_to_anchor=(1.15, -0.25), frameon=False, fontsize=9)
    ax.add_artist(legend1)

    if kwargs.get("saveFigure", False):
        savePath = kwargs.get("savePath", "fig.png")
        fig.savefig(f"{savePath}", dpi=300, bbox_inches="tight")

    sns.despine()
    plt.show()