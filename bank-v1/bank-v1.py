from datetime import datetime
import locale

menu = """

[d] Deposit
[w] Withdraw
[e] Extract
[q] Quit

=> """

balance = 0
limit = 500
extract = ""
withdraw_count = 0
WITHDRAW_LIMIT = 3


def withdraw():
    _ = locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
    global withdraw_count
    global extract
    global balance
    try:
        amount_to_withdraw = float(input("How much do you want to withdraw? "))
    except ValueError:
        print("Invalid Number")
        return False
    if amount_to_withdraw > balance:
        print(
            f"You don't have all this money.\nCurrent Balance | {locale.currency(balance, grouping=True)} |"
        )
        return False
    if withdraw_count >= WITHDRAW_LIMIT:
        print(f"MAX WITHDRAW LIMIT REACHED: {WITHDRAW_LIMIT}")
        return False

    if amount_to_withdraw > 500:
        print(
            f"The maximum amount to withdraw is {locale.currency(limit, grouping=True)}"
        )
        return False

    withdraw_count += 1
    balance -= amount_to_withdraw
    extract += f"""

    {"-"*50} 
        DATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        Withdraw value of: {locale.currency(amount_to_withdraw)}
    {"-"*50} 

    """
    print(f"Your current balance is now: {locale.currency(balance)}")
    return True


def deposit():
    global balance
    global extract
    _ = locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
    try:
        amount_to_deposit = float(
            input("How much do you want to deposit in your account? ")
        )
        if amount_to_deposit > 0:
            balance += amount_to_deposit
        extract += f"""

        {"-"*50} 
            DATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            Deposit value of: {locale.currency(amount_to_deposit)}
        {"-"*50} 

        """
        print(
            f"A deposit of {locale.currency(amount_to_deposit)} amount has been made into the account"
        )

        print(f"Your current balance is now: {locale.currency(balance)}")
        return True
    except ValueError:
        print("Invalid Number")
    return False


def print_extract():
    _ = locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
    global extract
    global balance
    if len(extract) <= 0:
        print("You haven't done anything in your account yet.", end="")
    print(extract)
    print(f"Current Balance {locale.currency(balance)}")


while True:
    input_option = input(menu)

    if input_option.lower() == "d":
        if not deposit():
            break

    elif input_option.lower() == "w":
        if not withdraw():
            break

    elif input_option.lower() == "e":
        print_extract()

    elif input_option.lower() == "q":
        break

    else:
        print("Invalid Option")
