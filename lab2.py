import math
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)


class Input:
    type_equations = 0
    a = 0
    b = 0
    accuracy = 0
    filename = 'input'
    type_of_input = 0

    def __init__(self):
        self.choose_equation()
        self.choose_boundaries()
        self.choose_accuracy()
        self.start_of_calculation()

    def choose_equation(self):
        while 1:
            try:
                print("\n♦ So, please, choose a equation: ♦\n"
                      "\t1. x^3 - x + 4 = 0\n"
                      "\t2. 5/x - 2x = 0\n"
                      "\t3. e^2x - 2 = 0\n"
                      "\t4. 4.45x^3 + 7.81x^2 - 9.62x - 8.17 = 0\n")
                answer = int(input("Variant: ").strip())
                if answer == 1:
                    self.type_equations = 1
                    break
                elif answer == 2:
                    self.type_equations = 2
                    break
                elif answer == 3:
                    self.type_equations = 3
                    break
                elif answer == 4:
                    self.type_equations = 4
                    break
                else:
                    get_answer(1)
                    continue
            except TypeError:
                get_answer(1)
                continue

    def choose_boundaries(self):
        while 1:
            try:
                print("Please, choose type of input:\n"
                      "\t1. File\n"
                      "\t2. Write\n")
                self.type_of_input = int(input("Type of input: ").strip())
                if self.type_of_input == 2:
                    print("Oh, you choose write! Nice choice!")
                    print("Please, input a border of segment, example: -10 10.\n")
                    limits = list(input("Border of segment: ").strip().split(" "))
                    if len(limits) == 2 and (float(limits[0].strip()) < float(limits[1].strip())):
                        self.a = float(limits[0].strip())
                        self.b = float(limits[1].strip())
                        break
                    else:
                        get_answer(1)
                        continue
                elif self.type_of_input == 1:
                    print("Oh, you choose file! Good choice!")
                    print('It\'s so great! Please, write the name of your file!')
                    self.filename = input()
                    self.a = float(self.get_data_from_file()[0][0])
                    self.b = float(self.get_data_from_file()[0][1])
                    print('Left is', self.a, 'and right is', self.b)
                    break
            except ValueError:
                get_answer(1)
            except TypeError:
                get_answer(1)

    def choose_accuracy(self):
        while 1:
            try:
                if self.type_of_input == 2:
                    print("\nPlease input accuracy of calculation.\n")
                    accuracy = float(input("Accuracy: ").strip())
                    if accuracy <= 0:
                        get_answer(1)
                        continue
                    else:
                        self.accuracy = accuracy
                        break
                elif self.type_of_input == 1:
                    if (float(self.get_data_from_file()[1][0])) <= 0:
                        get_answer(1)
                        continue
                    else:
                        self.accuracy = float(self.get_data_from_file()[1][0])
                        print('Accuracy is', self.accuracy)
                        break
            except ValueError:
                get_answer(1)
            except TypeError:
                get_answer(1)

    def get_data_from_file(self):
        try:
            with open(self.filename) as f:
                data = [list(map(float, row.split())) for row in f.readlines()]
            return data
        except FileNotFoundError:
            get_answer(8)

    def start_of_calculation(self):
        while 1:
            try:
                math_logic = MathLogic(self.type_equations, self.a, self.b, self.accuracy)
                print("Please, choose type of method:\n"
                      "\t1. Chord\n"
                      "\t2. Secant\n"
                      "\t3. Iteration")
                type_of_method = int(input("Type of method: ").strip())
                if type_of_method == 1:
                    math_logic.calculate_method_chord()
                    math_logic.print_table(1)
                elif type_of_method == 2:
                    math_logic.calculate_method_secant()
                    math_logic.print_table(2)
                elif type_of_method == 3:
                    math_logic.calculate_method_iter()
                    math_logic.print_table(3)
                print_result(math_logic)
                print("Should I save output in the file?:\n"
                      "\t• No\n"
                      "\t• Yes\n")
                type_of_output = input("Type of output: ").strip()
                if (type_of_output.lower() == 'yes') or (type_of_output.lower() == 'y'):
                    with open("output", "w") as file:
                        if type_of_method == 1:
                            math_logic.chord_table.insert(0, ["N", "a", "b", "x", "f(a)", "f(b)", "f(x)", "|a-b|"])
                            file.write(tabulate(math_logic.chord_table, tablefmt="psql"))
                        elif type_of_method == 2:
                            math_logic.secant_table.insert(0, ["N", "x(i-1)", "x(i)", "x(i+1)", "f(x(i+1))", "|x(i+1)-x(i)|"])
                            file.write(tabulate(math_logic.secant_table, tablefmt="psql"))
                        elif type_of_method == 3:
                            math_logic.iter_table.insert(0, ["N", "x(i)", "x(i+1)", "fi(i+1)", "f(x(i+1))", "|x(i+1)-x(i)|"])
                            file.write(tabulate(math_logic.iter_table, tablefmt="psql"))
                del math_logic
                break
            except TypeError:
                get_answer(1)
            except ValueError:
                get_answer(1)


