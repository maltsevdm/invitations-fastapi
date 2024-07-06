import json

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader

from src.config import PASSWORD
from src.schemas import AnketaSchema, Guest, GuestUpdate, Sex
from src.telegram import send_by_telegram

db_file = "db.json"
guests: dict[str, Guest] = {}
with open(db_file) as file:
    for _id, guest in json.load(file).items():
        guests[_id] = Guest.model_validate_json(guest)


def write_to_db():
    with open(db_file, "w") as file:
        data = {_id: guest.model_dump_json() for _id, guest in guests.items()}
        json.dump(data, file, indent=4, ensure_ascii=False)


app = FastAPI()

origins = ["http://localhost"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/guest/all")
async def get_all_guests() -> dict[str, Guest]:
    return guests


@app.post("/guest/create")
async def add_guest(sid: str, guest: Guest, password: str) -> str:
    if password != PASSWORD:
        raise HTTPException(status_code=401, detail="Неправильный пароль")

    if sid in guests:
        raise HTTPException(status_code=400, detail="Гость с таким ID уже существует")
    guests[sid] = guest
    write_to_db()
    return "Гость добавлен"


@app.patch("/guest/{sid}")
async def update_guest(sid: str, data: GuestUpdate, password: str) -> dict:
    if password != PASSWORD:
        raise HTTPException(status_code=401, detail="Неправильный пароль")

    if sid not in guests:
        raise HTTPException(status_code=400, detail="Гость с таким sid не найден")

    data_dict = data.model_dump()

    for k, v in data_dict.items():
        if v is not None:
            guests[sid][k] = v

    write_to_db()
    return guests[sid]


@app.delete("/guest/{sid}")
async def delete_guest(sid: str, password: str) -> Response:
    if password != PASSWORD:
        raise HTTPException(status_code=401, detail="Неправильный пароль")

    if sid not in guests:
        raise HTTPException(status_code=400, detail="Гость с таким sid не найден")

    del guests[sid]
    write_to_db()
    return Response(status_code=200)


@app.get("/{sid}")
async def get_guest_page(sid: str):
    if sid not in guests:
        raise HTTPException(status_code=404, detail="Гостя нет в списке :(")

    environment = Environment(
        loader=FileSystemLoader("frontend/"),
        comment_start_string="{=",
        comment_end_string="=}",
    )
    names = guests[sid].names
    sex = guests[sid].sex
    print(sex)
    if not sex:
        template = environment.get_template("index_many.html")
    elif sex == Sex.female:
        template = environment.get_template("index_female.html")
    else:
        template = environment.get_template("index_male.html")

    if len(names) > 1:
        names = ", ".join(names[:-1]) + " и " + names[-1]
    else:
        names = names[0]

    content = template.render(names=names.upper())

    return HTMLResponse(content=content)


@app.post("/send_to_tg")
async def send_to_telegram(password: str, anketa: AnketaSchema):
    if password != PASSWORD:
        raise HTTPException(status_code=401, detail="Неправильный пароль")

    text = f"""📌 ID гостя: {anketa.id}
📌 Присутствие: {"✅" if anketa.accept else "❌"}"""

    if anketa.children is not None:
        text += f"\n👨‍👨‍👦 Дети: {"✅" if anketa.children else "❌"}"

    if anketa.drinks:
        text += "\n🥂 Напитки: " + ", ".join(anketa.drinks)

    if anketa.comment:
        text += f"\n✏️ Коммент: {anketa.comment}"

    await send_by_telegram(text)


app.mount("/", StaticFiles(directory="frontend"), name="static")
