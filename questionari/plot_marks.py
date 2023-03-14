import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import seaborn as sns
import glob

#sns.set_palette("tab20")

def get_units(data: pd.DataFrame) -> pd.DataFrame:
    rows = []
    unit_studs, unit_marks = [], []
    for unit in data["Unit"].unique():
        # subset to the unit
        subset = data[data["Unit"] == unit]
        studs, marks = subset["Students"], subset["Mark"]
        unit_stud = sum(studs) / len(studs)
        unit_mark = sum(studs * marks) / sum(studs)
        rows.append([unit, unit_stud, unit_mark])

    columns=["Unit", "Students", "Mark"]
    df = pd.DataFrame(rows, columns=columns)
    return df

def plot_units(units: pd.DataFrame, yy: str):
    studs, marks = units["Students"], units["Mark"]

    fig = plt.figure(f"units-scatter-{yy}")
    sns.scatterplot(x=studs, y=marks)

    fig = plt.figure(f"units-scatter")
    sns.scatterplot(x=studs, y=marks, label=yy)

    fig = plt.figure("units-density")
    avg, std = np.average(marks), np.std(marks)
    text = f"{yy}:\navg={avg:.2f},\nstd={std:.2f}"
    sns.kdeplot(marks, label=text)

def plot_questions(data: pd.DataFrame, yy: str):
    marks = data["Mark"]
    fig = plt.figure("questions-density")
    avg, std = np.average(marks), np.std(marks)
    text = f"{yy}:\navg={avg:.2f},\nstd={std:.2f}"
    sns.kdeplot(marks, label=text)

def plot_question(data: pd.DataFrame, quest: int, yy: str):
    # Subset to the question
    subset = data[data["Question"] == quest]
    studs, marks = subset["Students"], subset["Mark"]

    fig = plt.figure(f"questions-density-Q{quest:02}")
    avg, std = np.average(marks), np.std(marks)
    text = f"{yy}:\navg={avg:.2f},\nstd={std:.2f}"
    sns.kdeplot(marks, label=text, fill=True)

    fig = plt.figure(f"questions-density-{yy}")
    text = f"Q{quest:02}"
    sns.kdeplot(marks, label=text)

    fig = plt.figure(f"questions-scatter-{yy}")
    sns.scatterplot(x=studs, y=marks, label=f"Q{quest:02}")

def main():
    for filename in reversed(glob.glob("marks-*.csv")):
        # transform data
        yy = filename.split("-", 1)[1].split(".", 1)[0]
        data = pd.read_csv(filename)
        #data.to_csv(f"marks-{yy}.csv", index=False)
        units = get_units(data)
        #units.to_csv(f"units-{yy}.csv", index=False)

        # plot data
        plot_units(units, yy)
        plot_questions(data, yy)
        for quest in range(1, 12):
            plot_question(data, quest, yy)

    # save figures
    for i in plt.get_fignums():
        fig = plt.figure(i)
        plt.legend()
        fig.savefig(fig.get_label() + ".pdf")

main()
