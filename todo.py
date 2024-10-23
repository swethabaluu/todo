import streamlit as st
from pymongo import MongoClient
from datetime import datetime, date  # Import both datetime and date from datetime module
from bson.objectid import ObjectId  # To handle MongoDB ObjectId

# MongoDB Atlas connection
client = MongoClient("mongodb+srv://swethabalu276:Student123@cluster0.tvrpc.mongodb.net/todo_db?retryWrites=true&w=majority&appName=Cluster0")
db = client.todo_db

# Function to add a new task (Create)
def add_todo(username, task, deadline):
    if isinstance(deadline, date):  # Corrected isinstance check
        # Convert datetime.date to datetime.datetime
        deadline = datetime.combine(deadline, datetime.min.time())  
    
    todos_collection = db[username]
    todos_collection.insert_one({
        'task': task,
        'deadline': deadline,
        'completed': False
    })

# Function to read and display tasks (Read)
def read_todos(username):
    todos_collection = db[username]
    todos = list(todos_collection.find().sort('deadline', 1))  # Sort tasks by deadline
    return todos

# Function to update a task's details (Update)
def update_todo_details(username, task_id, task, deadline):
    if isinstance(deadline, date):
        deadline = datetime.combine(deadline, datetime.min.time())  
    
    todos_collection = db[username]
    todos_collection.update_one(
        {'_id': ObjectId(task_id)},
        {'$set': {'task': task, 'deadline': deadline}}
    )

# Function to update a task's completion status (Update)
def update_todo_status(username, task_id, completed):
    todos_collection = db[username]
    todos_collection.update_one(
        {'_id': ObjectId(task_id)},
        {'$set': {'completed': completed}}
    )

# Function to delete a task (Delete)
def delete_todo(username, task_id):
    todos_collection = db[username]
    todos_collection.delete_one({'_id': ObjectId(task_id)})

# Function to display tasks and provide options for CRUD operations
def display_tasks(username):
    todos = read_todos(username)
    if todos:
        for todo in todos:
            task = todo['task']
            deadline = todo['deadline']
            completed = todo['completed']
            task_id = str(todo['_id'])  # Convert ObjectId to string for Streamlit keys
            
            # Display task with a checkbox for completion status
            task_text = f"{task} - Deadline: {deadline.strftime('%Y-%m-%d')}"
            st.write(task_text)
            
            if st.checkbox("Completed", completed, key=f"status_{task_id}"):
                update_todo_status(username, task_id, not completed)
            
            # Edit task details
            if st.button(f"Edit Task", key=f"edit_{task_id}"):
                new_task = st.text_input("New Task Name:", task, key=f"new_task_{task_id}")
                new_deadline = st.date_input("New Deadline:", deadline, key=f"new_deadline_{task_id}")
                if st.button("Update Task", key=f"update_task_{task_id}"):
                    update_todo_details(username, task_id, new_task, new_deadline)
                    st.success(f"Task '{new_task}' updated successfully!")
            
            # Delete task
            if st.button(f"Delete Task", key=f"delete_{task_id}"):
                delete_todo(username, task_id)
                st.warning(f"Task '{task}' deleted successfully!")
    else:
        st.write("No tasks found.")

# Function to prioritize tasks (Deadline-based prioritization)
def prioritize_tasks(username):
    todos = read_todos(username)
    
    overdue = []
    today = []
    upcoming = []

    for todo in todos:
        deadline = todo['deadline']
        if deadline.date() < datetime.today().date():
            overdue.append(todo)
        elif deadline.date() == datetime.today().date():
            today.append(todo)
        else:
            upcoming.append(todo)

    st.write(f"Overdue Tasks: {len(overdue)}")
    st.write(f"Today's Tasks: {len(today)}")
    st.write(f"Upcoming Tasks: {len(upcoming)}")

# Streamlit app main function
def main():
    st.title("To-Do List App (CRUD Operations)")

    # Get the user's name
    username = st.text_input("Enter your name:")
    
    if username:
        # Input fields for adding a new task (Create)
        task = st.text_input("Task:")
        deadline = st.date_input("Deadline:")
        
        if st.button("Add Task"):
            if task and deadline:
                add_todo(username, task, deadline)
                st.success("Task added successfully!")
            else:
                st.error("Please enter both task and deadline.")
        
        # Display the tasks (Read) and CRUD options
        st.write("### Your Tasks")
        display_tasks(username)
        
        # Task prioritization based on deadlines
        st.write("### Task Prioritization")
        prioritize_tasks(username)

if __name__ == "__main__":
    main()
