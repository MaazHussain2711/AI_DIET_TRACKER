# user_profile.py

class UserProfile:
    def __init__(self, name, age, gender, height_cm, weight_kg, activity_level, goal):
        self.name = name
        self.age = age
        self.gender = gender.lower()
        self.height_cm = height_cm
        self.weight_kg = weight_kg
        self.activity_level = activity_level.lower()
        self.goal = goal.lower()

    def calculate_bmr(self):
        """
        Calculate BMR using Mifflin-St Jeor Equation
        """
        if self.gender == 'male':
            return 10 * self.weight_kg + 6.25 * self.height_cm - 5 * self.age + 5
        elif self.gender == 'female':
            return 10 * self.weight_kg + 6.25 * self.height_cm - 5 * self.age - 161
        else:
            raise ValueError("Invalid gender. Please use 'male' or 'female'.")

    def get_activity_multiplier(self):
        """
        Return multiplier based on activity level
        """
        levels = {
            'sedentary': 1.2,            # Little or no exercise
            'light': 1.375,              # Light exercise/sports 1–3 days/week
            'moderate': 1.55,            # Moderate exercise 3–5 days/week
            'active': 1.725,             # Hard exercise 6–7 days/week
            'very active': 1.9           # Very hard exercise or physical job
        }
        return levels.get(self.activity_level, 1.2)

    def calculate_tdee(self):
        """
        Calculate Total Daily Energy Expenditure (TDEE)
        """
        bmr = self.calculate_bmr()
        return bmr * self.get_activity_multiplier()

    def get_calorie_goal(self):
        """
        Adjust calorie target based on user's goal
        """
        tdee = self.calculate_tdee()
        if self.goal == 'lose':
            return tdee - 500
        elif self.goal == 'gain':
            return tdee + 500
        else:
            return tdee

    def summary(self):
        """
        Return a dictionary summary of user profile
        """
        return {
            'Name': self.name,
            'BMR': round(self.calculate_bmr(), 2),
            'TDEE': round(self.calculate_tdee(), 2),
            'Daily Calorie Goal': round(self.get_calorie_goal(), 2)
        }
