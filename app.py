import streamlit as st
import json
import os

# Custom CSS for effects
custom_css = """
<style>
/* Button hover effect */
.stButton > button:hover {
    background-color: #4682B4; /* SteelBlue */
    color: white;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #F0F8FF; /* AliceBlue */
}

/* Title styling */
h1 {
    color: #1E90FF; /* DodgerBlue */
    text-shadow: 2px 2px 4px #A9A9A9; /* DarkGray */
}

/* To-Do item styling */
.stMarkdown h2 {
    color: #1E90FF; /* DodgerBlue */
}
</style>
"""

DATA_FILE = 'todos.json'

def load_todos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_todos(todos):
    with open(DATA_FILE, 'w') as f:
        json.dump(todos, f, indent=4)

def app():
    st.set_page_config(layout="wide")
    st.title("Daily To-Do App")

    # Inject custom CSS
    st.markdown(custom_css, unsafe_allow_html=True)

    todos = load_todos()

    # Sidebar for adding new todos
    with st.sidebar:
        st.header("Add New To-Do")
        title = st.text_input("Title")
        description = st.text_area("Description")
        status = st.selectbox("Status", ["To Do", "In Progress", "Closed", "On-Hold"])
        if st.button("Add To-Do"):
            if description and title:
                todos.append({"title": title, "description": description, "status": status})
                save_todos(todos)
                st.success("To-Do added successfully!")
            else:
                st.error("Title and Description cannot be empty.")

    # Main content area for displaying todos and dashboard
    st.header("Your To-Do List")
    
    if todos:
        # Display To-Dos
        for i, todo in enumerate(todos):
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.write(f"**Title:** {todo['title']}")
                st.write(f"**Description:** {todo['description']}")
            with col2:
                current_status = todo['status']
                new_status = st.selectbox(f"Status for {i}", ["To Do", "In Progress", "Closed", "On-Hold"], index=["To Do", "In Progress", "Closed", "On-Hold"].index(current_status), key=f"status_{i}")
                if new_status != current_status:
                    todos[i]['status'] = new_status
                    save_todos(todos)
                    st.experimental_rerun()
            with col3:
                if st.button("Delete", key=f"delete_{i}"):
                    todos.pop(i)
                    save_todos(todos)
                    st.experimental_rerun()
        
        # Dashboard
        st.markdown("---")
        st.header("To-Do Dashboard")
        
        status_counts = {}
        for status_option in ["To Do", "In Progress", "Closed", "On-Hold"]:
            status_counts[status_option] = sum(1 for todo in todos if todo['status'] == status_option)
        
        st.write("### To-Do Status Summary")
        st.bar_chart(status_counts)

    else:
        st.info("No To-Do items yet. Add some using the sidebar!")

if __name__ == "__main__":
    app()
