import pandas as pd
from datetime import datetime
from core.data_manager import fetch_filepath, load_data


def filter_session_by_user(data: pd.DataFrame, user: int):
    filtered_df = data[
        data["userID"] == user
    ]
    return filtered_df


def filter_session_by_date(data: pd.DataFrame):
    def enter_date(txt):
        date_entry = input(f'enter {txt} date as YYYY-MM-DD: ')

        return date_entry
    data["SessionDatetime"] = pd.to_datetime(data["Starttime"])
    start_date = enter_date('starting')
    end_date = enter_date('ending')
    filtered_df = data[
        (start_date <= data["SessionDatetime"]) &
        (data["SessionDatetime"] <= end_date)
        ]
    return filtered_df


def filter_log_by_session(data: pd.DataFrame, session_id: int):
    filtered_df = data[data["SessionID"] == session_id]
    return filtered_df


def display_session_history(display_session_data: pd.DataFrame, display_log_data):

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


def history_menu(user_id: int):
    filepaths = fetch_filepath()
    session_data = load_data(filepaths["session"])
    user_session_data = filter_session_by_user(session_data, user_id)
    log_data = load_data(filepaths["log"])
    print("\n---History portal---")
    print("1.Show all sessions \n2.filter sessions by date\n3.Exit history portal")
    choice = input("Enter: ")
    if choice == "1":
        display_session_history(user_session_data, log_data)
        history_menu(user_id)
    elif choice == "2":
        filtered_session_data = filter_session_by_date(user_session_data)
        display_session_history(filtered_session_data, log_data)
        history_menu(user_id)
    elif choice == "3":
        print("\n---Exiting log menu---")


if __name__ == "__main__":
    history_menu(1)
