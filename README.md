# Student Performance Analytics System

## Overview

The **Student Performance Analytics System** is a Python-based desktop application built using **Tkinter** and **Matplotlib**. It helps manage student academic records, analyze performance, and generate insightful reports.

This system stores student data in a **CSV file**, ensuring persistent storage and easy data handling.

---

## Features

### Core Functionalities

* Add new student records
* Update existing student data
* Delete student records
* Search students by ID or Name
* Generate individual report cards

### Analytics & Insights

* Subject-wise average performance
* Class-wise performance comparison
* Pass/Fail statistics
* Visual charts using Matplotlib

### Data Management

* Automatic CSV file creation (`students.csv`)
* Data validation (marks between 0–100)
* Schema auto-fix for old data formats
* Export reports:

  * Summary report (`.txt`)
  * Class-wise CSV files

---

## Technologies Used

* **Python**
* **Tkinter** (GUI)
* **Matplotlib** (Data Visualization)
* **CSV Module** (Data Storage)
* **OS Module**

---

## How to Run

1. **Clone the repository**

```
git clone (https://github.com/minahil3999-bit/Student-Performance-Analytics-System)
```

2. **Open project folder**

```
cd Student Performance Analytics
```

3. **Run the program**

```
Student Performance Analytics System.py
```

---

## Application Workflow

1. Launch the app → Welcome screen appears
2. Click **"Initialize Dashboard Engine"**
3. Use buttons to:

   * Manage student records
   * View reports
   * Run analytics

---

## Grading Criteria

| Percentage | Grade |
| ---------- | ----- |
| ≥ 85%      | A     |
| ≥ 70%      | B     |
| ≥ 50%      | C     |
| < 50%      | Fail  |

---

## Output Examples

* Transcript window with:

  * Total marks
  * Average
  * Grade

* Dashboard:

  * Bar charts for subject averages
  * Class performance comparison

* Exported files:

  * `performance_summary_report.txt`
  * `class_<class_name>_analytics.csv`

---

## Notes

* Ensure `students.csv` is **not open in Excel** while running
* All fields are required when adding/updating data
* Marks must be between **0 and 100**

---

## Future Improvements

* Login system (Admin/User roles)
* Database integration (SQLite/MySQL)
* PDF report generation
* Advanced analytics (Topper, trends)
* UI enhancements

---

## Author

**Minahil Noor**
GitHub: https://github.com/minahil3999-bit

---

