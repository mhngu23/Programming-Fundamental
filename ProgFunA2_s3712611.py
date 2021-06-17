# Assignment 2
# Minh Hoang Nguyen
# s3712611

"""Thank you for reading!
    The highest level that I have attempted in this assignment will be High Distinction
    Submission History:
    ProgFunA2_s3712611.py: 14 April 2021
    ProgFunA2_s3712611 (Week 7).py: 26 April 2021
    ProgFunA2_s3712611 (Week 8).py: 1 May 2021 
    ProgFunA2_s3712611 (Week 9).py: 8 May 2021 
    ProgFunA2_s3712611 (Week 10).py: 15 May 2021 
    ProgFunA2_s3712611 (week 11).py: 21 May 2021   
    ProgFunA2_s3712611 (final).py: 31 May 2021
    Overview Reflection: 
    The most challenging parts are:
    * Interpreting the Project Brief.
    * Implementing Object Oriented Programming into the program is very hard. However, I have been able to learn a lot 
    from completing this assignment, and now, I understand why using OOP is more convenient. 
    * Still, I could have implement it better if more time is available. 
    * The Operations.order_display sometime crash (depend on the number of order in the orders.txt file and number of
    customer in the customers.txt). I have tested it out with many samples, but sometime it crash.
    * I tried to prevent empty input file products.txt and orders.txt with os.stat, however, it can only prevent file
    with no text. File with blank lines still can go through this empty file check since its file size is not equal to
    0.
    """

import sys
import datetime
import os


class Error(Exception):
    pass


class ProductInputError(Error):
    """Raise when there is an ordering problem related to product.
    Eg: Product is not exist.
    Product has negative or no price.
    A new customer order a free product."""
    pass


class OtherInputError(Error):
    """Raise when the input from the user does not meet the requirements
    Eg: When asked for y or n and receives a
    When asked for 1 or 2 receives 3"""
    pass


class Customer:
    """Class Customer was designed as a parent class for Retail Customer and WholeSale Customer
    Since the discount_rate for these customers are different, ID, name and customer_type are the only inputs for this
    class.
    ID and name attribute are set privately to prevent access by user but the customer_type must be able to be changed
    for convinience."""
    def __init__(self, ID, name, customer_type):
        self.__ID = ID
        self.__name = name
        self.customer_type = customer_type

    @property
    def ID(self):
        return self.__ID

    @property
    def name(self):
        return self.__name

    def get_discount(self, price):
        """This was designed as an empty method since the discount rate is different between Retail and Wholesale
        Customer."""
        pass


class RetailCustomer(Customer):
    """Class RetailCustomer was designed to inherit from Class Customer.
    Attributes such as ID, name, customer_type were inherited since this is common attributes between the 2 types of
    customer.
    Default discount rate were set for the whole class as 10% according to the project brief"""
    discount_rate = 10

    def __init__(self, ID, name, customer_type, discount_rate, total):
        super().__init__(ID, name, customer_type)
        self.order_value = 0
        self.discount_rate = discount_rate
        self.discount_amount = 0
        self.total = float(total)

    def set_discount_rate(self, order_value, discount_rate):
        """This method is used for new customer or to prevent the case discount_rate was mistakenly left out. Then
         the default discount_rate of 10% would be used for these object."""
        if float(discount_rate) == 0:
            self.discount_rate = float(RetailCustomer.discount_rate)
        else:
            self.discount_rate = float(discount_rate)

    def get_discount(self, order_value):
        self.discount_amount = float(order_value) * float(self.discount_rate) / 100
        return self.discount_amount

    def display(self):
        print("ID: {}, name: {}, customer type: {}, discount_rate: {}, total: {}".format(self.ID,
                                                                                         self.name,
                                                                                         self.customer_type,
                                                                                         self.discount_rate,
                                                                                         self.total))

    @staticmethod
    def set_rate(new_rate):
        RetailCustomer.discount_rate = float(new_rate)


class WholesaleCustomer(Customer):
    """Class WholesaleCustomer was designed to inherit from Class Customer.
        Attributes such as ID, name, customer_type were inherited since this is common attributes between the 2 types of
        customer.
        Default discount rate 1 were set for the whole class as 10% according to the project brief. This discount_rate
        is for order under the threshold_rate, which is set as 1000 according to the project brief.
        The default for the discount rate is set to discount rate 1 + 5
        """
    total = 0
    threshold_rate = 1000
    discount_rate_1 = 10
    discount_rate_2 = discount_rate_1 + 5

    def __init__(self, ID, name, customer_type, discount_rate, total):
        super().__init__(ID, name, customer_type)
        self.discount_amount = 0
        self.discount_rate = discount_rate
        self.total = float(total)
        self.order_value = 0
        self.threshold_rate = WholesaleCustomer.threshold_rate

    def set_discount_rate(self, order_value, discount_rate):
        if float(discount_rate) == 0:
            self.discount_rate = float(WholesaleCustomer.discount_rate_1)
        elif float(discount_rate) != 0 and float(order_value) <= self.threshold_rate:
            self.discount_rate = float(discount_rate)
        elif float(discount_rate) != 0 and float(order_value) > self.threshold_rate:
            self.discount_rate = float(discount_rate) + 5

    def get_discount(self, order_value):
        self.discount_amount = float(order_value) * float(self.discount_rate) / 100
        return self.discount_amount

    def display(self):
        print("ID: {}, name: {}, customer type: {}, discount_rate: {}, total: {}".format(self.ID,
                                                                                         self.name,
                                                                                         self.customer_type,
                                                                                         self.discount_rate,
                                                                                         self.total))

    @staticmethod
    def set_rate(new_rate):
        WholesaleCustomer.discount_rate_1 = float(new_rate)
        WholesaleCustomer.discount_rate_2 = float(new_rate) + 5

    @staticmethod
    def set_threshold_rate(new_rate):
        WholesaleCustomer.threshold_rate = float(new_rate)


