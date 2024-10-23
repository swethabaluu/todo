import streamlit as st
from pymongo import MongoClient
import datetime
import pandas as pd
import matplotlib.pyplot as plt

# MongoDB connection string
MONGO_URI = "mongodb+srv://swethabalu276:Student123@cluster0.tvrpc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client['vcc']  # Replace 'vcc' with your database name
todos_collection = db['todos']  # Replace 'todos' with your collection name

# Function to add a new todo
def add_todo(username, task, deadline):
    if isinstance(deadline, datetime.date):
        deadline = datetime.datetime.combine(deadline, datetime.datetime.min.time())  # Combine with min time
    todos_collection.insert_one({'username': username, 'task': task, 'deadline': deadline, 'completed': False})

# Function to get todos for a specific user
def get_todos(username):
    return list(todos_collection.find({'username': username}))

# Function to mark a todo as completed
def mark_completed(todo_id):
    todos_collection.update_one({'_id': todo_id}, {'$set': {'completed': True}})

# Function to update a todo
def update_todo(todo_id, task, deadline, completed):
    if isinstance(deadline, datetime.date):
        deadline = datetime.datetime.combine(deadline, datetime.datetime.min.time())  # Combine with min time
    todos_collection.update_one({'_id': todo_id}, {'$set': {'task': task, 'deadline': deadline, 'completed': completed}})

# Function to delete a todo
def delete_todo(todo_id):
    todos_collection.delete_one({'_id': todo_id})

# Streamlit UI
def main():
    st.title("To-Do List Application")

    username = st.text_input("Enter your name")

    if username:
        st.subheader(f"Hello, {username}! Manage your tasks below:")
        
        # Add a new todo
        task = st.text_input("Enter a new task", key="task_input")  # Specify a key for state management
        deadline = st.date_input("Select a deadline", datetime.date.today())

        if st.button("Add Task"):
            if task:
                add_todo(username, task, deadline)
                st.success("Task added successfully!")
                st.session_state.task_input = ""  # Clear the input box after adding the task
            else:
                st.warning("Please enter a task!")

        # Display todos
        todos = get_todos(username)
        if todos:
            # Sort todos by deadline
            todos.sort(key=lambda x: x['deadline'])

            # Prepare data for visualization
            task_names = [todo['task'] for todo in todos]
            deadlines = [todo['deadline'] for todo in todos]
            
            # Create a DataFrame for visualization
            df = pd.DataFrame({'Task': task_names, 'Deadline': deadlines})
            df['Deadline'] = pd.to_datetime(df['Deadline'])  # Ensure deadlines are in datetime format

            # Plotting the tasks by deadline
            plt.figure(figsize=(10, 5))
            plt.barh(df['Task'], df['Deadline'].dt.date, color='skyblue')
            plt.xlabel("Deadline")
            plt.title("Tasks Prioritized by Deadline")
            plt.xticks(rotation=45)
            st.pyplot(plt)

            for todo in todos:
                # Safely retrieve the 'deadline' field using get()
                deadline_str = todo.get('deadline')
                if isinstance(deadline_str, datetime.datetime):
                    deadline_str = deadline_str.strftime("%Y-%m-%d")  # Format deadline for display
                else:
                    deadline_str = "No deadline set"

                st.write(f"**Task:** {todo['task']} | **Deadline:** {deadline_str}")
                
                # Checkbox to mark as completed
                if st.checkbox("Mark as done", key=todo['_id']):
                    mark_completed(todo['_id'])
                    st.success("Task marked as done!")

                # Update task
                if st.button("Update", key=f"update-{todo['_id']}"):
                    new_task = st.text_input("Update Task", value=todo['task'])
                    new_deadline = st.date_input("Update Deadline", value=deadline_str if isinstance(deadline_str, str) else datetime.date.today())
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
