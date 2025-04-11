score = 0

print("Welcome to the Real Madrid Quiz!")

answer1 = input("1. In which year was Real Madrid founded? ")
if answer1 == "1902":
    print("Correct!")
    score += 1
else:
    print("Wrong! The correct answer is 1902.")

answer2 = input("2. Who is Real Madrid's all-time top scorer? ")
if answer2.lower() == "cristiano ronaldo":
    print("Correct!")
    score += 1
else:
    print("Wrong! The correct answer is Cristiano Ronaldo.")

answer3 = input("3. What is the name of Real Madrid’s home stadium? ")
if answer3.lower() == "santiago bernabeu":
    print("Correct!")
    score += 1
else:
    print("Wrong! The correct answer is Santiago Bernabeu.")

answer4 = input("4. How many UEFA Champions League titles has Real Madrid won (as of 2024)? ")
if answer4 == "15":
    print("Correct!")
    score += 1
else:
    print("Wrong! The correct answer is 15.")

answer5 = input("5. Who is the current manager of Real Madrid (2024)? ")
if answer5.lower() == "carlo ancelotti":
    print("Correct!")
    score += 1
else:
    print("Wrong! The correct answer is Carlo Ancelotti.")

print("You scored", score, "out of 5!")
