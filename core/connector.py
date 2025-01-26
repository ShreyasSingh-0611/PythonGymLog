import mysql.connector
from datetime import datetime


def connect_to_db():
    print("connecting to db")
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tiger",
        database="workout_log"
    )
    print(conn.is_connected())
    if conn.is_connected():
        print("connection successful")
    else:
        print("connection unsuccessful")
    return conn


def insert_session(conn, session):
    cursor = conn.cursor()
    sql = 'INSERT INTO workoutsessions (Starttime,Endtime,UserID) VALUES (%s,%s,%s)'
    val = (session['starttime'], session['endtime'],1)
    cursor.execute(sql, val)
    conn.commit()
    session_id = cursor.lastrowid
    cursor.close()
    return session_id


def insert_workout_logs(conn, session_id, session):
    cursor = conn.cursor()
    for exercise in session["exercises"]:
        for i, set_data in enumerate(exercise["sets"], start=1):
            sql = """
            INSERT INTO WorkoutLogs (SessionID, ExerciseName, SetNumber, Reps, Weight)
            VALUES (%s, %s, %s, %s, %s)
            """
            val = (session_id, exercise["name"], i, set_data["reps"], set_data["weight"])
            cursor.execute(sql, val)
    conn.commit()
    cursor.close()


def save_session(session):
    conn = connect_to_db()
    session_id = insert_session(conn, session)  # Save session metadata
    insert_workout_logs(conn, session_id, session)  # Save workout logs
    print("\n--- Session Saved Successfully ---")
    conn.close()
