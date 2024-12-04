import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import prover  

gui = tk.Tk()
gui.geometry("800x500")
gui.configure(bg="#c3b5df")

# Keep track of the current question index and score
current_question_index = 0
score = 0

# Define a list of questions and their corresponding functions
questions = [
    ("Princesses and Tigers", "A prisoner is given by the King holding him the opportunity to improve his situation if he solves a puzzle.\n"
        "He is told there are three rooms in the castle: one room contains a lady and the other two contain a tiger each.\n"
        "If the prisoner opens the door to the room containing the lady, he will marry her and get a pardon. \n"
        "If he opens a door to a tiger room though, he will be eaten alive. Of course the prisoner wants to get married and be set free than being eaten alive.\n"
        "The door of each room has a sign bearing a statement that may be either true or false.\n"
        "The sign on the door of the room containing the lady is true and at least one of the signs on the doors of the rooms containing tigers is false. The signs say respectively:\n"
        "The sign on the door 1: there is a tiger in room 2.\n"           
        "The sign on the door 2: there is a tiger in this room.\n"                    
        "The sign on the door 3: there is a tiger in room 1.\n"                    
        "In which room is the lady?\n"),  
    ("Curiosity killed the cat", "We know that:\n"
        "1. Everyone who loves all animals is loved by someone.\n" 
        "2. Anyone who kills an animal is loved by no one.\n"
        "3. Jack loves all animals.\n"
        "4. Either Jack or Curiosity killed the cat, who is named Tuna.\n"
        "5. Cats are animals.\n"
        "Who killed the cat?\n"),  
    ("Einstein's Riddle", "There are five houses in a row: a, b, c, d and e. Each has a different color (red, green, yellow, blue, white) and an owner of different nationality. The owners have different pets, smoke a certain brand of cigar and prefer different drinks. We know that:\n"
        "1. The Brit lives in the red house.\n" 
        "2. The Swede keeps dogs as pets.\n"
        "3. The Dane drinks tea.\n"
        "4. The green house is on the immediate left of the white house.\n"
        "5. The green house's owner drinks coffee.\n"
        "6. The owner who smokes Pall Mall rears birds.\n"
        "7. The owner of the yellow house smokes Dunhill.\n"
        "8. The owner living in the center house drinks milk.\n"
        "9. The Norwegian lives in the first house.\n"
        "10. The owner who keeps the horse lives next to the one who smokes Dunhill.\n"
        "11. The owner who smokes Blends lives next to the one who keeps cats.\n"
        "12. The owner who smokes Bluemasters drinks beer.\n"
        "13. The German smokes Prince.\n"
        "14. The Norwegian lives next to the blue house.\n"
        "15. The owner who smokes Blends lives next to the one who drinks water.\n"
        "Who owns the fish?\n"),  
    ("Inspector Beethoven III", "Handel has been killed and Beethoven is on the case. He has interviewed the four suspects and their statements are shown below.\n"
        "Each suspect has said two sentences. One sentence of each suspect is a lie and one sentence is the truth. Help Beethoven figure out who the killer is.\n"
        "Joplin: I did not kill Handel. Either Grieg is the killer or none of us is.\n" 
        "Grieg: I did not kill Handel. Gershwin is the killer.\n"
        "Strauss: I did not kill Handel. Grieg is lying when he says Gershwin is the killer.\n"
        "Gershwin: I did not kill Handel. If Joplin did not kill him, then Grieg did.\n"
        "Who is the killer?\n"), 
    ("Mr. Froopaloop's Fiance", "Hans Ernest Froopaloop, Jr. will marry one of three women: Audrey, Brenda, and Charlotte. Here are some facts:\n"
        "1. Of Audrey and Brenda:\n"
        "a. Either they both have blue eyes or neither has blue eyes.\n"
        "b. One has red hair and the other does not.\n"
        "2. Of Audrey and Charlotte:\n"
        "a. Either they both have red hair or neither has red hair.\n"
        "b. One is 5'11'' and the other is not.\n"
        "3. Of Brenda and Charlotte:\n"
        "a. One has blue eyes and the other does not.\n"
        "b. One is 5'11'' and the other is not.\n"
        "4. Of the three characteristics; blue eyes, red hair and 5'11'':\n"
        "a. If any of the three women has exactly two of the three characteristics, Mr. Froopaloop will marry the one with the least number of characteristics.\n"
        "b. If any of the three women has exactly one of the three characteristics, Mr. Froopaloop will marry the one with the greatest number of characteristics.\n"
        "Who will Mr. Froopaloop marry?\n"), 
    ("Family murder", "A crime took place in Alice's family, you know the following:\n"
        "Alice, Alice’s husband, their son, their daughter, and Alice’s brother were involved in a murder. One of the five killed one of the other four. The following facts refer to the five people mentioned:\n"
        "1. A man and a woman were together in a bar at the time of the murder.\n"
        "2. The victim and the killer were together on a beach at the time of the murder.\n"
        "3. One of Alice’s two children was alone at the time of the murder.\n"
        "4. Alice and her husband were not together at the time of the murder.\n"
        "5. The victim’s twin was not the killer.\n"
        "6. The killer was younger than the victim.\n"
        "Which one of the five was the victim?\n")  
]

