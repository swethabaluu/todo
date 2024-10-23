import streamlit as st
from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB connection
client = MongoClient("mongodb+srv://swethabalu276:Student123@cluster0.tvrpc.mongodb.net/todo_db?retryWrites=true&w=majority&appName=Cluster0")
db = client.todo_db

# Function to add a new task (Create)
def add_task(username, task):
    todos_collection = db[username]
    todos_collection.insert_one({
        'task': task,
        'completed': False
    })

# Function to read/display tasks (Read)
def get_tasks(username):
    todos_collection = db[username]
    return list(todos_collection.find())

# Function to update a task's completion status (Update)
def update_task_status(username, task_id, completed):
    todos_collection = db[username]
    todos_collection.update_one(
        {'_id': ObjectId(task_id)},
        {'$set': {'completed': completed}}
    )

# Function to delete a task (Delete)
def delete_task(username, task_id):
    todos_collection = db[username]
    todos_collection.delete_one({'_id': ObjectId(task_id)})

# Streamlit app
def main():
    st.title("Simple To-Do List")

    # Get the user's name
    username = st.text_input("Enter your name:")
    
    if username:
        # Create: Add a new task
        task = st.text_input("New Task:")
        if st.button("Add Task"):
            add_task(username, task)
            st.success("Task added successfully!")
        
        # Read: Display existing tasks
        st.write("### Your Tasks")
        tasks = get_tasks(username)
        for task in tasks:
            task_name = task['task']
            task_id = str(task['_id'])
            completed = task['completed']
            
            # Update: Checkbox to mark task as completed or not
            if st.checkbox(task_name, completed, key=task_id):
                update_task_status(username, task_id, not completed)
            
            # Delete: Button to remove the task
            if st.button("Delete", key=f"delete_{task_id}"):
                delete_task(username, task_id)
                st.warning(f"Task '{task_name}' deleted successfully!")

if __name__ == "__main__":
    main()
