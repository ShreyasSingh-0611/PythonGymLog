# This is the Main Menu
from core.log_portal import log_menu
from core.history_portal import history_menu

def main_menu(userID):
    print("\n---Main menu---")
    print("1.Log\n2.History\n3.Exit navigation")
    choice = int(input("Enter: "))
    if choice == 1:

        log_menu(userID)
        main_menu(userID)
    elif choice == 2:
        history_menu(userID)
        main_menu(userID)
    elif choice == 3:
        print("Thank you!")
    else:
        print("Incorrect Response")
        main_menu(userID)


print("Welcome to Gym Log.")
print("Here are some guidelines")
print("1.This is a prototype")
print("2.I have not really managed Value Errors, so entering wrong datatypes would lead to program not working")
print("3.Most inputs are integers used for navigation, and floats in certain cases like weight")
print('4.Cancelling individual sets and such is not possible. However cancelling Sessions is possible')

main_menu(1)