def startPage():
    for widget in gui.winfo_children():
        widget.destroy()

    image_path = "/mnt/c/Users/hozas/OneDrive/De toate/facultate/AI/quiz-game/quiz.jpg"  

    try:
        background_image = Image.open(image_path)  # Try loading the image
        background_image = background_image.resize((800, 500), Image.Resampling.LANCZOS)  # Resize the image to fit the window
        bg_image = ImageTk.PhotoImage(background_image)  # Convert the image for Tkinter
    except Exception as e:
        print("Error loading image:", e)
        background_image = None  # Set it to None if there is an issue with loading the image

    if background_image:
        # Create a label to hold the background image
        background_label = tk.Label(gui, image=bg_image)
        background_label.place(relwidth=1, relheight=1)  # Set the background label to cover the entire window
    else:
        # Set a default background color if the image cannot be loaded
        gui.configure(bg="#d4c7cd")

    # Create a frame to hold the title and button with a common background
    frame = tk.Frame(gui, bg="#ad8cef", padx=20, pady=20)  
    frame.pack(pady=(150, 50))  

    # Title label inside the frame
    title = tk.Label(frame, text="Quiz Game", font=('Helvetica bold', 48), fg="white", bg="#ad8cef", bd=0)
    title.pack(pady=10)  

    # Start button inside the frame
    startGameButton = tk.Button(frame, text="Start", command=lambda: chooseQuestion(), fg="white", bg="#ad8cef", width=20, height=2)
    startGameButton.pack(pady=20) 
    gui.mainloop()

