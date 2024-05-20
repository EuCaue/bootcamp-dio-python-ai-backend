from abc import ABC, abstractmethod
import locale
import re


class Transaction(ABC):
    @abstractmethod
    def register(self, account):
        pass


class Withdrawal(Transaction):
    def __init__(self, value: float):
        self.value = value

    def register(self, account):
        if (
            account.balance >= self.value
            and account.num_withdrawals < 3
            and self.value <= 500
        ):
            account.balance -= self.value
            account.history.add_transaction(self)
            account.num_withdrawals += 1
            print(
                f"Withdrawal of {locale.currency(self.value, grouping=True)} successful."
            )
            return True
        elif account.num_withdrawals >= 3:
            print("Maximum number of withdrawals reached.")
            return False
        elif self.value > 500:
            print("Withdrawal amount must be 500 or less.")
            return False
        else:
            print("Insufficient balance to withdraw.")
            return False


class Deposit(Transaction):
    def __init__(self, value):
        self.value = value

    def register(self, account):
        account.balance += self.value
        account.history.add_transaction(self)
        print(f"Deposit of {locale.currency(self.value, grouping=True)} successful.")
        return True


class History:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)


class Account:
    def __init__(self, client, number):
        self.balance = 0.0
        self.number = number
        self.agency = "0001"
        self.client = client
        self.history = History()

    def withdraw(self, value):
        withdrawal = Withdrawal(value)
        return withdrawal.register(self)

    def deposit(self, value):
        deposit = Deposit(value)
        return deposit.register(self)


class CheckingAccount(Account):
    def __init__(self, client, number: int, overdraft_limit=500):
        super().__init__(client, number)
        self.overdraft_limit = overdraft_limit
        self.num_withdrawals = 0


class Client:
    def __init__(self, address: str):
        self.address = address
        self.accounts = []

    def perform_transaction(self, account, transaction):
        return transaction.register(account)

    def add_account(self, account):
        self.accounts.append(account)


class Individual(Client):
    def __init__(self, name, cpf, birth_date, address):
        super().__init__(address)
        self.name = name
        self.cpf = cpf
        self.birth_date = birth_date


def check_birth_date(date: str):
    pattern = r"^\d{2}/\d{2}/\d{4}$"
    return bool(re.match(pattern, date))


def check_cpf(cpf: str):
    pattern = r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"
    return bool(re.match(pattern, cpf))


def create_user(clients):
    name = input("Type your name: ").strip()

    while True:
        birth_date = input("Type your birth date (DD/MM/YYYY): ").strip()
        if check_birth_date(birth_date):
            break
        else:
            print("Invalid birth date format. Please use DD/MM/YYYY.")

    while True:
        cpf = input("Type your CPF (XXX.XXX.XXX-XX): ").strip()
        if check_cpf(cpf):
            if any(client.cpf == cpf for client in clients):
                print("CPF already registered. Please use a different CPF.")
            else:
                break
        else:
            print("Invalid CPF format. Please use XXX.XXX.XXX-XX.")

    street_address = input("Type your street address: ").strip()
    house_number = input("Type your house number: ").strip()
    neighborhood = input("Type your neighborhood: ").strip()
    city = input("Type your city name: ").strip()
    state_abbr = input("Type your state abbreviation: ").strip()

    formatted_address = (
        f"{street_address}, - {house_number} - {neighborhood} - {city} - {state_abbr}"
    )
    user = Individual(name, cpf, birth_date, formatted_address)
    clients.append(user)
    return user


def create_account(clients, accounts):
    user_cpf = input("Type the user CPF: ").strip()
    user = next((client for client in clients if client.cpf == user_cpf), None)

    if user:
        account_number = len(accounts) + 1
        new_account = CheckingAccount(user, account_number)
        user.add_account(new_account)
        accounts.append(new_account)
        return new_account
    else:
        print(f"No user found with CPF {user_cpf}")
        return None


def show_accounts(accounts):
    print("\n\t\t\tACCOUNTS\n", "=" * 50)
    for account in accounts:
        print(
            f"\n\tAgency: {account.agency}\n",
            f"\tAccount Number: {account.number}\n",
            f"\tUser CPF: {account.client.cpf}\n",
        )
    print("=" * 50)


def show_users(clients):
    print("\n\t\t\tUSERS\n", "=" * 50)
    for client in clients:
        print(
            f"\n\tName: {client.name}\n"
            f"\tBirth Date: {client.birth_date}\n"
            f"\tCPF: {client.cpf}\n"
            f"\tAddress: {client.address}\n"
        )
    print("=" * 50)


def main():
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

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

    clients = []
    accounts = []

    while True:
        input_option = input(menu).strip().lower()

        if input_option == "d":
            account_number = int(input("Enter account number: "))
            account = next(
                (account for account in accounts if account.number == account_number),
                None,
            )
            if account:
                value = float(input("How much do you want to deposit? "))
                account.deposit(value)
            else:
                print("Account not found.")

        elif input_option == "w":
            account_number = int(input("Enter account number: "))
            account = next(
                (account for account in accounts if account.number == account_number),
                None,
            )
            if account:
                value = float(input("How much do you want to withdraw? "))
                account.withdraw(value)
            else:
                print("Account not found.")

        elif input_option == "e":
            account_number = int(input("Enter account number: "))
            account = next(
                (account for account in accounts if account.number == account_number),
                None,
            )
            if account:
                print("=" * 25, "EXTRACT", "=" * 25)
                for transaction in account.history.transactions:
                    transaction_type = (
                        "Deposit" if isinstance(transaction, Deposit) else "Withdrawal"
                    )
                    print(
                        f"{transaction_type}: {locale.currency(transaction.value, grouping=True)}"
                    )
                print(
                    f"Current Balance: {locale.currency(account.balance, grouping=True)}"
                )
            else:
                print("Account not found.")

        elif input_option == "nu":
            if create_user(clients):
                print("New user successfully created.")

        elif input_option == "na":
            if create_account(clients, accounts):
                print("New account successfully created.")

        elif input_option == "sa":
            if accounts:
                show_accounts(accounts)
            else:
                print("No accounts created yet.")

        elif input_option == "su":
            if clients:
                show_users(clients)
            else:
                print("No users created yet.")

        elif input_option == "q":
            print("Bye, have a nice day! :)")
            break

        else:
            print("Invalid Option")


if __name__ == "__main__":
    main()
