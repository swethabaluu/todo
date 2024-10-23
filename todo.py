import streamlit as st
import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import datetime

# Load environment variables from .env file
load_dotenv()

# MongoDB connection
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client.todo_db
todos_collection = db.todos

# Function to add a todo
def add_todo(username, task, deadline):
    todos_collection.insert_one({
        'username': username,
        'task': task,
        'deadline': deadline,
        'completed': False
    })

# Function to get todos
def get_todos(username):
    return list(todos_collection.find({'username': username}))

# Function to update a todo
def update_todo(todo_id, task, deadline, completed):
    todos_collection.update_one(
        {'_id': todo_id},
        {'$set': {'task': task, 'deadline': deadline, 'completed': completed}}
    )

# Function to delete a todo
def delete_todo(todo_id):
    todos_collection.delete_one({'_id': todo_id})

# Function to mark todo as completed
def mark_completed(todo_id):
    todos_collection.update_one(
        {'_id': todo_id},
        {'$set': {'completed': True}}
    )

# Streamlit UI
def main():
    st.title("To-Do List Application")

    username = st.text_input("Enter your name")

    if username:
        st.subheader(f"Hello, {username}! Manage your tasks below:")
        
        # Add a new todo
        task = st.text_input("Enter a new task")
        deadline = st.date_input("Select a deadline", datetime.date.today())

        if st.button("Add Task"):
            add_todo(username, task, deadline)
            st.success("Task added successfully!")

        # Display todos
        todos = get_todos(username)
        if todos:
            for todo in todos:
                deadline_str = todo['deadline'].strftime("%Y-%m-%d")  # Format deadline for display
                st.write(f"**Task:** {todo['task']} | **Deadline:** {deadline_str}")
                
                # Checkbox to mark as completed
                if st.checkbox("Mark as done", key=todo['_id']):
                    mark_completed(todo['_id'])
                    st.success("Task marked as done!")

                # Update task
                if st.button("Update", key=f"update-{todo['_id']}"):
                    new_task = st.text_input("Update Task", value=todo['task'])
                    new_deadline = st.date_input("Update Deadline", value=todo['deadline'])
                    update_todo(todo['_id'], new_task, new_deadline, todo['completed'])
                    st.success("Task updated successfully!")

                # Delete task
                if st.button("Delete", key=f"delete-{todo['_id']}"):
                    delete_todo(todo['_id'])
                    st.success("Task deleted successfully!")
        else:
            st.write("No tasks found.")

if __name__ == "__main__":
    main()
