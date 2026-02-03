import higher_or_lower_art_17 as hla, higher_or_lower_data_17 as datafile
import random

print(hla.logo)

print(
    "Let's play Higher Lower game. You need to compare the popularity of 2 famous people or entities."
)
print(
    "(popularity defined by their followers count on Instagram platform, in millions)"
)

## print(datafile.data)

a = random.choice(datafile.data)
b = random.choice(datafile.data)
# print(a)
# print(a["name"])


def pair():
    print(f"Compare A: {a["name"]}, a {a["description"]}, from {a["country"]}.")
    # print(f"{a["name"]}, {a["follower_count"]}")
    print(hla.vs)
    print(f"Against B: {b["name"]}, a {b["description"]}, from {b["country"]}.")
    # print(f"{b["name"]}, {b["follower_count"]}")


pair()

score = 0
playing = True

while playing:
    reply = input("Who has more followers? Type 'A' or 'B': ").upper()
    if (reply == "A" and a["follower_count"] >= b["follower_count"]) or (
        reply == "B" and a["follower_count"] < b["follower_count"]
    ):
        score += 1
        if reply == "A" and a["follower_count"] > b["follower_count"]:
            a = a
            b = random.choice(datafile.data)
        elif reply == "B" and a["follower_count"] < b["follower_count"]:
            a = b
            b = random.choice(datafile.data)
        if a == b:
            b = random.choice(datafile.data)
        reply = pair()
    elif reply not in ("A", "B"):
        print("Invalid entry. Only type 'A' or 'B': ")
    else:
        print(f"That's wrong, you lost. Final score: {score}")
        playing = False
        break
