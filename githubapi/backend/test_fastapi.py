import os
import sys
import logging
from datetime import datetime, timedelta
from starlette.middleware.sessions import SessionMiddleware
from starlette.config import Config
import httpx
import requests
from database import Base, SessionLocal, engine
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from models import Goal, Streak, User,OAuth2Token
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal
from starlette.responses import JSONResponse
import secrets
from authlib.integrations.starlette_client import OAuth, OAuthError
from auth import login, auth, oauth
from fastapi import APIRouter
from starlette.middleware.sessions import SessionMiddleware



config = Config('.env')

load_dotenv()
github_client_id = os.getenv("GITHUB_CLIENT_ID")
github_secret = os.getenv("GITHUB_SECRET")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# token = os.getenv("TEST_AUTH")
app = FastAPI()
router = APIRouter()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class GoalCreate(BaseModel):
    username: str
    goal_type: str
    target: int


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
            user = User(username=self.username,
                        access_token=self.token, contributions={})
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
def output(request: Request, username: str, start_date: str, end_date: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    access_token = user.access_token
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token not found")

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
async def login_route(request: Request):
    return await login(request)

@router.get("/auth",name="auth")
async def auth_route(code: str, request: Request, db: Session = Depends(get_db)):
    return await auth( request, db)


@app.get('/logout')
async def logout(request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')


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


@app.post("/set-goal")
async def set_goal(goal: GoalCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == goal.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    start_date = datetime.now().date()
    if goal.goal_type == "daily":
        end_date = start_date
    elif goal.goal_type == "weekly":
        end_date = start_date + timedelta(days=6)
    elif goal.goal_type == "monthly":
        end_date = (start_date.replace(day=1) + timedelta(days=32)
                    ).replace(day=1) - timedelta(days=1)
    else:
        raise HTTPException(status_code=400, detail="Invalid goal type")

    new_goal = Goal(username=goal.username, goal_type=goal.goal_type,
                    target=goal.target, start_date=start_date, end_date=end_date)
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)
    return {"message": "Goal set successfully"}


@app.get("/get-goals")
def get_goals(username: str, db: Session = Depends(get_db)):
    goals = db.query(Goal).filter(Goal.username == username).all()
    return goals


@app.get("/check-goal-progress")
def check_goal_progress(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    access_token = user.access_token
    # username = user.username
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token not found")

    goals = db.query(Goal).filter(Goal.username == username).all()
    progress = []

    for goal in goals:
        end_date = min(goal.end_date, datetime.now().date())
        contri = Contributions(username, access_token, str(
            goal.start_date), str(end_date), db)
        contributions_data = contri.get()
        contributions = sum(contributions_data['contributions'])

        progress.append({
            "goal_type": goal.goal_type,
            "target": goal.target,
            "current": contributions,
            "start_date": str(goal.start_date),
            "end_date": str(goal.end_date),
            "is_completed": datetime.now().date() > goal.end_date,
            "is_achieved": contributions >= goal.target
        })

    return progress


@app.put("/update-goal/{goal_id}")
def update_goal(goal_id: int, goal_type: str, target: int, db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    goal.goal_type = goal_type
    goal.target = target
    db.commit()
    return {"message": "Goal updated successfully"}


@app.delete("/delete-goal/{goal_id}")
def delete_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    db.delete(goal)
    db.commit()
    return {"message": "Goal deleted successfully"}


app.include_router(router)