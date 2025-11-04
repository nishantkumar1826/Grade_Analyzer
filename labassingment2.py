"""
GradeBook Analyzer
Author: Nishant Kumar
Date: 2025-11-04
Course: Programming for Problem Solving using Python
Description:
   tool to read student marks (manual or CSV), compute statistics,
  assign grades, display results table, filter pass/fail, and optionally
  export final grade table to CSV.
"""

import csv
import sys
from statistics import mean, median
from typing import Dict, Tuple, List

# -----------------------
# Task 3: Statistical functions
# -----------------------
def calculate_average(marks: Dict[str, float]) -> float:
    if not marks:
        return 0.0
    return mean(marks.values())

def calculate_median(marks: Dict[str, float]) -> float:
    if not marks:
        return 0.0
    # use statistics.median for correctness
    return median(marks.values())

def find_max_score(marks: Dict[str, float]) -> Tuple[str, float]:
    if not marks:
        return ("", 0.0)
    name = max(marks, key=marks.get)
    return (name, marks[name])

def find_min_score(marks: Dict[str, float]) -> Tuple[str, float]:
    if not marks:
        return ("", 0.0)
    name = min(marks, key=marks.get)
    return (name, marks[name])

# -----------------------
# Task 4: Grade assignment
# -----------------------
def assign_grade(score: float) -> str:
    """Return letter grade for a numeric score."""
    if score >= 90:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 50:
        return "C"
    elif score >= 33:
        return "D"
    else:
        return "F"

def build_gradebook(marks: Dict[str, float]) -> Dict[str, str]:
    return {name: assign_grade(score) for name, score in marks.items()}

def grade_distribution(grades: Dict[str, str]) -> Dict[str, int]:
    dist = {g: 0 for g in ["A", "B", "C", "D", "F"]}
    for g in grades.values():
        if g in dist:
            dist[g] += 1
    return dist

# -----------------------
# Task 5: Pass/Fail filter using list comprehension
# -----------------------
def pass_fail_lists(marks: Dict[str, float], pass_threshold: float = 40.0) -> Tuple[List[Tuple[str,float]], List[Tuple[str,float]]]:
    passed = [(n, s) for n, s in marks.items() if s >= pass_threshold]
    failed = [(n, s) for n, s in marks.items() if s < pass_threshold]
    return passed, failed

# -----------------------
# CSV handling functions
# -----------------------
def load_csv(filepath: str) -> Dict[str, float]:
    marks = {}
    try:
        with open(filepath, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            #  only Accept files with header like: Name,Marks or direct rows name,mark
            for row in reader:
                if not row:
                    continue
                # only take first two columns
                name = row[0].strip()
                try:
                    score = float(row[1])
                except (IndexError, ValueError):
                    # skip or treat invalid as 0
                    print(f"Warning: invalid or missing mark for '{name}', skipping.")
                    continue
                marks[name] = score
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
    except Exception as e:
        print(f"Error reading CSV: {e}")
    return marks

def export_csv(filepath: str, marks: Dict[str, float], grades: Dict[str, str]) -> None:
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Marks", "Grade"])
            for name in marks:
                writer.writerow([name, marks[name], grades.get(name, "")])
        print(f"Exported results to '{filepath}'.")
    except Exception as e:
        print(f"Error exporting CSV: {e}")

# -----------------------
# Task 6: Display / formatting utilities
# -----------------------
def print_results_table(marks: Dict[str, float], grades: Dict[str, str]) -> None:
    # Determine column widths
    name_w = max([len("Name")] + [len(n) for n in marks.keys()]) + 2
    marks_w = max(len("Marks"), 7) + 2
    grade_w = len("Grade") + 2

    header = f"{'Name'.ljust(name_w)}{'Marks'.rjust(marks_w)}{'Grade'.rjust(grade_w)}"
    sep = "-" * (name_w + marks_w + grade_w)
    print("\n" + header)
    print(sep)
    # Sort by name for consistent display
    for name in sorted(marks.keys()):
        m = marks[name]
        g = grades.get(name, "")
        print(f"{name.ljust(name_w)}{str(m).rjust(marks_w)}{g.rjust(grade_w)}")
    print(sep + "\n")

def print_summary(marks: Dict[str, float], grades: Dict[str, str]) -> None:
    avg = calculate_average(marks)
    med = calculate_median(marks)
    max_name, max_score = find_max_score(marks)
    min_name, min_score = find_min_score(marks)
    dist = grade_distribution(grades)

    print("Analysis Summary:")
    print(f"  Total students: {len(marks)}")
    print(f"  Average (mean): {avg:.2f}")
    print(f"  Median: {med:.2f}")
    print(f"  Highest: {max_name} ({max_score})")
    print(f"  Lowest : {min_name} ({min_score})")
    print("  Grade distribution:")
    for g in ["A","B","C","D","F"]:
        print(f"    {g}: {dist[g]}")

# -----------------------
# Task 2: Manual entry
# -----------------------
def manual_entry() -> Dict[str, float]:
    marks = {}
    print("\nManual data entry. Type 'done' as name when finished.")
    while True:
        name = input("Enter student name (or 'done'): ").strip()
        if name.lower() == 'done':
            break
        if not name:
            print("Name cannot be empty. Try again.")
            continue
        score_raw = input(f"Enter marks for {name}: ").strip()
        try:
            score = float(score_raw)
            marks[name] = score
        except ValueError:
            print("Invalid mark. Please enter a numeric value (e.g., 78 or 78.5).")
    return marks

# -----------------------
#  main loop(task 1) 
# -----------------------
def main():
    print("="*50)
    print("Welcome to GradeBook Analyzer")
    print("Options: 1) Manual entry  2) Load CSV  3) Exit")
    print("="*50)

    while True:
        choice = input("\nChoose an option (1-manual, 2-csv, 3-exit): ").strip()
        if choice == '1':
            marks = manual_entry()
        elif choice == '2':
            path = input("Enter CSV file path (e.g., students.csv): ").strip()
            marks = load_csv(path)
            if not marks:
                print("No valid student data loaded from CSV.")
        elif choice == '3':
            print("Exiting. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please select 1, 2, or 3.")
            continue

        # If no students, loop back
        if not marks:
            print("No student records to analyze. Try again or add students.")
            continue

        # Build grades & summaries
        grades = build_gradebook(marks)
        print_results_table(marks, grades)
        print_summary(marks, grades)

        # Task 5: pass/fail with list comprehension
        passed, failed = pass_fail_lists(marks, pass_threshold=40.0)
        print(f"\nPassed students ({len(passed)}): {[n for n, _ in passed]}")
        print(f"Failed students ({len(failed)}): {[n for n, _ in failed]}")
        # Repeat or exit loop
        again = input("\nDo you want to run another analysis? (y/n): ").strip().lower()
        if again != 'y':
            print("Thankyou. Have a nice day!")
            break

if __name__ == "__main__":
    main()
