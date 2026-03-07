from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


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

#


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "Hello World", "content": "This is my first post", "id": 1},
            {"title": "Hello World Again",
             "content": "This is my second post", "id": 2},
            {"title": "Hello World Again Again",
                "content": "This is my third post", "id": 3}
            ]


@app.post('/posts')
def create_post(post: Post):
    print(post)
    post_dict = post.dict() # converts the pydantic model to a dictionary use model_dump
    post_dict['id'] =randrange(0, 100000)
    my_posts.append(post_dict)
    return {"Post Created!": my_posts}

# 

@app.get('/posts/{id}')
def get_post(id: int):
    for post in my_posts:
        if post['id'] == id:
            return {"Post Found!": post}
    return {"Error": "Post Not Found!"}



# post method with validation using pydantic model
@app.post('/right')
def right(new_post: validation):
    print(new_post)
    return {"Posted!": new_post}


# post method without validation using Body
@app.post('/vote')
def vote_post(payload: dict = Body(...)):
    print(payload)
    return {'Vote Posted!': f"{payload['hello']} : {payload['reply']}"}
