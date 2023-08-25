import sys
import random
import matplotlib.pyplot as pyplot


def read_to_list(file_name):
    """Open a file of data in percent, convert to decimal & return a list."""
    with open(file_name) as in_file:
        lines = [float(line.strip()) for line in in_file]
        decimal = [round(line / 100, 5) for line in in_file]
        return decimal


def default_input(prompt, default=None):
    """Allow use of default values in input."""
    prompt = '{}[{}]:'.format(prompt, default)
    response = input(prompt)
    if not response and default:
        return default
    else:
        return response


# load data files with orginal datat in percent format
print("\nNote:Input data should be in percent, not in decimal!\n")

try:
    bonds = read_to_list('10yrUSTBond.txt')
    stocks = read_to_list('SP500Returns.txt')
    infl_rate = read_to_list('USInflationRate.txt')
except IOError as e:
    print("{}.\nTerminating program.".format(e), file=sys.stderr)
    sys.exit(1)

# get user input; use dictionary for investment-type arguemnts
investment_type_args = {'bonds': bonds, 'stocks': stocks}

# print input legend for user
print(" stocks = S&P500")
print(" bonds = 10-yr Treasury Bond")
print("Press ENTER to take default value shown in [brackets]. \n")

# get user input
invest_type = default_input("Enter investment type: (stocks, bonds): \n",
                            'bonds').lower()
while invest_type not in investment_type_args:
    invest_type = input("Invalid investment. Enter investment type "
                        "as listed in prompt: ")


start_value = default_input("Input starting value of investments: \n",
                            ' 2000000')
while not start_value.isdigit():
    start_value = input("Invalid input! Input integer only: ")


withdrawal = default_input("Input annual pre-tax withdrawal"
                           " (today's $): \n", '80000')
while not withdrawal.isdigit():
    withdrawal = input("Invalid input! Input integer only: ")


min_years = default_input("Input minimum years in retirement: \n", '18')
while not min_years.isdigit():
    min_years = input("Invalid input! Input integer only: ")


most_likely_years = default_input("Input most-likely years in retirement: \n",
                                  '25')
while not most_likely_years.isdigit():
    most_likely_years = input("Invalid input! Input integer only: ")


max_years = default_input("Input maximum years in retirement: \n", '40')
while not max_years.isdigit():
    max_years = input("Invalid input! Input integer only: ")


num_cases = default_input("Input number of cases to run: \n", '50000')
while not num_cases.isdigit():
    num_cases = input("Invalid input! Input integer only: ")
