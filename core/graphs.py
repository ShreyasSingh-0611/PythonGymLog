import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
def bar_number_of_sets_per_exercise(df):
    df_sets = df.groupby("ExerciseName")["NumberOfSets"].sum()
    plt.bar(df_sets.index, df_sets.values)
    plt.xlabel("Exercise")
    plt.ylabel("Total Sets")
    plt.title("Total Sets Performed for Each Exercise")
    plt.xticks(rotation=90)
    plt.show()

def plot_max_weight_by_session_date(exercise_name,log_df,session_df):

    # Use the SessionDate column directly
    log_df = log_df.merge(session_df[['SessionID', 'SessionDate']], on='SessionID')

    # Filter data for the chosen exercise
    df_exercise = log_df[log_df['ExerciseName'] == exercise_name]

    # Get the max weight lifted per session date
    df_max_weight = df_exercise.groupby('SessionDate')['Weight'].max().reset_index()

    # Plot the data
    plt.figure(figsize=(10, 5))
    plt.plot(df_max_weight['SessionDate'], df_max_weight['Weight'], marker='o', linestyle='-')
    plt.xlabel('Session Date')
    plt.ylabel('Max Weight (kg)')
    plt.title(f'Max Weight for {exercise_name} Over Time')
    plt.xticks(rotation=45)
    plt.gca().set_ylim(ymin=0,ymax=(df_exercise["Weight"].max())+5.0)
    plt.grid()
    plt.show()

def bar_sessions_by_date(session_df):
    # Convert SessionDate to datetime format
    session_df["SessionDate"] = pd.to_datetime(session_df["SessionDate"])

    # Get the last session date in the dataset
    last_date = pd.to_datetime(date.today())
    start_date = last_date - pd.Timedelta(days=7)
    # Filter sessions from the last 7 days
    last_week_df = session_df[session_df["SessionDate"] >= start_date]
    # Count sessions per day
    sessions_per_day = last_week_df["SessionDate"].value_counts().sort_index()

    # Plot the data
    plt.figure(figsize=(8, 5))
    plt.bar(sessions_per_day.index, sessions_per_day.values, color="blue", alpha=0.7)
    plt.xlabel("Session Date")
    plt.ylabel("Number of Sessions")
    plt.title("Sessions Per Day (Last 7 Days)")
    plt.xticks(rotation=45)
    plt.yticks(range(0,(sessions_per_day.values.max()+2)), rotation=0)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()

plot_max_weight_by_session_date("Bench Press",pd.read_csv("log.csv"),pd.read_csv("session.csv"))