class Product:
    """ID, name, and price attribute are set privately to prevent access by user but the stock must be able to be
    changed conviniently for the purpose of stock update.
    The count value is for all individual product object, so whenever the product is ordered the count will update once.
    This is used to track the most popular product.
    """
    def __init__(self, ID, name, price, stock):
        self.__ID = ID
        self.__name = name
        self.__price = price
        self.stock = stock
        self.count = 0

    @property
    def ID(self):
        return self.__ID

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    def display(self):
        print("ID: {}, name: {}, price: {}, qty: {}".format(self.__ID, self.__name, self.price,
                                                            self.stock))


class Orders:
    """Orders Class have all attributes that will be used for the calculation of the total price of an order.
    Beside that it has attribute date which will take in all extra information that have the form of a date.
    All other extra information will be treated as a comment and will be added to the comment attribute."""
    def __init__(self, customer, product, product_quantity, other):
        self.records = Records()
        self.__customer = customer
        self.__product = product
        self.product_price = self.product_price()
        self.product_quantity = product_quantity
        self.order_value = float(self.product_price) * int(self.product_quantity)
        self.discount_amount = self.discount_amount()
        self.total_price = self.order_value - float(self.discount_amount)
        self.date = None
        self.comment = None
        if other is not None:
            for i in range(len(other)):
                try:
                    datetime.datetime.strptime(str(other[i]).strip(), "%Y-%m-%d")
                except ValueError:
                    self.comment = str(other[i]).strip()
                    continue
                else:
                    self.date = datetime.datetime.strptime(str(other[i]).strip(), "%Y-%m-%d")
                    continue
        else:
            self.date = None
            self.comment = None

    @property
    def customer(self):
        return self.__customer

    @property
    def product(self):
        return self.__product

    def discount_amount(self):
        """This method first search for the customer object using the customer name or ID. Then the method get_discount
        was used to return the discount amount"""
        customer = self.records.find_customers(str(self.__customer).strip())
        order_value = self.order_value
        discount = customer.get_discount(order_value)
        return discount

    def product_price(self):
        return self.records.find_products(self.__product).price

    def display(self):
        print(self.customer, 'purchased', self.product, 'x', self.product_quantity, '\n'
                                                                                    'Unit Price: $'
              +
              str(self.product_price), '\n'
                                       'Total '
                                       'Price: '
                                       '$' +
              str(self.total_price))


class Combo:
    """Class Combo has attribute combo_product_combination which is the list of product that makes up this combo
    The price for this whole combo are then calculated using the combo_price_calculation(), which first search for
    all the product in this combo using their ID and then take the sum"""
    def __init__(self, ID, name, product_combination, stock):
        self.__ID = ID
        self.__name = name
        self.__combo_product_combination = product_combination
        self.stock = stock
        self.price = self.combo_price_calculation()
        self.count = 0

    @property
    def ID(self):
        return self.__ID

    @property
    def name(self):
        return self.__name

    @property
    def combo_product_combination(self):
        return self.__combo_product_combination

    def combo_price_calculation(self):
        temp = Records()
        combo_price = 0
        for ID in self.__combo_product_combination:
            product_price = temp.find_products(str(ID).strip()).price
            combo_price = combo_price + float(product_price)
        return combo_price

    def display(self):
        print("ID: {}, name: {}, products include: {}, price: {}, qty: {}".format(self.__ID, self.__name,
                                                                                  ','.join(
                                                                                      self.__combo_product_combination),
                                                                                  self.price, self.stock))


