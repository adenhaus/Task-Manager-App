from datetime import date, datetime

# Functions >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


def get_info_from_task(num, assign):
    with open("tasks.txt", "r") as tasks_read:
        # Create a list of the tasks
        b = tasks_read.read()
        task_info = b.split("\n\n")

        print("")

        words_list = []

        # Split tasks.txt into separate task items
        for i in task_info:
            x = i.split("\n")
            if len(x) > 6:
                words = x[num]
                words = words.split(":")
                assignment = words[0].lower().strip()
                if assignment == assign:
                    words = words[1].strip()
                    words_list.append(words)
        return words_list


def reg_user():
    with open("user.txt", "a") as user_write:
        not_registered = True

        # Create a list of already registered usernames
        with open("user.txt", "r") as user_read:
            a = user_read.read()
            registered_list = []
            registered_users = a.split("\n")
            for i in registered_users:
                i = i.split(", ")
                registered_list.extend(i)

        while not_registered:
            new_username = input("\nSet username:     ")

            # Check if new username is already registered
            if new_username not in registered_list:
                new_password = input("Set password:     ")

                # Check if passwords match
                while True:
                    confirm_new_password = input("Confirm your password:        ")

                    if confirm_new_password == new_password:
                        print("\nNew user created for " + new_username)
                        user_write.write("\n" + new_username + ", " + new_password)
                        not_registered = False
                        break

                    else:
                        print("Passwords do not match. Try again.")

            else:
                print("That username already exists. Try again.")
                not_registered = True


def add_task():
    # Open tasks.txt file
    with open("tasks.txt", "a") as task_write:

        # Make sure that the user entered is registered
        wrong_info = True
        while wrong_info:

            assigned_user = input("\nWhich user is the task assigned to? ")
            assigned_user = assigned_user.lower()

            with open("user.txt", "r") as user_read:
                for line in user_read:
                    info = line.split(", ")

                    if assigned_user == info[0]:
                        break

                if assigned_user == info[0]:
                    break

                else:
                    print("Please enter a valid user. The currently registered users are:")
                    for line in user_read:
                        info = line.split(", ")
                        print(info[0])

        # Ask for the rest of the task information
        task_title = input("What is the task title? ")
        task_description = input("Task description: ")
        due_date = input("Due date (format must be yyyy-mm-dd): ")
        date_assigned = date.today()
        is_completed = "No"

        # Here I assign a number to the task
        with open("tasks.txt", "r") as tasks_read:

            # Create a list of the tasks
            a = tasks_read.read()
            task_info = a.split("\n\n")

            print("")

            # Create an empty list
            num_list = []

            # Split tasks.txt into separate task items
            for i in task_info:
                x = i.split("\n")

                if len(x) > 5:
                    words = x[6]
                    words = words.split(":")
                    assignment = words[0].lower().strip()
                    if assignment == "task number":
                        number = words[1].strip()

                        num_list.append(int(number))

        # This way, the tasks will be numbered in the order they were created
        # Additionally, we will never have a duplicate number
        task_num = max(num_list) + 1

        # Write the information to the tasks.txt file
        task_write.write(
            "User: " + assigned_user + "\nTask Title: " + task_title + "\nTask description: " + task_description +
            "\nDue Date: " + due_date + "\nDate Assigned: " +
            str(date_assigned) + "\nCompleted: " + is_completed + "\nTask Number: " + str(task_num) + "\n\n")


def view_all():
    # Open tasks.txt file
    with open("tasks.txt", "r") as tasks_read:
        # Print all tasks
        print(tasks_read.read())


def view_mine():
    # Open tasks.txt file
    with open("tasks.txt", "r") as tasks_read:

        # Create a list of the tasks
        a = tasks_read.read()
        task_info = a.split("\n\n")

        print("")
        is_user = True

        # Split tasks.txt into separate task items
        for i in task_info:
            x = i.split("\n")
            words = x[0]
            words = words.split(":")
            assignment = words[0].lower().strip()
            if assignment == "user":
                user = words[1].strip()

                # Check if the username of a task in the list corresponds to the currently logged in user
                if user == username:
                    print(i, end="\n\n")
                    is_user = False

        if is_user:
            print("You have no tasks!")


