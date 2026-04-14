
from fastapi import FastAPI, Path
from pydantic import BaseModel, Field

app = FastAPI()

@app.get("/product/{id}")
async def detail_view(id: int):
    return {"product": f"Stock number {id}"}

@app.get("/users/{name}/{age}")
async def users(name:str, age:int):
    return {"username": name, "userage": age}

@app.get("/users/{name}")
async def users2(name:str, age:int = 25):
    return {"username": name, "userage": age}

@app.get("/country/{country}")
async def list_cities(country:str, limit:int):
    country_dict = {
        "russia": ["Moscow", "St. Petersburg", "Novosibirsk", "Kazan", "Nizhny Novgorod"],
        "usa": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
        "canada": ["Toronto", "Vancouver", "Montreal", "Calgary", "Edmonton"]
    }
    if country not in country_dict:
        return {"error": "Country not found"}

    if limit < 0 or limit > 5:
        return {"error": "Limit must be between 0 and 5"}

    return {"country": country, "cities": country_dict[country][:limit]}


@app.get("/user/{name}")
async def user(name: str = Path(min_length=4, max_length=20, description="Enter your name")):
    return {"username": name}

@app.get("/category/{category_id}/products")
async def category(category_id: int = Path(gt=0, description="Enter your id"), page: int = 1):
    return {"category_id": category_id, "page": page}
