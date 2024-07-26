#!/usr/local/bin/python3
import os
import sys
from datetime import datetime, timedelta

import httpx
import requests
from database import SessionLocal, engine
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from models import Base, User
from sqlalchemy.orm import Session
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

load_dotenv()
github_client_id = os.getenv("GITHUB_CLIENT_ID")
github_secret = os.getenv("GITHUB_SECRET")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# Configure CORS


middleware = [
    Middleware(SessionMiddleware, secret_key="your-secret-key", https_only=True),
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
]

app = FastAPI(middleware=middleware)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)


class Contributions:
    def __init__(self, username="", token="", start_date="", end_date="", db: Session = None):
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
        self.db = db

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

        db_user = self.db.query(User).filter(User.username == self.username).first()
        if not db_user:
            db_user = User(username=self.username, contributions=self.contributions)
            self.db.add(db_user)
        else:
            db_user.contributions = self.contributions

        self.db.commit()

        return list(self.contributions.values())


result = Contributions()


@app.get("/contributions")
def output(
    request: Request, username: str, start_date: str, end_date: str, db: Session = Depends(get_db)
):
    token = request.session.get("access_token")
    print(f"access token from session:{token}")
    result = Contributions(username, token, start_date, end_date, db)
    try:
        r = result.get()
        return JSONResponse(content=r)
    except HTTPException as e:
        return JSONResponse(content=e)


@app.get("/login")
async def login():
    return RedirectResponse(
        f"https://github.com/login/oauth/authorize?client_id={github_client_id}&redirect_uri=https://github-contri-api.vercel.app/github-code",
        status_code=302,
    )


@app.get("/github-code")
async def github_code(code: str, request: Request):
    params = {"client_id": github_client_id, "client_secret": github_secret, "code": code}
    headers = {"Accept": "application/json"}
    async with httpx.AsyncClient() as client:

        response = await client.post(
            url="https://github.com/login/oauth/access_token", params=params, headers=headers
        )
        response_json = response.json()
        access_token = response_json["access_token"]
        request.session["access_token"] = access_token
    headers["Authorization"] = f"Bearer {access_token}"
    async with httpx.AsyncClient() as client:

        response = await client.get(url="https://api.github.com/user", headers=headers)
        response_json = response.json()
        # access_token = response_json["access_token"]
        # print("ok")
        username = response_json["login"]
        res = RedirectResponse(url=f"https://githubcontri.vercel.app/main?username={username}")
        return res
