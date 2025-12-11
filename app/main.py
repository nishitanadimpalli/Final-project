from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pathlib import Path
from fastapi import Response

from app.routers import users, auth, calculations


app = FastAPI()

# -------------------------------------------
# CORS (allow frontend to call backend)
# -------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # you can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------
# Routers
# -------------------------------------------
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(calculations.router)

# -------------------------------------------
# Static Directory Setup
# -------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"


# -------------------------------------------
# Serve Pages
# -------------------------------------------
@app.get("/", response_class=HTMLResponse)
def root():
    return FileResponse(STATIC_DIR / "login.html")

@app.get("/login-page")
def login_page():
    file = (STATIC_DIR / "login.html").read_text()
    return Response(content=file, media_type="text/html",
                    headers={"Cache-Control": "no-cache, no-store, must-revalidate"})

@app.get("/register-page")
def register_page():
    file = (STATIC_DIR / "register.html").read_text()
    return Response(content=file, media_type="text/html",
                    headers={"Cache-Control": "no-cache, no-store, must-revalidate"})


@app.get("/calculations-page", response_class=HTMLResponse)
def calculations_page():
    return FileResponse(STATIC_DIR / "calculations.html")

@app.get("/stats-page", response_class=HTMLResponse)
def stats_page():
    return FileResponse(STATIC_DIR / "stats.html")
