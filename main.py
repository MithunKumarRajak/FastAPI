from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World From FastAPI"}

# class for validation using pydantic model
class validation(BaseModel):
    hello: str
    reply: str
    published: bool = True
    rating: Optional[int] = None

# post method with validation using pydantic model
@app.post('/right')
def right(new_post: validation):
    print(new_post)
    return {f"{new_post.hello} : {new_post.reply}"}

# post method without validation using Body
@app.post('/vote')
def vote_post(payload: dict = Body(...)):
    print(payload)
    return {'Vote Posted!': f"{payload['hello']} : {payload['reply']}"}
