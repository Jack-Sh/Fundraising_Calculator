import pandas

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


# checks that a field isn't blank
def not_blank(question):
    valid = False

    while not valid:
        response = input(question)

        # If the name is not blank, program continues
        if response != "":
            return response

        # If the name is blank, show error and repeat the loop
        else:
            print("Sorry - this can't be blank")


# currency formatting function
def currency(x):
    return "${:.2f}".format(x)


# gets expenses, returns list which has dataframe and subtotal
def get_expenses(var_fixed):

    # set up dictionaries and lists

    item_list = []
    quantity_list = []
    price_list = []

    variable_dict = {
        "Item": item_list,
        "Quantity": quantity_list,
        "Price": price_list
    }

    # loop to get component quantity and price
    item_name = ""
    while item_name.lower() != "xxx":

        # get name, quantity and item
        print()
        item_name = not_blank("Item name: ")

        if item_name.lower() == "xxx":
            break

        if var_fixed == "variable":
            quantity = num_check("Quantity: ", "The amount must be a whole number and more than zero", int)

        else:
            quantity = 1

        price = num_check("How much for a single item? $", "Price must be a number more than zero", float)

        # add item, quantity and price to list
        item_list.append(item_name)
        quantity_list.append(quantity)
        price_list.append(price)

    # set up dataframe and set the first row to 'item'
    expense_frame = pandas.DataFrame(variable_dict)
    expense_frame = expense_frame.set_index('Item')

    # calculate cost of each component
    expense_frame['Cost'] = expense_frame['Quantity'] * expense_frame['Price']

    # find sub total
    sub_total = expense_frame['Cost'].sum()

    # currency formatting (uses function)
    add_dollars = ['Price', 'Cost']
    for item in add_dollars:
        expense_frame[item] = expense_frame[item].apply(currency)

    return [expense_frame, sub_total]


# *** Main routine ***

# Get product name
product_name = not_blank("Product name: ")

# get variable costs
variable_expenses = get_expenses("variable")
variable_frame = variable_expenses[0]
variable_sub = variable_expenses[1]

# get fixed costs
fixed_expenses = get_expenses("fixed")
fixed_frame = fixed_expenses[0]
fixed_sub = fixed_expenses[1]

# *** Printing Area ***

print("\n----- Variable Costs -----")
print(variable_frame)
print()

# print the subtotal for variable costs
print("Variable Costs: ${:.2f}".format(variable_sub))

# print the dataframe
print("\n----- Fixed Costs -----")
print(fixed_frame[['Cost']])
print()

# print the subtotal for fixed costs
print("Fixed Costs: ${:.2f}".format(fixed_sub))