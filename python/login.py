"""
login.py

Has a class for initializing an account and handles all
the things an account could be used for in our website.

Auth: Tristan Kruithof
Date: 10/04/2026
Version: 1.0
PEP-8:
"""

import json
import os
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_validator import validate_email


class Account:
    def __init__(self, email="", newsletter="", admin=False, active=False):
        """
        Initializes an Account object and calls the check_date function.

        :param str email: Email of the account
        :param bool newsletter: If the account wants a newsletter
        :param bool admin: If account is an admin
        :param bool active: If account is active
        """
        # Paths
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.filepath_acc = os.path.join(self.BASE_DIR, '../static', 'database', "accounts.json")
        self.filepath_time = os.path.join(self.BASE_DIR, '../static', 'database', "time")
        self.newick_path = os.path.join(self.BASE_DIR, '../Tools', 'ete4_input', "newick.nwk")

        # Accounts variables
        self.email = email.strip()
        self.newsletter = bool(newsletter)
        self.runs = 0
        self.status = [active, ""]
        self.accounts = []
        self.account = {}
        self.admin = admin

        # Password and check_date call
        self.secret_password = "ditiseensupergeheimwachtwoord"
        self.check_date()


    def __str__(self):
        """
        Returns a string with the current account information and status

        :return: str : with current account information
        """
        # When printing an object this returns
        return f"Email: {self.email}, Newsletter: {self.newsletter}, Admin {self.admin}, Runs: {self.runs}, Status: {self.status}"


    def check_date(self):
        """
        Checks if the current time is equal to the time in the file, time.
        If so calls reset_runs.

        :return: None
        """
        with open(self.filepath_time, "r+") as time_file:
            time = time_file.read()
            # Gets the current time but only the date as string
            time_now = str(datetime.datetime.now().date())
            if time == time_now:
                pass
            else:
                # Goes to the beginning of the file and deletes the contents
                time_file.truncate(0)
                time_file.seek(0)
                # Writes the new time
                time_file.write(time_now)
                self.reset_runs()


    def load_accounts(self):
        """
        Opens the account file and gets the current account and all the accounts.

        :return: None
        """
        with open(self.filepath_acc, "r") as account_file:
            # Opens the file and sets it to accounts
            self.accounts = json.load(account_file)
            # Checks if account is equal to current email and if so saves it as account
            self.account = next((user for user in self.accounts if user["email"] == self.email), {})
            # If the account exists update the other account variables.
            if self.account:
                self.newsletter = self.account['newsletter']
                self.runs = self.account['runs']
                self.admin = self.account['admin']


    def save_accounts(self):
        """
        Saves the current account to the accounts file or all the accounts.

        :return:
        """
        with open(self.filepath_acc, "w") as account_file:
            # If something is in account replace the current version of the account in accounts
            if self.account:
                acc_index = next(idx for idx, user in enumerate(self.accounts) if user['email'] == self.account['email'])
                self.accounts[acc_index] = self.account
            # Dump the new accounts in the accounts file
            json.dump(self.accounts, account_file, indent=2)


    def signin(self, password=""):
        """
        Calls the load_accounts function and checks if the current account is already in the file, if so
        it handles it and else it writes it to the new file. Can also be given a password to signin as an admin
        if your account does not yet exist. Also checks if the domain of the email is legit and does exist.

        :param str password: Password to sign in, if given.
        :return: None
        """
        # Loads the account
        self.load_accounts()

        # If the account already exists run the else otherwise...
        if not self.account:
            # Tries to verify email that was filled in and check if the domain of the email is real
            try:
                # Uses the email_validator library that does stated above
                verified = validate_email(self.email, check_deliverability=True)
                self.email = verified.normalized
                # If a password was given check if it's the same as the secret password if so
                # Make the user an admin
                if password:
                    self.admin = self.secret_password == password.lower().strip()

                # Adds a new account to accounts if it did not exist
                self.accounts.append({"email": self.email, "newsletter": self.newsletter, "runs" : self.runs, "admin": self.admin, "trees" : {}})
                self.save_accounts()

                if self.admin:
                    self.status = [True, "Successfully registered and logged in as admin! |"]
                else:
                    self.status = [True, "Successfully registered and logged in! |"]

            except Exception as e:
                self.status = [False, f"Email is invalid | {str(e)}"]
        else:
            self.runs = self.account['runs']
            self.admin = self.account['admin']

            # Logic that follows after getting the runs and admin status of the current account
            if self.runs < 10 and not self.admin:
                self.status = [True, "Account already exists, but logged in anyways. |"]
            elif self.runs < 10 and self.admin:
                self.status = [True, "Account already exists, but logged in anyways as admin. |"]
            elif self.runs >= 10 and not self.admin:
                self.status = [False, "Account has had too many runs and cannot be used!"]
            else:
                self.status = [True, "Account has had more than 10 runs, but logged in anyways as admin. |"]


    def send_newsletter(self, title="", body="", exclude=True):
        """
        Sends a newsletter to the accounts that have it enabled, can
        exclude current account. Calls load_accounts to check for
        newsletter accounts.

        :param str title: The title of the newsletter
        :param str body: The body of the newsletter
        :param bool exclude: True if you want your own account excluded
        :return: self.status
        """
        # Checks if a title and body were given
        if title and body:
            self.load_accounts()
            accounts = self.accounts
            # Makes a bool of exclude so logic can be aplied
            bool(exclude)

            accounts = [user for user in accounts if user["newsletter"]]
            # If the user wants to be excluded, and they are subscribed, remove them from
            # The local accounts list
            if exclude and self.newsletter:
                accounts = [user for user in accounts if not user["email"] == self.email]

            # If there are still accounts left in the local list run this
            if accounts:
                # My test email address
                sender = "tristankruithof19@gmail.com"
                # The password is an app password that I had to request
                # This is generally not safe to share, but I wanted to
                # Deliver a working addition to the site
                password = "xske qevv xtyu xovp"

                # Uses smpt library to send a very simple email
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
        """
        Adds a new run to the current saved account or the email that was given.

        :param str email: Email for where to add a run
        :return: self.status
        """
        if email:
            self.email = email

        self.load_accounts()

        # Checks if the current account exists
        if self.account:
            runs = self.account['runs']
            # If it has been 10 runs return False
            if runs >= 10:
                self.status = [False, "Too many runs!"]
                return self.status
            # Otherwise add +1 to the runs of the current account
            else:
                self.account['runs'] += 1
                self.save_accounts()

                self.status = [True, ""]
                return self.status

        self.status = [False, "No account added!"]
        return self.status


    def save_tree(self, tree_name):
        """
        Checks if the tree name already exists and links it to the
        current newick file and writes that into the current account
        and saves it in account.json.

        :param str tree_name: name for the tree
        :return: None
        """
        # Checks if there's a newick at all just as a fail-safe
        # If so it opens it and reads it.
        if os.path.exists(self.newick_path):
            with open(os.path.join(self.newick_path), "r") as tree_file:
                tree_newick = tree_file.read()
                # loads accounts and gets the trees from the current account
                self.load_accounts()

                if self.account:
                    trees = self.account['trees']

                    # Checks for name duplicates and otherwise adds the tree name as
                    # A dict linked to the newick
                    if tree_name in trees:
                        self.status = [False, "Tree already exists!"]
                    else:
                        trees[tree_name] = tree_newick
                        self.account['trees'] = trees
                        self.save_accounts()

                        self.status = [True, "Tree saved!"]
                else:
                    self.status = [False, "Account does not exist!"]
        else:
            self.status = [False, "No newick found!"]


    def reset_runs(self):
        """
        Resets the runs counter to 0 for all accounts.
        And gets called when the time is different in the file.

        :return: None
        """
        self.load_accounts()

        # Resets the runs for all users
        for user in self.accounts:
            user['runs'] = 0

        self.save_accounts()


if __name__ == '__main__':
    test_account = Account("test@gmail.com")
    test_account.signin()
    print(test_account)