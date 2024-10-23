import streamlit as st
from pymongo import MongoClient
from bson import ObjectId
import matplotlib.pyplot as plt
import pandas as pd

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
            
            # Task display with checkbox for completed status
            col1, col2, col3 = st.columns([6, 1, 1])
            with col1:
                # Set the checkbox value based on the task's completion status
                checkbox_value = st.checkbox(task, value=completed, key=task_id)

                # Update the task status if checkbox state changes
                if checkbox_value != completed:
                    update_todo_status(username, task_id, checkbox_value)
            with col2:
                if not completed:
                    st.warning("⚠️")
            with col3:
                if st.button("Delete", key=f"del_{task_id}"):
                    delete_task(username, task_id)
                    st.success("Task deleted successfully!")

# Function to plot task completion status
def plot_task_completion(username):
    todos_collection = db[username]
    todos = list(todos_collection.find())
    
    if todos:
        # Count completed and incomplete tasks
        completed_count = sum(1 for todo in todos if todo['completed'])
        incomplete_count = len(todos) - completed_count

        # Create a DataFrame for plotting
        data = pd.DataFrame({
            'Status': ['Completed', 'Incomplete'],
            'Count': [completed_count, incomplete_count]
        })

        # Plotting the bar chart
        plt.figure(figsize=(6, 4))
        plt.bar(data['Status'], data['Count'], color=['green', 'red'])
        plt.title('Task Completion Status')
        plt.xlabel('Status')
        plt.ylabel('Number of Tasks')
        plt.xticks(rotation=0)
        st.pyplot(plt)  # Display the plot in Streamlit

# Streamlit app main function
def main():
    st.title("To-Do List App")

    # Get the user's name
    username = st.text_input("Enter your name:")
    
    if username:
        st.write(f"Hello, {username}!")
        
        # Input field for adding a new task
        task = st.text_input("New Task:")
        
        if st.button("Add"):
            if task:
                add_todo(username, task)
                st.success("Task added successfully!")
            else:
                st.error("Please enter a task.")

        # Display tasks
        st.write("### Your Tasks")
        display_tasks(username)

        # Plot task completion status
        st.write("### Task Completion Status")
        plot_task_completion(username)

if __name__ == "__main__":
    main()
