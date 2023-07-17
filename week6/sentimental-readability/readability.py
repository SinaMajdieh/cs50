def main():
    # prompting the user for input text
    text = str(input("Text: "))
    # counting the letter
    letters = len([char for char in text if char.isalpha()])
    # counting words
    words = len(text.split())
    # counting sentences
    sentences = len([char for char in text if char == "." or char == "?" or char == "!"])
    # calculating oleman-Liau index
    L = (letters / words) * 100
    S = (sentences / words) * 100
    index = round(0.0588 * L - 0.296 * S - 15.8)
    # printing the results
    if index > 16:
        print("Grade 16+")
    elif index < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {index}")
   

main()