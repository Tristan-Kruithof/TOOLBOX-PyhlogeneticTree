import json
import os
import datetime
from email_validator import validate_email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Account:
    def __init__(self, email="", newsletter="", admin=False, **kwargs):
        self.email = email.strip()
        self.newsletter = bool(newsletter)
        self.runs = 0
        self.status = [None, ""]
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.filepath_acc = os.path.join(self.BASE_DIR, '../static', 'database', "accounts.json")
        self.filepath_time = os.path.join(self.BASE_DIR, '../static', 'database', "time")
        self.accounts = None
        self.account = None
        self.admin = admin
        self.secret_password = "ditiseensupergeheimwachtwoord"
        self.check_date()


    def __str__(self):
        return f"Email: {self.email}, Newsletter: {self.newsletter}, Admin {self.admin}, Runs: {self.runs}, Status: {self.status}"


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
            self.account = next((user for user in self.accounts if user["email"] == self.email), None)
            if self.account:
                self.newsletter = self.account['newsletter']
                self.runs = self.account['runs']
                self.admin = self.account['admin']


    def save_accounts(self, account_list):
        with open(self.filepath_acc, "w") as account_file:
            json.dump(account_list, account_file, indent=2)


    def signin(self, password=""):
        self.load_accounts()
        
        if not self.account:
            try:
                print(self.email)
                verified = validate_email(self.email, check_deliverability=True)
                self.email = verified.normalized

                if password:
                    self.admin = self.secret_password == password.lower().strip()

                self.accounts.append({"email": self.email, "newsletter": self.newsletter, "runs" : self.runs, "admin": self.admin})
                self.save_accounts(self.accounts)

                if self.admin:
                    self.status = [True, "Successfully registered and logged in as admin! |"]
                else:
                    self.status = [True, "Successfully registered and logged in! |"]

            except Exception as e:
                self.status = [False, f"Email is invalid | {str(e)}"]

        else:
            self.runs = self.account['runs']
            self.admin = self.account['admin']

            if self.runs < 10 and not self.admin:
                self.status = [True, "Account already exists, but logged in anyways. |"]
            elif self.runs < 10 and self.admin:
                self.status = [True, "Account already exists, but logged in anyways as admin. |"]
            elif self.runs >= 10 and not self.admin:
                self.status = [False, "Account has had too many runs and cannot be used!"]
            else:
                self.status = [True, "Account has had more than 10 runs, but logged in anyways as admin. |"]


    def send_newsletter(self, title="", body="", exclude=True):
        if title and body:
            self.load_accounts()
            accounts = self.accounts
            bool(exclude)

            accounts = [user for user in accounts if user["newsletter"]]

            if exclude and self.newsletter:
                accounts = [user for user in accounts if not user["email"] == self.email]

            if accounts:
                sender = "tristankruithof19@gmail.com"
                password = "xske qevv xtyu xovp"

                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(sender, password)
                    for account in accounts:
                        email = account['email']
                        msg = MIMEMultipart()
                        msg['From'] = sender
                        msg['To'] = email
                        msg['Subject'] = title
                        msg.attach(MIMEText(body, "plain"))
                        server.sendmail(sender, email, msg.as_string())

            self.status = [True, "Newsletter sent!"]
            return self.status
        else:
            self.status = [False, "No title or body was given!"]
            return self.status


    def add_run(self, email=''):
        if email:
            self.email = email
        self.load_accounts()
        if self.account:
            runs = self.account['runs']
            if runs >= 10:
                self.status = [False, "Too many runs!"]
                return self.status
            else:
                for user in self.accounts:
                    if user['email'] == self.account['email']:
                        user['runs'] += 1

                self.save_accounts(self.accounts)

                self.status = [True, ""]
                return self.status

        self.status = [False, "No account added!"]
        return self.status


    def reset_runs(self):
        self.load_accounts()

        for user in self.accounts:
            user['runs'] = 0

        self.save_accounts(self.accounts)


if __name__ == '__main__':
    test_account = Account("test@gmail.com")
    test_account.signin()
    print(test_account)
