import os
import seaborn as sns
import matplotlib.pyplot as plt

from pandas import DataFrame

def plot_df(df: DataFrame, output="output.png"):
    sns.barplot(df, x="host", y="count()", hue="host")
    plt.savefig(output)
    plt.close()
    print("The image has been saved to " + os.path.realpath(output))
