import streamlit as st
import sqlite3
import hashlib

# Create or connect to the SQLite database
conn = sqlite3.connect('user_database.db')
c = conn.cursor()

# Create a users table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS testers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        first_name TEXT,
        last_name TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
''')
conn.commit()

# Function to create a password hash
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Streamlit app title
st.title("Secure Text Summarization App")

# Sidebar for authentication
st.sidebar.header("User Authentication")
menu = st.sidebar.radio("Menu", ["Home", "Login", "Register", "Reset Password"])

# Main content
if menu == "Home":
    st.header("Welcome to the Text Summarization App")
    st.write("Please log in or register to access the app's features.")

elif menu == "Login":
    st.header("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        c.execute("SELECT * FROM testers WHERE email = ?", (email,))
        user = c.fetchone()
        if user and user[5] == hash_password(password):
            st.success(f"Logged in as {user[1]} {user[2]} ({user[4]})")

            st.subheader("Text Summarization")
            input_text = st.text_area("Enter the text you want to summarize")
            sentences_count = st.number_input("Number of sentences in the summary", min_value=1, max_value=10, value=5)
            summarize_button = st.button("Summarize")

            if summarize_button:
                # Implement text summarization logic here
                st.subheader("Summary:")
                st.write("Summary will appear here.")

        else:
            st.error("Login failed. Please check your email and password.")

elif menu == "Register":
    st.header("Register")
    title = st.radio("Title", ["Mr.", "Mrs.", "Miss", "Ms."], index=0)
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    password_confirmation = st.text_input("Password Confirmation", type="password")
    register_button = st.button("Register")

    if register_button:
        if password == password_confirmation:
            hashed_password = hash_password(password)
            c.execute("INSERT INTO testers (title, first_name, last_name, email, password) VALUES (?, ?, ?, ?, ?)",
                      (title, first_name, last_name, email, hashed_password))
            conn.commit()
            st.success(f"Registered successfully as {title} {first_name} {last_name} ({email})")
        else:
            st.error("Password and password confirmation do not match.")

elif menu == "Reset Password":
    st.header("Reset Password")
    email = st.text_input("Email")
    reset_button = st.button("Reset Password")

    if reset_button:
        st.error("Password reset functionality is not implemented in this example.")

# Close the SQLite connection when the app is finished
conn.close()
