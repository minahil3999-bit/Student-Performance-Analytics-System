import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

FILE = "students.csv"
SUBJECTS = ["Math", "Science", "English"]
HEADERS = ["ID", "Name", "Class", "Math", "Science", "English"]


# ---------------- DATA PERSISTENCE LAYER ----------------

def init_file():
    """Initializes the file with the strict required schema if it doesn't exist."""
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(HEADERS)


def read_data():
    """Reads the CSV file, handles missing files, and ensures schema compliance."""
    if not os.path.exists(FILE):
        init_file()
        return [HEADERS]

    try:
        with open(FILE, "r", encoding="utf-8") as f:
            rows = list(csv.reader(f))
            if not rows or len(rows) == 0:
                return [HEADERS]

            # Auto-Fix Schema: Check if header matches requirements
            if rows[0] != HEADERS:
                if len(rows[0]) == 5:  # Upgrading old 5-column structure safely
                    upgraded_rows = [HEADERS]
                    for r in rows[1:]:
                        if len(r) == 5:
                            upgraded_rows.append([r[0], r[1], "10A", r[2], r[3], r[4]])
                    write_data(upgraded_rows)
                    return upgraded_rows
                else:
                    return [HEADERS]
            return rows
    except PermissionError:
        messagebox.showerror("File Lock Error",
                             "The file 'students.csv' is open in another program.\nPlease close it and try again.")
        return [HEADERS]
    except Exception as e:
        messagebox.showerror("File Error", f"Could not read dataset: {e}")
        return [HEADERS]


