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
    hasError = False
    try:
        amount_to_withdraw = float(input("How much do you want to withdraw? "))
        if amount_to_withdraw > balance:
            print(
                f"You don't have all this money.\nCurrent Balance | {locale.currency(balance, grouping=True)} |"
            )
            hasError = True
        if withdraw_count >= WITHDRAW_LIMIT and not hasError:
            print(f"MAX WITHDRAW LIMIT REACHED: {WITHDRAW_LIMIT}")
            hasError = True

        if amount_to_withdraw > limit and not hasError:
            print(
                f"The maximum amount to withdraw is {locale.currency(limit, grouping=True)}"
            )
            hasError = True

        if amount_to_withdraw <= 0 and not hasError:
            print("You need to specify a value greater than 0 to withdraw.", end="")
            hasError = True

        if not hasError:
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
    except ValueError:
        print("Invalid Number")
        return False


def deposit():
    global balance
    global extract
    _ = locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
    hasError = False
    try:
        amount_to_deposit = float(
            input("How much do you want to deposit in your account? ")
        )
        print()
        if not amount_to_deposit > 0:
            print("You need to deposit some amount greater than 0.", end="")
            hasError = True

        if not hasError:
            balance += amount_to_deposit
            extract += f"""

            {"-"*50} 
                DATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                Deposit value of: {locale.currency(amount_to_deposit)}
            {"-"*50} 

            """
            print(
                f"A deposit of {locale.currency(amount_to_deposit)} amount has been made into the account."
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
    print("=" * 25, "EXTRACT", "=" * 25)
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
        print("Bye, have a nice day! :)")
        break

    else:
        print("Invalid Option")