class MathLogic:
    param_1 = 1
    param_2 = 1
    param_3 = 1
    param_4 = 1
    param_lambda = 1
    status = 0
    solvable = 1
    type_equations = 0
    a = 0
    b = 0
    steps = 0
    previous_count = 0
    x0 = 0
    x1 = 0
    accuracy = 0
    result = 0
    segments = []
    chord_table = []
    secant_table = []
    iter_table = []

    def __init__(self, type_equations, a, b, accuracy):
        self.type_equations = type_equations
        self.a = a
        self.segments = []
        self.steps = 0
        self.solvable = 1
        self.status = 0
        self.previous_count = 0
        self.result = 0
        self.b = b
        self.accuracy = accuracy
        self.x0 = a
        self.x1 = b

    def calculate_method_chord(self):
        self.chord_table = []
        self.result = self.a - ((self.b - self.a) * self.function(self.a)) / (
                self.function(self.b) - self.function(self.a))
        if self.a <= self.result <= self.b:
            self.chord_table.append(
                [self.steps, self.a, self.b, self.result, self.function(self.a), self.function(self.b),
                 self.function(self.result)])
            if self.check_derivative():
                if self.function(self.a) * self.function(self.b) < 0:
                    while 1:
                        self.steps += 1
                        if self.solvable and (self.steps < 2500000):
                            self.segments.append([self.result, self.function(self.result)])
                            self.do_method_chord()
                            if abs((self.result - self.previous_count) <= self.accuracy or abs(
                                    self.function(self.result)) <= self.accuracy) and (
                                    self.a <= self.result <= self.b):
                                break
                        else:
                            if self.steps == 2500000:
                                self.status = 3
                            else:
                                self.status = 1
                            break
                else:
                    self.status = 2
        else:
            self.status = 5

    def calculate_method_secant(self):
        self.secant_table = []
        self.steps = 0
        if abs(self.x1 - self.x0) > self.accuracy:
            while 1:
                try:
                    self.previous_count = self.x1
                    self.x1 = self.x1 - (self.x1 - self.x0) * self.function(self.x1) / (
                            self.function(self.x1) - self.function(self.x0))
                    self.secant_table.append(
                        [self.steps, self.x0, self.previous_count, self.x1, self.function(self.x1),
                         abs(self.x1 - self.previous_count)])
                    self.steps += 1
                    self.x0 = self.previous_count
                    if abs(self.x1 - self.x0) <= self.accuracy:
                        break
                except ZeroDivisionError:
                    self.x1 = self.x1 - (self.x1 - self.x0) * self.function(self.x1) / (
                            self.function(self.x1) - self.function(self.x0) + 1e-8)
        else:
            self.status = 2
            print_result(self)
        self.result = self.x1

    def calculate_method_iter(self):
        self.iter_table = []
        self.param_lambda = - 1 / max(self.function_1(self.a), self.function_1(self.b))
        self.previous_count = self.a
        self.result = self.param_function(self.previous_count)
        self.steps = 0
        if abs(self.result - self.previous_count) > self.accuracy:
            while 1:
                self.result = self.param_function(self.previous_count)
                self.iter_table.append(
                    [self.steps, self.previous_count, self.result, self.param_function(self.result),
                     self.function(self.result), abs(self.result - self.previous_count)])
                self.steps += 1
                if abs(self.result - self.previous_count) <= self.accuracy:
                    break
                self.previous_count = self.result
        else:
            get_answer(3)

    def check_derivative(self):
        float_range = np.arange(self.a, self.b, (self.b - self.a) / 100)
        convergence = 1
        if self.function_1(self.a) < 0:
            flag = 1
        else:
            flag = 0
        previous_flag = flag
        for i in float_range:
            if self.function_1(i) < 0:
                flag = 1
            else:
                flag = 0
            if previous_flag != flag:
                convergence = 0
                break
            previous_flag = flag
        if self.function_2(self.a) < 0:
            flag = 1
        else:
            flag = 0
        previous_flag = flag
        for i in float_range:
            if self.function_2(i) < 0:
                flag = 1
            else:
                flag = 0
            if previous_flag != flag:
                convergence = 0
                break
            previous_flag = flag
        return convergence

    def fi_function(self, x):
        try:
            if self.type_equations == 1:
                return math.pow(x, 3) + 4
            elif self.type_equations == 2:
                return 5 / x - x
            elif self.type_equations == 3:
                return math.pow(math.e, 2 * x) - 2 + x
            elif self.type_equations == 4:
                return 4.45 * math.pow(x, 3) + 7.81 * math.pow(x, 2) - 8.62 * x - 8.17
        except ZeroDivisionError:
            return self.fi_function(x + 1e-8)
        except OverflowError:
            self.status = 3

    def param_function(self, x):
        try:
            if self.type_equations == 1:
                return self.param_lambda * math.pow(x, 3) - self.param_lambda * x + x + 4 * self.param_lambda
            elif self.type_equations == 2:
                return self.param_lambda * 5 / x - self.param_lambda * 2 * x + x
            elif self.type_equations == 3:
                return self.param_lambda * math.pow(math.e, 2 * x) - self.param_lambda * 2 + x
            elif self.type_equations == 4:
                return self.param_lambda * 4.45 * math.pow(x, 3) + self.param_lambda * 7.81 * math.pow(x,
                                                                                                       2) - self.param_lambda * 9.62 * x - self.param_lambda * 8.17 + x
        except ZeroDivisionError:
            return self.param_function(x + 1e-8)
        except OverflowError:
            self.status = 3

    def function(self, x):
        try:
            if self.type_equations == 1:
                return math.pow(x, 3) - x + 4
            elif self.type_equations == 2:
                return 5 / x - 2 * x
            elif self.type_equations == 3:
                return math.pow(math.e, 2 * x) - 2
            elif self.type_equations == 4:
                return 4.45 * math.pow(x, 3) + 7.81 * math.pow(x, 2) - 9.62 * x - 8.17
        except ZeroDivisionError:
            return self.function(x + 1e-8)
        except OverflowError:
            self.status = 3

    def function_1(self, x):
        try:
            if self.type_equations == 1:
                return 3 * math.pow(x, 2) - 1
            elif self.type_equations == 2:
                return -5 / (math.pow(x, 2)) - 2
            elif self.type_equations == 3:
                return 2 * math.pow(math.e, 2 * x)
            elif self.type_equations == 4:
                return 4.45 * 3 * math.pow(x, 2) + 2 * 7.81 * x - 9.62
        except ZeroDivisionError:
            return self.function_1(x + 1e-8)
        except OverflowError:
            self.status = 3

    def function_2(self, x):
        try:
            if self.type_equations == 1:
                return 6 * x
            elif self.type_equations == 2:
                return 10 / (math.pow(x, 3))
            elif self.type_equations == 3:
                return 4 * math.pow(math.e, 2 * x)
            elif self.type_equations == 4:
                return 4.45 * 6 * x + 2 * 7.81
        except ZeroDivisionError:
            return self.function_2(x + 1e-8)
        except OverflowError:
            self.status = 3

    def do_method_chord(self):
        try:
            count = self.result
            self.result = self.result - ((self.a - self.result) * self.function(self.result)) / (
                    self.function(self.a) - self.function(self.result))
            self.previous_count = count
            if self.function(self.a) * self.function(self.result) < 0:
                self.b = self.result
            elif self.function(self.result) * self.function(self.b) < 0:
                self.a = self.result
            self.chord_table.append(
                [self.steps, self.a, self.b, self.result, self.function(self.a), self.function(self.b),
                 self.function(self.result), abs(self.a - self.b)])
        except ValueError:
            self.result = self.result - ((self.a - self.result) * self.function(self.result)) / (
                    self.function(self.a) - self.function(self.result))
        except TypeError:
            self.result = self.result - ((self.a - self.result) * self.function(self.result)) / (
                    self.function(self.a) - self.function(self.result))
        except ZeroDivisionError:
            self.result = self.result - ((self.a - self.result) * self.function(self.result + 1e-8)) / (
                    self.function(self.a) - self.function(self.result + 1e-8))

    def print_table(self, type_of_table):
        if type_of_table == 1:
            print('Method Chord:')
            print(tabulate(self.chord_table, headers=["№", "a", "b", "x", "f(a)", "f(b)", "f(x)", "|a-b|"],
                           tablefmt="fancy_grid", floatfmt="2.5f"))
        elif type_of_table == 2:
            print('Method Secant:')
            print(tabulate(self.secant_table, headers=["№", "x(i-1)", "x(i)", "x(i+1)", "f(x(i+1))", "|x(i+1)-x(i)|"],
                           tablefmt="fancy_grid", floatfmt="2.5f"))
        elif type_of_table == 3:
            print('Method Iter:')
            print(tabulate(self.iter_table, headers=["№", "x(i)", "x(i+1)", "fi(i+1)", "f(x(i+1))", "|x(i+1)-x(i)|"],
                           tablefmt="fancy_grid", floatfmt="2.5f"))


