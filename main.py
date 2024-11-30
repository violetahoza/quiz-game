import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import prover

gui = tk.Tk()
gui.geometry("800x500")
gui.configure(bg="#d4c7cd")

def startPage():
    for widget in gui.winfo_children():
        widget.destroy()

    # Center the title
    title = tk.Label(text="Quiz Game", font=('Helvetica bold', 48), fg="#40031e", bg="#d4c7cd")
    title.pack(pady=(150, 10))  # Padding above is 200, below is 10

    # Center the button
    startGameButton = tk.Button(text="Start", command=lambda: chooseQuestion(), fg="white", bg="#40031e", width=20, height=2)
    startGameButton.pack(pady=(10, 50))  # Padding above is 10, below is 50

    gui.mainloop()

def chooseQuestion():
    for widget in gui.winfo_children():
        widget.destroy()

    # Create a frame for question selection
    frame = tk.Frame(gui, bg="#d4c7cd")
    frame.pack(pady=20)

    # Add a title for the question selection
    title = tk.Label(frame, text="Choose a Question", font=('Helvetica bold', 24), fg="#40031e", bg="#d4c7cd")
    title.grid(row=0, column=0, columnspan=2, pady=(10, 20))  # Center title across two columns

    # Create buttons based on descriptions and attach commands
    questions = [
        ("Princesses and Tigers", questionPage1),
        ("Curiosity killed the cat", questionPage2),
        ("Einstein's Riddle", questionPage3),
    ]

    # Arrange buttons in a vertical list
    for idx, (description, command) in enumerate(questions):
        questionBtn = tk.Button(frame, text=description, fg="white", bg="#40031e", width=25, height=2, command=command)
        questionBtn.grid(row=1 + idx, column=0, padx=20, pady=(10, 5))  # Place buttons below the title

    # Back button at the end, same dimensions as question buttons
    backButton = tk.Button(frame, text="Back", command=startPage, fg="white", bg="#40031e", width=25, height=2)
    backButton.grid(row=len(questions) + 1, column=0, padx=20, pady=(10, 10))  # Place back button below all question buttons

    gui.mainloop()

def questionPage1():
    for widget in gui.winfo_children():
        widget.destroy()

    # Title for the question
    title = tk.Label(gui, text="Question 1: Princesses and Tigers", font=('Helvetica bold', 24), fg="#40031e", bg="#d4c7cd")
    title.pack(pady=20)

    # Create a frame for the question description
    descriptionFrame = tk.Frame(gui, bg="#d4c7cd")
    descriptionFrame.pack(pady=(10, 20), padx=10)

    # Create a Text widget for the question description
    questionDescription = tk.Text(descriptionFrame, wrap=tk.WORD, height=12, width=80, bg="#f0f0f0", fg="#40031e", font=('Helvetica', 12)) 
    questionDescription.insert(tk.END, 
        "A prisoner is given by the King holding him the opportunity to improve his situation if he solves a puzzle.\n"
        "He is told there are three rooms in the castle: one room contains a lady and the other two contain a tiger each.\n"
        "If the prisoner opens the door to the room containing the lady, he will marry her and get a pardon. \n"
        "If he opens a door to a tiger room though, he will be eaten alive. Of course the prisoner wants to get married and be set free than being eaten alive.\n"
        "The door of each room has a sign bearing a statement that may be either true or false.\n"
        "The sign on the door of the room containing the lady is true and at least one of the signs on the doors of the rooms containing tigers is false. The signs say respectively:\n"
        "The sign on the door 1: there is a tiger in room 2.\n"           
        "The sign on the door 2: there is a tiger in this room.\n"                    
        "The sign on the door 3: there is a tiger in room 1.\n"                    
        "In which room is the lady?\n"
    )
    questionDescription.config(state=tk.DISABLED)  # Make the Text widget read-only
    questionDescription.pack()

    # Create a frame for the room buttons
    buttonFrame = tk.Frame(gui, bg="#d4c7cd")
    buttonFrame.pack(pady=(10, 20))  # Add some padding above and below the button frame

    # Room buttons in the same row
    room1Btn = tk.Button(buttonFrame, text="Room 1", fg="white", bg="#40031e", width=10, height=2, command=lambda: [revealAnswer(prover.puzzle(1, 1))])
    room1Btn.grid(row=0, column=0, padx=10)  # Button for Room 1
    room2Btn = tk.Button(buttonFrame, text="Room 2", fg="white", bg="#40031e", width=10, height=2,  command=lambda: [revealAnswer(prover.puzzle(1, 2))])
    room2Btn.grid(row=0, column=1, padx=10)  # Button for Room 2
    room3Btn = tk.Button(buttonFrame, text="Room 3", fg="white", bg="#40031e", width=10, height=2,  command=lambda: [revealAnswer(prover.puzzle(1, 3))])
    room3Btn.grid(row=0, column=2, padx=10)  # Button for Room 3

    backButton = tk.Button(gui, text="Back", command=chooseQuestion, fg="white", bg="#40031e", width=10, height=2)  
    backButton.pack(pady=20)  

    gui.mainloop()

