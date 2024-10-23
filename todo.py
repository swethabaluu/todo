import streamlit as st
import pymongo
from pymongo import MongoClient
import datetime
import matplotlib.pyplot as plt

# MongoDB connection
MONGODB_URI = "mongodb+srv://swethabalu276:Student123@cluster0.tvrpc.mongodb.net/todo_db?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGODB_URI)
db = client["todo_db"]

# Collection for todos
todos_collection = db["todos"]

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

# Function to mark a todo as completed
def mark_completed(todo_id):
    todos_collection.update_one({'_id': todo_id}, {'$set': {'completed': True}})

# Function to delete a todo
def delete_todo(todo_id):
    todos_collection.delete_one({'_id': todo_id})

# Function to visualize tasks
def visualize_tasks(todos):
    if todos:
        completed = [todo['deadline'] for todo in todos if todo['completed']]
        not_completed = [todo['deadline'] for todo in todos if not todo['completed']]
        
        labels = 'Completed', 'Not Completed'
        sizes = [len(completed), len(not_completed)]
        
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig1)

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
            if task:
                add_todo(username, task, deadline)
                st.success("Task added successfully!")
                st.session_state.task_input = ""  # Clear the input box after adding the task
            else:
                st.error("Task name cannot be empty.")

        # Display todos
        todos = get_todos(username)
        if todos:
            sorted_todos = sorted(todos, key=lambda x: x['deadline'])  # Sort by deadline
            for index, todo in enumerate(sorted_todos):
                deadline_str = todo['deadline'].strftime("%Y-%m-%d")
                st.write(f"{index + 1}. **Task:** {todo['task']} | **Deadline:** {deadline_str}")

                # Checkbox to mark as completed
                if st.checkbox("Mark as done", key=todo['_id']):
                    mark_completed(todo['_id'])
                    st.success("Task marked as done!")

                # Caution if not completed
                if not todo['completed']:
                    st.warning("⚠️ This task is not completed yet!")

                # Delete task
                if st.button("Delete", key=f"delete-{todo['_id']}"):
                    delete_todo(todo['_id'])
                    st.success("Task deleted successfully!")
        else:
            st.write("No tasks found.")

        # Visualize tasks
        visualize_tasks(todos)

if __name__ == "__main__":
    main()
