import database
import sys

if __name__ == '__main__':
    try:

        command = sys.argv[1]

        if command == "CREATE": #create premium for user USERNAME and unit time TIME
            USERNAME = sys.argv[2]
            TIME = int(sys.argv[3])
            database.add(None, TIME, USERNAME)
        elif command == "UPDATE": #update premium time for user USERNAME to new time NEW_TIME
            USERNAME = sys.argv[2]
            NEW_TIME = sys.argv[3]
            database.update_user_time(USERNAME, NEW_TIME)
        elif command == "DELETE": #delete user USERNAME from base
            USERNAME = sys.argv[2]
            database.remove_by_username(USERNAME)
        elif command == "ADD_FULL": #add full user data, BE CAREFUL WITH THIS COMMAND PLEASE, BECAUSE TABLE HAS TG ID!
            USERNAME = sys.argv[2]
            NEW_TIME = sys.argv[3]
            NEW_ID = sys.argv[4]
            database.add(NEW_ID, NEW_TIME, USERNAME)
        else:
            raise Exception('Wrong command')

    except Exception as e:
        print(e)
