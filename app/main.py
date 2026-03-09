from fastapi import FastAPI, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
# for database connection
import psycopg2
from psycopg2.extras import RealDictCursor
import time

#
app = FastAPI()


# For the database connection
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password='123456', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Database connection failed!")
        print("Error:", error)
        time.sleep(3)


# root endpoint

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

# class for post method data validation using pydantic model


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


@app.post('/post')
def create_post(post: Post):
    print(post)
    post_dict = post.dict()  # converts the pydantic model to a dictionary use model_dump
    post_dict['id'] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"Post Created!": my_posts}

#


@app.get('/post/{id}')
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


# now getting data of posts from database
@app.get('/posts')
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    print(posts)
    return {"Data from database": posts}


# now creating a post in database
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()  # to save the changes in database
    return {"Data from database": new_post}


# now getting a post by id from database
@app.get('/posts/{id}')
def get_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),)) # to prevent SQL injection attack we use parameterized query and pass the id as a
    post = cursor.fetchone()
    print(post)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"Data from database": post}

# now deleting a post by id from database
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    deleted_post = cursor.fetchone()
    print(deleted_post)
    conn.commit()
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"Data from database": deleted_post}

# now updating a post by id from database
@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    print(updated_post)
    conn.commit()
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"Data from database": updated_post}