def chooseQuestion():
    global current_question_index
    current_question_index = 0  # Reset question index
    
    for widget in gui.winfo_children():
        widget.destroy()

    frame = tk.Frame(gui, bg="#c3b5df")
    frame.pack(pady=20)

    title = tk.Label(frame, text="Choose a Question", font=('Helvetica bold', 24), fg="#6f2bae", bg="#c3b5df")
    title.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    for idx, (description, _) in enumerate(questions):
        row = 1 + idx // 2
        column = idx % 2
        questionBtn = tk.Button(frame, text=description, fg="white", bg="#8b5ebf", width=25, height=2, command=lambda idx=idx: questionPage(idx))
        questionBtn.grid(row=row, column=column, padx=20, pady=(10, 5))

    backButton = tk.Button(frame, text="Back", command=startPage, fg="white", bg="#8b5ebf", width=25, height=2)
    backButton.grid(row=(len(questions) + 1) // 2 + 1, column=0, columnspan =2, padx=20, pady=(10, 10))

def questionPage(question_index):
    global current_question_index
    current_question_index = question_index  # Update the current question index
    for widget in gui.winfo_children():
        widget.destroy()

    title = tk.Label(gui, text=f"Question {question_index + 1}: {questions[question_index][0]}", font=('Helvetica bold', 24), fg="#6f2bae", bg="#c3b5df")
    title.pack(pady=20)

    descriptionFrame = tk.Frame(gui, bg="#c3b5df")
    descriptionFrame.pack(pady=(10, 20), padx=10)

    questionDescription = tk.Text(descriptionFrame, wrap=tk.WORD, height=12, width=80, bg="#c3b5df", fg="#3f1269", font=('Helvetica', 12))
    questionDescription.insert(tk.END, questions[question_index][1])
    questionDescription.config(state=tk.DISABLED)
    questionDescription.pack()

    buttonFrame = tk.Frame(gui, bg="#c3b5df")
    buttonFrame.pack(pady=(10, 20))

    # Create answer buttons based on the question
    if question_index == 0:  # Princesses and Tigers
        room1Btn = tk.Button(buttonFrame, text="Room 1", fg="white", bg="#8b5ebf", width=10, height=2, command=lambda: [revealAnswer(prover.puzzle(1, 1))])
        room1Btn.grid(row=0, column=0, padx=10)
        room2Btn = tk.Button(buttonFrame, text="Room 2", fg="white", bg="#8b5ebf", width=10, height=2, command=lambda: [revealAnswer(prover.puzzle(1, 2))])
        room2Btn.grid(row=0, column=1, padx=10)
        room3Btn = tk.Button(buttonFrame, text="Room 3", fg="white", bg="#8b5ebf", width=10, height=2, command=lambda: [revealAnswer(prover.puzzle(1, 3))])
        room3Btn.grid(row=0, column=2, padx=10)

    elif question_index == 1:  # Curiosity killed the cat
        btn1 = tk.Button(buttonFrame, text="Jack", fg="white", bg="#8b5ebf", width=10, height=2, command=lambda: [revealAnswer(prover.puzzle(2, 1))])
        btn1.grid(row=0, column=0, padx=10)
        btn2 = tk.Button(buttonFrame, text="Curiosity", fg="white", bg="#8b5ebf", width=10, height=2, command=lambda: [revealAnswer(prover.puzzle(2, 2))])
        btn2.grid(row=0, column=1, padx=10)

    elif question_index == 2:  # Einstein's Riddle
        btn1 = tk.Button(buttonFrame, text="The Brit", fg="white", bg="#8b5ebf", width=10, height=2, command=lambda: [revealAnswer(prover.puzzle(3, 1))])
        btn1.grid(row=0, column=0, padx=10)
        btn2 = tk.Button(buttonFrame, text="The Swede", fg="white", bg="#8b5ebf", width=10, height=2, command=lambda: [revealAnswer(prover.puzzle(3, 2))])
        btn2.grid(row=0, column=1, padx=10)
        btn3 = tk.Button(buttonFrame, text="The Dane", fg="white", bg="#8b5ebf", width=10, height=2, command=lambda: [revealAnswer(prover.puzzle(3, 3))])
        btn3.grid(row=0, column=2, padx=10)
        btn4 = tk.Button(buttonFrame, text="The Norwegian", fg="white", bg="#8b5ebf", width=10, height=2, command=lambda: [revealAnswer(prover.puzzle(3, 4))])
        btn4.grid(row=0, column=3, padx=10)
        btn5 = tk.Button(buttonFrame, text="The German", fg="white", bg="#8b5ebf", width=10, height=2, command=lambda: [revealAnswer(prover.puzzle(3, 5))])
        btn5.grid(row=0, column=4, padx=10)

    elif question_index == 3:  # Inspector Beethoven III
        btn1 = tk.Button(buttonFrame, text="Joplin", fg="white", bg="#8b5ebf", width=10, height=2, command=lambda: [revealAnswer(prover.puzzle(4, 1))])
        btn1.grid(row=0, column=0, padx=10)
        btn2 = tk.Button(buttonFrame, text="Grieg", fg="white", bg="#8b5ebf", width=10, height=2, command=lambda: [revealAnswer(prover.puzzle(4, 2))])
        btn2.grid(row=0, column=1, padx=10)
        btn3 = tk.Button(buttonFrame, text="Strauss", fg="white", bg="#8b5ebf", width=10, height=2, command=lambda: [revealAnswer(prover.puzzle(4, 3))])
        btn3.grid(row=0, column=2, padx=10)
        btn4 = tk.Button(buttonFrame, text="Gershwin", fg="white", bg="#8b5ebf", width=10, height=2, command=lambda: [revealAnswer(prover.puzzle(4, 4))])
        btn4.grid(row=0, column=3, padx=10)

    elif question_index == 4:  # Mr. Froopaloop's Fiance
        btn1 = tk.Button(buttonFrame, text="Audrey", fg="white", bg="#8b5ebf", width=10, height=2, command=lambda: [revealAnswer(prover.puzzle(5, 1))])
        btn1.grid(row=0, column=0, padx=10)
        btn2 = tk.Button(buttonFrame, text="Charlotte", fg="white", bg="#8b5ebf", width=10, height=2, command=lambda: [revealAnswer(prover.puzzle(5, 2))])
        btn2.grid(row=0, column=1, padx=10)
        btn3 = tk.Button(buttonFrame, text="Brenda", fg="white", bg="#8b5ebf", width=10, height=2, command=lambda: [revealAnswer(prover.puzzle(5, 3))])
        btn3.grid(row=0, column=2, padx=10)

    elif question_index == 5:  # Family murder
        btn1 = tk.Button(buttonFrame, text="Alice", fg="white", bg="#8b5ebf", width=10, height=2, command=lambda: [revealAnswer(prover.puzzle(6, 1))])
        btn1.grid(row=0, column=0, padx=10)
        btn2 = tk.Button(buttonFrame, text="Alice's husband", fg="white", bg="#8b5ebf", width=10, height=2, command=lambda: [revealAnswer(prover.puzzle(6, 2))])
        btn2.grid(row=0, column=1, padx=10)
        btn3 = tk.Button(buttonFrame, text="Alice's son", fg="white", bg="#8b5ebf", width=10, height=2, command=lambda: [revealAnswer(prover.puzzle(6, 3))])
        btn3.grid(row=0, column=2, padx=10)
        btn4 = tk.Button(buttonFrame, text="Alice's daughter", fg="white", bg="#8b5ebf", width=10, height=2, command=lambda: [revealAnswer(prover.puzzle(6, 4))])
        btn4.grid(row=0, column=3, padx=10)
        btn5 = tk.Button(buttonFrame, text="Alice's brother", fg="white", bg="#8b5ebf", width=10, height=2, command=lambda: [revealAnswer(prover.puzzle(6, 5))])
        btn5.grid(row=0, column=4, padx=10)

    # Add Back and Next buttons
    actionButtonFrame = tk.Frame(gui, bg="#c3b5df")
    actionButtonFrame.pack(pady=20)

    backButton = tk.Button(actionButtonFrame, text="Back", command=chooseQuestion, fg="white", bg="#8b5ebf", width=10, height=2)
    backButton.grid(row=0, column=0, padx=10)

    nextButton = tk.Button(actionButtonFrame, text="Next", command=goToNextQuestion, fg="white", bg="#8b5ebf", width=10, height=2)
    nextButton.grid(row=0, column=1, padx=10)

def goToNextQuestion():
    global current_question_index
    current_question_index += 1
    if current_question_index < len(questions):
        questionPage(current_question_index)
    else:
        showScore()

def revealAnswer(answer):
    global score
    for widget in gui.winfo_children():
        widget.destroy()

    revealFrame = tk.Frame(gui, bg="#c3b5df")
    revealFrame.pack(pady=50)

    label1 = tk.Label(revealFrame, text="Your answer is:", font=('Helvetica bold', 20), fg="#6f2bae", bg="#c3b5df")
    label1.pack(pady=(0, 20))

    resultLabel = tk.Label(revealFrame, text="CORRECT" if answer else "WRONG", font=('Helvetica bold', 20), fg="green" if answer else "#b80f0a", bg="#c3b5df")
    resultLabel.pack(pady=(0, 20))

    # Update score if the answer is correct
    if answer:
        score += 1

    # Add Back and Next buttons
    actionButtonFrame = tk.Frame(gui, bg="#c3b5df")
    actionButtonFrame.pack(pady=20)

    backButton = tk.Button(actionButtonFrame, text="Back", command=lambda: questionPage(current_question_index), fg="white", bg="#8b5ebf", width=10, height=2)
    backButton.grid(row=0, column=0, padx=10)

    nextButton = tk.Button(actionButtonFrame, text="Next", command=goToNextQuestion, fg="white", bg="#8b5ebf", width=10, height=2)
    nextButton.grid(row=0, column=1, padx=10)

def showScore():
    for widget in gui.winfo_children():
        widget.destroy()

    scoreFrame = tk.Frame(gui, bg="#c3b5df")
    scoreFrame.pack(pady=50)

    scoreLabel = tk.Label(scoreFrame, text=f"Your final score is: {score}/{len(questions)}", font=('Helvetica bold', 24), fg="#6f2bae", bg="#c3b5df")
    scoreLabel.pack(pady=(0, 20))

    backButton = tk.Button(scoreFrame, text="Back to Start", command=startPage, fg="white", bg="#8b5ebf", width=20, height=2)
    backButton.pack(pady=20)

if __name__ == "__main__":
    startPage()