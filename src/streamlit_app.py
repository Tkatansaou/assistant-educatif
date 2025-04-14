import streamlit as st
import requests
from typing import Dict, List

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Operator1 - Task Manager",
    page_icon="✅",
    layout="wide"
)

st.title("Operator1 - Task Manager")

def get_tasks() -> List[Dict]:
    response = requests.get(f"{API_URL}/tasks")
    return response.json()

def create_task(title: str, description: str):
    response = requests.post(
        f"{API_URL}/tasks",
        json={"title": title, "description": description}
    )
    return response.json()

def update_task(task_id: int, title: str, description: str, status: str):
    response = requests.put(
        f"{API_URL}/tasks/{task_id}",
        json={"title": title, "description": description, "status": status}
    )
    return response.json()

def delete_task(task_id: int):
    response = requests.delete(f"{API_URL}/tasks/{task_id}")
    return response.json()

# Create new task section
st.header("Create New Task")
with st.form("new_task_form", clear_on_submit=True):
    title = st.text_input("Task Title")
    description = st.text_area("Task Description")
    submit_button = st.form_submit_button("Create Task")
    
    if submit_button and title and description:
        try:
            create_task(title, description)
            st.success("Task created successfully!")
        except Exception as e:
            st.error(f"Error creating task: {str(e)}")

# Display tasks section
st.header("Tasks")
try:
    tasks = get_tasks()
    
    if not tasks:
        st.info("No tasks found. Create a new task to get started!")
    
    for task in tasks:
        with st.expander(f"Task #{task['id']}: {task['title']}"):
            with st.form(f"edit_task_{task['id']}", clear_on_submit=True):
                edited_title = st.text_input("Title", value=task['title'])
                edited_description = st.text_area("Description", value=task['description'])
                edited_status = st.selectbox(
                    "Status",
                    options=["pending", "in_progress", "completed"],
                    index=["pending", "in_progress", "completed"].index(task['status'])
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("Update"):
                        try:
                            update_task(
                                task['id'],
                                edited_title,
                                edited_description,
                                edited_status
                            )
                            st.success("Task updated successfully!")
                        except Exception as e:
                            st.error(f"Error updating task: {str(e)}")
                
                with col2:
                    if st.form_submit_button("Delete", type="primary"):
                        try:
                            delete_task(task['id'])
                            st.success("Task deleted successfully!")
                        except Exception as e:
                            st.error(f"Error deleting task: {str(e)}")

except Exception as e:
    st.error(f"Error fetching tasks: {str(e)}")

# Add auto-refresh
st.empty()
st.button("Refresh Tasks") 