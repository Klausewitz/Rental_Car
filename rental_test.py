import sys
import Pyro5.errors
from Pyro5.api import Proxy

# Check that the Python file rental.py exists.
import os.path
if(os.path.isfile("rental.py")==False):
	print("Error you need to call the Python file rental.py!")

# Check that the class is called rental. That is, the file rental.py contains the expression "rental(object):"
file_text = open('rental.py', 'r').read()
if("rental(object):" not in file_text):
	print("Error you need to call the Python class rental!")

sys.excepthook = Pyro5.errors.excepthook
rental_object = Proxy("PYRONAME:example.rental")

rental_object.add_user("Conor Reilly", "123456")
rental_object.add_user("Yunhan Liu", "234567")
rental_object.add_user("Muxun Zhao", "345678")
rental_object.add_user("Theywhy They", "114514")
print(rental_object.return_users())
rental_object.add_manufacturer("BMW", "Germany")
rental_object.add_manufacturer("KAMAZ", "Russia")
print(rental_object.return_manufacturers())
rental_object.add_rental_car("BMW", "3 Series")
rental_object.add_rental_car("BMW", "3 Series")
rental_object.add_rental_car("KAMAZ", "43114")
print(rental_object.return_cars_not_rented())
rental_object.rent_car("Conor Reilly", "3 Series", 2000, 3, 3)
rental_object.end_rental("Conor Reilly", "3 Series", 2000, 4, 4)
rental_object.rent_car("Conor Reilly", "3 Series", 2019, 1, 3)
rental_object.rent_car("Muxun Zhao", "43114", 2019, 1, 3)
print(rental_object.return_cars_rented())
rental_object.end_rental("Conor Reilly", "3 Series", 2019, 2, 4)
rental_object.delete_car("43114")
print(rental_object.return_cars_rented())
print(rental_object.return_cars_not_rented())
rental_object.end_rental("Muxun Zhao", "43114", 2019, 2, 5)
rental_object.delete_car("43114")
print(rental_object.return_cars_rented())
print(rental_object.return_cars_not_rented())
rental_object.delete_user("Conor Reilly")
rental_object.delete_user("Yunhan Liu")
print(rental_object.return_users())
rental_object.rent_car("Conor Reilly", "3 Series", 2019, 3, 3)
rental_object.end_rental("Conor Reilly", "3 Series", 2019, 4, 4)
rental_object.rent_car("Conor Reilly", "3 Series", 2219, 3, 3)
rental_object.end_rental("Conor Reilly", "3 Series", 2219, 4, 4)
print(rental_object.user_rental_date("Conor Reilly", 2010, 1, 1, 2029, 2, 1))
print(rental_object.user_rental_date("Theywhy They", 2010, 1, 1, 2029, 2, 1))
