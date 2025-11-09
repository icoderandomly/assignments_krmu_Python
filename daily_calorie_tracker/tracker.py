# tracker.py
# Name: Harsh Singh
# Roll No: 2501730400
# Date: 06-Nov-2025
# Project: Daily Calorie Tracker

print("Welcome to Daily Calorie Tracker!")
print("This program helps you keep track of your meals and calories.\n")

meal_names = []
meal_calories = []

meals = int(input("How many meals did you have today? "))

for i in range(meals):
    name = input("Enter meal name: ")
    cal = float(input("Enter calories for " + name + ": "))
    meal_names.append(name)
    meal_calories.append(cal)

total = sum(meal_calories)
average = total / meals

limit = float(input("\nEnter your daily calorie limit: "))

print("\n----Daily Report----")
print("Meal Name      Calories")

for i in range(meals):
    print(meal_names[i], "      ", meal_calories[i])

print("======================")
print("Total Calories:", total)
print("Average Calories:", average)

if total > limit:
    print("You have crossed your daily limit!")
else:
    print("You are within your daily limit!")