def print_result(math_logic):
    if math_logic.solvable == 1:
        if math_logic.status == 0:
            print("\nEquation root: " + str(math_logic.result) + "\n" +
                  "Count of iteration: " + str(math_logic.steps) + "\n" +
                  "Calculation error: " + str(math_logic.accuracy) + "\n")
            draw_graph(math_logic)
        elif math_logic.status == 1:
            get_answer(3)
        elif math_logic.status == 2:
            get_answer(4)
        elif math_logic.status == 3:
            get_answer(5)
        elif math_logic.status == 4:
            get_answer(6)
        elif math_logic.status == 5:
            get_answer(3)
    else:
        get_answer(2)


def get_answer(type_answer):
    if type_answer == 1:
        print("Incorrect input.\n")
    elif type_answer == 2:
        print("No solution.\n")
    elif type_answer == 3:
        print("There is no concrete solution or it doesn't exist.\n")
    elif type_answer == 4:
        print("Convergence condition is not satisfied on this segment.\n")
    elif type_answer == 5:
        print("Counts of iteration reached 2.5 million , solution not found.\n")
    elif type_answer == 6:
        print("The initial approximation is poorly selected, solution not found.\n")
    elif type_answer == 7:
        print("Counts of iteration reached 250 thousand , solution not found.\n")
    elif type_answer == 8:
        print("The file isn't found.\n")


