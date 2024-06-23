import json

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from src.telegram import send_by_telegram
from fastapi.middleware.cors import CORSMiddleware

from src.config import PASSWORD

db_file = "db.json"

with open(db_file) as file:
    guests: list[dict] = json.load(file)


def write_to_db():
    with open(db_file, "w") as file:
        json.dump(guests, file, indent=4, ensure_ascii=False)


app = FastAPI()
app.mount("/frontend", StaticFiles(directory="frontend"), name="static")
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/guest/all")
async def get_all_guests() -> list[dict]:
    return guests


@app.post("/guest/create")
async def add_guest(guest: dict, password: str) -> str:
    if password != PASSWORD:
        raise HTTPException(status_code=401, detail="Неправильный пароль")

    for item in guests:
        if guest["id"] == item["id"]:
            raise HTTPException(
                status_code=400, detail="Гость с таким ID уже существует"
            )
    guests.append(guest)
    write_to_db()
    return "Гость добавлен"


@app.patch("/guest/{id}")
async def update_guest(id: str, data: dict, password: str) -> dict:
    if password != PASSWORD:
        raise HTTPException(status_code=401, detail="Неправильный пароль")

    for guest in guests:
        if guest["id"] == id:
            for k, v in data.items():
                guest[k] = v
            break
    else:
        raise HTTPException(status_code=400, detail="Гость с таким id не найден")

    write_to_db()
    return guest


@app.delete("/guest/{id}")
async def delete_guest(id: str, password: str) -> Response:
    if password != PASSWORD:
        raise HTTPException(status_code=401, detail="Неправильный пароль")

    for j, guest in enumerate(guests):
        if guest["id"] == id:
            i = j
            break
    else:
        raise HTTPException(status_code=400, detail="Гость с таким id не найден")

    del guests[i]
    write_to_db()
    return Response(status_code=200)


@app.get("/{id}")
async def get_guest_page(id: str):
    for guest in guests:
        if guest["id"] == id:
            break
    else:
        raise HTTPException(status_code=404)
    with open("frontend/index.html") as file:
        return HTMLResponse(content=file.read())


@app.get("/test/test")
async def test(message: str):
    await send_by_telegram("Отправка сообщения с кнопки на странице")


@app.on_event("shutdown")
async def shutdown():
    await send_by_telegram("Мне плохо! Я прилёг :(")