class Records:
    customers_data = []
    products_data = []
    orders_data = []
    customers_list = []
    products_list = []
    orders_list = []
    combos_list = []

    def read_customers(self, file_name):
        try:
            customers_file = open(file_name, 'r')
            line_from_file = customers_file.readline()
            while line_from_file != "":
                """The customers_file will be read until there is no more line to read."""
                fields_from_line = line_from_file.split(",")
                self.customers_data.append(fields_from_line)
                line_from_file = customers_file.readline()
            for data in self.customers_data:
                """data[2] is the data that include the type of customers. I use this to classify which type of customer
                or which object should be created for this data."""
                if data[2].strip() == 'R':
                    customer = RetailCustomer(data[0].strip(), data[1].strip(), data[2].strip(),
                                              data[3].strip(),
                                              data[4].strip())
                    self.customers_list.append(customer)
                if data[2].strip() == 'W':
                    customer = WholesaleCustomer(data[0].strip(), data[1].strip(), data[2].strip(),
                                                 data[3].strip(),
                                                 data[4].strip())
                    self.customers_list.append(customer)
            Records.customers_data = []
            customers_file.close()
        except FileNotFoundError:
            print('The current customer file is missing')
            print('Program will exit')
            sys.exit()

    def read_products(self, file_name):
        try:
            products_file = open(file_name, 'r')
            line_from_file = products_file.readline()
            while line_from_file != "":
                """The product file will be read until there is no more line to read."""
                fields_from_line = line_from_file.split(',')
                self.products_data.append(fields_from_line)
                line_from_file = products_file.readline()
            for data in self.products_data:
                """Since both Product and Combo will be included in the same product_file it is important to 
                diffirentiate them. This was done using their ID. Single product has P initial in their ID, while,
                combo has C initial in their ID."""
                if (data[0].strip())[0] == 'P':
                    product = Product(data[0].strip(), data[1].strip(), data[2].strip(), data[3].strip())
                    self.products_list.append(product)
                elif (data[0].strip())[0] == 'C':
                    combo = Combo(data[0].strip(), data[1].strip(), data[2:len(data) - 2],
                                  data[len(data) - 1].strip())
                    self.combos_list.append(combo)
            Records.products_data = []
            products_file.close()
        except FileNotFoundError:
            print('The current product file is missing')
            print('Program will exit')
            sys.exit()

    def read_orders(self):
        file_name = None
        while file_name is None:
            try:
                file_name = input('Please enter the name/path of the order file [Eg: March/orders1.txt]: ')
                orders_file = open(file_name, 'r')
                line_from_file = orders_file.readline()
                while line_from_file != "":
                    fields_from_line = line_from_file.split(',')
                    self.orders_data.append(fields_from_line)
                    line_from_file = orders_file.readline()
                for data in self.orders_data:
                    try:
                        if int(data[2].strip()) <= int(self.find_products(str(data[1]).strip()).stock):
                            """Handling when the quantity ordered is higher than the available stock of the product"""
                            if len(data) <= 3:
                                """This is to handle the case when there are date or comment input from the file.
                                Since the first 3 values in this data are fixed only those followed would be checked"""
                                order = Orders(data[0].strip(), data[1].strip(), data[2].strip(), None)
                                self.orders_list.append(order)
                                product = self.find_products(str(data[1]).strip())
                                product.stock = int(product.stock) - int(data[2].strip())
                                product.count += 1
                                customer = self.find_customers(str(data[0]).strip())
                                customer.total = float(customer.total) + float(order.total_price)
                            else:
                                order = Orders(data[0].strip(), data[1].strip(), data[2].strip(),
                                               data[3:len(data)])
                                self.orders_list.append(order)
                                product = self.find_products(str(data[1]).strip())
                                product.stock = int(product.stock) - int(data[2].strip())
                                product.count += 1
                                customer = self.find_customers(str(data[0]).strip())
                                customer.total = float(customer.total) + float(order.total_price)
                        elif int(data[2].strip()) > int(self.find_products(str(data[1]).strip()).stock):
                            raise ProductInputError
                    except ProductInputError:
                        print('ERROR: This specific order for', str((data[0]).strip()), 'of', str((data[1]).strip()),
                              'cannot be process because we '
                              'do not have '
                              'enough stock')
                        print('The current stock for this item is: ', self.find_products(str(data[1]).strip()).stock)
                        print('Other orders in this file will still be processed')
                        continue
                Records.orders_data = []
                orders_file.close()
            except FileNotFoundError:
                print('The order file cannot be found')
                print('Please re-enter the file path')
                file_name = None

    def find_customers(self, search_value=None):
        if search_value.isdigit():
            """This is to diffirentiate the search_value, which can be either ID or name. The ID of a customer is
            always a number so the is.digit() function will return True, while, the name would return False."""
            for i in range(len(self.customers_list)):
                if search_value == self.customers_list[i].ID:
                    return self.customers_list[i]
                elif search_value != self.customers_list[i].ID:
                    if i == len(self.customers_list) - 1:
                        return None
                    else:
                        continue
        else:
            for i in range(len(self.customers_list)):
                if search_value == self.customers_list[i].name:
                    return self.customers_list[i]
                elif search_value != self.customers_list[i].name:
                    if i == len(self.customers_list) - 1:
                        return None
                    else:
                        continue

    def find_products(self, search_value=None):
        if search_value[1:len(search_value)].isdigit():
            """This is to diffirentiate the search_value, which can be either ID or name. The second digit for an 
            ID of a product (Example: P1) is always a number so the is.digit() function will return True, while, the 
            name would return False."""
            for i in range(len(self.products_list)):
                if search_value == self.products_list[i].ID:
                    return self.products_list[i]
                elif search_value != self.products_list[i].ID:
                    if i == len(self.products_list) - 1:
                        for j in range(len(self.combos_list)):
                            if search_value == self.combos_list[j].ID:
                                return self.combos_list[j]
                            elif search_value != self.combos_list[j].ID:
                                if j == len(self.combos_list) - 1:
                                    return None
                                else:
                                    continue
                    else:
                        continue
        else:
            for i in range(len(self.products_list)):
                if search_value == self.products_list[i].name:
                    return self.products_list[i]
                elif search_value != self.products_list[i].name:
                    if i == len(self.products_list) - 1:
                        for j in range(len(self.combos_list)):
                            if search_value == self.combos_list[j].name:
                                return self.combos_list[j]
                            elif search_value != self.combos_list[j].name:
                                if j == len(self.combos_list) - 1:
                                    return None
                                else:
                                    continue
                    else:
                        continue

    def list_customers(self):
        for customer in self.customers_list:
            customer.display()
        input('Press enter to continue\n')

    def list_products(self):
        for product in self.products_list:
            product.display()
        for combo in self.combos_list:
            combo.display()
        input('Press enter to continue\n')

    def save_customers(self, file_name):
        output_file = open(file_name, "w")
        for customer in self.customers_list:
            output_file.write(str(customer.ID) + ', ' + str(customer.name) + ', ' + str(customer.discount_rate) + ', ' +
                              str(customer.total))
        output_file.close()

    def save_products(self, file_name):
        output_file = open(file_name, "w")
        for product in self.products_list:
            output_file.write(str(product.ID) + ', ' + str(product.name) + ', ' + str(product.price) + ', ' +
                              str(product.stock))
        for combo in self.combos_list:
            output_file.write(str(combo.ID) + ', ' + str(combo.name) + ', ' + str(combo.combo_product_combination) +
                              ', ' +
                              str(combo.stock))
        output_file.close()


