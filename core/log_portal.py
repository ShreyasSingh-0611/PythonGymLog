from datetime import datetime
#from connector import save_session
from core.data_manager import backup_sessions


def log_menu(user_id):
    print("\n---Log portal---")
    print("1.Start session")
    print("2. Exit log portal")
    choice = input("Enter: ")
    if choice == '1':
        start_session(user_id)
        log_menu(user_id)
    elif choice == '2':
        print("\n---Exiting log menu---")
    else:
        print("Kindly enter valid response")
        log_menu(user_id)


def start_session(user_id):
    print("\n----New Session----")
    session = {"exercises": [], "starttime": datetime.now(), "userID": user_id}
    print(f'Start Time: {session["starttime"]}')
    while True:
        print('Options')
        print('1.Add exercise\n2.End session')
        choice = input('Enter: ')
        if choice == '1':
            add_exercise(session)
        elif choice == '2':
            end_session(session)
            break
        else:
            print("Kindly enter valid Response")


def add_exercise(session):
    exercise_name = input('Enter Exercise Name: ')
    exercise = {'name': exercise_name, 'sets': []}
    while True:
        print(f'Current Exercise: {exercise_name}')
        print("Options")
        print("1.Add Sets\n2.Finish Exercise")
        choice = input('Enter: ')
        if choice == '1':
            add_sets(exercise)
        elif choice == '2':
            session['exercises'].append(exercise)
            break
        else:
            print("Kindly enter valid response")


def add_sets(exercise):
    print("\n---Add Sets---")
    while True:
        try:
            weight = float(input("Enter Weight in kg: "))
            reps = int(input('Enter Reps: '))
            number_of_sets = int(input("Enter number of sets: "))
            break
        except ValueError:
            print("Invalid Input! Enter correct value types")
    set_data = {'reps': reps, 'weight': weight, 'number_of_sets': number_of_sets}
    exercise['sets'].append(set_data)
    print(f'{number_of_sets} sets {reps} reps with {weight} kg')


def end_session(session):
    session["endtime"] = datetime.now()
    print('\n---Session ended---')
    print(f'session start time: {session["starttime"]}')
    print(f'Session end time: {session["endtime"]}')
    print(f'Session Duration: {session["endtime"] - session["starttime"]}')
    print(session)
#   save_session(session)
    backup_sessions(session)


if __name__ == "__main__":
    log_menu(1)