def specific_task():
    # Open tasks.txt file
    with open("tasks.txt", "r") as tasks_read:

        # Create a list of the tasks
        a = tasks_read.read()
        task_info = a.split("\n\n")

        for i in task_info:
            x = i.split("\n")
            if len(x) > 5:
                words = x[6]
                date = x[3]
                words = words.split(":")
                date = date.split(":")
                assignment = words[0].lower().strip()
                assignment_date = date[0].lower().strip()
                if assignment == "task number" and assignment_date == "due date":
                    task_number = words[1].strip()
                    due_date = date[1].strip()
                    if task_number == user_choice:
                        print("\n" + i)
                        return i, task_info, due_date


def generate_reports():
    # Create a list of already registered usernames
    with open("user.txt", "r") as user_read:
        a = user_read.read()
        registered_list = []
        registered_users = a.split("\n")

        for i in registered_users:
            i = i.split(", ")
            registered_list.extend(i)
        del registered_list[1::2]

    with open("tasks.txt", "r") as tasks_read:
        # Create a list of the tasks
        a = tasks_read.read()
        task_info = a.split("\n\n")
        task_amt = len(task_info)

        with open("user_overview.txt", "w") as user_o:

            user_o.write("\nTasks per user: \n")
            for person in registered_list:
                tasks_per_user = (person + ": " + str(a.count(person)))
                user_o.write(str(tasks_per_user) + "\n")

            user_o.write("\nPercentage of all tasks assigned to user: \n")
            for person in registered_list:
                percentage_tasks_per_user = (person + ": " + format(a.count(person) / task_amt * 100, '.2f'))
                user_o.write(str(percentage_tasks_per_user) + "%\n")

            user_o.write("\nPercentage of tasks assigned to user that have been completed: \n")
            for person in registered_list:
                counter = 0
                counter2 = 0
                for i in task_info:
                    if person in i and "Yes" in i:
                        counter += 1

                if a.count(person) > 0:
                    percentage_completed_per_user = counter / a.count(person) * 100
                    perc_complete = (person + ": " + format(percentage_completed_per_user, '.2f') + "%\n")

                    user_o.write(perc_complete)

            user_o.write("\nPercentage of tasks assigned to user that are incomplete:\n")
            for person in registered_list:
                counter = 0
                counter2 = 0
                for i in task_info:
                    if person in i and "Yes" in i:
                        counter += 1

                if a.count(person) > 0:
                    percentage_incomplete_per_user = 100 - (counter / a.count(person) * 100)
                    perc_incomplete = (person + ": " + format(percentage_incomplete_per_user, '.2f') + "%\n")

                    user_o.write(perc_incomplete)

            user_o.write("\nPercentage of tasks assigned to user that are incomplete and overdue:\n")
            dates = get_info_from_task(3, "due date")

            for person in registered_list:
                counter1 = 0
                for i in dates:
                    index = dates.index(i)
                    if datetime.strptime(i, '%Y-%m-%d') < datetime.today() and "No" in task_info[index] and person in \
                            task_info[index]:
                        counter1 += 1

                tasks_overdue = counter1

                if a.count(person) > 0:
                    percentage_incomplete_overdue_per_user = counter1 / a.count(person) * 100
                    perc_overdue_incomplete = (
                                person + ": " + format(percentage_incomplete_overdue_per_user, '.2f') + "%\n")

                    user_o.write(perc_overdue_incomplete)

            user_o.write("\nIf a user's name does not appear above, it means they do not have any assigned tasks.\n")

        with open("user_overview.txt", "r") as user_r:
            print(user_r.read())


def mark_or_edit():
    answer, info, due_date = specific_task()

    # To mark as completed or edit
    print("\nm - mark as completed\ned - edit task")
    user_choice2 = input()

    # I did not include the following code in the view_mine()
    # function because it is performing a different task

    if user_choice2 == "m":
        index = info.index(answer)
        answer = answer.replace("No", "Yes")
        info[index] = answer
        print(answer)
        with open("tasks.txt", "w") as write_tasks:
            list = "\n\n".join(info)
            write_tasks.write(list)

    elif user_choice2 == "ed":
        index = info.index(answer)
        info[index] = answer
        answer_list = answer.split()
        if "Yes" in answer_list:
            print("This task has already been completed.")

        else:
            print("\nu - change user\nd - change due date")
            operation = input()

            if operation == "u":
                new_user = input("Who would you like to reassign the task to? ")
                index = info.index(answer)
                answer = answer.replace(username, new_user)
                info[index] = answer
                print(answer)

                with open("tasks.txt", "w") as write_tasks:
                    list = "\n\n".join(info)
                    write_tasks.write(list)

            elif operation == "d":
                new_date = input("Set the new due date: ")
                index = info.index(answer)
                answer = answer.replace(due_date, new_date)
                info[index] = answer
                print("\n" + answer)

                with open("tasks.txt", "w") as write_tasks:
                    list = "\n\n".join(info)
                    write_tasks.write(list)


