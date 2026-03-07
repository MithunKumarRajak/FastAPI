from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World From FastAPI"}


@app.get('/right')
def right():
    return 'Do Vote!!!'


@app.post('/vote')
def vote_post(payload: dict = Body(...)):
    print(payload)
    return {'Vote Posted!': f"{payload['hello']} : {payload['reply']}"}

