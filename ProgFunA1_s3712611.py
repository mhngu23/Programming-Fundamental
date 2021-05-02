# Assignment 1
# Minh Hoang Nguyen
# s3712611

"""In this assignment, my reflection will be marked in the """ """ bracket 
    whereas technical comment will be marked with the # symbol
    Overview Reflection: 
    The most challenging parts are:
    * Interpreting the Project Brief, which I think is very crucial considering if this is a real world problem
    Problem with the code:
    * The placing_order function could have been divided into shorter functions.
    * The product_list_update function sometime crash, still not sure why.  
    * Cannot format the last order summary table properly,  which  I could have fixed if I have more time. Accordingly,
    to the length of the string. In this case I am using a static value
    Reference List:
    [1]: A. Song. (2021). COSC2531ProgrammingFundamentalsAssignment 1. [Online]. 
    Available: https://rmit.instructure.com/courses/79857/assignments/570145.
    [2]: w3schools.com, "Python zip() Function"; https://www.w3schools.com/python/ref_func_zip.asp.
    [3]: note.nkmk.me, "Unpack a tuple / list in Python"; https://note.nkmk.me/en/python-tuple-list-unpack/
    """

customer_name_list = []
product_name_list = ["pen", "book", "ruler", "rubber", "pencil", "notebook"]
product_price_list = ["2", "N/A", "8", "0", "1", "10"]
"""Task 1.6: 
    Products and their prices in this program are stored in 2 different lists: product_name_list, product_price_list.
    The items and their prices are stored from input in chronological order and are assumed to be printed in this order. 
    An item with index 1 has a price of index 1 in its list.
    Eg: In the original list pen has a price of $2"""
product_stock = [100, 100, 100, 100, 100, 100, 100]
total_price_order_history = {}
# A dictionary where the keys are the customer's name and the values are the total money that customer has spent
order_list = [[0] * len(product_name_list)] * len(customer_name_list)
# Create a list in a list.
# First list is based on the number of name of the customer in customer_name_list.
# Second list is for each customer create a list of [0,0,0,0]. The number of [0] is equal to the number of product.
"""Reflection:
I could have use a dictionary to store the order_list as values and keys instead of a list in a list, and that would 
make the program more efficient. 
However, due to not being able to format the final table using this method, I used list in list"""


def placing_order():
    # This function is used to let the user input the new order. It used the function <.index()> to get the index of
    # the input and link it with the associate lists that I need.
    """Reflection:
        I could have divided this function into smaller functions to improve its usability.
        The function was made on the assumption that customer name only include first name and is case sensitive, this
        is not true in real problem. It can be improved on this.
        All intended ERROR return user back to the MENU which is inefficient, it could have automatically make a new
        order"""
    global customer_name_list, product_name_list, product_price_list, product_stock
    product_name, product_quantity, product_price, total_price = None, None, None, None
    customer_name = str(input('Enter the name of the customer [Eg:Jack]:\n').strip())
    # Display a message asking the customer name.
    while product_name is None:
        print('These are the current products:')
        print(*product_name_list, sep=',')  # [3]
        # Print out the product list so customer will know what the store have.
        product_name = str(input('Enter the name of the product (only product available will be executed):\n').strip())
        if product_name in product_name_list:  # Check if product name is in the product list
            product_index = product_name_list.index(product_name)
            # looking up product index in the product list.
            product_price = product_price_list[product_index]
            # Getting the product price using the above product index.
            if product_price_list[product_index] != 'N/A':
                if (customer_name not in customer_name_list) and (float(product_price_list[product_index]) == 0):
                    # Checking if an customer is a regular customer if they are not they cannot order free item.
                    print('ERROR: Sorry this order cannot be process as this is not a regular customer'
                          'Only regular customer can order free item')
                    input('Press enter to go back to the menu\n')
                    return
                else:
                    while product_quantity is None:
                        product_quantity = input('Enter the quantity of the product (only enter number):\n').strip()
                        try:
                            product_quantity = int(product_quantity)
                        except ValueError:
                            print('Please only enter an integer as this is the quantity')
                            product_quantity = None
                    if product_quantity > product_stock[product_index]:
                        # Checking if there are enough stock for the order.
                        print('ERROR: This order cannot be process as there are not enough stocks for this product\n',
                              'The current stocks for this product are: ')
                        print(product_name, 'has {} items in stock'.format(product_stock[product_index]))
                        # Display the current stock for the item.
                        input('Press enter to go back to the menu\n')
                        return
                    else:
                        product_stock[product_index] = product_stock[product_index] - product_quantity
                        # Reduce the quantity of product in stock after each order.
                        if customer_name in customer_name_list:
                            total_price = returning_customer(product_price, product_quantity, customer_name,
                                                             product_index)
                        else:
                            total_price = new_customer(product_price, product_quantity, customer_name, product_index)
            else:
                print('ERROR: This product is not available to order due to pricing issue\n')
                input('Press enter to go back to the menu\n')
                return
        else:
            print('ERROR: This product is not available in our stock list\n')
            input('Press enter to go back to the menu\n')
            return
    print(customer_name, 'purchased', product_name, 'x', product_quantity, '\n'
                                                                           'Unit Price: ', product_price, '\n'
                                                                                                          'Total '
                                                                                                          'Price: '
                                                                                                          '$' +
          str(total_price))
    input('Press enter to go back to menu!\n')


