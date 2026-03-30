import json
import os
import datetime


class Account:
    def __init__(self, email="", newsletter=""):
        self.email = email
        self.newsletter = newsletter
        self.runs = 0
        self.status = [None, ""]
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.filepath_acc = os.path.join(self.BASE_DIR, '../static', 'database', "accounts.json")
        self.filepath_time = os.path.join(self.BASE_DIR, '../static', 'database', "time")
        self.accounts = None
        self.check_date()


    def check_date(self):
        with open(self.filepath_time, "r+") as time_file:
            time = time_file.read()
            time_now = str(datetime.datetime.now().date())
            if time == time_now:
                pass
            else:
                time_file.truncate(0)
                time_file.seek(0)

                time_file.write(time_now)
                self.reset_runs()


    def load_accounts(self):
        with open(self.filepath_acc, "r") as account_file:
            self.accounts = json.load(account_file)
            account = next((user for user in self.accounts if user["email"] == self.email), None)

        return account


    def save_accounts(self, account_list):
        with open(self.filepath_acc, "w") as account_file:
            json.dump(account_list, account_file, indent=2)


    def signin(self):
        self.email = self.email.strip()

        account = self.load_accounts()

        if not account:
            if self.newsletter:
                self.newsletter = True

            self.accounts.append({"email": self.email, "newsletter": self.newsletter, "runs" : self.runs})
            self.save_accounts(self.accounts)

            self.status = [True, "Successfully registered and logged in! |"]

        else:
            self.runs = account['runs']

            if self.runs < 10:
                self.status = [True, "Account already exists, but logged in anyways. |"]
            else:
                self.status = [False, "Account has had too many runs and cannot be used! |"]


    def send_newsletter(self):
        pass


    def add_run(self, email=''):
        if email:
            self.email = email
        account = self.load_accounts()
        if account:
            runs = account['runs']
            if runs >= 10:
                return False, "Too many runs!"
            else:
                for user in self.accounts:
                    if user['email'] == account['email']:
                        user['runs'] += 1

                self.save_accounts(self.accounts)

                return True, ""

        return False, "No account added!"


    def reset_runs(self):
        self.load_accounts()

        for user in self.accounts:
            user['runs'] = 0

        self.save_accounts(self.accounts)


if __name__ == '__main__':
    pass
