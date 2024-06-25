from trig import sine, cosine, tangent, cosecant, secant, cotangent


class Menu:
    def __init__(self):
        self.trig_function = None
        self.given_angle = None

    def run_menu(self):
        user_wants_to_continue = True

        while user_wants_to_continue:
            self._select_trig_function()

            if self.trig_function == "Exit":
                user_wants_to_continue = False
            else:
                self._get_angle_from_user()
                if self.trig_function == "Sine":
                    approx = sine(self.given_angle)
                    print("sin(" + str(self.given_angle) + ") = " + str(approx))
                elif self.trig_function == "Cosine":
                    approx = cosine(self.given_angle)
                    print("cos(" + str(self.given_angle) + ") = " + str(approx))
                elif self.trig_function == "Tangent":
                    approx = tangent(self.given_angle)
                    print("tan(" + str(self.given_angle) + ") = " + str(approx))
                elif self.trig_function == "Cosecant":
                    approx = cosecant(self.given_angle)
                    print("csc(" + str(self.given_angle) + ") = " + str(approx))
                elif self.trig_function == "Secant":
                    approx = secant(self.given_angle)
                    print("sec(" + str(self.given_angle) + ") = " + str(approx))
                elif self.trig_function == "Cotangent":
                    approx = cotangent(self.given_angle)
                    print("cot(" + str(self.given_angle) + ") = " + str(approx))
                print("Press Enter to continue.")
                input()

    def _select_trig_function(self):
        prompt = "Which would you like to approximate?"
        options = ("Sine", "Cosine", "Tangent", "Cosecant", "Secant", "Cotangent", "Exit")

        user_selection_as_int = _get_user_selection_from_menu(prompt, options)
        self.trig_function = options[user_selection_as_int]

    def _get_angle_from_user(self):
        prompt = "What angle would you like to get the " + str(self.trig_function.lower()) + " of?"
        self.given_angle = _get_float_input(prompt)


def _get_user_selection_from_menu(prompt, options):
    option_not_chosen = True

    while option_not_chosen:
        print(prompt)
        for i in range(0, len(options)):
            print("[" + str(i) + "]: " + str(options[i]))
        try:
            selection = int(input())
            if selection < 0 or selection > len(options):
                raise ValueError
            else:
                return selection
        except ValueError:
            print("Invalid input. You must input an integer from 0-" + str(len(options) - 1) + ".\n")


def _get_float_input(prompt):
    float_not_inputted = True

    while float_not_inputted:
        print(prompt)
        try:
            user_input = float(input())
            return user_input
        except ValueError:
            print("Invalid input. You must input a numerical value.")
