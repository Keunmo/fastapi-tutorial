from curses.ascii import HT
from enum import Enum
from tkinter.messagebox import NO
from unittest import result
from fastapi import FastAPI, Query, Path, Cookie, Header
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import Union

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []
    # image: Image | None = None


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]
    

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str


class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type = "car"


class PlaneItem(BaseItem):
    type = "plane"
    size: int


class ModelName(str, Enum):
    vgg16 = "vgg"
    resnet18 = "resnet"
    lenet_ = "lenet"


items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@app.get("/users")
async def read_user():
    return ["Rick", "Morty"]


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    # request accepted only when model_name is one of ModelName's values (vgg, resnet, lenet)
    print(model_name)
    print(model_name.name)
    print(model_name.value)
    if model_name == ModelName.vgg16:
        return {"model_name": model_name, "message": "Deep Learning FTW"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all images"}
    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    res = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            res.append(line)
    return {"file": file_path, "contents": res}


fake_items_db = [{"item_name": "aaa"}, {"item_name": "bbb"}, {"item_name": "ccc"}, {"item_name": "ddd"},
                {"item_name": "eee"}, {"item_name": "fff"}, {"item_name": "ggg"}, {"item_name": "hhh"},
                {"item_name": "iii"}, {"item_name": "jjj"}, {"item_name": "kkk"}, {"item_name": "lll"},
                {"item_name": "mmm"}, {"item_name": "nnn"}, {"item_name": "ooo"}, {"item_name": "ppp"}]


# @app.get("/items/{item_num}")
# async def read_item(item_num: int):
#     if 0 <= item_num <= len(fake_items_db):
#         return fake_items_db[item_num]
#     else:
#         return "item idx should between 0 ~ {}".format(item_num)


# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: str | None = Query(default=None, max_length=50), short: bool = False):
#     item = {"item_id": item_id, 'q': q}
#     if not short:
#         item.update({"desc": "This is an amazing item that has a long description"})
#     return item


# @app.get("/items/{item_id}")
# async def read_items(item_id: int = Path(title="The ID of the item to get"), 
#                     q: str | None = Query(default=None, alias='item-query')):
#     result = {"item_id": item_id}
#     print(q)
#     if q:
#         result.update({"q": q})
#     return result


@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]


# @app.get("/items/")
# async def read_items(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip:skip+limit]

# @app.get("/items/")
# async def read_items(q: list[str] | None = Query(default=[])):
#     query_items = {"q": q}
#     return query_items

# @app.get("/items/")
# async def read_items(ads_id: str | None = Cookie(default=None)):
#     return {"ads_id": ads_id}

@app.get("/items/")
async def read_items(user_agent: str | None = Header(default=None)):
    return {"User-Agent": user_agent}


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"desc": "This is an amazing item that has a long description"})
    return item


# def item_wrapper(item: Item):
#     item_dict = item.dict()
#     if item.tax:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict


# @app.post("/items/")
# async def create_item1(item: Item):
#     item_dict = item.dict()
#     if item.tax:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict

def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved


# @app.post("/user/", response_model=UserOut)
# async def create_user(user: UserIn):
#     return user


# @app.post("/items/", response_model=Item)
# async def create_item(item: Item):
#     new_offer = Offer
#     new_offer.name = item.name
#     new_offer.description = item.description
#     new_offer.price = item.price
#     new_offer.items = [item]
#     return new_offer # error! return type must be Item, as declared at @wrapper method


# @app.post("/items/", response_model=Item, status_code=201)
# async def create_item(item: Item):
#     return item


@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer


@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    return images


# @app.put("/items/{item_id}")
# async def create_item2(item_id: int, item: Item, q: str | None = None):
#     item_dict = await create_item1(item)
#     result =  {"item_id": item_id, **item_dict} # **연산자는 dict을 merge할때 사용.
#     if q:
#         result.update({"q": q})
#     return result

# @app.put("/items/{item_id}")
# async def update_item(
#     *, # 왜 있는거지???
#     item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
#     q: str | None = None,
#     item: Item | None = None,
#     user: User | None = None
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     if item:
#         results.update({"item": item})
#     if user:
#         results.update({"user": user})
#     return results
