import tkinter as tk
import pandas as pd
from tkinter import messagebox
from datetime import datetime, date
from core.data_manager import backup_sessions, load_data, fetch_filepath, filter_log_by_session
from core.graphs import bar_sessions_by_date, bar_number_of_sets_per_exercise, plot_max_weight_by_session_date
# List of exercises (this can be expanded or replaced with a database)
exercise_list = ["Push-up", "Squat", "Deadlift", "Lunge", "Pull-up", "Bench Press",
                 "Plank", "Crunches", "Lat Pull-down", "Bicep Curls", "Overhead Tricep extensions",
                 "Leg Curls", "Leg extensions"]

filepath = fetch_filepath()
session_data = load_data(filepath["session"])
log_data = load_data(filepath["log"])

# Function to switch between frames

def show_frame(frame):
    for f in [start_page_frame, log_portal_frame, history_portal_frame, graphs_portal_frame]:
        f.pack_forget()
    frame.pack()


# log_portal functions

# Function to open the "Add Session" window
def open_add_session_window():
    add_session_window = tk.Toplevel(root)
    add_session_window.title("Add Session")
    add_session_window.geometry("400x400")

    session = {"exercises": [], "starttime": datetime.now(), "session_date": date.today(), "userID": 1}

    # Header Label
    header_label = tk.Label(add_session_window, text="Workout Session", font=("Arial", 16, "bold"))
    header_label.pack(pady=10)

    # Start Date and Time Label
    start_label = tk.Label(add_session_window, text=f"Start Time: {session['starttime']}")
    start_label.pack()

    # Exercise Frame
    exercise_frame = tk.Frame(add_session_window)
    exercise_frame.pack(pady=10)

    # Buttons Frame
    buttons_frame = tk.Frame(add_session_window)
    buttons_frame.pack(pady=10)

    # Function to handle adding exercise to session
    def add_exercise_to_session(exercise_name):
        exercise_subframe = tk.Frame(exercise_frame, pady=5)
        exercise_subframe.pack(fill="x")

        exercise_label = tk.Label(exercise_subframe, text=exercise_name, font=("Arial", 12))
        exercise_label.grid(row=0, column=0, columnspan=4, sticky="w")

        sets = []

        def add_set():
            row = len(sets) + 3

            set_frame = tk.Frame(exercise_subframe)
            set_frame.grid(row=row, column=0, columnspan=5, sticky="w")

            weight_entry = tk.Entry(set_frame, width=10)
            weight_entry.grid(row=0, column=0)

            reps_entry = tk.Entry(set_frame, width=10)
            reps_entry.grid(row=0, column=1)

            sets_entry = tk.Entry(set_frame, width=10)
            sets_entry.grid(row=0, column=2)

            save_var = tk.IntVar(value=1)  # Default to checked
            save_checkbox = tk.Checkbutton(set_frame, variable=save_var)
            save_checkbox.grid(row=0, column=3)

            set_data = {
                "weight_entry": weight_entry,
                "reps_entry": reps_entry,
                "sets_entry": sets_entry,
                "save_var": save_var
            }
            sets.append(set_data)

        add_set_button = tk.Button(exercise_subframe, text="Add Set", command=add_set)
        add_set_button.grid(row=1, column=0, columnspan=4, pady=5, sticky="w")

        weight_label = tk.Label(exercise_subframe, text="Weight", font=("Arial", 10))
        weight_label.grid(row=2, column=0)

        reps_label = tk.Label(exercise_subframe, text="Reps", font=("Arial", 10))
        reps_label.grid(row=2, column=1)

        sets_label = tk.Label(exercise_subframe, text="Sets", font=("Arial", 10))
        sets_label.grid(row=2, column=2)

        session["exercises"].append({"name": exercise_name, "sets": sets})

    def open_exercise_window(add_exercise_callback):
        exercise_window = tk.Toplevel()
        exercise_window.title("Add Exercise")
        exercise_window.geometry("400x300")
        search_entry = tk.Entry(exercise_window, font=("Arial", 12))
        search_entry.pack(pady=10)
        exercise_listbox = tk.Listbox(exercise_window, height=10, font=("Arial", 12), width=30)
        exercise_listbox.pack()
        for exercise in exercise_list:
            exercise_listbox.insert(tk.END, exercise)

        def update_listbox(event):
            search_term = search_entry.get().lower()
            exercise_listbox.delete(0, tk.END)
            for exercise in exercise_list:
                if search_term in exercise.lower():
                    exercise_listbox.insert(tk.END, exercise)

        search_entry.bind("<KeyRelease>", update_listbox)

        def fillout(event):
            try:
                selected_exercise = exercise_listbox.get(exercise_listbox.curselection())
                search_entry.delete(0, tk.END)
                search_entry.insert(0, selected_exercise)
            except tk.TclError:
                pass

        exercise_listbox.bind("<<ListboxSelect>>", fillout)

        def submit_exercise():
            exercise_name = search_entry.get()
            if exercise_name in exercise_list:
                messagebox.showinfo("Exercise Added", f"{exercise_name} has been added to the session.")
                add_exercise_callback(exercise_name)
                exercise_window.destroy()
            else:
                messagebox.showerror("Error", "Exercise not found!")

        submit_button = tk.Button(exercise_window, text="Submit", command=submit_exercise)
        submit_button.pack()
        cancel_button = tk.Button(exercise_window, text="Cancel", command=exercise_window.destroy)
        cancel_button.pack()

    # Add Exercise Button
    add_exercise_button = tk.Button(buttons_frame, text="Add Exercise",
                                    command=lambda: open_exercise_window(add_exercise_to_session))
    add_exercise_button.pack()

    # Save Session Button
    def save_session():
        session["endtime"] = datetime.now()
        for exercise in session["exercises"]:
            exercise["sets"] = [
                {
                    "weight": float(set_data["weight_entry"].get() or 0),
                    "reps": int(set_data["reps_entry"].get() or 0),
                    "number_of_sets": int(set_data["sets_entry"].get() or 0)
                }
                for set_data in exercise["sets"] if set_data["save_var"].get() == 1
            ]
        backup_sessions(session)
        add_session_window.destroy()

    save_session_button = tk.Button(buttons_frame, text="Save Session", command=save_session)
    save_session_button.pack()

    # Cancel Session Button
    def cancel_session():
        response = messagebox.askyesnocancel("Cancel Session",
                                             "This session will not be saved. Do you want to continue?")
        if response:
            add_session_window.destroy()

    cancel_session_button = tk.Button(buttons_frame, text="Cancel Session", command=cancel_session)
    cancel_session_button.pack()