def questionPage2():
    for widget in gui.winfo_children():
        widget.destroy()

    # Title for the question
    title = tk.Label(gui, text="Question 2: Curiosity killed the cat", font=('Helvetica bold', 24), fg="#40031e", bg="#d4c7cd")
    title.pack(pady=20)

    # Create a frame for the question description
    descriptionFrame = tk.Frame(gui, bg="#d4c7cd")
    descriptionFrame.pack(pady=(10, 20), padx=10)

    # Create a Text widget for the question description
    questionDescription = tk.Text(descriptionFrame, wrap=tk.WORD, height=12, width=80, bg="#f0f0f0", fg="#40031e", font=('Helvetica', 12)) 
    questionDescription.insert(tk.END, 
        "We know that:\n"
        "1. Everyone who loves all animals is loved by someone.\n" 
        "2. Anyone who kills an animal is loved by no one.\n"
        "3. Jack loves all animals.\n"
        "4. Either Jack or Curiosity killed the cat, who is named Tuna.\n"
        "5. Cats are animals.\n"
        "Who killed the cat?\n"
    )
    questionDescription.config(state=tk.DISABLED)  # Make the Text widget read-only
    questionDescription.pack()

    # Create a frame for the room buttons
    buttonFrame = tk.Frame(gui, bg="#d4c7cd")
    buttonFrame.pack(pady=(10, 20))  # Add some padding above and below the button frame

    btn1 = tk.Button(buttonFrame, text="Jack", fg="white", bg="#40031e", width=10, height=2, command=lambda: [revealAnswer(prover.puzzle(2, 1))])
    btn1.grid(row=0, column=0, padx=10)
    btn2 = tk.Button(buttonFrame, text="Curiosity", fg="white", bg="#40031e", width=10, height=2,  command=lambda: [revealAnswer(prover.puzzle(2, 2))])
    btn2.grid(row=0, column=1, padx=10)  
    backButton = tk.Button(gui, text="Back", command=chooseQuestion, fg="white", bg="#40031e", width=10, height=2)  
    backButton.pack(pady=20)  

    gui.mainloop()

def questionPage3():
    for widget in gui.winfo_children():
        widget.destroy()

    gui.mainloop()

def revealAnswer(answer):
    for widget in gui.winfo_children():
        widget.destroy()

    # Create a frame for the reveal answer page
    revealFrame = tk.Frame(gui, bg="#d4c7cd")
    revealFrame.pack(pady=50)  # Center the frame with padding

    # Title for the answer reveal
    label1 = tk.Label(revealFrame, text="Your answer is:", font=('Helvetica bold', 20), fg="#40031e", bg="#d4c7cd")
    label1.pack(pady=(0, 20))  # Add padding below

    # Display whether the answer is correct or wrong
    resultLabel = tk.Label(revealFrame, text="CORRECT" if answer else "WRONG", font=('Helvetica bold', 20), fg="#40031e", bg="#d4c7cd")
    resultLabel.pack(pady=(0, 20))  # Add padding below

    # Create a back button for navigation
    backButton = tk.Button(revealFrame, text="Back", command=chooseQuestion, fg="white", bg="#40031e", width=15, height=2)
    backButton.pack(pady=20)  # Add padding below the button

    gui.mainloop()

if __name__ == "__main__":
    startPage()