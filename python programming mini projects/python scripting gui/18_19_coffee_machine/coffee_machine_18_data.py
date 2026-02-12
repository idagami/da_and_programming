MENU = { # constant
    "espresso": {
        "ingredients": {
            "water": 50,
            "milk": 0, # TODO do not give error 
            #if certain ingredient missing in espresso
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {
    "water": 300,
    "milk": 300,
    "coffee": 150,
    "cups": 50,
}