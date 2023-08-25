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
