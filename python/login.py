import json
import os


class Account:
    def __init__(self, email, newsletter):
        self.email = email
        self.newsletter = newsletter
        self.warnings = 0
        self.status = [None, ""]
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def signup(self):
        self.email = self.email.strip()
        filepath = os.path.join(self.BASE_DIR, '../static', 'database', "accounts.json")
        with open(filepath, "r") as file:

            accounts = json.load(file)

        account = next((user for user in accounts if user["email"] == self.email), None)

        if not account:
            accounts.append({"email": self.email, "newsletter": self.newsletter, "warnings" : self.warnings})
            with open(filepath, "w") as account_file:
                json.dump(accounts, account_file, indent=0)

            self.status = [True, "Successfully registered and logged in!"]

        else:
            self.warnings = account['warnings']

            if self.warnings < 3:
                self.status = [True, "Account already exists, but logged in anyways."]
            else:
                self.status = [False, "Account has had too many warnings and cannot be used!"]


    def warning(self):
        if self.warnings < 3:
            self.warnings += 1
        else:
            self.signup()


if __name__ == '__main__':
    pass
