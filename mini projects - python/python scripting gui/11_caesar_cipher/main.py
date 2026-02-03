import caesar_cipher_art_11 as ca

print(ca.logo)

alphabet = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]


def input_data():
    direction = ""
    while direction not in ("encode", "decode"):
        direction = input(
            "Type 'encode' to encrypt, type 'decode' to decrypt:\n"
        ).lower()

    if direction not in ("encode", "decode"):
        print("Wrong input. Please pick your action: encode or decode: ")

    text = input("Type your message:\n").lower()
    shift = int(input("Type the shift number:\n"))
    return (text, direction, shift)


def encrypt(text, shift):
    encoded_text = ""
    for letter in text:
        if letter in alphabet:
            old_letter_index = alphabet.index(letter)
            # print(old_letter_index)
            new_letter_index = old_letter_index + shift
            new_letter_index = new_letter_index % len(alphabet)
            # print(new_letter_index)
            new_letter = alphabet[new_letter_index]
        else:
            new_letter = letter
        encoded_text += new_letter

    # print(encoded_text)
    print(f"Entered text: {text}")
    print(f"Encoded text: {encoded_text}")


# encrypt(original_text = text, shift_amount = shift)


def decrypt(text, shift):
    decoded_text = ""
    for letter in text:
        if letter in alphabet:
            old_letter_index = alphabet.index(letter)
            # print(old_letter_index)
            new_letter_index = old_letter_index - shift
            new_letter_index = new_letter_index % len(alphabet)
            # print(new_letter_index)
            new_letter = alphabet[new_letter_index]
        else:
            new_letter = letter
        decoded_text += new_letter

    print(f"Entered encoded text: {text}")
    print(f"Decoded text: {decoded_text}")


# decrypt(original_text = text, shift_amount = shift)


def caesar():
    text, direction, shift = input_data()
    if direction == "encode":
        encrypt(text, shift)
    else:
        decrypt(text, shift)


caesar()

restart = "yes"
while restart == "yes":
    restart = input("Would you like to go again? Type 'yes' or 'no: ").lower()
    if restart == "yes":
        caesar()

if restart == "no":
    print("Thank you and goodbye!")
