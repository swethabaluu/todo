import streamlit as st
from pymongo import MongoClient
from bson import ObjectId

# MongoDB Atlas connection
client = MongoClient("mongodb+srv://swethabalu276:Student123@cluster0.tvrpc.mongodb.net/todo_db?retryWrites=true&w=majority&appName=Cluster0")
db = client.todo_db

# Function to add a new task
def add_todo(username, task):
    todos_collection = db[username]
    todos_collection.insert_one({
        'task': task,
        'completed': False
    })

# Function to update a task's completion status
def update_todo_status(username, task_id, completed):
    todos_collection = db[username]
    todos_collection.update_one(
        {'_id': ObjectId(task_id)},
        {'$set': {'completed': completed}}
    )

# Function to delete a task
def delete_task(username, task_id):
    todos_collection = db[username]
    todos_collection.delete_one({'_id': ObjectId(task_id)})

# Function to display tasks with completion status
def display_tasks(username):
    todos_collection = db[username]
    todos = list(todos_collection.find().sort('task', 1))
    if todos:
        for todo in todos:
            task = todo['task']
            completed = todo['completed']
            task_id = str(todo['_id'])
            
            # Task display with checkbox for completed status and caution symbol for incomplete tasks
            col1, col2, col3 = st.columns([6, 1, 1])
            with col1:
                if st.checkbox(task, completed, key=task_id):
                    update_todo_status(username, task_id, not completed)
            with col2:
                if not completed:
                    st.warning("⚠️")
            with col3:
                if st.button("Delete", key=f"del_{task_id}"):
                    delete_task(username, task_id)
                    st.success("Task deleted successfully!")

# Streamlit app main function
def main():
    st.title("To-Do List App")

    # Get the user's name
    username = st.text_input("Enter your name:")
    
    if username:
        st.write(f"Hello, {username}!")
        
        # Input field for adding a new task
        task = st.text_input("New Task:", key="task_input")
        
        if st.button("Add"):
            if task:
                add_todo(username, task)
                st.success("Task added successfully!")
                # Reset the task input field for the next task
                st.session_state.task_input = ""
            else:
                st.error("Please enter a task.")

        # Display tasks
        st.write("### Your Tasks")
        display_tasks(username)

if __name__ == "__main__":
    main()