# history_portal_related_functions


def show_all(log_data: pd.DataFrame, session_data: pd.DataFrame, output_frame: tk.Frame):
    output_frame.pack_forget()
    # Iterate over session_data using iterrows()
    for index, row in session_data.iterrows():
        # Create a frame for each session
        session_frame = tk.Frame(output_frame, bd=2, relief="solid", padx=10, pady=10)
        session_frame.pack(padx=10, pady=5, fill="x", expand=True)

        # Create and pack Session Date label
        session_date_label = tk.Label(session_frame, text=f"Session Date: {row['SessionDate']}")
        session_date_label.pack(anchor="w")

        # Create and pack Start Time label
        start_time_label = tk.Label(session_frame, text=f"Start Time: {row['Starttime']}")
        start_time_label.pack(anchor="w")

        # Create and pack End Time label
        end_time_label = tk.Label(session_frame, text=f"End Time: {row['Endtime']}")
        end_time_label.pack(anchor="w")

        # Create an empty frame for exercises (currently empty)
        exercise_frame = tk.Frame(session_frame, bd=1, relief="solid", height=50, bg="lightgray")
        exercise_frame.pack(pady=10, fill="x")
        session_log_data = filter_log_by_session(log_data, row["SessionID"]).sort_values(by=["LogID"])
        for j, log_row in log_data.iterrows():
            if log_row["SetOrder"] == 1:
                exercise_name_label = tk.Label(exercise_frame, text=log_row["ExerciseName"])
                exercise_name_label.pack()
            exercise_info_text = f'{log_row["SetOrder"]}.{log_row["Weight"]}kg X {log_row["Reps"]} reps X {log_row["NumberOfSets"]} sets'
            exercise_info_label = tk.Label(exercise_frame, text=exercise_info_text)
            exercise_info_label.pack()
    output_frame.pack()

# Function to choose Exercise for max weight

# Initialize the root window
root = tk.Tk()
root.title("Workout Log System")

# Create a menu
menu = tk.Menu(root)
root.config(menu=menu)
menu.add_command(label="Start Page", command=lambda: show_frame(start_page_frame))
menu.add_command(label="Log Portal", command=lambda: show_frame(log_portal_frame))
menu.add_command(label="History Portal", command=lambda: show_frame(history_portal_frame))
menu.add_command(label="Graphs Portal", command=lambda: show_frame(graphs_portal_frame))

# Create frames for each page
start_page_frame = tk.Frame(root)
log_portal_frame = tk.Frame(root)
history_portal_frame = tk.Frame(root)
graphs_portal_frame = tk.Frame(root)

# Start page
start_label = tk.Label(start_page_frame, text="Welcome to the Workout Log System!", font=("Arial", 16))
start_label.pack(pady=50)

# Log portal
log_label = tk.Label(log_portal_frame, text="Log your workout here.", font=("Arial", 16))
log_label.pack(pady=20)

# Add Session button
add_session_button = tk.Button(log_portal_frame, text="Add Session", command=open_add_session_window)
add_session_button.pack(pady=10)

# History portal
history_label = tk.Label(history_portal_frame, text="View your workout history here.", font=("Arial", 16))
history_label.pack(pady=50)

# Create the frame for buttons
buttons_frame = tk.Frame(history_portal_frame)
buttons_frame.pack(pady=20)

# Create the "Show All" button
show_all_button = tk.Button(buttons_frame, text="Show All", width=15, command=lambda: show_all(log_data, session_data, output_frame))
show_all_button.grid(row=0, column=0, padx=10)

# Create the frame for output
output_frame = tk.Frame(history_portal_frame)
output_frame.pack()
# Graphs portal frame
graph_label = tk.Label(graphs_portal_frame, text="View your workout graphs here.", font=("Arial", 16))
graph_label.pack(pady=50)

sessions_by_date_label = tk.Label(graphs_portal_frame, text="1.Sessions by date of last week")
sessions_by_date_button = tk.Button(graphs_portal_frame, text="Show",
                                    command=lambda: bar_sessions_by_date(session_data))
sessions_by_date_label.pack()
sessions_by_date_button.pack()
number_of_sets_per_exercise_label = tk.Label(graphs_portal_frame, text="2.Number of sets per exercise")
number_of_sets_per_exercise_button = tk.Button(graphs_portal_frame, text="Show",
                                               command=lambda: bar_number_of_sets_per_exercise(log_data))
number_of_sets_per_exercise_label.pack()
number_of_sets_per_exercise_button.pack()


# Run the start page first
start_page_frame.pack()

# Run the application
root.mainloop()
