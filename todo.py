# todo.py

from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# MongoDB connection
MONGODB_URI = os.getenv('MONGODB_URI')
client = MongoClient(MONGODB_URI)
db = client['todo_db']
todos_collection = db['todos']

def add_todo(task):
    todos_collection.insert_one({'task': task})
    print(f'Task added: {task}')

def view_todos():
    todos = todos_collection.find()
    print("\nCurrent To-Do List:")
    for todo in todos:
        print(f"- {todo['task']} (ID: {todo['_id']})")
    print("")

def update_todo(todo_id, new_task):
    result = todos_collection.update_one({'_id': todo_id}, {'$set': {'task': new_task}})
    if result.modified_count > 0:
        print(f'Task updated to: {new_task}')
    else:
        print("No task found with that ID.")

def delete_todo(todo_id):
    result = todos_collection.delete_one({'_id': todo_id})
    if result.deleted_count > 0:
        print(f'Task with ID {todo_id} deleted.')
    else:
        print("No task found with that ID.")

def main():
    while True:
        print("To-Do List Menu:")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Exit")
        choice = input("Choose an option (1-5): ")

        if choice == '1':
            task = input("Enter task: ")
            add_todo(task)
        elif choice == '2':
            view_todos()
        elif choice == '3':
            todo_id = input("Enter task ID to update: ")
            new_task = input("Enter new task: ")
            update_todo(todo_id, new_task)
        elif choice == '4':
            todo_id = input("Enter task ID to delete: ")
            delete_todo(todo_id)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please choose again.")

if __name__ == '__main__':
    main()
