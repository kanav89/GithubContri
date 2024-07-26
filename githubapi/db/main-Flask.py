#!/usr/local/bin/python3

import argparse
import sys
from datetime import datetime, timedelta

import requests
from flask import Flask, jsonify, request
from flask_restful import Api, Resource

github_app = Flask(__name__)
github_api = Api(github_app)


# github_app.app_context().push()


class Contributions(Resource):

    def __init__(self, username="", token="", start_date="", end_date=""):

        if username == token == start_date == end_date == "":
            args = request.args
            username = args.get("username")
            token = args.get("token")
            start_date = args.get("start_date")
            end_date = args.get("end_date")
            # if username is None : raise error

        self.username = username
        self.token = token
        self.start_date = start_date
        self.end_date = end_date
        self.contributions = {}

        # defining authentication header
        self.header = {"Authorization": "token " + self.token}

        # declaring list of dates
        self.dates_commits = []
        self.dates_issues = []

    def correct_dates(self, date_str, checker):
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            if date_obj.year < 2008:
                sys.exit("Github wasn't even founded before 2008. Try again.")
            date_obj = date_obj + timedelta(days=checker)
            return str(date_obj), None
        except:
            sys.exit("Invalid input(s). Try again.")  # modify acc to error

    def initialize(self):

        self.DATE_SINCE, e = self.correct_dates(self.start_date, -1)
        if e is not None:
            pass
            # throw http error
        self.DATE_UNTIL, e = self.correct_dates(self.end_date, 1)
        if e is not None:
            pass
            # throw http error
        if self.DATE_SINCE >= self.DATE_UNTIL:
            sys.exit("Entered 'start date' must be before the entered 'end date'. Try again.")

        ds_obj = datetime.strptime(self.DATE_SINCE, "%Y-%m-%d").date()
        du_obj = datetime.strptime(self.DATE_UNTIL, "%Y-%m-%d").date()
        diff = (du_obj - ds_obj).days
        for i in range(1, diff):
            d = str(ds_obj + timedelta(days=i))
            self.contributions[d] = 0

    def get(self):

        def check_status(z):
            return z.status_code == 200

        self.initialize()

        # if user joined within timeframe, count as a contribution
        user_url = f"https://api.github.com/users/{self.username}"
        user_response = requests.get(user_url, headers=self.header)
        if check_status(user_response):
            user_response = user_response.json()
            user_date = user_response["created_at"][:10]
            if user_date in self.contributions.keys():
                self.contributions[user_date] += 1

        # checking repos created in timeframe
        repo_url = f"https://api.github.com/user/repos?since={self.DATE_SINCE}&type=owner"
        repo_response = requests.get(repo_url, headers=self.header)
        if check_status(repo_response):
            repo_response = repo_response.json()
            for r in repo_response:
                repo_date = r["created_at"][:10]
                if repo_date >= self.DATE_UNTIL:
                    continue
                if repo_date in self.contributions.keys():
                    self.contributions[repo_date] += 1

        # fetching all repos
        all_repos_url = "https://api.github.com/user/repos"
        all_repos_response = requests.get(all_repos_url, headers=self.header)
        if check_status(all_repos_response):
            all_repos_response = all_repos_response.json()

            for a in all_repos_response:
                repo_name = a["name"]
                repo_owner = a["owner"]["login"]

                # checking commits made in specific repo
                commits_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?since={self.DATE_SINCE}"
                commits_response = requests.get(commits_url, headers=self.header)

                # remove checking for 'commit' not in c later
                if check_status(commits_response):
                    commits_response = commits_response.json()
                    for c in commits_response:
                        if "commit" not in c:
                            continue
                        if "author" not in c["commit"]:
                            continue
                        if "name" not in c["commit"]["author"]:
                            continue
                        if c["commit"]["author"]["name"] != self.username:
                            continue
                        commit_date = c["commit"]["author"]["date"][:10]
                        if commit_date >= self.DATE_UNTIL:
                            continue
                        # adding commit dates to list
                        self.dates_commits.append(commit_date)

        # checking issues created in timeframe
        issues_url = f"https://api.github.com/issues?filter=created&since={self.DATE_SINCE}"
        issues_response = requests.get(issues_url, headers=self.header)

        if check_status(issues_response):
            issues_response = issues_response.json()
            for i in issues_response:
                issue_date = i["created_at"][:10]
                if issue_date >= self.DATE_UNTIL:
                    continue
                # adding issue dates to list
                self.dates_issues.append(issue_date)

        # comparing commit dates and updating contributions
        for dc in self.dates_commits:
            if dc in self.contributions.keys():
                self.contributions[dc] += 1

        # comparing issue dates and updating contributions
        for di in self.dates_issues:
            if di in self.contributions.keys():
                self.contributions[di] += 1

        response = jsonify(list(self.contributions.values()))
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


github_api.add_resource(Contributions, "/contributions")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Get Contributions in GitHub")
    parser.add_argument(
        "--cli", action=argparse.BooleanOptionalAction, required=False, default=False
    )
    parser.add_argument("-u", dest="username", type=str, help="Enter Username", required=False)
    parser.add_argument("-t", dest="token", type=str, help="Enter token", required=False)
    parser.add_argument("-s", dest="start_date", type=str, help="Enter start date", required=False)
    parser.add_argument("-e", dest="end_date", type=str, help="Enter end date", required=False)
    args = parser.parse_args()

    username = args.username
    token = args.token
    start_date = args.start_date
    end_date = args.end_date

    if not (args.cli):
        github_app.run()
    else:
        c = Contributions(username, token, start_date, end_date)
        l, e = c.get()
        if e == 200:
            print(l)
        else:
            print("Error!")
