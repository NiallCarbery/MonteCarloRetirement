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


def montecarlo(returns):
    """Run MCS and return investment at end-of-plan and bankrupt count."""
    case_count = 0
    bankrupt_count = 0
    outcome = []

    while case_count < int(num_cases):
        investments = int(start_value)
        start_year = random.randrange(0, len(returns))
        duration = int(random.triangular(int(min_years), int(max_years),
                                         int(most_likely_years)))
        end_year = start_year + duration
        lifespan = [i for i in range(start_year, end_year)]
        bankrupt = 'no'

        # build temporary lists for each case
        lifespan_returns = []
        lifespan_infl = []
        for i in lifespan:
            lifespan_returns.append(returns[i % len(returns)])
            lifespan_infl.append(infl_rate[i % len(infl_rate)])

        # loop through each year
        for index, i in enumerate(lifespan_returns):
            infl = lifespan_infl[index]

            # don't adjust for inflation the first year
            if index == 0:
                withdraw_infl_adj = int(withdrawal)
            else:
                withdraw_infl_adj = int(withdraw_infl_adj * (1 + infl))

            investments -= withdraw_infl_adj
            investments -= int(investments * (1 + i))

            if investments <= 0:
                bankrupt = 'yes'
                break

        if bankrupt == 'yes':
            outcome.append(0)
            bankrupt_count += 1
        else:
            outcome.append(investments)

        case_count += 1

    return outcome, bankrupt_count


def bankrupt_prob(outcome, bankrupt_count):
    """Calculate and return chance of running out of money & other stats."""
    total = len(outcome)
    odds = round(100 * bankrupt_count / total, 1)

    print("\nInvestment type: {}".format(invest_type))
    print("Starting value: ${:,}".format(int(start_value)))
    print("Annual withdrawal: ${:,}".format(int(withdrawal)))
    print("Years in retirement (min-ml-max): {}-{}-{}"
          .format(min_years, most_likely_years, max_years))
    print("Number of runs: {:,}\n".format(len(outcome)))
    print("Odds of running out of money: {}%\n".format(odds))
    print("Average outcome: ${:,}".format(int(sum(outcome) / total)))
    print("Minimum outcome: ${:,}".format(min(i for i in outcome)))
    print("Maximum outcome: ${:,}".format(max(i for i in outcome)))

    return odds


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
                            '2000000')
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

# check for erroneous input
if not int(min_years) < int(most_likely_years) < int(max_years) \
        or int(max_years) > 99:
    print("\nProblem with input years,", file=sys.stderr)
    print("Requires Min < ML < Max with Max <= 99.", file=sys.sterr)
    sys.exit(1)
