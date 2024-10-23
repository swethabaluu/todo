# todo.py

import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from bson.objectid import ObjectId

# Load environment variables from .env file
load_dotenv()

# MongoDB connection
MONGODB_URI = os.getenv('MONGODB_URI')
client = MongoClient(MONGODB_URI)
db = client['todo_db']
todos_collection = db['todos']

# Function to add a todo
def add_todo(task):
    todos_collection.insert_one({'task': task})

# Function to view todos
def view_todos():
    return todos_collection.find()

# Function to update a todo
def update_todo(todo_id, new_task):
    todos_collection.update_one({'_id': ObjectId(todo_id)}, {'$set': {'task': new_task}})

# Function to delete a todo
def delete_todo(todo_id):
    todos_collection.delete_one({'_id': ObjectId(todo_id)})

# Streamlit app interface
def main():
    st.title("To-Do List")

    # Add a task
    task = st.text_input("Enter a new task")
    if st.button("Add Task"):
        if task:
            add_todo(task)
            st.success(f'Task added: {task}')
        else:
            st.warning("Please enter a task.")

    # Display tasks
    st.subheader("Current To-Do List")
    todos = view_todos()
    
    for todo in todos:
        col1, col2 = st.columns([3, 1])
        col1.text(todo['task'])
        with col2:
            if st.button("Delete", key=todo['_id']):
                delete_todo(todo['_id'])
                st.success(f'Task with ID {todo["_id"]} deleted.')
                st.experimental_rerun()  # Refresh the page

if __name__ == '__main__':
    main()
