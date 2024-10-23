import streamlit as st
from pymongo import MongoClient
from datetime import datetime
import matplotlib.pyplot as plt

# MongoDB connection
MONGODB_URI = "mongodb+srv://swethabalu276:Student123@cluster0.tvrpc.mongodb.net/todo_db?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGODB_URI)
db = client.todo_db

def add_todo(username, task, deadline):
    # Convert deadline to datetime
    if isinstance(deadline, datetime.date):
        deadline = datetime.combine(deadline, datetime.min.time())

    # Insert the task into the MongoDB collection
    todos_collection = db[username]
    todos_collection.insert_one({
        'task': task,
        'deadline': deadline,
        'completed': False
    })

def get_todos(username):
    todos_collection = db[username]
    return list(todos_collection.find())

def update_todo_status(username, task, completed):
    todos_collection = db[username]
    todos_collection.update_one({'task': task}, {'$set': {'completed': completed}})

def delete_todo(username, task):
    todos_collection = db[username]
    todos_collection.delete_one({'task': task})

def main():
    st.title("To-Do List Application")

    # User input for name
    username = st.text_input("Enter your name:")
    
    if username:
        # Input box for task and deadline
        task = st.text_input("Enter a new task:", key='task_input')
        deadline = st.date_input("Select a deadline:", key='deadline_input')

        if st.button("Add Task"):
            if task:
                add_todo(username, task, deadline)
                st.success("Task added successfully!")
                st.session_state.task_input = ""  # Clear the input box after adding the task
            else:
                st.warning("Please enter a task.")

        # Display the current tasks
        todos = get_todos(username)
        if todos:
            # Sort tasks based on deadline
            todos.sort(key=lambda x: x['deadline'])

            for idx, todo in enumerate(todos):
                completed = todo['completed']
                task_name = todo['task']
                task_deadline = todo['deadline']
                
                # Display task with options to update status and delete
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.write(f"{idx + 1}. Task: **{task_name}** | Deadline: **{task_deadline}**")
                
                with col2:
                    if st.checkbox("Mark as done", value=completed, key=f"checkbox_{idx}"):
                        update_todo_status(username, task_name, True)
                        st.success("Task marked as completed!")
                        st.experimental_rerun()  # Refresh to show updated state

                with col3:
                    if st.button("Delete", key=f"delete_{idx}"):
                        delete_todo(username, task_name)
                        st.success("Task deleted successfully!")
                        st.experimental_rerun()  # Refresh to show updated state

            # Visualize task completion with a pie chart
            completed_count = sum(1 for todo in todos if todo['completed'])
            not_completed_count = len(todos) - completed_count

            labels = ['Completed', 'Not Completed']
            sizes = [completed_count, not_completed_count]
            colors = ['#66c2a5', '#fc8d62']
            explode = (0.1, 0)  # explode 1st slice

            # Create pie chart
            fig, ax = plt.subplots()
            ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                   autopct='%1.1f%%', shadow=True, startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
            st.pyplot(fig)

if __name__ == "__main__":
    main()
