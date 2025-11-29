import csv
import sys

def calculate_average(marks_dict):
    vals = list(marks_dict.values())
    return sum(vals) / len(vals) if vals else 0

def calculate_median(marks_dict):
    vals = sorted(marks_dict.values())
    n = len(vals)
    if n == 0:
        return 0
    mid = n // 2
    if n % 2:
        return vals[mid]
    return (vals[mid - 1] + vals[mid]) / 2

def find_max_score(marks_dict):
    if not marks_dict:
        return None, None
    name = max(marks_dict, key=marks_dict.get)
    return name, marks_dict[name]

def find_min_score(marks_dict):
    if not marks_dict:
        return None, None
    name = min(marks_dict, key=marks_dict.get)
    return name, marks_dict[name]

def assign_grades(marks_dict):
    grades = {}
    distribution = {"A":0,"B":0,"C":0,"D":0,"F":0}
    for name, score in marks_dict.items():
        if score >= 90:
            g = "A"
        elif score >= 80:
            g = "B"
        elif score >= 70:
            g = "C"
        elif score >= 60:
            g = "D"
        else:
            g = "F"
        grades[name] = g
        distribution[g] += 1
    return grades, distribution

def read_csv(path):
    d = {}
    try:
        with open(path, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                name = row[0].strip()
                try:
                    score = float(row[1])
                except:
                    continue
                d[name] = score
    except FileNotFoundError:
        print("File not found.")
    return d

def manual_input():
    d = {}
    print("Enter at least 5 students (type 'done' as name to finish):")
    while True:
        name = input("Name: ").strip()
        if name.lower() == "done":
            break
        if name == "":
            continue
        score_raw = input("Marks (0-100): ").strip()
        try:
            score = float(score_raw)
        except:
            print("Invalid marks, try again.")
            continue
        d[name] = score
    return d

def print_table(marks_dict, grades_dict):
    print("\nName".ljust(20) + "Marks".rjust(8) + "   " + "Grade".rjust(6))
    print("-" * 36)
    for name, mark in marks_dict.items():
        g = grades_dict.get(name, "")
        print(f"{name.ljust(20)}{str(int(mark)).rjust(8)}   {g.rjust(6)}")
    print()

def export_csv(filename, marks_dict, grades_dict):
    try:
        with open(filename, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Name","Marks","Grade"])
            for name, mark in marks_dict.items():
                writer.writerow([name, int(mark), grades_dict.get(name,"")])
        print("Exported to", filename)
    except Exception as e:
        print("Export failed:", e)

def run_analysis(marks):
    if not marks:
        print("No data to analyze.")
        return
    avg = calculate_average(marks)
    med = calculate_median(marks)
    max_name, max_score = find_max_score(marks)
    min_name, min_score = find_min_score(marks)
    grades, dist = assign_grades(marks)
    passed = [n for n,s in marks.items() if s >= 40]
    failed = [n for n,s in marks.items() if s < 40]
    print("\n--- Analysis Summary ---")
    print(f"Students analysed: {len(marks)}")
    print(f"Average: {avg:.2f}")
    print(f"Median: {med}")
    print(f"Highest: {max_name} ({int(max_score)})")
    print(f"Lowest: {min_name} ({int(min_score)})")
    print("\nGrade distribution:")
    for k in ["A","B","C","D","F"]:
        print(f"{k}: {dist[k]}")
    print(f"\nPassed ({len(passed)}): {', '.join(passed) if passed else 'None'}")
    print(f"Failed ({len(failed)}): {', '.join(failed) if failed else 'None'}")
    print_table(marks, grades)
    while True:
        choice = input("Export results to CSV? (y/n): ").strip().lower()
        if choice == "y":
            fname = input("Filename (example: results.csv): ").strip()
            export_csv(fname, marks, grades)
            break
        if choice == "n":
            break

def main():
    print("GradeBook Analyzer")
    while True:
        print("\nMenu:")
        print("1. Manual entry")
        print("2. Load from CSV")
        print("3. Exit")
        choice = input("Choose (1/2/3): ").strip()
        if choice == "1":
            marks = manual_input()
            if len(marks) < 1:
                print("No students entered.")
            run_analysis(marks)
        elif choice == "2":
            path = input("CSV path: ").strip()
            marks = read_csv(path)
            if not marks:
                print("No valid rows found in CSV.")
            run_analysis(marks)
        elif choice == "3":
            print("Exiting. Goodbye.")
            sys.exit()
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
