class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def display_details(self):
        print(f"{self.year} {self.make} {self.model}")

    def start(self):
        print(f"{self.year} {self.make} {self.model} is staring...")

car1 = Car("Toyota", "Corolla", 2020)
car2 = Car("Honda", "Civic", 2022)

car1.display_details()
car1.start()

# car2.display_details()
# car2.start()