def returning_customer(product_price, product_quantity, customer_name, product_index):
    """This function is used to calculate the total price for returning customer.
        Returning customer will get 10% discount.
        This function updates the total_price_order_history dictionary which stores the value each customer has spent.
        It also updates the order_list which summarize all orders that has been placed in the past"""
    global customer_name_list, product_name_list, total_price_order_history, order_list
    print('Returning customer get 10% discount')
    total_price = float(product_price) * product_quantity * 90 / 100
    # Getting 10% discount for loyal customer
    total_price_order_history[customer_name] += total_price
    # Summing the total price of this order and past order onto total_price_order_history dictionary
    # Ex: Customer order 100$ before + 100$ this time = 200$
    customer_index = customer_name_list.index(customer_name)
    order = individual_order(len(product_name_list), product_quantity, product_index)
    order_list[customer_index] = [int(x) + int(y) for x, y in zip(order_list[customer_index], order)]  # [2]
    # The list of customer is store in chronological order. 1st customer is index 1, 2nd is 2
    # The code above will plus past order of a customer with his/her new order
    # Ex: [0,10,0,0] + [10,0,0,0] = [10,10,0,0]
    return total_price


def new_customer(product_price, product_quantity, customer_name, product_index):
    """This function is used to calculate the total price for new customer.
        The function also updates total_price_order_history dictionary which stores the value each customer has spent.
        It also updates the order_list which summarize all orders that has been placed in the past."""
    global customer_name_list, product_name_list, total_price_order_history, order_list
    total_price = float(product_price) * product_quantity
    customer_name_list.append(customer_name)
    # This is a new customer so his/her name will be add to the list for future use
    total_price_order_history.update({customer_name: total_price})
    # This is a new customer so his/her order value will be add to the dictionary for future use
    order = individual_order(len(product_name_list), product_quantity, product_index)
    order_list.append(order)
    # This is a new customer so his/her order value will be add to the order list for future use
    return total_price


def product_list_update():
    global product_name_list, product_price_list
    answer = None
    while answer not in ('y', 'n'):
        answer = (str(input('Do you wish to update the product list (This is no return) [Enter y or n]?\n'))).lower()
        if answer == 'y':
            product_name_list = []  # Creating a brand new product list.
            product_price_list = []  # Creating a brand new associate price list for each product
            product_name_list = [product_name.strip() for product_name in input('Enter the new product list ['
                                                                                'Eg:phone,PC, '
                                                                                'laptop,television]:\n').split(',')]
            # Asking the user to input a new product list.
            """Reflection:
            Instead of separating by space, I separated each product with comma to make it easier to manage.
            I think letting user input item by item is more appropriate and easier to manage error.
            However, as the assignment brief [1] asks to enter a list of products, I decided to follow."""
            product_price_list = [product_price.strip() for product_price in input('Enter the new product price ['
                                                                                   'Eg:1,0, '
                                                                                   '3.5,N/A]: '
                                                                                   '\n(Product price enter must be '
                                                                                   'the same '
                                                                                   'with the order of the product '
                                                                                   'list above) '
                                                                                   '\n(Enter 0 for free product) '
                                                                                   '\n(Enter N/A for product with '
                                                                                   'unknown '
                                                                                   'price) '
                                                                                   '\n(negative price will be treat '
                                                                                   'as N/A)\n').split(',')]
            # Asking the user to input the new price for each product in the same order.
            for index in range(len(product_price_list)):
                if float(product_price_list[index]) < 0:
                    # If the user input an negative price, you want to change it to N/A
                    product_price_list[index] = 'N/A'
                else:
                    continue
            if len(product_name_list) != len(product_price_list):
                # If the number of product price is not equal to the number of product, asked the users to re-input.
                print('Function cannot be execute as the number of products is different from the number of prices')
                print('Please try again!')
                answer = None
            else:
                print('The new product list are:')
                print(*product_name_list, sep=',')  # [3]
                # Print out the new product list
                print('The price of the new product are:')
                print(*product_price_list, sep=',')  # [3]
                # Print out the new product price
                input('\nPress enter to go back to menu!\n')
        elif answer == 'n':
            input('Press enter to go back to menu!\n')
            break
        else:
            print('Please only enter [Eg:y/n]')
            answer = None


