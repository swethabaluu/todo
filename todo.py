import streamlit as st
from pymongo import MongoClient
import datetime
from datetime import datetime
import matplotlib.pyplot as plt

# MongoDB Atlas connection
client = MongoClient("mongodb+srv://swethabalu276:Student123@cluster0.tvrpc.mongodb.net/todo_db?retryWrites=true&w=majority&appName=Cluster0")
db = client.todo_db

# Function to add a new task
def add_todo(username, task, deadline):
    if isinstance(deadline, datetime.date):
        # Convert datetime.date to datetime.datetime
        deadline = datetime.combine(deadline, datetime.min.time())  
    
    todos_collection = db[username]
    todos_collection.insert_one({
        'task': task,
        'deadline': deadline,
        'completed': False
    })

# Function to update a task's completion status
def update_todo_status(username, task_id, completed):
    todos_collection = db[username]
    todos_collection.update_one(
        {'_id': task_id},
        {'$set': {'completed': completed}}
    )

# Function to display and update tasks
def display_tasks(username):
    todos_collection = db[username]
    todos = list(todos_collection.find().sort('deadline', 1))  # Sort tasks by deadline
    if todos:
        for todo in todos:
            task = todo['task']
            deadline = todo['deadline']
            completed = todo['completed']
            task_id = todo['_id']
            
            # Show task with a checkbox for completion status
            task_text = f"{task} - Deadline: {deadline.strftime('%Y-%m-%d')}"
            if st.checkbox(task_text, completed, key=str(task_id)):
                update_todo_status(username, task_id, not completed)  # Toggle completed status

# Function to prioritize tasks and visualize deadlines using a pie chart
def visualize_priorities(username):
    todos_collection = db[username]
    todos = list(todos_collection.find())

    if todos:
        # Categorize tasks by remaining time (overdue, today, future)
        overdue = 0
        today = 0
        upcoming = 0

        for todo in todos:
            deadline = todo['deadline']
            if deadline.date() < datetime.today().date():
                overdue += 1
            elif deadline.date() == datetime.today().date():
                today += 1
            else:
                upcoming += 1

        labels = ['Overdue', 'Today', 'Upcoming']
        sizes = [overdue, today, upcoming]
        colors = ['#FF4C4C', '#FFD700', '#90EE90']
        
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig)
    else:
        st.write("No tasks available to visualize.")

# Streamlit app main function
def main():
    st.title("To-Do List App")

    # Get the user's name
    username = st.text_input("Enter your name:")
    
    if username:
        # Input fields for adding a new task
        task = st.text_input("Task:")
        deadline = st.date_input("Deadline:")
        
        if st.button("Add Task"):
            if task and deadline:
                add_todo(username, task, deadline)
                st.success("Task added successfully!")
            else:
                st.error("Please enter both task and deadline.")
        
        st.write("### Your Tasks")
        display_tasks(username)
        
        st.write("### Task Priority Visualization")
        visualize_priorities(username)

if __name__ == "__main__":
    main()