def draw_graph(math_logic):
    try:
        ax = plt.gca()
        plt.grid()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        minimum = math_logic.a
        maximum = math_logic.b
        for segment in math_logic.segments:
            if segment[0] < minimum:
                minimum = segment[0]
            elif segment[1] > maximum:
                maximum = segment[1]
        x = np.linspace(minimum, maximum, 100)
        equations = {1: ["f(x) = x^3 - x + 4", [(math.pow(i, 3) - x + 4) for i in x]],
                     2: ["f(x) = 5/x - 2x", [(5 / i - 2 * i) for i in x]],
                     3: ["f(x) = e^2x - 2", [(math.pow(math.e, 2 * i) - 2) for i in x]],
                     4: ["f(x) = 4.45x^3 + 7.81x^2 - 9.62x - 8.17",
                         [(4.45 * math.pow(i, 3) + 7.81 * math.pow(i, 2) - 9.62 * i - 8.17) for i in x]]}
        plt.title("Graph: " + equations[math_logic.type_equations][0])
        plt.plot(x, equations[math_logic.type_equations][1], color="g", linewidth=2)
        plt.plot(x, 0 * x, color="black", linewidth=1)
        plt.scatter(math_logic.result, 0, color="r", s=80)
        plt.show()
        del x
    except ValueError:
        return
    except ZeroDivisionError:
        return
    except OverflowError:
        return


if __name__ == "__main__":
    print("☺ Hello, pretty human! Let's solve some equations! ☻")
    while 1:
        new_input = Input()
        del new_input
        continue