def print_customer_name_list():
    if not customer_name_list:
        print("You have not had any customer yet!")
        input('Press enter to go back to menu!\n')
        return
    else:
        print('These are your current customers:')
        print(*customer_name_list, sep=',')
        input('Press enter to go back to menu!\n')


def print_product_name_list():
    if not product_name_list:
        print("You have not entered any product yet!")
        input('Press enter to go back to menu!\n')
        return
    else:
        print('This is the product menu: ')
        for index in range(len(product_name_list)):
            print(product_name_list[index], 'is ${}'.format(product_price_list[index]))
    input('Press enter to go back to menu!\n')


def replenish():
    global product_stock
    while True:
        try:
            quantity_stock = int(input('Please enter the quantity of the updated product stock: '))
            for product in range(len(product_name_list)):
                product_stock[product] = quantity_stock
                """Reflection:
                    Instead of updating all the stocks, this could have been changed to updating for specific one."""
                # Update the product_stock list with the new quantity inputted by the user.
                print('The current stocks for', product_name_list[product], 'is', product_stock[product])
            input('Press enter to go back to menu! \n')
            break
        except ValueError:
            print('This is not valid since quantity of the product in stock can only be integer number')


def valuable_customer():
    global total_price_order_history
    if total_price_order_history == {}:
        print('You have no customer yet!')
        input('Press enter to go back to menu\n')
        return
    else:
        temp = max(total_price_order_history.values())
        # Looking for the highest value in the values of the total_price_order_history dictionary.
        for customer_name, price in total_price_order_history.items():
            if price == temp:
                # Use the temp number to look for the keys and also the most valuable customer.
                print(customer_name, 'is the current most valuable customer')
                input('Press enter to go back to menu! \n')


def individual_order(number_of_product, product_quantity, product_index):
    # Return an individual order in the form of a list. Ex: [10,0,0,0] for 4 products
    order = [0] * number_of_product
    order[product_index] += product_quantity
    return order


def display_order_summary():
    """Reflection:
        I spend quite sometime on formatting this table, however, cannot get it right.
        I could have create a column variable and used its length to format
        If the product name length is > the column variable length I can fixed the input n for {:n} for the output
        by the amount of different"""
    global product_name_list, customer_name_list, order_list
    s = '    ' + '{:>10}' * len(product_name_list)
    s2 = '{:4}' + '{:>10}' * (len(product_name_list))
    print(s.format(*product_name_list))
    for i in range(len(customer_name_list)):
        for j in range(len(order_list[i])):
            order_list[i][j] = str(order_list[i][j])
        print(s2.format(customer_name_list[i], *order_list[i]))
    input('Press enter to go back to menu!\n')


if __name__ == '__main__':
    print('Welcome to assignment 1')
    while True:
        option = input('\nYou can choose from the following options\n'
                       '1: to place a new order\n'
                       '2: to update the current product list\n'
                       '3: to display the customer list\n'
                       '4: to display the products and their prices\n'
                       '5: to update the stock inventory\n'
                       '6: to find the most valuable customer\n'
                       '7: to see the summary of all the orders\n'
                       '0: to exit the program\n')

        if option == '1':
            placing_order()
        elif option == '2':
            product_list_update()
        elif option == '3':
            print_customer_name_list()
        elif option == '4':
            print_product_name_list()
        elif option == '5':
            replenish()
        elif option == '6':
            valuable_customer()
        elif option == '7':
            display_order_summary()
        elif option == '0':
            print('See you next time!')
            break
        else:
            print('This option is not available at the moment. PLease re-enter your choice')
