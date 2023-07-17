from cs50 import get_int
# prompting the user for the half-height 
# waiting for the user to insert a valid input  (inclusively between 1 and 8)
while True:
    height = get_int("Height: ")
    if height in range(1, 9):
        break
# printing the half-pyramids
for i in range(height):
    print((height-1-i) * " " + (i+1) * "#" + "  " + (i+1) * "#")
