# ============================================================
# 1. FUNCTIONS
# ============================================================

# Calculate BMR
def calculate_bmr(weight, height, age, sex):
    if sex == "male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5

    elif sex == "female":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    else:
        raise ValueError(
            "Invalid sex entered. Please enter 'male' or 'female'."
        )

    return bmr


# Calculate TDEE
def calculate_tdee(bmr, activity_level):
    if activity_level == "sedentary":
        activity_factor = 1.2

    elif activity_level == "lightly active":
        activity_factor = 1.375

    elif activity_level == "moderately active":
        activity_factor = 1.55

    elif activity_level == "very active":
        activity_factor = 1.725

    else:
        raise ValueError(
            "Invalid activity level. Please enter "
            "'sedentary', 'lightly active', "
            "'moderately active', or 'very active'."
        )

    tdee = bmr * activity_factor

    return tdee


# Calculate calorie target based on goal
def calculate_calorie_target(goal, tdee):
    if goal == "Fat loss":
        calorie_target = tdee - 400

    elif goal == "Maintain weight":
        calorie_target = tdee

    elif goal == "Muscle gain":
        calorie_target = tdee + 250

    elif goal == "Recomposition":
        calorie_target = tdee - 200

    else:
        raise ValueError("Invalid goal.")

    return calorie_target


# Calculate macros
def calculate_macros(weight, target_calories):
    protein = weight * 2.0
    fat = weight * 0.8

    protein_calories = protein * 4
    fat_calories = fat * 9

    carb_calories = target_calories - protein_calories - fat_calories
    carbs = carb_calories / 4

    return protein, fat, carbs

if __name__ == "__main__":
            # ============================================================
            # 2. GET USER INPUT
            # ============================================================

            user_name = input("Enter your name: ")

            while True:
                try:
                    age = int(input("Enter your age: "))
                    if age > 0:
                        break
                    else:
                        print("Invalid input. Please enter a valid age.")

                except ValueError:
                    print("Invalid input. Please enter a valid age.")


            while True:
                try:
                    height = float(input("Enter your height in centimeters: "))
                    if height > 0:
                        break
                    else:
                        print("Invalid input. Please enter a valid height.")

                except ValueError:
                    print("Invalid input. Please enter a valid height.")


            while True:
                try:
                    weight = float(input("Enter your weight in kilograms: "))
                    if weight > 0:
                        break
                    else:
                        print("Invalid input. Please enter a valid weight.")

                except ValueError:
                    print("Invalid input. Please enter a valid weight.")


            while True:
                sex = input("Enter your sex (male/female): ")

                if sex in ["male", "female"]:
                    break

                else:
                    print("Invalid input. Please enter 'male' or 'female'.")


            while True:
                activity_level = input(
                    "Enter your activity level "
                    "(sedentary, lightly active, moderately active, very active): "
                )

                if activity_level in [
                    "sedentary",
                    "lightly active",
                    "moderately active",
                    "very active",
                ]:
                    break

                else:
                    print(
                        "Invalid input. Please enter 'sedentary', "
                        "'lightly active', 'moderately active', or 'very active'."
                    )


            # ============================================================
            # 3. CALCULATIONS
            # ============================================================

            # Calculate BMR
            bmr = calculate_bmr(weight, height, age, sex)

            print(
                f"\nHello {user_name}, your Basal Metabolic Rate (BMR) is: "
                f"{bmr:.0f} calories/day\n"
            )


            # Calculate TDEE
            tdee = calculate_tdee(bmr, activity_level)

            print(
                f"\n{user_name}, your estimated TDEE is: "
                f"{tdee:.0f} calories/day\n"
            )


            # ============================================================
            # 4. GOAL SELECTION
            # ============================================================

            print("\n====== WHAT IS YOUR GOAL ======\n")
            print("1. Fat loss")
            print("2. Maintenance")
            print("3. Muscle Gain")
            print("4. Recomposition")


            while True:
                try:
                    goal = int(
                        input("\nEnter the number corresponding to your goal: ")
                    )

                    if goal in [1, 2, 3, 4]:
                        break

                    else:
                        print(
                            "Invalid input. Please enter a number between 1 and 4."
                        )

                except ValueError:
                    print("Invalid input. Please enter a valid number.")


            target_calories = calculate_calorie_target(goal, tdee)

            print(
                f"\nYour estimated daily calorie target is: "
                f"{target_calories:.0f} kcal"
            )


            # ============================================================
            # 5. MACRO CALCULATION
            # ============================================================

            protein, fat, carbs = calculate_macros(
                weight,
                target_calories
            )


            # ============================================================
            # 6. DISPLAY RESULTS
            # ============================================================

            print("\n====== YOUR DAILY MACRO TARGETS ======\n")

            print(f"Calories:      {target_calories:.0f} kcal")
            print(f"Protein:       {protein:.1f} g")
            print(f"Fat:           {fat:.1f} g")
            print(f"Carbohydrates: {carbs:.1f} g")