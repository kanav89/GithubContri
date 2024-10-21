from fastapi import Depends, HTTPException, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from database import get_db
from models import User,OAuth2Token
from authlib.integrations.starlette_client import OAuth,OAuthError
from starlette.config import Config

config = Config('.env')
oauth = OAuth(config)

oauth.register(
    name='github',
    client_id=config('GITHUB_CLIENT_ID'),
    client_secret=config('GITHUB_SECRET'),
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
)



async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.github.authorize_redirect(request, redirect_uri)

async def auth(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.github.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')    
    resp = await oauth.github.get('user', token=token)
    user_data = resp.json()
    
    username = user_data['login']
    access_token = token['access_token']

    try:
        user = db.query(User).filter(User.username == username).first()
        if user:
            user.access_token = access_token
        else:
            user = User(username=username, access_token=access_token)
            db.add(user)
        db.commit()
        db.refresh(user)

        # Update or create OAuth2Token
        oauth2_token = db.query(OAuth2Token).filter(OAuth2Token.user_id == user.id).first()
        if oauth2_token:
            oauth2_token.access_token = access_token
            oauth2_token.expires_at = token.get('expires_at')
        else:
            oauth2_token = OAuth2Token(
                user_id=user.id,
                name='github',
                token_type=token.get('token_type', 'bearer'),
                access_token=access_token,
                expires_at=token.get('expires_at')
            )
            db.add(oauth2_token)
        db.commit()

        # Set session data
        request.session['user_id'] = user.id
        request.session['username'] = username

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")

    return RedirectResponse(url=f"http://localhost:5173/page?username={username}")