def write_data(rows):
    """Saves records back to the local CSV database file."""
    try:
        with open(FILE, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerows(rows)
    except PermissionError:
        messagebox.showerror("Permission Error",
                             "Cannot write data. Please close 'students.csv' if it is open in Excel.")
    except Exception as e:
        messagebox.showerror("File Error", f"Failed to save tracking records: {e}")


# ---------------- PERFORMANCE CALCULATION MODULE ----------------

def compute_metrics(math_val, sci_val, eng_val):
    """Calculates summary statistics and maps correct academic letter ranks."""
    total = math_val + sci_val + eng_val
    avg = total / 3.0
    pct = (total / 300.0) * 100.0

    if pct >= 85:
        grade = "A"
    elif pct >= 70:
        grade = "B"
    elif pct >= 50:
        grade = "C"
    else:
        grade = "Fail"

    return total, avg, pct, grade


# ---------------- MAIN APPLICATION INTERFACE ----------------

def open_main_app():
    welcome.destroy()

    global root, table, bg, text, accent, card_bg

    root = tk.Tk()
    root.title("Student Performance Analytics System")
    root.geometry("1050x650")

    # Midnight Dark Blue & Teal Theme Configuration
    bg = "#0b132b"  # Deep Midnight Blue Base
    text = "#f4f6f9"  # Crisp Light Gray-White for Labels
    accent = "#00b4d8"  # Vibrant Teal/Cyan Accent
    card_bg = "#1c2541"  # Dark Slate Blue for Cards/Tables

    root.configure(bg=bg)

    # ---------------- MODERN THEMING & STYLES ----------------

    style = ttk.Style()
    style.theme_use("clam")

    style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6, background=accent, foreground="#0b132b")
    style.map("TButton", background=[("active", "#0077b6")], foreground=[("active", "white")])

    # Treeview style configured with #e2e8f0 foreground text for student row visibility
    style.configure("Treeview",
                    background=card_bg,
                    foreground="#e2e8f0",
                    rowheight=30,
                    fieldbackground=card_bg,
                    font=("Segoe UI", 10))

    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#3a506b", foreground=text)
    style.map("Treeview", background=[("selected", "#0077b6")], foreground=[("selected", "#ffffff")])

    # ---------------- TABLE RENDERING LOGIC ----------------

    def load_table():
        """Clears the visual grid and populates rows read directly from the CSV."""
        table.delete(*table.get_children())
        rows = read_data()

        if len(rows) > 1:
            for r in rows[1:]:
                if len(r) < 6:
                    continue
                try:
                    m, s, e = float(r[3]), float(r[4]), float(r[5])
                    _, _, pct, grade = compute_metrics(m, s, e)

                    display_vals = [r[0], r[1], r[2], r[3], r[4], r[5], f"{pct:.1f}%", grade]
                    table.insert("", "end", values=display_vals)
                except (ValueError, IndexError):
                    table.insert("", "end", values=r + ["Parsing Error", "Error"])

    def validate(sid, name, s_class, m, s, e):
        """Validates entry rules and constraints."""
        if not sid or not name or not s_class or not m or not s or not e:
            messagebox.showerror("Validation Error", "All data input fields must be filled completely.")
            return False
        try:
            m_f, s_f, e_f = float(m), float(s), float(e)
            if not (0 <= m_f <= 100 and 0 <= s_f <= 100 and 0 <= e_f <= 100):
                messagebox.showerror("Validation Error", "Subject scores must fall strictly between 0 and 100.")
                return False
        except ValueError:
            messagebox.showerror("Validation Error", "Academic grades must be valid real numbers.")
            return False
        return True

    # ---------------- INTERFACE OPERATIONS (CRUD) ----------------

    def add_window():
        win = tk.Toplevel(root)
        win.title("Add Student Record")
        win.configure(bg=bg)
        win.geometry("350x300")
        win.resizable(False, False)

        labels = ["ID", "Name", "Class", "Math", "Science", "English"]
        entries = []

        for i, l in enumerate(labels):
            tk.Label(win, text=l, bg=bg, fg=text, font=("Segoe UI", 10)).grid(row=i, column=0, padx=20, pady=8,
                                                                              sticky="w")
            e = tk.Entry(win, font=("Segoe UI", 10), bg=card_bg, fg=text, insertbackground="white", bd=1)
            e.grid(row=i, column=1, padx=20, pady=8, sticky="ew")
            entries.append(e)

        def save():
            data = [e.get().strip() for e in entries]
            if not validate(*data):
                return

            rows = read_data()
            for r in rows[1:]:
                if r[0] == data[0]:
                    messagebox.showerror("Conflict", f"Student ID '{data[0]}' already exists.")
                    return

            rows.append(data)
            write_data(rows)
            load_table()
            win.destroy()
            messagebox.showinfo("Success", "New entry added successfully.")

        ttk.Button(win, text="Save Entry", command=save).grid(row=6, column=0, columnspan=2, pady=15)

    def update_window():
        selected = table.selection()
        if not selected:
            messagebox.showerror("Selection Required", "Select a student target row from the list table first.")
            return

        sid = table.item(selected[0])["values"][0]
        rows = read_data()
        current_idx, current_row = -1, None

        for idx, r in enumerate(rows):
            if r[0] == str(sid):
                current_idx = idx
                current_row = r
                break

        if current_row is None:
            messagebox.showerror("Error", "Selected record data was not found.")
            return

        win = tk.Toplevel(root)
        win.title("Update Student Marks")
        win.configure(bg=bg)
        win.geometry("350x300")
        win.resizable(False, False)

        labels = ["Name", "Class", "Math", "Science", "English"]
        entries = []

        for i, l in enumerate(labels):
            tk.Label(win, text=l, bg=bg, fg=text, font=("Segoe UI", 10)).grid(row=i, column=0, padx=20, pady=8,
                                                                              sticky="w")
            e = tk.Entry(win, font=("Segoe UI", 10), bg=card_bg, fg=text, insertbackground="white", bd=1)
            e.insert(0, current_row[i + 1])
            e.grid(row=i, column=1, padx=20, pady=8, sticky="ew")
            entries.append(e)

        def save_update():
            updated_fields = [e.get().strip() for e in entries]
            if not validate(sid, *updated_fields):
                return

            rows[current_idx] = [str(sid)] + updated_fields
            write_data(rows)
            load_table()
            win.destroy()
            messagebox.showinfo("Updated", "Student metrics values updated.")

        ttk.Button(win, text="Update Record", command=save_update).grid(row=6, column=0, columnspan=2, pady=15)

    def delete_student():
        selected = table.selection()
        if not selected:
            messagebox.showerror("Selection Required", "Highlight a profile entry to remove.")
            return

        sid = table.item(selected[0])["values"][0]
        if messagebox.askyesno("Verification", f"Permanently wipe student tracking info for ID {sid}?"):
            rows = read_data()
            new_rows = [rows[0]] + [r for r in rows[1:] if r[0] != str(sid)]
            write_data(new_rows)
            load_table()
            messagebox.showinfo("Purged", "Student history record completely removed.")

    def search_student():
        win = tk.Toplevel(root)
        win.title("Search Database")
        win.configure(bg=bg)
        win.geometry("300x150")
        win.resizable(False, False)

        tk.Label(win, text="Enter Student ID or Full Name:", fg=text, bg=bg, font=("Segoe UI", 10)).pack(pady=10)
        e = tk.Entry(win, font=("Segoe UI", 10), bg=card_bg, fg=text, insertbackground="white")
        e.pack(pady=5)

        def find():
            q = e.get().strip().lower()
            table.delete(*table.get_children())
            all_rows = read_data()
            found = False

            for r in all_rows[1:]:
                if q in r[0].lower() or q in r[1].lower():
                    m, s, p = float(r[3]), float(r[4]), float(r[5])
                    _, _, pct, grade = compute_metrics(m, s, p)
                    table.insert("", "end", values=[r[0], r[1], r[2], r[3], r[4], r[5], f"{pct:.1f}%", grade])
                    found = True

            if not found:
                messagebox.showinfo("Search Result", "No student matches found.")
                load_table()
            win.destroy()

        ttk.Button(win, text="Execute Search", command=find).pack(pady=10)

    def report_card():
        selected = table.selection()
        if not selected:
            messagebox.showerror("Selection Required", "Highlight a student line to generate its report card.")
            return

        d = table.item(selected[0])["values"]
        m, s, e_val = float(d[3]), float(d[4]), float(d[5])
        tot, avg, pct, grade = compute_metrics(m, s, e_val)

        win = tk.Toplevel(root)
        win.configure(bg=card_bg)
        win.title(f"Academic Transcript - {d[1]}")
        win.geometry("420x380")

        tk.Label(win, text="ACADEMIC TRANSCRIPT", bg=card_bg, fg=accent, font=("Segoe UI", 12, "bold")).pack(pady=15)

        details = [
            f"Student ID: {d[0]}",
            f"Full Name: {d[1]}",
            f"Class Track: {d[2]}",
            "----------------------------------",
            f"Mathematics Score: {d[3]}/100",
            f"Science Score: {d[4]}/100",
            f"English Lit Score: {d[5]}/100",
            "----------------------------------",
            f"Cumulative Total: {tot:.1f}",
            f"Calculated Mean Score: {avg:.2f}",
            f"Overall Grade Code Rank: {grade}"
        ]

        for line in details:
            color = "#00b4d8" if "Grade" in line else (text if "Score" in line else "white")
            tk.Label(win, text=line, bg=card_bg, fg=color, font=("Segoe UI", 10)).pack(anchor="w", padx=30, pady=2)

    def analytics_dashboard():
        rows = read_data()[1:]
        if not rows:
            messagebox.showinfo("Analytics Engine", "Database file contains no student data records.")
            return

        total_cohort = len(rows)
        pass_count = fail_count = 0
        sum_math = sum_sci = sum_eng = 0
        class_groups = {}

        for r in rows:
            m, s, e_val = float(r[3]), float(r[4]), float(r[5])
            _, _, pct, grade = compute_metrics(m, s, e_val)

            sum_math += m
            sum_sci += s
            sum_eng += e_val

            if grade != "Fail":
                pass_count += 1
            else:
                fail_count += 1

            c_name = r[2]
            if c_name not in class_groups:
                class_groups[c_name] = []
            class_groups[c_name].append(pct)

        win = tk.Toplevel(root)
        win.configure(bg=bg)
        win.title("Performance Analytics Dashboard")
        win.geometry("750x570")

        top_bar = tk.Frame(win, bg=card_bg)
        top_bar.pack(fill="x", side="top", padx=10, pady=10)

        tk.Label(top_bar, text=f"Total Cohort: {total_cohort} Students", bg=card_bg, fg="white",
                 font=("Segoe UI", 10, "bold")).pack(side="left", padx=15)
        tk.Label(top_bar, text=f"Passing Rate: {((pass_count / total_cohort) * 100):.1f}%", bg=card_bg, fg="#00b4d8",
                 font=("Segoe UI", 10, "bold")).pack(side="left", padx=15)
        tk.Label(top_bar, text=f"Failing / Attention: {fail_count}", bg=card_bg, fg="#ff4d6d",
                 font=("Segoe UI", 10, "bold")).pack(side="left", padx=15)

        # Object-Oriented Isolated Figure Structure
        fig = Figure(figsize=(7, 3.5), facecolor=bg)
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)

        # Chart 1: Subject wise Averages
        ax1.bar(SUBJECTS, [sum_math / total_cohort, sum_sci / total_cohort, sum_eng / total_cohort],
                color=["#00b4d8", "#90e0ef", "#0077b6"])
        ax1.set_title("Subject Means Breakdown", color="#ffffff", fontsize=10, fontweight="bold")
        ax1.set_ylim(0, 100)
        ax1.set_facecolor(card_bg)
        ax1.tick_params(colors="#ffffff", labelsize=9)
        ax1.spines['bottom'].set_color('#3a506b')
        ax1.spines['left'].set_color('#3a506b')
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)

        # Chart 2: Class Benchmarks
        classes = list(class_groups.keys())
        class_averages = [sum(v) / len(v) for v in class_groups.values()]
        ax2.bar(classes, class_averages, color="#00b4d8")
        ax2.set_title("Class Benchmarks Comparison", color="#ffffff", fontsize=10, fontweight="bold")
        ax2.set_ylim(0, 100)
        ax2.set_facecolor(card_bg)
        ax2.tick_params(colors="#ffffff", labelsize=9)
        ax2.spines['bottom'].set_color('#3a506b')
        ax2.spines['left'].set_color('#3a506b')
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)

        canvas = FigureCanvasTkAgg(fig, master=win)

        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=True, padx=20, pady=10)

        canvas.draw()  # 🔥 IMPORTANT: force rendering
        def trigger_export():
            summary_txt_path = "performance_summary_report.txt"
            with open(summary_txt_path, "w", encoding="utf-8") as f:
                f.write("==================================================\n")
                f.write("            STUDENT PERFORMANCE REPORT            \n")
                f.write("==================================================\n\n")
                f.write(f"Total Cohort Size Evaluated: {total_cohort} records\n")
                f.write(f"Math Group Mean: {sum_math / total_cohort:.2f}\n")
                f.write(f"Science Group Mean: {sum_sci / total_cohort:.2f}\n")
                f.write(f"English Group Mean: {sum_eng / total_cohort:.2f}\n")

            all_rows = read_data()
            header = all_rows[0] + ["Total", "Average", "Percentage", "Grade"]

            structured_df_map = {}
            for r in all_rows[1:]:
                m_v, s_v, e_v = float(r[3]), float(r[4]), float(r[5])
                t, av, pc, gr = compute_metrics(m_v, s_v, e_v)
                cls = r[2]
                if cls not in structured_df_map:
                    structured_df_map[cls] = []
                structured_df_map[cls].append(r + [t, f"{av:.2f}", f"{pc:.1f}%", gr])

            for class_id, group_rows in structured_df_map.items():
                with open(f"class_{class_id}_analytics.csv", "w", newline="", encoding="utf-8") as out_f:
                    writer = csv.writer(out_f)
                    writer.writerow(header)
                    writer.writerows(group_rows)

            messagebox.showinfo("Export Engine",
                                f"Summary saved to '{summary_txt_path}' and Class CSV reports generated successfully.")

        ttk.Button(win, text="📥 Export Summary Reports & Class Tracks", command=trigger_export).pack(pady=15)

    # ---------------- INTERFACE ACTION BUTTONS CONTROLS ----------------

    control_frame = tk.Frame(root, bg=bg)
    control_frame.pack(fill="x", side="top", padx=15, pady=15)

    ttk.Button(control_frame, text="➕ Add Student", command=add_window).pack(side="left", padx=5)
    ttk.Button(control_frame, text="✏️ Update Record", command=update_window).pack(side="left", padx=5)
    ttk.Button(control_frame, text="❌ Delete Student", command=delete_student).pack(side="left", padx=5)
    ttk.Button(control_frame, text="🔍 Search Profile", command=search_student).pack(side="left", padx=5)
    ttk.Button(control_frame, text="📜 View Transcript", command=report_card).pack(side="left", padx=5)
    ttk.Button(control_frame, text="📊 Run System Analytics", command=analytics_dashboard).pack(side="left", padx=5)
    ttk.Button(control_frame, text="🔄 Refresh Table View", command=load_table).pack(side="right", padx=5)

    # ---------------- MAIN TREEVIEW COMPONENT DATA GRID ----------------

    cols = ("ID", "Name", "Class", "Math", "Science", "English", "Percentage", "Grade")
    table = ttk.Treeview(root, columns=cols, show="headings")

    for c in cols:
        table.heading(c, text=c)
        table.column(c, anchor="center", width=120 if c in ["Name", "Percentage"] else 85)

    table.pack(fill="both", expand=True, padx=15, pady=15)

    load_table()
    root.mainloop()


# ---------------- APPLICATION LANDING WELCOME SCREEN ----------------

init_file()

welcome = tk.Tk()
welcome.title("Welcome Hub")
# Make window larger & responsive
welcome.geometry("600x350")
welcome.minsize(500, 300)
welcome.resizable(True, True)

# Center window on screen
screen_w = welcome.winfo_screenwidth()
screen_h = welcome.winfo_screenheight()

x = (screen_w // 2) - (600 // 2)
y = (screen_h // 2) - (350 // 2)

welcome.geometry(f"600x350+{x}+{y}")
welcome.configure(bg="#0b132b")

tk.Label(welcome, text="Student Performance Analytics System", font=("Segoe UI", 18, "bold"), bg="#0b132b",
         fg="white").pack(pady=(60, 30))

style_welcome = ttk.Style()
style_welcome.theme_use("clam")
style_welcome.configure("Welcome.TButton", font=("Segoe UI", 10, "bold"), padding=8, background="#00b4d8",
                        foreground="#0b132b")

ttk.Button(welcome, text="Initialize Dashboard Engine", style="Welcome.TButton", command=open_main_app).pack()

welcome.mainloop()