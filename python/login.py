import json
import os


class Account:
    def __init__(self, email, newsletter):
        self.email = email
        self.newsletter = newsletter
        self.warnings = 0
        self.status = [None, ""]
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.filepath = os.path.join(self.BASE_DIR, '../static', 'database', "accounts.json")
        self.accounts = None


    def load_accounts(self):
        with open(self.filepath, "r") as account_file:
            self.accounts = json.load(account_file)

        return self.accounts


    def save_accounts(self, account_list):
        with open(self.filepath, "w") as account_file:
            json.dump(account_list, account_file, indent=2)


    def signin(self):
        self.email = self.email.strip()

        accounts = self.load_accounts()
        account = next((user for user in accounts if user["email"] == self.email), None)

        if not account:
            if self.newsletter:
                self.newsletter = True

            accounts.append({"email": self.email, "newsletter": self.newsletter, "warnings" : self.warnings})
            self.save_accounts(accounts)

            self.status = [True, "Successfully registered and logged in! |"]

        else:
            self.warnings = account['warnings']

            if self.warnings < 3:
                self.status = [True, "Account already exists, but logged in anyways. |"]
            else:
                self.status = [False, "Account has had too many warnings and cannot be used!"]


    def send_newsletter(self):
        pass


    def warning(self):
        if self.warnings < 3:
            self.warnings += 1
        else:
            self.signin()


if __name__ == '__main__':
    pass
