import random

# Constants
MAX_BET = 100
MIN_BET = 1

ROWS = 4
COLS = 4
# Dictionary defining count of each symbol
symbols_count = {
    "A": 4,
    "B": 6,
    "C": 12,

    "D": 24,
}
# Dictionary defining value of each symbol
symbols_value = {
    "A": 100,
    "B": 25,
    "C": 15,
    "D": 3,
}


def check_winnings(columns, lines, bet, values):
    """
    Calculate the winnings based on parameters.
    :param columns: result of spin (list)
    :param lines: number of lines to bet on (int)
    :param bet: Bet amount of each line (int)
    :param values: Symbol values (dict)
    :return: a tuple containing the total winnings and the winning lines (tuple)
    """
    winnings = 0
    winning_lines = []
    # check rows
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)
    # Hidden bonus, if all lines check columns and diagonal
    if lines == len(columns[0]) == len(columns):
        i_diagonal1 = 0
        i_diagonal2 = len(columns[0]) - 1
        symbol = columns[0][i_diagonal1]
        symbol2 = columns[0][i_diagonal2]
        diagonal1_win = True
        diagonal2_win = True
        for column in columns:
            # check column
            if len(column) == column.count(column[0]):  # Check if in column is only one symbol
                winnings += values[column[0]] * bet
                print("Bonus! Strike in column(s)")
            # check diagonally across the matrix
            if symbol == column[i_diagonal1] and diagonal1_win:
                i_diagonal1 += 1
            else:
                diagonal1_win = False
                i_diagonal1 += 1
            if symbol2 == column[i_diagonal2] and diagonal2_win:
                i_diagonal2 -= 1
            else:
                diagonal2_win = False
                i_diagonal2 -= 1
        else:
            if diagonal1_win:
                winnings += values[symbol] * bet
                print("Bonus! Strike diagonally across")
            if diagonal2_win:
                winnings += values[symbol2] * bet
                print("Bonus! Strike diagonally across")

    return winnings, winning_lines


def get_slot_machine_spin(rows, cols, symbols):
    """
    Generate random spin of slot machine.
    :param rows: Number of rows in the slot machine (int)
    :param cols: Number of columns in the slot machine (int)
    :param symbols: Count of each symbol (dict)
    :return: A list of columns representing the slot machine spin (list)
    """
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)

    return columns


def print_slot_machine(columns):
    """
    Print the slot machine spin.
    :param columns: list of columns in the slot machine (list)
    :return: None
    """
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")
        print()


def deposit():
    """
    Prompt the user to enter the deposit amount.
    :return: The deposit amount (int)
    """
    while True:
        amount = input("What would you like to deposit? $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Amount must be greater than 0.")
        else:
            print("Please enter a number.")
    return amount


def get_number_of_lines():
    """
    Prompt the user to get number of lines to bet on.
    :return: The number of lines to bet on (int)
    """
    while True:
        lines = input(f"Enter the numbers of lines to bet on from 1 to {ROWS}? ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= ROWS:
                break
            else:
                print("Enter a valid number of lines.")
        else:
            print("Please enter a number.")
    return lines


def get_bet():
    """
    Prompt user to enter the bet amount for each line
    :return: The bet amount
    """
    while True:
        amount = input("What would you like to bet on each line? $")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Amount must be between ${MIN_BET} - ${MAX_BET}")
        else:
            print("Please enter a number.")
    return amount


def spin(balance):
    """
    Perform a spin of slot machine
    :param balance: The current balance (int)
    :return: Result balance after spin (int)
    """
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines
        if total_bet > balance:
            print(f"You do not have enough money to bet that amount, your current balance is: ${balance}.")
        else:
            break

    print(f"You are betting ${bet} on {lines} lines. Total bet is equal to: ${total_bet}.")
    slots = get_slot_machine_spin(ROWS, COLS, symbols_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbols_value)
    print(f"You won ${winnings}")
    print(f"You won on lines:", *winning_lines)
    return balance + winnings - total_bet


def main():
    """
    Main function to run slot machine
    """
    balance = deposit()
    while True:
        print(f"Current balance is ${balance}")
        answer = input("Press enter to spin or q to quit.")
        if answer == "q":
            break
        balance = spin(balance)

    print(f"You left with ${balance}")


if __name__ == '__main__':
    main()
