from sys import exit 


def main():
    # getting the valid card number input
    card = get_card_number()
    
    # check for Luhn’s Algorithm 
    checksum = luhn_checksum(card)
    
    # find out the type of credit card
    # checksum of Luhn’s Algorithm
    if checksum == 0:
        # first digit of the card number as a int
        first_dig = int(card[0])
        # first 2 digits of the card number as an int
        first_two_dig = int(card[:2])
        # validating for american express credit card
        if first_two_dig in [34, 37] and len(card) == 15:
            print("AMEX")
        # validating for master credit card
        elif first_two_dig in range(51, 56) and len(card) == 16:
            print("MASTERCARD")
        # validating for visa credit card
        elif first_dig == 4 and (13 <= len(card) and len(card) <= 16):
            print("VISA")
        # invalid if none of above is true
        else:
            print("INVALID")
    # remainder of checksum was not 0
    else:
        print("INVALID")

        
# prompting user for credit card untill the input is valid
def get_card_number():
    while True:
        try:
            card = input("Number: ")
            if len(card) > 0 and int(card):
                break
        except ValueError:
            continue
        except:
            exit(0)
    return card


# Luhn’s Algorithm
def luhn_checksum(card):
    # listing the digits of a number or string
    def list_digits(num):
        return [int(dig) for dig in str(num)]
    digs = list_digits(card)
    odd_digs = digs[-1::-2]
    even_digs = digs[-2::-2]
    checksum = 0
    checksum += sum(odd_digs)
    for i in even_digs:
        checksum += sum(list_digits(i*2))
    return checksum % 10


# calling main
main()