def order_input(customer_search_value, product_search_value, product_quantity):
    if customer_search_value is None:
        print('You can search for the customer using ID or name')
        customer_search_value = str(input('Enter the ID or name of the customer [Eg:1 or Jack]:\n').strip())
    if product_search_value is None:
        print('You can search for the product using ID or name')
        product_search_value = str(input('Enter the ID or name of the product [Eg:P1 or Wine]:\n').strip())
        while product_quantity is None:
            product_quantity = input('Enter the quantity of the product (only enter number):\n').strip()
            try:
                product_quantity = int(product_quantity)
            except ValueError:
                print('Please only enter an integer as this is the quantity')
                product_quantity = None
    return customer_search_value, product_search_value, int(product_quantity)


class Operations:
    def __init__(self):
        self.records = Records()
        option = None
        while option is None:
            option = input('\nYou can choose from the following options\n'
                           '1: to display the current customer list\n'
                           '2: to display the current product list\n'
                           '3: to place an order\n'
                           '4: to adjust the discount rate\n'
                           '5: to show the orders\n'
                           '6: to update the stock (replenish)\n'
                           '7: to reveal the most valuable customer\n'
                           '8: to reveal the most popular product\n'
                           '0: to exit the program\n')
            if option == '1':
                self.records.list_customers()
                option = None
            elif option == '2':
                self.records.list_products()
                option = None
            elif option == '3':
                temp = None
                while temp is None:
                    try:
                        temp = str(input('\nYou can choose from the following options\n'
                                         '1: to read from an existing text order file\n'
                                         '2: to manually input a new order\n'
                                         '0: to exit to the main menu\n'))
                        if temp == '1':
                            print('Note: Orders from the file will be read from the top to bottom\n'
                                  'Product with not enough stock will not be processed\n'
                                  'If an top order uses up all the stock the next order with the same product will '
                                  'not be processed\n'
                                  'First come first serve\n')
                            self.records.read_orders()
                            input('Press enter to return to main menu')
                            option = None
                        elif temp == '2':
                            self.placing_order()
                            option = None
                        elif temp == '0':
                            option = None
                        else:
                            raise OtherInputError
                    except OtherInputError:
                        print('ERROR: The option you input is not available!! Please re-input')
                        temp = None
            elif option == '4':
                self.discount_rate()
                option = None
            elif option == '5':
                self.order_display()
                option = None
            elif option == '6':
                self.replenish()
                option = None
            elif option == '7':
                self.valuable_customer()
                option = None
            elif option == '8':
                self.popular_product()
                option = None
            elif option == '0':
                print('See you next time!')
                break
            else:
                print('This option is not available at the moment. PLease re-enter your choice')
                option = None

    def placing_order(self):
        customer_search_value, product_search_value, quantity = order_input(None, None, None)
        customer = self.records.find_customers(customer_search_value)
        product = None
        while product is None:
            try:
                product = self.records.find_products(product_search_value)
                if product is not None:
                    try:
                        if float(product.price) >= 0 and product.price is not None:
                            try:
                                if float(product.price) > 0 or customer is not None:
                                    while True:
                                        if int(quantity) < 0 or int(quantity) > int(product.stock):
                                            print('ERROR: There is not enough stock for this item!!!')
                                            print(product.name,
                                                  'only has {} items in stock'.format(product.stock))
                                            input('Press enter to return to main menu\n')
                                            return
                                        else:
                                            if customer is None:
                                                temp = None
                                                while temp is None:
                                                    try:
                                                        temp = input(
                                                            'This is a new customer. Do you want to create an account '
                                                            'for '
                                                            'him? ['
                                                            'Eg: y/n]: ')
                                                        if temp == 'y':
                                                            customer_name = str(
                                                                input('Enter the name of the customer '
                                                                      '[Eg: James]:\n').strip())
                                                            customer_id = str(len(self.records.customers_list) + 1)
                                                            customer_type = str(
                                                                input('Is this a retail or wholesale customer? [R or W '
                                                                      'only]: '))
                                                            if customer_type == 'R':
                                                                new_customer = RetailCustomer(customer_id,
                                                                                              customer_name,
                                                                                              customer_type,
                                                                                              0, 0)
                                                                self.records.customers_list.append(new_customer)
                                                                order = Orders(new_customer.name, product.name,
                                                                               quantity,
                                                                               None)
                                                                new_customer.set_discount_rate(new_customer.order_value,
                                                                                               new_customer.
                                                                                               discount_rate)
                                                                new_customer.total += order.total_price
                                                                order.display()
                                                                self.records.orders_list.append(order)
                                                                product.stock = str(int(product.stock) - int(quantity))
                                                                product.count += 1
                                                                print("Remaining stock: {}".format(product.stock))
                                                                temp = None
                                                                while temp is None:
                                                                    try:
                                                                        temp = input(
                                                                            'Do you want to see the information of '
                                                                            'this '
                                                                            'product? '
                                                                            '[Eg: '
                                                                            'y/n]: ')
                                                                        if temp == 'y':
                                                                            product.display()
                                                                            input('Press enter to return to main menu\n'
                                                                                  )
                                                                            return
                                                                        elif temp == 'n':
                                                                            input('Press enter to return to main menu\n'
                                                                                  )
                                                                            return
                                                                        else:
                                                                            raise OtherInputError
                                                                    except OtherInputError:
                                                                        print('ERROR: Please only enter y or n (Case '
                                                                              'Sensitive)!!!')
                                                                        temp = None
                                                                input('Press enter to continue\n')
                                                            elif customer_type == 'W':
                                                                new_customer = WholesaleCustomer(customer_id,
                                                                                                 customer_name,
                                                                                                 customer_type,
                                                                                                 0, 0)
                                                                self.records.customers_list.append(new_customer)

                                                                order = Orders(new_customer.name, product.name,
                                                                               quantity,
                                                                               None)
                                                                new_customer.set_discount_rate(new_customer.order_value,
                                                                                               new_customer.
                                                                                               discount_rate)
                                                                new_customer.total += order.total_price
                                                                order.display()
                                                                self.records.orders_list.append(order)
                                                                product.stock = str(int(product.stock) - int(quantity))
                                                                product.count += 1
                                                                print("Remaining stock: {}".format(product.stock))
                                                                temp = None
                                                                while temp is None:
                                                                    try:
                                                                        temp = input(
                                                                            'Do you want to see the information of '
                                                                            'this '
                                                                            'product? '
                                                                            '[Eg: '
                                                                            'y/n]: ')
                                                                        if temp == 'y':
                                                                            product.display()
                                                                            input('Press enter to return to main menu\n'
                                                                                  )
                                                                            return
                                                                        elif temp == 'n':
                                                                            input('Press enter to return to main menu\n'
                                                                                  )
                                                                            return
                                                                        else:
                                                                            raise OtherInputError
                                                                    except OtherInputError:
                                                                        print('ERROR: Please only enter y or n (Case '
                                                                              'Sensitive)!!!')
                                                                        temp = None
                                                        elif temp == 'n':
                                                            input('Press enter to return to main menu\n')
                                                            return
                                                        else:
                                                            raise OtherInputError
                                                    except OtherInputError:
                                                        print('ERROR: Please only enter y or n (Case Sensitive)!!!')
                                                        temp = None
                                            else:
                                                customer.order_value = float(product.price) * float(quantity)
                                                customer.set_discount_rate(customer.order_value,
                                                                           customer.discount_rate)
                                                customer.get_discount(customer.order_value)
                                                order = Orders(customer.name, product.name, quantity, None)
                                                customer.total = customer.total + order.total_price
                                                order.display()
                                                self.records.orders_list.append(order)
                                                product.stock = str(int(product.stock) - int(quantity))
                                                product.count += 1
                                                print("Remaining stock: {}".format(product.stock))
                                                temp = None
                                                while temp is None:
                                                    try:
                                                        temp = input(
                                                            'Do you want to see the information of this product? '
                                                            '[Eg: y/n]: ')
                                                        if temp == 'y':
                                                            product.display()
                                                            input('Press enter to return to main menu\n')
                                                            return
                                                        elif temp == 'n':
                                                            input('Press enter to return to main menu\n')
                                                            return
                                                        else:
                                                            raise OtherInputError
                                                    except OtherInputError:
                                                        print('ERROR: Please only enter y or n (Case Sensitive)')
                                                        temp = None
                                else:
                                    raise ProductInputError
                            except ProductInputError:
                                print('You are a new customer, you cannot order a free product')
                                input('Press enter to return to main menu\n')
                                return
                        else:
                            raise ProductInputError
                    except ProductInputError:
                        print('This product cannot be order at the moment due to price issue')
                        input('Press enter to return to main menu\n')
                        return
                else:
                    raise ProductInputError
            except ProductInputError:
                print('The product you search for does not exist')
                print('These are the current products: ')
                self.records.list_products()
                customer_search_value, product_search_value, quantity = order_input(customer_search_value, None,
                                                                                    None)

    def discount_rate(self):
        temp = None
        while temp is None:
            try:
                temp = str(input('Are you sure you want to change the discount rate!'
                                 ' This is no go back? [Eg: y/n]: ')).lower()
                if temp == 'y':
                    rate_type = None
                    while rate_type is None:
                        try:
                            rate_type = str(input('Do you want to change the default rate or the rate of '
                                                  'a particular person? [1 or 2 only]: \n'
                                                  '<Note: Select option 2 to change the rate of old customer>\n'
                                                  '<Option 1 only change the default discount rate of new customer>\n'))
                            if rate_type == '1':
                                customer_type = None
                                while customer_type is None:
                                    try:
                                        customer_type = str(
                                            input('Are you going to set rate for a retail or wholesale customer? [R '
                                                  'or W '
                                                  'only]: '))
                                        """This is asked since WholeSale Customer also have the option to set the
                                        threshold, while, the Retail Customer does not have this option."""
                                        if customer_type == 'R':
                                            new_rate = None
                                            while new_rate is None:
                                                try:
                                                    new_rate = float(input('Please enter the new rate: '))
                                                    RetailCustomer.set_rate(new_rate)
                                                    print('\nAll new Retail Customer will have discount rate of: ',
                                                          new_rate, '%')
                                                    print(
                                                        'To change the rate of old customer, please select 2 and '
                                                        'change each of them '
                                                        'individually')
                                                    input('Press enter to return to main menu\n')
                                                    return
                                                except TypeError:
                                                    print('ERROR: Discount Rate has to be a number!!!')
                                                    new_rate = None
                                        elif customer_type == 'W':
                                            threshold_or_discount_rate = None
                                            while threshold_or_discount_rate is None:
                                                try:
                                                    threshold_or_discount_rate = str(
                                                        input('Do you want to change the discount rate or threshold '
                                                              'rate'
                                                              ' of '
                                                              'the Wholesale Customer? [1 or 2 only]: '))
                                                    if threshold_or_discount_rate == '1':
                                                        new_rate = None
                                                        while new_rate is None:
                                                            try:
                                                                new_rate = float(input('Please enter the new rate: '))
                                                                WholesaleCustomer.set_rate(new_rate)
                                                                print('All new Wholesale Customer will have discount '
                                                                      'rate of: ', new_rate, '%')
                                                                print(
                                                                    'To change the rate of old customer, please '
                                                                    'select 2 and '
                                                                    'change each of them '
                                                                    'individually')
                                                                input('Press enter to return to main menu\n')
                                                                return
                                                            except TypeError:
                                                                print('ERROR: Discount Rate has to be a number!!!')
                                                                new_rate = None

                                                    elif threshold_or_discount_rate == '2':
                                                        new_rate = None
                                                        while new_rate is None:
                                                            try:
                                                                new_rate = float(input('Please enter the new '
                                                                                       'threshold rate: '))
                                                                WholesaleCustomer.set_threshold_rate(new_rate)
                                                                print('All new Wholesale Customer with order price '
                                                                      'lower than', new_rate,
                                                                      'will have the '
                                                                      'discount rate '
                                                                      'of: ',
                                                                      WholesaleCustomer.discount_rate_1, '%')
                                                                print('All new Wholesale Customer with order price '
                                                                      'higher than', new_rate,
                                                                      'will have the '
                                                                      'discount rate '
                                                                      'of: ',
                                                                      WholesaleCustomer.discount_rate_2, '%')
                                                                print(
                                                                    'To change the rate of old customer, please '
                                                                    'select 2 and change each of them '
                                                                    'individually')
                                                                input('Press enter to return to main menu\n')
                                                                return
                                                            except TypeError:
                                                                print('Threshold rate must be a number')
                                                                new_rate = None
                                                    else:
                                                        raise OtherInputError
                                                except OtherInputError:
                                                    print('ERROR: Please only enter option 1 or 2')
                                                    threshold_or_discount_rate = None
                                        else:
                                            raise OtherInputError
                                    except OtherInputError:
                                        print('ERROR: Please only enter R or W (Case sensitive)!!!')
                                        customer_type = None
                            elif rate_type == '2':
                                print('You can search for the customer using ID or name')
                                customer_search_value = None
                                while customer_search_value is None:
                                    try:
                                        customer_search_value = str(
                                            input('Enter the ID or name of the customer you want to change rate'
                                                  ' [Eg:1 or Jack]: ').strip())
                                        customer = self.records.find_customers(customer_search_value)
                                        if customer is not None:
                                            if customer.customer_type == 'W':
                                                threshold_or_discount_rate = input('This is an Wholesale Customer\n'
                                                                                   'Do you want to change the '
                                                                                   'discount rate or '
                                                                                   'threshold '
                                                                                   'rate? [1 or 2 only]:\n')
                                                if threshold_or_discount_rate == '1':
                                                    new_rate = None
                                                    while new_rate is None:
                                                        try:
                                                            new_rate = float(input('Please enter the new rate: '))
                                                            customer.discount_rate = new_rate
                                                            print(customer.name, ' will have discount '
                                                                                 'rate of: ', new_rate, '%')
                                                            input('Press enter to return to main menu\n')
                                                            return
                                                        except TypeError:
                                                            print('ERROR: Discount Rate has to be a number!!!')
                                                            new_rate = None
                                                elif threshold_or_discount_rate == '2':
                                                    new_rate = None
                                                    while new_rate is None:
                                                        try:
                                                            new_rate = float(input('Please enter the new '
                                                                                   'threshold rate: '))
                                                            customer.threshold_rate = new_rate
                                                            print('All order from ', customer.name, ' with order price '
                                                                                                    'lower than',
                                                                  customer.threshold_rate,
                                                                  '$ will have the '
                                                                  'discount rate '
                                                                  'of: ',
                                                                  customer.discount_rate, '%')
                                                            print('All order from ', customer.name, ' with order price '
                                                                                                    'higher than',
                                                                  customer.threshold_rate,
                                                                  '$ will have the '
                                                                  'discount rate '
                                                                  'of: ',
                                                                  float(customer.discount_rate) + 5, '%')
                                                            input('Press enter to return to main menu\n')
                                                            return
                                                        except TypeError:
                                                            print('ERROR: Discount Rate has to be a number!!!')
                                                            new_rate = None
                                            elif customer.customer_type == 'R':
                                                new_rate = float(input('Please enter the new rate: '))
                                                customer.discount_rate = new_rate
                                                input('Press enter to return to main menu\n')
                                                return
                                        else:
                                            raise OtherInputError
                                    except OtherInputError:
                                        print('ERROR: This customer cannot be found! Please re-enter another name')
                                        customer_search_value = None
                            else:
                                raise OtherInputError
                        except OtherInputError:
                            print('ERROR: Please only enter option 1 or 2!!!')
                            rate_type = None
                elif temp == 'n':
                    input('Press enter to return to main menu\n')
                    return
                else:
                    raise OtherInputError
            except OtherInputError:
                print('ERROR: Please only enter y or n (Case Sensitive)!!!')
                temp = None

    def order_display(self):
        product_name_list = []
        customer_name_list = []
        order_detail_list = []
        order_display = [[0 for i in range(len(self.records.products_list) + len(self.records.combos_list) + 1)] for j
                         in range(len(self.records.customers_list))]
        s = '{:15}' + '{:10}' * (len(self.records.products_list) + len(self.records.combos_list)) + '{:10}'
        s2 = '{:8}' + '{:10}' * (len(self.records.products_list) + len(self.records.combos_list)) + '{:10}'
        s3 = '{:2}' + '{:10}' * (len(self.records.products_list) + len(self.records.combos_list)) + '{:10}'
        s4 = '{:2}' + '{:10}' * (len(self.records.products_list) + len(self.records.combos_list)) + '{:10}'
        for product in self.records.products_list:
            product_name_list.append(product.ID)
        for combo in self.records.combos_list:
            product_name_list.append(combo.ID)
        for customer in self.records.customers_list:
            customer_name_list.append(customer.name)
        for order in self.records.orders_list:
            order_detail_list.append([customer_name_list.index(self.records.find_customers(order.customer).name),
                                      product_name_list.index(self.records.find_products(order.
                                                                                         product
                                                                                         ).ID),
                                      int(order.product_quantity), order.total_price])
        for a in range(len(order_display)):
            for i in range(len(order_detail_list)):
                if a == order_detail_list[i][0]:
                    order_display[a][len(order_display[a])-1] += order_detail_list[i][3]
                    for b in range(len(order_display[a])):
                        if b == order_detail_list[i][1]:
                            order_display[a][b] = order_display[a][b] + int(order_detail_list[i][2])
                            continue
                        elif b != order_detail_list[i][1]:
                            continue
                elif a != order_detail_list[i][0]:
                    continue
        print(s.format(" ", *product_name_list, 'TOTAL'))
        for i in range(len(customer_name_list)):
            print(s2.format(customer_name_list[i], *order_display[i]))
        order_count = [0 for i in range(len(self.records.products_list) + len(self.records.combos_list) + 1)]
        product_dictionary = {}
        for product in self.records.products_list:
            product_dictionary.update({product.ID: product.count})
        for i in product_dictionary.keys():
            order_count[product_name_list.index(i)] += int(product_dictionary.get(i))
        order_count[len(order_count)-1] = sum(order_count[0:len(order_count)-2])
        order_total_quantity = [sum(column) for column in zip(*order_display)]
        order_total_quantity[len(order_total_quantity)-1] = sum(order_total_quantity[0:len(order_count)-1])
        print('------------------------------------------------------------------------------'*len(product_name_list))
        print(s3.format('OrderNum', *order_count))
        print(s4.format('OrderQty', *order_total_quantity))
        input('Press enter to return to main menu\n')
        return

    @staticmethod
    def replenish():
        temp = None
        while temp is None:
            try:
                temp = str(input('Are you sure you want to update the stock of the product?!'
                                 ' This is no go back? [Eg: y/n]: ')).lower()
                if temp == 'y':
                    quantity_stock = None
                    while quantity_stock is None:
                        try:
                            quantity_stock = int(input('Please enter the quantity of the updated product stock: '))
                            for product in Records.products_list:
                                product.stock = quantity_stock
                            for combo in Records.combos_list:
                                combo.stock = quantity_stock
                            print('Product stock has been successfully updated')
                            input('Press enter to return to main menu\n')
                            return
                        except TypeError:
                            print('ERROR:The stock must be an integer number!!!')
                            quantity_stock = None
                elif temp == 'n':
                    input('Press enter to return to main menu\n')
                    return
                else:
                    raise OtherInputError
            except OtherInputError:
                print('ERROR: Please only enter y or n (Case Sensitive)!!!')
                temp = None

    @staticmethod
    def valuable_customer():
        """This method search in the current customer list for all the customers and add their name and the total
        amount they have ordered to a dictionary.
        The maximum value of all the keys in this dictionary can then be located using the max function."""
        valuable_customer_dictionary = {}
        for customer in Records.customers_list:
            valuable_customer_dictionary.update({customer.name: customer.total})
        search_value = max(valuable_customer_dictionary.values())
        for name, value in valuable_customer_dictionary.items():
            if value == search_value:
                search_name = name
                print('The current most valuable customer is', search_name, 'with a total order value of $',
                      search_value)
        input('Press enter to return to main menu\n')
        return

    def popular_product(self):
        popular_product_dictionary = {}
        for product in self.records.products_list:
            popular_product_dictionary.update({product.name: product.count})
        search_value = max(popular_product_dictionary.values())
        for name, count in popular_product_dictionary.items():
            if count == search_value:
                search_name = name
                print('The current most popular product is', search_name, 'with a total time of order of',
                      search_value, ' times')
        input('Press enter to return to main menu\n')
        return


