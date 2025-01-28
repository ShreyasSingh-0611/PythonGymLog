import tkinter as tk


# Function to open the "Add Session" window
def open_add_session_window():
    add_session_window = tk.Toplevel(root)  # Create a new top-level window
    add_session_window.title("Add Session")
    add_session_window.geometry("400x300")

    # Header Label
    header_label = tk.Label(add_session_window, text="Workout Session", font=("Arial", 16, "bold"))
    header_label.grid(row=0, column=0, columnspan=2, pady=10)

    # Start Date and Time Label
    start_label = tk.Label(add_session_window, text="Start Date and Time:")
    start_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

    # Space to show exercises (currently empty)
    exercises_label = tk.Label(add_session_window, text="Exercises (None added yet):")
    exercises_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

    # Add Exercise Button (currently no functionality)
    add_exercise_button = tk.Button(add_session_window, text="Add Exercise")
    add_exercise_button.grid(row=3, column=1, padx=10, pady=10)

    # Save Session Button (initially hidden)
    save_session_button = tk.Button(add_session_window, text="Save Session")
    save_session_button.grid(row=4, column=1, padx=10, pady=10)
    save_session_button.grid_remove()  # Hide initially

    # Cancel Session Button
    cancel_session_button = tk.Button(add_session_window, text="Cancel Session", command=add_session_window.destroy)
    cancel_session_button.grid(row=4, column=0, padx=10, pady=10)


# Function to show the Start Page
def show_start_page():
    root.frame_for_current_page.pack_forget()
    root.frame_for_current_page = start_page_frame
    root.frame_for_current_page.pack()


# Function to show the Log Portal
def show_log_portal():
    root.frame_for_current_page.pack_forget()
    root.frame_for_current_page = log_portal_frame
    root.frame_for_current_page.pack()


# Function to show the History Portal
def show_history_portal():
    root.frame_for_current_page.pack_forget()
    root.frame_for_current_page = history_portal_frame
    root.frame_for_current_page.pack()


# Initialize the root window
root = tk.Tk()
root.title("Workout Log System")
root.geometry("400x200")
# Create a menu
menu = tk.Menu(root)
root.config(menu=menu)

menu.add_command(label="Start Page", command=show_start_page)
menu.add_command(label="Log Portal", command=show_log_portal)
menu.add_command(label="History Portal", command=show_history_portal)

# Create frames for each page
start_page_frame = tk.Frame(root)
log_portal_frame = tk.Frame(root)
history_portal_frame = tk.Frame(root)

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

# Initially display start page
root.frame_for_current_page = start_page_frame
root.frame_for_current_page.pack()

# Run the application
root.mainloop()
