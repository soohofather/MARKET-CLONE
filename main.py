from fastapi import FastAPI,UploadFile, Form, Response, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from typing import Annotated
import sqlite3

con = sqlite3.connect("db.db", check_same_thread = False)
cur = con.cursor()

cur.execute(f"""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                image BLOB,
                price INTEGER NOT NULL,
                description TEXT,
                place TEXT NOT NULL,
                insertAt INTEGER NOT NULL
            );
            """)
cur.execute(f"""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            );
            """)

app = FastAPI()

SECRET = "super_coding"

manager = LoginManager(SECRET, "/login.html")  

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서 요청 허용 (보안이 필요하면 특정 도메인 지정)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용 (GET, POST, OPTIONS 등)
    allow_headers=["*"],  # 모든 헤더 허용
)

@manager.user_loader()
def query_user(data):
    print(f"data: {data}")
    WHERE_STATEMENTS = f'id="{data}"'
    if type(data) == dict:
        WHERE_STATEMENTS = f'''id="{data['id']}'''
    print(WHERE_STATEMENTS)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    user = cur.execute(f"""
                       SELECT * from users WHERE {WHERE_STATEMENTS}
                       """).fetchone()

    return user

@app.post("/login")
def login(
    
    id : Annotated[str, Form()],
    password : Annotated[str, Form()]
):

    user = query_user(id)
    if not user:
        raise InvalidCredentialsException
    elif password != user["password"]:
        raise InvalidCredentialsException
    
    access_token = manager.create_access_token(
        data={
            "sub": user["id"],  
            "name": user["name"],  
            "email": user["email"]
        }
    )
    return {"access_token": access_token}
    

@app.post('/signup')
def signup(
    id : Annotated[str, Form()],
    password : Annotated[str, Form()],
    name : Annotated[str, Form()],
    email : Annotated[str, Form()]
    ):
    cur.execute(f"""
                INSERT INTO users(id, name, email, password)
                VALUES ("{id}", "{name}", "{email}", "{password}")
                """)
    con.commit()
    return "200"

@app.post('/items')
async def create_item(
                image: UploadFile,
                title: Annotated[str, Form()],
                price: Annotated[int, Form()],
                description: Annotated[str, Form()],
                place: Annotated[str, Form()],
                insertAt: Annotated[int, Form()],
                user = Depends(manager)
                ):
    image_bytes = await image.read()
    cur.execute(f"""
                INSERT INTO items(title,image,price,description,place, insertAt)
                VALUES ('{title}','{image_bytes.hex()}',{price},'{description}','{place}',{insertAt})
                """)
    con.commit()
    return '200'

@app.get('/items')
async def get_items(user = Depends(manager)):
    print(f"Authenticated user: {user}")  # JWT 토큰으로 인증된 사용자 정보 출력
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    rows = cur.execute(f"""
                       SELECT * FROM items;
                       """).fetchall()
    return JSONResponse(
        jsonable_encoder(dict(row) for row in rows)
        )
    
@app.get('/images/{item_id}')
async def get_image(item_id):
    cur = con.cursor()
    # 16진법
    image_bytes = cur.execute(F"""
                             SELECT image from items WHERE id={item_id}
                             """).fetchone()[0] # Tuple로 내려오는데 껍때기 1개를 없애기 위한
    # 16진법을 가져와서 해석해서 byte로 바꾼 후 content에 담아 Response
    return Response(content=bytes.fromhex(image_bytes), media_type='image/*')

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