def display_stats():
    dates = get_info_from_task(3, "due date")

    with open("tasks.txt", "r") as tasks_read:
        # Create a list of the tasks
        b = tasks_read.read()
        task_info = b.split("\n\n")

        for i in task_info:
            x = i.split("\n")

        task_amt = len(task_info) - 1
        tasks_completed = b.count("Completed: Yes")
        tasks_uncompleted = b.count("Completed: No")
        incomplete_percentage = b.count("Completed: No") / len(task_info) * 100

        counter1 = 0

        for i in dates:
            index = dates.index(i)
            if datetime.strptime(i, '%Y-%m-%d') < datetime.today() and "No" in task_info[index]:
                counter1 += 1

        tasks_overdue = counter1
        overdue_percentage = counter1 / task_amt * 100

        info_to_print_tasks = ("Total Tasks: " + str(task_amt) + "\nTasks Completed: " + str(
            tasks_completed) + "\nTasks Not Completed: " + str(
            tasks_uncompleted) + "\nIncomplete Percentage: " + format(incomplete_percentage, '.2f')
                               + "%\nTasks Overdue: " + str(counter1) + "\nOverdue Percentage: " +
                               format(overdue_percentage, '.2f') + "%")

        with open("task_overview.txt", "w") as task_o:
            task_o.write(info_to_print_tasks)

    with open("task_overview.txt", "r") as task_r:
        print(task_r.read())


# Login screen >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
print("LOGIN")

# Open user.txt file for reading
with open("user.txt", "r") as user_read:
    # Loop to check username and password
    wrong_info = True
    while wrong_info:

        username = input("Username:     ")

        user_read = open("user.txt", "r")

        # Loop through all lines of user.txt to see if username is registered
        for line in user_read:
            info = line.split(", ")

            if username == info[0]:
                break

        if username == info[0]:
            while True:

                # If username is valid, check corresponding password
                password = input("Password:     ")

                if password == info[1].strip():
                    wrong_info = False
                    break

                else:
                    print("Incorrect password. Please try again:")

        else:
            print("Username does not exist.")

        # Close user.txt file
        user_read.close()

# MAIN LOOP >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
running = True
while running:

    # Menu for admin
    if username == "admin":
        print("\nPlease select one of the following options:\nr - Register user\na - Add task\nva - "
              "View all tasks\nvm - View my tasks\nds - Display Statistics\ngr - Generate Reports\ne - Exit")

    # Menu for other users
    else:
        print("\nPlease select one of the following options:\na - Add task\nva - "
              "View all tasks\nvm - View my tasks\ne - Exit")

    # Allow user to choose an option
    choice = input("\n")

    # Register a new user ==============================================================================================
    if choice == "r":

        if username == "admin":
            reg_user()

        else:
            print("\nOnly the admin can do this.")

        user_return = input("Type '-1' to return to the main menu or 'e' to quit: ")
        if user_return == "e":
            break

    # Add task =========================================================================================================
    elif choice == "a":

        add_task()

        user_return = input("Type '-1' to return to the main menu or 'e' to quit: ")

        if user_return == "e":
            break

    # View all tasks ===================================================================================================
    elif choice == "va":

        view_all()

        user_return = input("\nType '-1' to return to the main menu or 'e' to quit: ")
        if user_return == "e":
            break

    # View user's tasks ================================================================================================
    elif choice == "vm":

        view_mine()

        user_choice = input("Enter the number of a task to view it or type '-1' to return to the main menu: ")
        if user_choice == "-1":
            continue

        # To view a specific task
        else:
            mark_or_edit()

        user_return = input("\nType '-1' to return to the main menu or 'e' to quit: ")
        if user_return == "e":
            break

    # Exit =============================================================================================================
    elif choice == "e":
        break

    # Statistics =======================================================================================================
    elif choice == "ds":

        display_stats()

        user_return = input("\nType '-1' to return to the main menu or 'e' to quit: ")
        if user_return == "e":
            break

    # Reports ==========================================================================================================
    elif choice == "gr":

        generate_reports()

        user_return = input("Type '-1' to return to the main menu or 'e' to quit: ")
        if user_return == "e":
            break

    # Error handler ====================================================================================================
    else:
        print("That is not a valid input.")

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
