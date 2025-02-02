import pandas as pd
from datetime import datetime
from core.data_manager import fetch_filepath, load_data,filter_session_by_user,filter_session_by_date,filter_log_by_session
from core.graphs import bar_sessions_by_date,bar_number_of_sets_per_exercise,plot_max_weight_by_session_date


# Data display as text

def display_session_history(display_session_data: pd.DataFrame, display_log_data: pd.DataFrame):

    def display_duration(start_time: datetime, end_time: datetime):
        dur = end_time - start_time
        hour, remainder = divmod(dur.total_seconds(), 3600)
        minute, second = divmod(remainder, 60)
        parts = str()
        if hour > 0:
            parts += f'{hour} h '
        if minute > 0:
            parts += f'{minute} m '
        parts += f'{second} s'
        return parts

    print("\n---Session History---")
    for session_index, session_row in display_session_data.iterrows():
        print(f'\n---#Session {session_row["SessionID"]}---')
        starttime = pd.to_datetime(session_row["Starttime"])
        endtime = pd.to_datetime(session_row["Endtime"])
        print(f'Date: {starttime.date()}')
        print(f'Time: {starttime.time()}')
        print(f'Duration: {display_duration(starttime, endtime)}')
        session_log_data = filter_log_by_session(display_log_data, session_row["SessionID"]).sort_values(by=["LogID"])
        for i, row in session_log_data.iterrows():
            if row["SetOrder"] == 1:
                print(f'---{row["ExerciseName"]}---')
            print(f'{row["SetOrder"]}. {row["Weight"]}kg X {row["Reps"]} reps X {row["NumberOfSets"]} sets')


# Function to navigate through History Portal


def history_menu(user_id: int):
    filepaths = fetch_filepath()
    session_data = load_data(filepaths["session"])
    user_session_data = filter_session_by_user(session_data, user_id)
    log_data = load_data(filepaths["log"])
    print("\n---History portal---")
    while True:
        print("1.Show all sessions \n2.Filter sessions by date\n3.See Graphs\n4.Exit history portal")
        choice = input("Enter: ")
        if choice == "1":
            display_session_history(user_session_data, log_data)
            history_menu(user_id)
        elif choice == "2":
            filtered_session_data = filter_session_by_date(user_session_data)
            display_session_history(filtered_session_data, log_data)
            history_menu(user_id)
        elif choice == "3":
            print("Choose Graph. \n1.Sessions by Date\n2. Number of sets by Exercise\n3.")
            selection = input("Enter:")
            if selection == "1":
                bar_sessions_by_date(user_session_data)
            elif selection == "2":
                bar_number_of_sets_per_exercise(log_data)
            elif selection == "3":
                exercise_name = input("Name Exercise")
                plot_max_weight_by_session_date(exercise_name,log_data,session_data)
        elif choice == "4":
            print("\n---Exiting log menu---")
            break
        else:
            print("Enter Valid amount")


if __name__ == "__main__":
    history_menu(1)