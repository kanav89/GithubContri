import os
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TEST_AUTH")


class StreakTracker:
    def __init__(self, username: str):
        self.username = username
        self.current_streak = 0
        self.longest_streak = 0
        self.last_contribution_date = None
        self.streak_history = {}

    def update_streak(self, contribution_date: datetime.date):
        if not self.last_contribution_date:
            self.current_streak = 1
        elif contribution_date == self.last_contribution_date + timedelta(days=1):
            self.current_streak += 1
        elif contribution_date > self.last_contribution_date:
            self.current_streak = 1
        else:
            # If the contribution date is before the last contribution date,
            # we don't update the streak (this handles out-of-order updates)
            return

        self.last_contribution_date = contribution_date

        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak

        self.update_streak_history(contribution_date)

    def update_streak_history(self, contribution_date: datetime.date):
        year = str(contribution_date.year)
        if year not in self.streak_history:
            self.streak_history[year] = {}
        self.streak_history[year][str(contribution_date)] = self.current_streak

    def get_streak_info(self):
        return {
            "current_streak": self.current_streak,
            "longest_streak": self.longest_streak,
            "last_contribution_date": str(self.last_contribution_date) if self.last_contribution_date else None,
            "streak_history": self.streak_history
        }


class Contributions:
    def __init__(self, username="", token="", start_date="", end_date=""):
        self.username = username
        self.token = token
        self.start_date = start_date
        self.end_date = end_date
        self.contributions = {}
        self.header = {"Authorization": "token " + self.token}
        self.dates_commits = []
        self.dates_issues = []
        self.streak_tracker = StreakTracker(username)
        self.contribution_dates = set()

    def correct_dates(self, date_str, checker):
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            if date_obj.year < 2008:
                raise ValueError(
                    "Github wasn't even founded before 2008. Try again.")
            date_obj = date_obj + timedelta(days=checker)
            return str(date_obj)
        except ValueError as e:
            raise ValueError("Invalid input(s). Try again.") from e

    def initialize(self):
        self.DATE_SINCE = self.correct_dates(self.start_date, -1)
        self.DATE_UNTIL = self.correct_dates(self.end_date, 1)
        if self.DATE_SINCE >= self.DATE_UNTIL:
            raise ValueError(
                "Entered 'start date' must be before the entered 'end date'. Try again.")

        ds_obj = datetime.strptime(self.DATE_SINCE, "%Y-%m-%d").date()
        du_obj = datetime.strptime(self.DATE_UNTIL, "%Y-%m-%d").date()
        diff = (du_obj - ds_obj).days
        for i in range(1, diff):
            d = str(ds_obj + timedelta(days=i))
            self.contributions[d] = 0

    def process_contribution(self, date_str):
        if date_str in self.contributions:
            self.contributions[date_str] += 1
            self.contribution_dates.add(
                datetime.strptime(date_str, "%Y-%m-%d").date())

    def get(self):
        def check_status(z):
            return z.status_code == 200

        self.initialize()

        user_url = f"https://api.github.com/users/{self.username}"
        user_response = requests.get(user_url, headers=self.header)
        if check_status(user_response):
            user_response = user_response.json()
            user_date = user_response["created_at"][:10]
            self.process_contribution(user_date)

        repo_url = f"https://api.github.com/user/repos?since={self.DATE_SINCE}&type=owner"
        repo_response = requests.get(repo_url, headers=self.header)
        if check_status(repo_response):
            repo_response = repo_response.json()
            for r in repo_response:
                repo_date = r["created_at"][:10]
                if repo_date >= self.DATE_UNTIL:
                    continue
                self.process_contribution(repo_date)

        all_repos_url = "https://api.github.com/user/repos"
        all_repos_response = requests.get(all_repos_url, headers=self.header)
        if check_status(all_repos_response):
            all_repos_response = all_repos_response.json()

            for a in all_repos_response:
                repo_name = a["name"]
                repo_owner = a["owner"]["login"]

                commits_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?since={self.DATE_SINCE}"
                commits_response = requests.get(
                    commits_url, headers=self.header)

                if check_status(commits_response):
                    commits_response = commits_response.json()
                    for c in commits_response:
                        if "commit" not in c or "author" not in c["commit"] or "name" not in c["commit"]["author"]:
                            continue
                        if c["commit"]["author"]["name"] != self.username:
                            continue
                        commit_date = c["commit"]["author"]["date"][:10]
                        if commit_date >= self.DATE_UNTIL:
                            continue
                        self.process_contribution(commit_date)

        issues_url = f"https://api.github.com/issues?filter=created&since={self.DATE_SINCE}"
        issues_response = requests.get(issues_url, headers=self.header)

        if check_status(issues_response):
            issues_response = issues_response.json()
            for i in issues_response:
                issue_date = i["created_at"][:10]
                if issue_date >= self.DATE_UNTIL:
                    continue
                self.process_contribution(issue_date)

        # Update streaks for all contribution dates
        for date in sorted(self.contribution_dates):
            self.streak_tracker.update_streak(date)

        return {
            "contributions": list(self.contributions.values()),
            "streak_info": self.streak_tracker.get_streak_info()
        }


# Example usage
if __name__ == "__main__":
    username = "kanav89"
    start_date = "2024-01-01"
    end_date = "2024-05-05"

    contributions = Contributions(username, token, start_date, end_date)
    result = contributions.get()

    print("Contributions:", result["contributions"])
    print("Streak Info:", result["streak_info"])
