import csv

for yy in ["2016-2017", "2017-2018"]:
    fn1, fn2 = f"report-{yy}.csv", f"marks-{yy}.csv"
    with open(fn1) as file1, open(fn2, "w") as file2:
        reader, writer = csv.reader(file1), csv.writer(file2)
        writer.writerow(["Unit", "Question", "Students", "Mark"])

        unit, question = None, None
        for row in reader:
            if row[0] == "UD:":
                unit = row[1].split()[0]
                question = 1
            elif "?" in row[0]:
                students = int(row[2])
                c10, c20, c30 = int(row[4]), int(row[6]), int(row[8])
                mark = (10*c10 + 20*c20 + 30*c30) / students
                writer.writerow([unit, question, students, mark])
                question += 1
