import os
import sys
from datetime import datetime, timedelta

import httpx
import requests
from database import Base, SessionLocal, engine
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from models import Streak, User
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

load_dotenv()
github_client_id = os.getenv("GITHUB_CLIENT_ID")
github_secret = os.getenv("GITHUB_SECRET")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# token = os.getenv("TEST_AUTH")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class StreakTracker:
    def __init__(self, username: str, db: Session):
        self.db = db
        self.username = username
        self.streak = self.get_or_create_streak()
        self.max_streak_between_dates = 0
        self.current_streak_between_dates = 0
        self.longest_streak_since_joining = 0
        self.last_date_checker = None
        self.date_list = set()
        self.count = 0

    def get_or_create_streak(self):
        streak = self.db.query(Streak).filter(
            Streak.username == self.username).first()
        if not streak:
            streak = Streak(username=self.username, current_streak=0,
                            longest_streak_between_dates=0, longest_streak_since_joining=0)
            self.db.add(streak)
            self.db.commit()
            self.db.refresh(streak)
        return streak

    def update_streak(self, contribution_date: datetime.date):
        print(contribution_date)
        if self.last_date_checker is None or contribution_date == self.last_date_checker + timedelta(days=-1):
            self.current_streak_between_dates += 1
        elif contribution_date == self.last_date_checker:
            self.current_streak_between_dates = self.current_streak_between_dates
        else:
            self.current_streak_between_dates = 1

        self.date_list.add(contribution_date)
        self.streak.longest_streak_between_dates = max(
            self.streak.longest_streak_between_dates, self.current_streak_between_dates)
        self.streak.last_contribution_date = max(self.date_list)

        print(self.current_streak_between_dates)
        self.count += 1
        self.last_date_checker = contribution_date
        self.db.commit()
        self.db.refresh(self.streak)

    def calculate_longest_streak_since_joining(self, dictt: dict):
        sorted_dates = sorted(datetime.strptime(
            date, "%Y-%m-%d").date() for date in dictt.keys())

        current_streak = 1
        longest_streak = 1

        for i in range(1, len(sorted_dates)):
            if sorted_dates[i] - sorted_dates[i-1] == timedelta(days=1):
                current_streak += 1
            else:
                longest_streak = max(longest_streak, current_streak)
                current_streak = 1

        longest_streak = max(longest_streak, current_streak)

        print(f"Longest streak: {longest_streak}")

        self.longest_streak_since_joining = longest_streak
        self.streak.longest_streak_since_joining = longest_streak
        self.db.commit()

    def calculate_current_streak(self, contributions: dict):
        sorted_dates = sorted(datetime.strptime(date, "%Y-%m-%d").date()
                              for date in contributions.keys())
        today = datetime.now().date()

        current_streak = 0
        for date in reversed(sorted_dates):
            if (today - date).days > current_streak:
                break
            current_streak += 1

        self.streak.current_streak = current_streak
        self.db.commit()

    def reset_streak_data(self):
        self.streak.longest_streak_between_dates = 0
        self.streak.last_contribution_date = None
        self.db.commit()

    def get_streak_info(self):
        self.db.refresh(self.streak)
        return {
            "current_streak": self.streak.current_streak,
            "longest_streak_since_joining": self.streak.longest_streak_since_joining,
            "max_streak_between_input_dates": self.streak.longest_streak_between_dates,
            "last_contribution_date":  str(self.streak.last_contribution_date),
        }