if __name__ == '__main__':
    print('Welcome to assignment 2')
    if len(sys.argv) != 1 and len(sys.argv) != 3:
        """The 1st arguement go into the command line is the name of the python file.
        The 2nd and 3rd arguement that go into the command line is the name of the 2 .txt files
        So, in total we have 3 files. If the python file is called by itself default file will be used."""
        print("ERROR: This program only accept 2 files from the command line!!!"
              "This program will search for 2 files:  "
              "Usage: theScript.py customerFile.txt productFile.txt"
              "if no file were provided the program will use default files")
        sys.exit(0)
    elif len(sys.argv) == 3:
        records = Records()
        if os.stat(sys.argv[1]).st_size != 0:
            records.read_customers(str(sys.argv[1]))
        if os.stat(sys.argv[2]).st_size != 0:
            records.read_products(str(sys.argv[2]))
        else:
            print('Product file cannot be empty')
            sys.exit()
        operation = Operations()
        records.save_customers(str(sys.argv[1]))
        records.save_products(str(sys.argv[2]))
    elif len(sys.argv) == 1:
        records = Records()
        if os.stat('customers.txt').st_size != 0:
            records.read_customers('customers.txt')
        if os.stat('products.txt').st_size != 0:
            records.read_products('products.txt')
        else:
            print('Product file cannot be empty')
            sys.exit()
        operation = Operations()
        records.save_customers('customers.txt')
        records.save_customers('products.txt')
