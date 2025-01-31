import pandas as pd
import matplotlib.pyplot as plt
def bar_number_of_sets_per_exercise():
    df = pd.read_csv("log.csv")
    df_sets = df.groupby("ExerciseName")["NumberOfSets"].sum()
    plt.bar(df_sets.index, df_sets.values)
    plt.xlabel("Exercise")
    plt.ylabel("Total Sets")
    plt.title("Total Sets Performed for Each Exercise")
    plt.xticks(rotation=90)
    plt.show()

def plot_max_weight_by_session_date(exercise_name):
    # Load data
    log_df = pd.read_csv("log.csv")
    session_df = pd.read_csv("session.csv")

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


plot_max_weight_by_session_date("Deadlift")