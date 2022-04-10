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


# *** Main routine ***

# set up dictionaries and lists

item_list= []
quantity_list = []
price_list = []

variable_dict = {
    "Item":item_list,
    "Quantity": quantity_list,
    "Price": price_list
}

# Get user data
product_name = not_blank("Product name: ")

# loop to get component quantity and price
item_name = ""
while item_name.lower() != "xxx":

    print()
    # get name, quantity and item
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
variable_frame = pandas.DataFrame(variable_dict)
variable_frame = variable_frame.set_index('Item')

# calculate cost of each component
variable_frame['Cost'] = variable_frame['Quantity'] * variable_frame['Price']

# find sub total
variable_sub = variable_frame['Cost'].sum()

# currency formatting (uses function)
add_dollars = ['Price', 'Cost']
for item in add_dollars:
    variable_frame[item] = variable_frame[item].apply(currency)

# Printing area

print()
print(variable_frame)
print()

print("Variable costs: ${:.2f}".format(variable_sub))
