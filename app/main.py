from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from .routes import users_router, chats_router
from fastapi.middleware.cors import CORSMiddleware

KEYCLOAK_URL = "http://localhost:8080/realms/myrealm"
KEYCLOAK_CIENT_ID = "myclient"
KEYCLOAK_CLIENT_SECRET = "EgwvLRKOmHGYyNuQaWGipzm2U61WD2DO"
KEYCLOAK_API_URL = f"{KEYCLOAK_URL}/protocol/openid-connect/token"

app = FastAPI(title="FastAPI + Postgres")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(users_router)
app.include_router(chats_router)

@app.get("/")
def health():
    return {"status": "ok"}