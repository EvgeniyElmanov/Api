from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()


class Task(BaseModel):
    title: str
    description: str
    status: bool


tasks_db = []


@app.get("/tasks", response_model=List[Task])
async def read_tasks():
    return tasks_db


@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int):
    task = next((task for task in tasks_db if task.get("id") == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    task_dict = task.dict()
    task_dict["id"] = len(tasks_db) + 1
    tasks_db.append(task_dict)
    return task_dict


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    index = task_id - 1
    if index < 0 or index >= len(tasks_db):
        raise HTTPException(status_code=404, detail="Task not found")
    tasks_db[index] = task.dict()
    tasks_db[index]["id"] = task_id
    return tasks_db[index]


@app.delete("/tasks/{task_id}", response_model=dict)
async def delete_task(task_id: int):
    index = task_id - 1
    if index < 0 or index >= len(tasks_db):
        raise HTTPException(status_code=404, detail="Task not found")
    deleted_task = tasks_db.pop(index)
    return {"message": "Task deleted successfully", "task": deleted_task}

