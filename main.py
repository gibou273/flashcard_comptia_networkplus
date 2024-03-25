from tkinter import Tk, Canvas, PhotoImage, Label, Button
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"


acronyms_to_learn = []
current_item = {}

try:
    with open("data/acronyms_to_learn.csv", "r") as file:
        content = file.readlines()
except FileNotFoundError:
    with open("data/acronyms.csv", "r") as file:
        content = file.readlines()
finally:
    for data in content:
        line = data.split(",")
        new_item = {
            "Abbreviation": line[0],
            "Meaning": line[1].strip()
        }
        acronyms_to_learn.append(new_item)


def next_card():
    global current_item
    global timer_to_flip_card
    screen.after_cancel(timer_to_flip_card)  # Resets timer back to zero every time you go to a new card
    current_item = random.choice(acronyms_to_learn)
    abbreviation_word = current_item["Abbreviation"]
    canvas.itemconfig(title_text, text="Abbreviation", fill="black")
    canvas.itemconfig(abbreviation_text, text=abbreviation_word, fill="black")
    canvas.itemconfig(card_background, image=img_card_front)
    timer_to_flip_card = screen.after(3000, func=flip_the_card)  # set up a new timer to wait for 3 seconds


def flip_the_card():
    abbreviation_meaning = current_item["Meaning"]
    canvas.itemconfig(title_text, text="Meaning", fill="white")
    canvas.itemconfig(abbreviation_text, text=abbreviation_meaning, fill="white")
    canvas.itemconfig(card_background, image=img_card_back)


def remove_known_acronym():
    global current_item
    acronyms_to_learn.remove(current_item)
    unknown_acronyms = pandas.DataFrame(acronyms_to_learn)
    unknown_acronyms.to_csv("data/acronyms_to_learn.csv", index=False)
    next_card()


screen = Tk()
screen.title("Flashcard - CompTIA Security+ Acronyms")
screen.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
# Flip the card after a given amount of seconds
timer_to_flip_card = screen.after(3000, func=flip_the_card)

canvas = Canvas(width=800, height=526)
img_card_front = PhotoImage(file="images/card_front.png")
img_card_back = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=img_card_front)
title_text = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
abbreviation_text = canvas.create_text(400, 263, text="", font=("Ariel", 20, "italic"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# unknown button
unknown_image = PhotoImage(file="images/wrong.png")
button_unknown = Button(image=unknown_image, highlightthickness=0, command=next_card)
button_unknown.grid(row=1, column=0)
# Known button
known_image = PhotoImage(file="images/right.png")
button_known = Button(image=known_image, highlightthickness=0, command=remove_known_acronym)
button_known.grid(row=1, column=1)

next_card()

screen.mainloop()