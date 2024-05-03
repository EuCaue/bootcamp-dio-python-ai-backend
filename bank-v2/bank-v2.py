from datetime import datetime
import locale
import re


def check_birth_date(date: str):
    pattern = r"^\d{2}/\d{2}/\d{4}$"

    if re.match(pattern, date):
        return True
    else:
        return False


def check_cpf(cpf: str):
    pattern = r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"

    if re.match(pattern, cpf):
        return True
    else:
        return False


def withdraw(
    *,
    withdraw_count: int,
    balance: float,
    WITHDRAW_LIMIT: int,
    extract: str,
    WITHDRAW_VALUE_LIMIT: int,
):
    _ = locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
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

        if amount_to_withdraw > WITHDRAW_VALUE_LIMIT and not hasError:
            print(
                f"The maximum amount to withdraw is {locale.currency(WITHDRAW_VALUE_LIMIT, grouping=True)}"
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


def deposit(
    balance: float,
    extract: str,
    /,
):
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


def print_extract(extract: str, /, *, balance: int):
    _ = locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
    if len(extract) <= 0:
        print("You haven't done anything in your account yet.", end="")
    print("=" * 25, "EXTRACT", "=" * 25)
    print(extract)
    print(f"Current Balance {locale.currency(balance)}")


def find_user(cpf: str, users: list[dict[str, str]]):
    user = [user for user in users if user["cpf"] == cpf]
    return user[0] if user else None


def create_user(user_list: list[dict[str, str]]):
    name = input("Type your name: ").strip()
    if len(name) <= 0:
        print(">>> Your name need to be more than 4 characters. <<<")
        return False
    birth_date = input("Type your birth date (DD/MM/YYYY): ").strip()
    if len(birth_date) <= 0:
        print(">>> Your birth date, cannot be empty. <<<")
        return False
    if not check_birth_date(birth_date):
        print(">>> Your birth date should be in this format DD/MM/YYYY. <<<")
        return False
    cpf = input("Type your CPF (XXX.XXX.XXX-XX): ").strip()

    if len(cpf) <= 0:
        print(">>> Your CPF cannot be empty. <<<")
        return False
    if not check_cpf(cpf):
        print(">>> Your CPF is not XXX.XXX.XXX-XX <<<")
        return False

    if find_user(cpf, user_list):
        print(">>> This person it's already in your database. <<<")
        return False

    street_address = input("Type your street address: ").strip()
    if len(street_address) <= 1:
        print(">>> Your street address need to be more than 1 character. <<<")
        return False

    house_number = input("Type your house number: ").strip()
    if len(house_number) <= 0:
        print(">>> Your House Number cannot be empty. <<<")
        return False

    neighborhood = input("Type your neighborhood: ").strip()
    if len(neighborhood) <= 2:
        print(">>> Your neighborhood cannot be empty. <<<")
        return False

    city = input("Type your city name: ").strip()
    if len(city) <= 2:
        print(">>> Your city name cannot be empty. <<<")
        return False
    state_abbr = input("Type your state abbreviation: ").strip()

    if len(state_abbr) <= 1:
        print(">>> Your state abbreviation cannot be empty. <<<")
        return False

    if len(state_abbr) > 3:
        print(">>> Your state abbreviation cannot greater than 3. <<<")
        return False

    formated_address = (
        f"{street_address}, - {house_number} - {neighborhood} - {city} - {state_abbr}"
    )
    user = {
        "name": name,
        "birth_date": birth_date,
        "cpf": cpf,
        "address": formated_address,
    }

    user_list.append(user)
    return user


def create_account(account_list: list[str | float | int], users: list[dict[str, str]]):
    user_cpf = input("Type the user CPF: ")
    if len(user_cpf) <= 1:
        print(">>> User cpt cannot be empty. <<<")
        return False

    if not check_cpf(user_cpf):
        print(">>> Your CPF is not XXX.XXX.XXX-XX <<<")
        return False

    user = find_user(user_cpf, users)
    if not user:
        print(f">>> None found with this CPF {user_cpf} <<<")
        return False

    AGENCY_NUMBER = "0001"
    account_number = len(account_list) + 1
    account = {
        "agency": AGENCY_NUMBER,
        "account_number": account_number,
        "user": user,
    }
    account_list.append(account)
    return account


def show_accounts(accounts: list[dict[str, str]]):
    print("\n\t\t\tACCOUNT\n", "=" * 50)
    for account in accounts:
        print(
            f"\n\tAgency: {account['agency']}\n",
            f"\tAccount Number: {account['account_number']}\n",
            f"\tUser CPF: {account['user']['cpf']}\n",
        )
    print("=" * 50)


def show_users(users: list[dict[str, str]]):
    print("\n\t\t\tUSERS\n", "=" * 50)
    for user in users:
        print(
            f"\n\tName: {user['name']}\n"
            f"\tBirth Date: {user['birth_date']}\n"
            f"\tCPF: {user['cpf']}\n"
            f"\tAddress: {user['address']}\n"
        )
    print("=" * 50)


def main():
    menu = """
    [d] Deposit
    [w] Withdraw
    [e] Extract
    [q] Quit
    [na] New Account
    [nu] New User
    [sa] Show Accounts
    [su] Show Users
    => """

    balance = 0
    limit = 500
    extract = ""
    withdraw_count = 0
    WITHDRAW_LIMIT = 3
    users = []
    accounts = []
    while True:
        input_option = input(menu)

        if input_option.lower() == "d":
            if not deposit(balance, extract):
                break

        elif input_option.lower() == "w":
            if not withdraw(
                balance=balance,
                withdraw_count=withdraw_count,
                WITHDRAW_LIMIT=WITHDRAW_LIMIT,
                extract=extract,
                WITHDRAW_VALUE_LIMIT=limit,
            ):
                break

        elif input_option.lower() == "e":
            print_extract(extract, balance=balance)

        elif input_option.lower() == "nu":
            new_user = create_user(users)
            if new_user:
                print("New user successfully created\n")
                print(
                    f"\n\tName: {new_user['name']}\n"
                    f"\tBirth Date: {new_user['birth_date']}\n"
                    f"\tCPF: {new_user['cpf']}\n"
                    f"\tAddress: {new_user['address']}\n"
                )

        elif input_option.lower() == "na":
            new_account = create_account(accounts, users)
            if new_account:
                print(
                    "New account uccessfully created\n",
                )
                print(
                    f"\n\tAgency: {new_account['agency']}\n",
                    f"\tAccount Number: {new_account['account_number']}\n",
                    f"\tUser Name: {new_account['user']["name"]}\n",
                    f"\tUser CPF: {new_account['user']["cpf"]}\n",
                )
        elif input_option.lower() == "sa":
            if len(accounts) > 0:
                show_accounts(accounts)
            else:
                print("Don't have any accounts created yet. :/")

        elif input_option.lower() == "su":
            if len(users) > 0:
                show_users(users)
            else:
                print("Don't have any users created yet. :/")

        elif input_option.lower() == "q":
            print("Bye, have a nice day! :)")
            break

        else:
            print("Invalid Option")


if __name__ == "__main__":
    main()
