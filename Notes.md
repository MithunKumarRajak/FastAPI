# Summery Notes

## FASTAPI

---
uvicorn - web server name hai yaha pe

main.py mai main ke jagah koi bhi naam likh shakte hai

and app ki jagah bhi kuch bhi likh shakte hai

uvicorn main:app ~= unicorn start : app --reload (app ko automatically reload karega)

---

- path operations

async word for async function in fastapi

we can change the fuction name as python

decorator ---> like a magic on python fuction
decorator start with @app

@app.get('/)
/ is root or default path

app is here refer to fastapi

and get is http method for user

http method mai order matter karta hai

---

post reqest

to send data to api server

post method mai agar postman se body se kuch data aaye to 'params' use kare use kar shakte hai

from fastapi.params import Body

* in dict mai string formating ke liye double quotes use kare  like " "

```
body se kuch bhi bheja jaa shakta hai So we have to do vadiation in fastapi 

So 'pydantic ' comes in for data validation 

pydantic se BaseModwl import kare forr this

