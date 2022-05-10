# functions


# function to check yes no question
def yes_no(question):

    to_check = ["yes", "no"]

    valid = False
    while not valid:

        response = input(question).lower()

        for var_item in to_check:
            if response == var_item:
                return response
            elif response == var_item[0]:
                return var_item

        print("Please enter either yes or no... \n")


def instructions():
    show_help = False
    while show_help == False:
        show_help = yes_no("Instructions? ").lower()

    if show_help == "yes":
        print()
        print("**** FRC Instructions ****")

    return ""


# main routine

instructions()
print()
print("Program Launches")