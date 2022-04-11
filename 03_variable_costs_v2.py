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
            print("Sorry - this can't be blank, please enter your name")


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

        quantity = num_check("Quantity: ", "The amount must be a whole number and more than zero", int)

        price = num_check("How much for a single item? $", "Price must be a number more than zero", float)

        # add item, quantity and price to list
        item_list.append(item_name)
        quantity_list.append(quantity)
        price_list.append(price)

    # set up dataframe
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

# product name
product_name = not_blank("Product name: ")

variable_expenses = get_expenses("variable")
variable_frame = variable_expenses[0]
variable_sub = variable_expenses[1]

# printing area

print()
print(variable_frame)
print()

print("Variable costs: ${:.2f}".format(variable_sub))
