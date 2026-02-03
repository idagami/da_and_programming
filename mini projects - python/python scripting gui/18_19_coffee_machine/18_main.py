import coffee_machine_art_18 as cma
import coffee_machine_18_data as data

MENU = data.MENU
resources = data.resources

print(cma.logo2, cma.logo)

cash = 0

while True:
    drink = input("Please select your drink: espresso / latte / cappuccino: ").lower()
    if drink == "report":
        print(f"Water: {resources['water']} ml")
        print(f"Milk: {resources['milk']} ml")
        print(f"Coffee: {resources['coffee']} g")
        print(f"Cups: {resources['cups']} pc")
        print(f"Money: ${cash}")
    elif drink == "off":
        print("Shutting machine down...")
        break
    elif drink not in ("cappuccino", "latte", "espresso", "report", "off"):
        print("Invalid input.")
        continue
    else:
        enough_resources = True

        for item in MENU[drink]["ingredients"]:
            if MENU[drink]["ingredients"][item] > resources[item]:
                print(f"Sorry, there isn't enough {item}.")
                enough_resources = False

        if not enough_resources or resources["cups"] < 1:
            if resources["cups"] < 1:
                print("Sorry, there are no cups left.")
            continue

        if enough_resources:
            print(f"The cost is ${MENU[drink]['cost']}. Please insert coins.")
            quarters = int(input("How many quarters entered: "))
            dimes = int(input("How many dimes entered: "))
            money_inserted = 0.25 * quarters + 0.1 * dimes
            if money_inserted < MENU[drink]["cost"]:
                print("Insufficient funds. Refunding the money.")
                continue
            # print(money_inserted)
            else:
                if money_inserted > MENU[drink]["cost"]:
                    change = round(money_inserted - MENU[drink]["cost"], 2)
                    print(f"Your change is ${change}")
            resources["water"] = (
                resources["water"] - MENU[drink]["ingredients"]["water"]
            )
            resources["milk"] = resources["milk"] - MENU[drink]["ingredients"]["milk"]
            resources["coffee"] = (
                resources["coffee"] - MENU[drink]["ingredients"]["coffee"]
            )
            resources["cups"] = resources["cups"] - 1
            cash = cash + MENU[drink]["cost"]
            print(f"Here is your {drink} \u2615. Enjoy!")
        else:
            for item in MENU[drink]["ingredients"]:
                if MENU[drink]["ingredients"][item] > resources[item]:
                    print(f"Sorry, there isn't enough {item}.")
