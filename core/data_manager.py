import pandas as pd


def fetch_filepath():
    return {
            "session": "session.csv",
            "log": "log.csv",
            "exercise": "exercise.csv"
        }


def load_data(filepath):
    try:
        df = pd.read_csv(filepath, sep=',', header=0)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        df = pd.DataFrame()
    return df


def save_data(data, filepath):
    data.to_csv(filepath, index=False)


def input_session(data: pd.DataFrame, session: dict):
    session_id = data['SessionID'].max()+1 if not data.empty else 1
    new_row = pd.DataFrame(
        {'SessionID': session_id,
         'Starttime': session['starttime'],
         'Endtime': session['endtime'],
         'userID': session['userID']},
        index=[0]
    )
    if data.empty:
        df = new_row
    else:
        df = pd.concat([data, new_row], ignore_index=True)
    return df


def input_log(data, session_id, session):
    next_log_id = data["LogID"].max()+1 if not data.empty else 1
    new_rows = []
    for exercise in session["exercises"]:
        set_order = 1  # Initialize SetOrder for each exercise
        for set_data in exercise["sets"]:
            new_row = {
                "LogID": next_log_id,
                "SessionID": session_id,
                "ExerciseName": exercise["name"],
                "SetOrder": set_order,  # SetOrder groups sets
                "Reps": set_data["reps"],
                "Weight": set_data.get("weight", 0),
                "NumberOfSets": set_data.get("number_of_sets", 1)  # Default to 1
            }
            new_rows.append(new_row)
            set_order += 1  # Increment SetOrder for the next set group
            next_log_id += 1
    # Convert new rows to a DataFrame and concatenate with existing data
    new_rows_df = pd.DataFrame(new_rows)
    if data.empty:
        data = new_rows_df
    else:
        data = pd.concat([data, new_rows_df], ignore_index=True)
    return data


def backup_sessions(session):
    filepaths = fetch_filepath()
    session_data = load_data(filepaths["session"])
    log_data = load_data(filepaths["log"])
    session_data_changed = input_session(session_data, session)
    session_id = session_data_changed['SessionID'].max()
    log_data_changed = input_log(log_data, session_id, session)
    save_data(session_data_changed, filepaths["session"])
    save_data(log_data_changed, filepaths["log"])