class Contributions:
    def __init__(self, username="", token="", start_date="", end_date="",  db: Session = Depends(get_db)):
        self.username = username
        self.token = token
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        self.contributions = {}
        self.header = {"Authorization": "token " + self.token}
        self.db = db
        self.streak_tracker = StreakTracker(username, db)
        self.streak_tracker.count = 0
        self.streak_tracker.longest_streak_since_joining = 0
        self.join_date = None
        self.all_contributions = {}
        self.user = self.get_or_create_user()

    def get_or_create_user(self):
        user = self.db.query(User).filter(
            User.username == self.username).first()
        if not user:
            user = User(username=self.username, contributions={})
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        return user

    def correct_dates(self, date_str, checker):
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            if date_obj.year < 2008:
                sys.exit("Github wasn't even founded before 2008. Try again.")
            date_obj = date_obj + timedelta(days=checker)
            return str(date_obj), None
        except:
            sys.exit("Invalid input(s). Try again.")

    def initialize(self):
        ds_obj = self.start_date
        du_obj = self.end_date
        diff = (du_obj - ds_obj).days + 1
        for i in range(diff):
            d = str(ds_obj + timedelta(days=i))
            self.contributions[d] = 0

    def process_contribution(self, date_str):
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        self.all_contributions[date_str] = self.all_contributions.get(
            date_str, 0) + 1
        if date_str in self.contributions:
            self.contributions[date_str] += 1
            self.streak_tracker.update_streak(
                date_obj)

    def get(self):
        self.streak_tracker.reset_streak_data()
        self.streak_tracker.current_streak_between_dates = 0
        self.streak_tracker.max_streak_between_dates = 0
        self.streak_tracker.last_date_checker = None
        self.streak_tracker.date_list.clear()

        def check_status(z):
            return z.status_code == 200

        self.initialize()

        user_url = f"https://api.github.com/users/{self.username}"
        user_response = requests.get(user_url, headers=self.header)
        if check_status(user_response):
            user_response = user_response.json()
            self.join_date = datetime.strptime(
                user_response["created_at"][:10], "%Y-%m-%d").date()

        all_repos_url = "https://api.github.com/user/repos"
        all_repos_response = requests.get(all_repos_url, headers=self.header)
        if check_status(all_repos_response):
            all_repos_response = all_repos_response.json()

            for a in all_repos_response:
                repo_name = a["name"]
                repo_owner = a["owner"]["login"]

                commits_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?since={self.join_date}"
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
                        self.process_contribution(commit_date)

        issues_url = f"https://api.github.com/issues?filter=created&since={self.join_date}"
        issues_response = requests.get(issues_url, headers=self.header)

        if check_status(issues_response):
            issues_response = issues_response.json()
            for i in issues_response:
                issue_date = i["created_at"][:10]
                self.process_contribution(issue_date)

        self.streak_tracker.calculate_longest_streak_since_joining(
            self.all_contributions)
        self.streak_tracker.calculate_current_streak(self.all_contributions)
        streak_info = self.streak_tracker.get_streak_info()
        self.user.contributions = self.contributions
        self.db.commit()
        print(streak_info)
        return {
            "contributions": list(self.contributions.values()),
            "streak_info": streak_info,
            "join_date": str(self.join_date),
            "max_streak_between_input_dates": streak_info["max_streak_between_input_dates"]
        }


@app.get("/contributions")
def output(request: Request, username: str, start_date: str, end_date: str, access_token: str, db: Session = Depends(get_db)):

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://api.github.com/user", headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid access token")

    user_data = response.json()
    if user_data["login"] != username:
        raise HTTPException(
            status_code=403, detail="You can only access your own data")

    result = Contributions(username, access_token, start_date, end_date, db)
    try:
        r = result.get()['contributions']
        return JSONResponse(content=r)
    except HTTPException as e:
        return JSONResponse(content={"error": str(e)})


@app.get("/login")
async def login():
    return RedirectResponse(
        f"https://github.com/login/oauth/authorize?client_id={github_client_id}&redirect_uri=http://localhost:8000/github-code",
        status_code=302,
    )


@app.get("/github-code")
async def github_code(code: str, request: Request):
    params = {"client_id": github_client_id,
              "client_secret": github_secret, "code": code}
    headers = {"Accept": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url="https://github.com/login/oauth/access_token", params=params, headers=headers
        )
        response_json = response.json()
        access_token = response_json["access_token"]
        print(access_token)

    headers["Authorization"] = f"Bearer {access_token}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url="https://api.github.com/user", headers=headers)
        response_json = response.json()
        username = response_json["login"]
        res = RedirectResponse(
            url=f"http://localhost:5173/page?username={username}&access_token={access_token}")
        return res


@app.get("/streak-history")
def get_streak_history(username: str, db: Session = Depends(get_db)):
    streak = db.query(Streak).filter(Streak.username == username).first()
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return JSONResponse(content={"error": "User does not exist. Use the contribution finder first"})

    if not streak:
        return JSONResponse(content={"error": "No streak data found for this user"})

    response_data = {
        "Streak_for_which_data_is_shown": user.contributions,
        "current_streak": streak.current_streak,
        "longest_streak_between_selected_dates": streak.longest_streak_between_dates,
        "longest_streak_since_joining": streak.longest_streak_since_joining,
        "last_contribution_date": str(streak.last_contribution_date) if streak.last_contribution_date else None,

    }
    print(response_data)
    return JSONResponse(content=response_data)
