from enum import Enum
from tkinter.messagebox import NO
from fastapi import FastAPI, Query, Path
from pydantic import BaseModel, Field

app = FastAPI()


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


class ModelName(str, Enum):
    vgg16 = "vgg"
    resnet18 = "resnet"
    lenet_ = "lenet"


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
@app.get("/items/{item_id}")
async def read_items(item_id: int = Path(title="The ID of the item to get"), q: str | None = Query(default=None, alias='item-query')):
    result = {"item_id": item_id}
    print(q)
    if q:
        result.update({"q": q})
    return result



# @app.get("/items/")
# async def read_items(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip:skip+limit]
# @app.get("/items/")
# async def read_items(q: list[str] | None = Query(default=[])):
#     query_items = {"q": q}
#     return query_items


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"desc": "This is an amazing item that has a long description"})
    return item


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None

# def item_wrapper(item: Item):
#     item_dict = item.dict()
#     if item.tax:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict


@app.post("/items/")
async def create_item1(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# @app.put("/items/{item_id}")
# async def create_item2(item_id: int, item: Item, q: str | None = None):
#     item_dict = await create_item1(item)
#     result =  {"item_id": item_id, **item_dict} # **연산자는 dict을 merge할때 사용.
#     if q:
#         result.update({"q": q})
#     return result

@app.put("/items/{item_id}")
async def update_item(
    *, # 왜 있는거지???
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
    q: str | None = None,
    item: Item | None = None,
    user: User | None = None
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    if user:
        results.update({"user": user})
    return results
