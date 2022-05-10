import pandas
import math


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


# prints expenses
def expense_print(heading, frame, subtotal):
    print()
    print("----- {} Costs -----".format(heading))
    print(frame)
    print()
    print("{} Costs: ${:.2f}".format(heading, subtotal))
    return ""


# workout profit goal and total sales required
def profit_goal(total_costs):

    # initialise variables and error message
    error = "Please enter a valid profit goal\n"

    valid = False
    while not valid:

        # ask for a profit goal
        response = input("What is your profit goal? (eg $500 or 50%) ")

        # check if first character is $
        if response[0] == "$":
            profit_type = "$"
            # Get amount (everything after the $)
            amount = response[1:]

        # check if last character is %
        elif response[-1] == "%":
            profit_type = "%"
            # Get amount (everything after the $)
            amount = response[:-1]

        else:
            # set response to amount for now
            profit_type = "unknown"
            amount = response

        try:
            # check amount is a number more than zero
            amount = float(amount)
            if amount <= 0:
                print(error)
                continue

        except ValueError:
            print(error)

        if profit_type == "unknown" and amount >= 100:
            dollar_type = yes_no("Do you mean ${:.2f}. ie {:.2f} dollars? , y / n ".format(amount, amount))
            print()

            # set profit type based on user answer above
            if dollar_type == "yes":
                profit_type = "$"
            else:
                profit_type = "%"

        elif profit_type == "unknown" and amount < 100:
            percent_type = yes_no("Do you mean {}%? , y / n ".format(amount))
            print()

            if percent_type == "yes":
                profit_type = "%"
            else:
                profit_type = "$"

        # return profit goal to main routine
        if profit_type == "$":
            return amount
        else:
            goal = (amount / 100) * total_costs
            return goal


# rounding function
def round_up(amount, var_round_to):
    return int(math.ceil(amount / var_round_to)) * var_round_to


# instructions function
def instructions():
    show_help = False
    while show_help == False:
        show_help = yes_no("Would you like to see the instructions? ").lower()

    if show_help == "yes":
        print()
        print("**** FRC Instructions ****\n\n"
              "This program will ask you for the following:\n"
              "- The name of your product\n"
              "- How many units you intend to be producing\n"
              "- Each components name, quantity and cost (type xxx into item name to break the loop)\n"
              "- You will be asked if you have fixed costs. If yes enter the name and cost (use xxx again once you are done)\n"
              "- Profit goal (percent or dollar amount)\n"
              "- And what you want your selling price to be rounded to\n\n"
              "The program will then print out dataframes with your variable and fixed costs (if applicable)\n"
              "It will also output the total costs, profit targets, total sales required and a recommended sales price\n\n"
              "The data will also be written to a text file (it will have the same name as your product)")

    return ""


# *** Main routine ***

# Ask user if they want to see instructions
instructions()
print("\n----- Program Launched! -----\n")

# Get product name
product_name = not_blank("Product name: ")

how_many = num_check("How many items will you be producing? ",
                     "The number of items must be a whole number more than zero", int)

# get variable costs
print("\nPlease enter your variable costs below...")

variable_expenses = get_expenses("variable")
variable_frame = variable_expenses[0]
variable_sub = variable_expenses[1]

# ask if user has fixed costs
have_fixed = yes_no("\nDo you have fixed costs (y / n)? ")

if have_fixed == "yes":
    # get fixed costs
    fixed_expenses = get_expenses("fixed")
    fixed_frame = fixed_expenses[0]
    fixed_sub = fixed_expenses[1]

else:
    fixed_sub = 0

# work out total costs and profit target
all_costs = variable_sub + fixed_sub
profit_target = profit_goal(all_costs)

# Calculate total sales needed to reach goal
sales_needed = all_costs + profit_target

# Ask user for rounding
round_to = num_check("Round to nearest...? $", "Can't be 0", int)

# Calculate recommended price
selling_price = sales_needed / how_many
print("Selling Price (unrounded): ${:.2f}".format(selling_price))

recommended_price = round_up(selling_price, round_to)

# Write data to file

# change frames to strings
variable_txt = pandas.DataFrame.to_string(variable_frame)

if have_fixed == "yes":
    fixed_txt = pandas.DataFrame.to_string(fixed_frame)

# convert numbers to strings for text file
variable_sub_str = ("Variable Costs: ${:.2f}".format(variable_sub))
fixed_sub_str = ("Fixed Costs: ${:.2f}".format(fixed_sub))
all_costs_str = ("\n--- Total Costs: ${:.2f} ---".format(all_costs))
profit_target_str = ("Profit Target: ${:.2f}".format(profit_target))
total_sales_str = ("Total Sales: ${:.2f}".format(sales_needed))
selling_price_str = ("Minimum Price: ${:.2f}".format(selling_price))
recommended_price_str = ("Recommended Price: ${:.2f}".format(recommended_price))

# set up list of items that need to be written to the txt file
if have_fixed == "yes":
    to_write = [product_name, variable_txt, variable_sub_str, fixed_txt, fixed_sub_str, all_costs_str,
                "\n--- Profit & Sales Targets ---", profit_target_str, total_sales_str,
                "\n--- Pricing ---", selling_price_str, recommended_price_str]
else:
    to_write = [product_name, variable_txt, variable_sub_str, all_costs_str, "\n--- Profit & Sales Targets ---", profit_target_str,
                total_sales_str, "\n--- Pricing ---", selling_price_str, recommended_price_str]

# Write to file...
# create file to hold data (add .txt extension)
file_name = "{}.txt".format(product_name)
text_file = open(file_name, "w+")

# print out to_write list
for item in to_write:
    text_file.write(item)
    text_file.write("\n\n")

# close file
text_file.close()

# *** Printing Area ***

print("\n***** Fund Raising - {} *****".format(product_name))
print()
expense_print("Variable", variable_frame, variable_sub)
print()

if have_fixed == "yes":
    expense_print("Fixed", fixed_frame[['Cost']], fixed_sub)
    print()

print("\n----- Total Costs: ${:.2f} -----".format(all_costs))
print()

print("\n----- Profit & Sales Targets -----")
print()
print("Profit Target: ${:.2f}".format(profit_target))
print("Total Sales: ${:.2f}".format(all_costs + profit_target))
print()

print("\n----- Pricing -----")
print()
print("Minimum Price: ${:.2f}".format(selling_price))
print("Recommended Price: ${:.2f}".format(recommended_price))