import coffee_machine_art_18 as cma
from menu_class_19 import MenuItem, Menu
from coffee_maker_class_19 import CoffeeMaker
from money_machine_class_19 import MoneyMachine

print(cma.logo2, cma.logo)

MENU = Menu()
coffee_maker = CoffeeMaker()
# instead of previous 'resources'. ask the coffee maker the report / if resources sufficient / to make coffee
money_machine = MoneyMachine()

while True:
    choice = input(f"Please select your drink: {MENU.get_items()}: ")
    drink = MENU.find_drink(choice)
    if choice == "report":
        coffee_maker.report()
        money_machine.report()
    elif choice == "off":
        print("Shutting machine down...")
        break
    elif drink is None:
        print("Invalid input.")
        continue
    else:
        if coffee_maker.is_resource_sufficient(drink):
            print(f"The cost is ${drink.cost}. Please insert coins.")
            money_machine.make_payment
            if money_machine.make_payment(drink.cost) == False:
                print("Insufficient funds. Refunding the money.")
                continue
            coffee_maker.make_coffee(drink)
