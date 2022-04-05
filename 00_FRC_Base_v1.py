# functions


# number checking function
def num_check(question, error, num_type):
    valid = False
    while not valid:

        try:
            response = num_type(input(question))

            if response <= 0:
                print(error)
            else:
                return response

        except ValueError:
            print(error)


# Main routine
# Ask user how many items they need
get_int = num_check("How many do you need? ",
                    "Please enter an amount more than 0\n",
                    int)

# Ask user how much each item costs
get_cost = num_check("How much does it cost? $",
                     "Please enter a number more than 0\n",
                     float)

# print how many items the user needs and the cost (testing)
print()
print("You need:", get_int)
print("It costs:",get_cost)