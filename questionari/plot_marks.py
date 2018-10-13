import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import seaborn as sns
import glob

sns.set_palette("tab20")

def get_marks(data: pd.DataFrame) -> pd.DataFrame:
    rows = []
    unit, question = None, None

    for i, row in data.iterrows():
        if row[0] == "UD:":
            unit = row[1].split()[0]
            question = 1
        elif "?" in str(row[0]):
            students = np.int32(row[2])
            answers = np.int32(row[4:9:2])
            weights = np.arange(10, 40, 10)
            mark = np.sum(weights * answers) / students
            rows.append([unit, question, students, mark])
            question += 1

    columns=["Unit", "Question", "Students", "Mark"]
    df = pd.DataFrame(rows, columns=columns)
    return df

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
    sns.scatterplot(studs, marks)

    fig = plt.figure(f"units-scatter")
    sns.scatterplot(studs, marks, label=yy)

    fig = plt.figure("units-density")
    avg, std = np.average(marks), np.std(marks)
    text = f"{yy}:\navg={avg:.2f},\nstd={std:.2f}"
    sns.distplot(marks, label=text, hist=False, kde=True,
                 kde_kws={"shade": True, "linewidth": 3})

def plot_questions(data: pd.DataFrame, yy: str):
    marks = data["Mark"]
    fig = plt.figure("questions-density")
    avg, std = np.average(marks), np.std(marks)
    text = f"{yy}:\navg={avg:.2f},\nstd={std:.2f}"        
    sns.distplot(marks, label=text, hist=False, kde=True,
                 kde_kws={"shade": True, "linewidth": 3})

def plot_question(quest: int, data: pd.DataFrame, yy: str):
    # Subset to the question
    subset = data[data["Question"] == quest]
    studs, marks = subset["Students"], subset["Mark"]

    fig = plt.figure(f"questions-density-Q{quest:02}")
    avg, std = np.average(marks), np.std(marks)
    text = f"{yy}:\navg={avg:.2f},\nstd={std:.2f}"        
    sns.distplot(marks, label=text, hist=False, kde=True,
                 kde_kws={"shade": True, "linewidth": 3})

    fig = plt.figure(f"questions-density-{yy}")
    text = f"Q{quest:02}"
    sns.distplot(marks, label=text, hist=False, kde=True,
                 kde_kws={"shade": True, "linewidth": 3})

    fig = plt.figure(f"questions-scatter-{yy}")
    sns.scatterplot(studs, marks, label=f"Q{quest:02}")

def main():
    for filename in reversed(glob.glob("report-*.csv")):
        # transform data
        yy = filename[7:-4]
        report = pd.read_csv(filename)
        data = get_marks(report)
        #data.to_csv(f"marks-{yy}.csv", index=False)
        units = get_units(data)
        #units.to_csv(f"units-{yy}.csv", index=False)

        # plot data
        plot_units(units, yy)
        plot_questions(data, yy)
        for quest in range(1, 12):
            plot_question(quest, data, yy)

    # save figures
    for i in plt.get_fignums():
        fig = plt.figure(i)
        fig.savefig(fig.get_label() + ".pdf")

main()
