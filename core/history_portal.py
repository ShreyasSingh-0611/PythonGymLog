import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from core.data_manager import fetch_filepath, load_data

# Data Filters

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


# Data display by plots

def plot_sessions_last_week(data):
    data["SessionDatetime"] = pd.to_datetime(data["Starttime"])
    today = datetime.now().date()
    one_week_ago = today - timedelta(days=6)
    last_week_data = data[
        (data["SessionDatetime"].dt.date >= one_week_ago) &
        (data["SessionDatetime"].dt.date <= today)
        ]

    last_week_dates = [one_week_ago + timedelta(days=i) for i in range(7)]
    last_week_dates_str = [date.strftime("%Y-%m-%d") for date in last_week_dates]
    session_counts = last_week_data["SessionDatetime"].dt.date.value_counts()
    sessions_per_day = {date: session_counts.get(date, 0) for date in last_week_dates}
    sorted_sessions = dict(sorted(sessions_per_day.items()))

    # Plot the bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(sorted_sessions.keys(), sorted_sessions.values(), color="skyblue", edgecolor="none")
    plt.title("Number of Sessions Per Day (Last Week)", fontsize=14)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Number of Sessions", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()


# Main function of history portal


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