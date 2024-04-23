import datetime

from Pyro5.api import behavior, Daemon, expose, serve


@expose
@behavior(instance_mode='single')
class rental(object):

    def __init__(self):
        self.users = []
        self.manufacturers = []
        self.rental_cars = [] 
        self.rented_cars = [] 


    # task 1
    def add_user(self, user_name, user_number):
        user = {'name': user_name, 
                'number': user_number, 
                'car': None,
                'history': []
                }
        if user in self.users or self.__get_user(user_name) != None:
            return 0
        else:
            self.users.append(user)
            return 1
  

    # task 2
    def return_users(self):
        result = 'Users:\n'
        if self.users:
            for user in self.users:
                result += 'name: ' + user['name'] + ', phone number: ' + user['number'] + '\n'
        else:
            result += 'None\n'        
        return result    
    

    # task 3
    def add_manufacturer(self, manufacturer_name, manufacturer_country):
        manufacturer = {'name': manufacturer_name, 
                        'country': manufacturer_country
                        }
        if manufacturer in self.manufacturers or self.__get_manufacturer(manufacturer_name) != None:
            return 0
        else:
            self.manufacturers.append(manufacturer)
            return 1
        

    # task 4  
    def return_manufacturers(self):
        result = 'Manufacturers:\n'
        if self.manufacturers:
            for manu in self.manufacturers:
                result += 'name: ' + manu['name'] + ', country: ' + manu['country'] + '\n'
        else:
            result += 'None\n'   
        return result    


    # task 5
    def add_rental_car(self, manufacturer_name, car_model):
        car = {'manu': manufacturer_name, 
               'model': car_model,
               'rented': None
               }
        self.rental_cars.append(car)
        return car


    # task 6
    def return_cars_not_rented(self):
        result = 'Cars available:\n'
        if self.rental_cars:
            for car in self.rental_cars:
                result += 'manufacturer: ' + car['manu'] + ', model: ' + car['model'] + '\n'
        else:
            result += 'None\n'  
        return result


    # task 7
    def rent_car(self, user_name, car_model, year, month, day):
        # check input
        if year <= 0 or month <= 0 or day <= 0 or month > 12 or day > 31:
            # print('Please check the input of date!')
            return 0
        
        user = self.__get_user(user_name)
        start_time = datetime.date(year=year, month=month, day=day)
        car = self.__get_rental_car(car_model)
        if user == None:
            # print('There is no such a user in database.')
            return 0
        elif car == None:
            # print('There is no such a car in database.')
            return 0
        elif car['rented'] != None:
            # print('Sorry, all the cars with this model has been rented out.')
            return 0
        else:
            car['rented'] = start_time
            user['car'] = car_model
            self.rental_cars.remove(car)
            self.rented_cars.append(car)
            return 1
        

    # task 8
    def return_cars_rented(self):
        result = 'Cars rented:\n'
        if self.rented_cars:
            for car in self.rented_cars:
                result += 'manufacturer: ' + car['manu'] + ', model: ' + car['model'] + '\n'
        else:
            result += 'None\n'          
        return result
    
    
    # task 9
    def end_rental(self, user_name, car_model, year, month, day):
        # check input
        if year <= 0 or month <= 0 or day <= 0 or month > 12 or day > 31:
            # print('Please check the input of date!')
            return 0
        
        user = self.__get_user(user_name)
        end_time = datetime.date(year=year, month=month, day=day)
        car = self.__get_rented_car(car_model)
        start_time = car['rented']
        if user == None:
            # print('There is no such a user in database.')
            return 0
        elif car == None:
            # print('There is no such a car in database.')
            return 0
        elif start_time == None:
            # print('Sorry, all the cars with this model hasn't been rented out.')
            return 0
        elif user['car'] != car_model:
            # print('Sorry, the car user returing is not the rented car ')
            return 0
        else:
            car['rented'] = None
            user['car'] = None
            user['history'].append({'manu': car['manu'],
                                    'model': car['model'],
                                    'start': start_time,
                                    'end': end_time
                                    })
            self.rented_cars.remove(car)
            self.rental_cars.append(car)
            return 1
        

    # task 10
    def delete_car(self, car_model):
        car = self.__get_rental_car(car_model)
        if not car:
            return 0
        elif car['rented'] != None:
            return 0
        else:
            self.rental_cars.remove(car)
            return 1
        

    # task 11
    def delete_user(self, user_name):
        user = self.__get_user(user_name)
        if len(user['history']) == 0:
            self.users.remove(user)
            return 1
        else:
            return 0
        
        
    # task 12
    def user_rental_date(self, user_name, start_year, start_month, start_day, end_year, end_month, end_day):
        user = self.__get_user(user_name)
        start_time = datetime.date(year=start_year, month=start_month, day=start_day)
        end_time = datetime.date(year=end_year, month=end_month, day=end_day)
        records = user['history']
        history_result = 'Record of User ' + user_name + ':\n'
        for record in records:
            if record['start'] >= start_time and record['end'] <= end_time:
                history_result += record['manu'] + ' - ' + record['model'] + ' from ' + str(record['start']) + ' to ' + str(record['end']) + '\n'
        if history_result == 'Record of User ' + user_name + ':\n':        
            return history_result + 'None\n'
        else:
            return history_result        


    #############################################################################################

  
    def __get_user(self, name):
        for user in self.users:
            if user['name'] == name:
                return user
        return None
    
    def __get_rental_car(self, model):
        for car in self.rental_cars:
            if car['model'] == model:
                return car
        return None    
    
    def __get_manufacturer(self, name):
        for manufacturer in self.manufacturers:
            if manufacturer['name'] == name:
                return manufacturer
        return None    
    
    def __get_rented_car(self, model):
        for car in self.rented_cars:
            if car['model'] == model:
                return car
        return None  


daemon = Daemon()
serve({rental: 'example.rental'}, daemon=daemon, use_ns=True)

#if __name__ == '__main__': 
#    main()