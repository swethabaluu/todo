# todo.py

import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from bson.objectid import ObjectId
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# MongoDB connection
MONGODB_URI = os.getenv('MONGODB_URI')
client = MongoClient(MONGODB_URI)
db = client['todo_db']  # Use your database name here
todos_collection = db['todos']  # Use your collection name here

# Function to add a todo
def add_todo(username, task, deadline):
    # Convert deadline to datetime
    deadline = datetime.combine(deadline, datetime.min.time())
    todos_collection.insert_one({'username': username, 'task': task, 'deadline': deadline, 'completed': False})

# Function to view todos for a specific user
def view_todos(username):
    return todos_collection.find({'username': username})

# Function to update a todo
def update_todo(todo_id, new_task, new_deadline):
    # Convert new_deadline to datetime
    new_deadline = datetime.combine(new_deadline, datetime.min.time())
    todos_collection.update_one({'_id': ObjectId(todo_id)}, {'$set': {'task': new_task, 'deadline': new_deadline}})

# Function to delete a todo
def delete_todo(todo_id):
    todos_collection.delete_one({'_id': ObjectId(todo_id)})

# Function to mark a todo as completed
def mark_as_completed(todo_id):
    todos_collection.update_one({'_id': ObjectId(todo_id)}, {'$set': {'completed': True}})

# Streamlit app interface
def main():
    st.set_page_config(page_title="To-Do List App", page_icon="📝", layout="wide")
    st.title("📝 To-Do List Application")
    st.markdown("---")

    # User input for name
    username = st.text_input("👤 Enter your name", placeholder="Your Name")
    
    if username:
        # Add a task section
        st.subheader("Add a New Task")
        task = st.text_input("🆕 Enter a new task", placeholder="Task description")
        deadline = st.date_input("🗓️ Select a deadline", min_value=datetime.today().date())

        if st.button("✅ Add Task"):
            if task:
                add_todo(username, task, deadline)
                st.success(f'Task added: {task}', icon="✅")
            else:
                st.warning("❗ Please enter a task.", icon="⚠️")

        # Display tasks
        st.markdown("---")
        st.subheader(f"📋 {username}'s Current To-Do List")
        todos = view_todos(username)

        for todo in todos:
            col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
            
            with col1:
                # Task text with caution for pending tasks
                completed_status = todo.get('completed', False)
                deadline_str = todo['deadline'].strftime("%Y-%m-%d")  # Format deadline for display
                task_display = f"{todo['task']} (Deadline: {deadline_str})"
                
                if not completed_status:
                    st.markdown(f"<div style='color: #D50000;'>{task_display}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='color: #4CAF50;'>{task_display} - Completed</div>", unsafe_allow_html=True)

            with col2:
                # Checkbox for completion
                if not completed_status:
                    if st.checkbox("✅ Work Done", key=f"completed_{todo['_id']}"):
                        mark_as_completed(todo['_id'])
                        st.success(f'Task marked as done: {todo["task"]}', icon="✅")
                        st.experimental_rerun()  # Refresh the page

            with col3:
                # Update functionality
                new_task = st.text_input("Update task", value=todo['task'], key=f"new_task_{todo['_id']}")
                new_deadline = st.date_input("Update deadline", value=todo['deadline'].date(), key=f"new_deadline_{todo['_id']}")
                
                if st.button("🔄 Update", key=f"update_{todo['_id']}"):
                    if new_task:
                        update_todo(todo['_id'], new_task, new_deadline)
                        st.success(f'Task updated to: {new_task}', icon="✅")
                        st.experimental_rerun()  # Refresh the page

            with col4:
                # Delete functionality
                if st.button("❌ Delete", key=todo['_id']):
                    delete_todo(todo['_id'])
                    st.success(f'Task deleted: {todo["task"]}', icon="✅")
                    st.experimental_rerun()  # Refresh the page
    else:
        st.warning("❗ Please enter your name to manage your To-Do list.", icon="⚠️")

if __name__ == '__main__':
    main()
