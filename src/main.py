from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(
    title="Operator1 API",
    description="API for managing tasks and operations",
    version="1.0.0"
)

class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    status: str = "pending"

tasks: List[Task] = []
task_counter = 1

@app.get("/")
async def root():
    return {"message": "Welcome to Operator1 API"}

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    return tasks

@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    global task_counter
    task.id = task_counter
    task_counter += 1
    tasks.append(task)
    return task

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    task = next((t for t in tasks if t.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, updated_task: Task):
    task_idx = next((idx for idx, t in enumerate(tasks) if t.id == task_id), None)
    if task_idx is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    updated_task.id = task_id
    tasks[task_idx] = updated_task
    return updated_task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    task_idx = next((idx for idx, t in enumerate(tasks) if t.id == task_id), None)
    if task_idx is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    tasks.pop(task_idx)
    return {"message": "Task deleted successfully"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 