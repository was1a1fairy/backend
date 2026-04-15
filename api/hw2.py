from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field

app = FastAPI()

TODOS = [
    {"id": 1, "title": "task1", "description": "lalalalala", "is_completed": False},
    {"id": 2, "title": "task2", "description": "lalalalala", "is_completed": True},
    {"id": 3, "title": "task3", "description": "lalalalala", "is_completed": False}
]

class TODO(BaseModel):

    id: int = Field(gt=0)
    title: str = Field(min_length=0,max_length=100)
    description: str|None
    is_completed: bool

@app.get("/todos")
async def get_todos(limit: int = Query(0, ge=1, le=100), is_completed: bool | None = Query(None), search: str | None = Query(None, min_length=2, max_length=50)):
    result = TODOS.copy()
    
    if limit > 0:
        result = result[:limit]
    if is_completed is not None:
        result = [todo for todo in result if todo["is_completed"] == is_completed]
    if search:
        result = [todo for todo in result if search.lower() in todo["title"].lower()]

    return result

@app.get("/todos/{id}")
async def get_todo(id: int):
    if not [todo for todo in TODOS if todo["id"] == id]:
        return {"error": "Todo not found"}
    return [todo for todo in TODOS if todo["id"] == id][0]

@app.post("/todos")
async def create_todo(todo: TODO):
    new_todo = todo.dict()
    new_todo["id"] = max([t["id"] for t in TODOS]) + 1 if TODOS else 1
    TODOS.append(new_todo)
    return new_todo

@app.put("/todos/{id}")
async def update_todo(id: int, todo: TODO):
    todo_list = [t for t in TODOS if t["id"] == id]
    if not todo_list:
        return {"error": "Todo not found"}
    
    for i in range(len(TODOS)):
        if TODOS[i]["id"] == id:
            TODOS[i] = todo.dict()
            TODOS[i]["id"] = id
            return TODOS[i]
    return {"error": "Todo not found"}

@app.patch("/todos/{id}")
async def patch_todo(id: int, todo: TODO):
    for i in range(len(TODOS)):
        if TODOS[i]["id"] == id:
            todo_data = todo.dict()
            for key, value in todo_data.items():
                if value is not None:
                    TODOS[i][key] = value
            return TODOS[i]
    return {"error": "Todo not found"}


@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    todo_list = [t for t in TODOS if t["id"] == todo_id]
    if not todo_list:
        return {"error": "Todo not found"}
    
    for i in range(len(TODOS)):
        if TODOS[i]["id"] == todo_id:
            deleted_todo = TODOS.pop(i)
            return {"message": "Todo deleted", "todo": deleted_todo}
    return {"error": "Todo not found"}
