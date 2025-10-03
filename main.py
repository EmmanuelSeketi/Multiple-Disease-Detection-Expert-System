import streamlit as st
import mysql.connector
import hashlib

# Optional imports with safe fallbacks
try:
    from streamlit_option_menu import option_menu
except Exception:
    option_menu = None

try:
    from streamlit_extras.colored_header import colored_header
except Exception:
    def colored_header(label: str = "", description: str = "", color_name: str = None):
        st.markdown(f"**{label}**\n{description}")

# Import page modules (these should be import-safe)
from symptom_module import symptome
from bot_module import chat_bot
from malaria_module import malaria
from diabetes_module import diabetes

# Quick dev flag: set True to bypass login and go straight to the home dashboard
# Change to False to restore normal login flow
SKIP_AUTH = True


def connect_to_database():
    """Return a MySQL connection. Update credentials if needed for your environment."""
    return mysql.connector.connect(host="localhost", user="root", password="", database="disease")


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def insert_user(firstname, lastname, email, gender, age, username, password):
    try:
        hashed = hash_password(password)
        conn = connect_to_database()
        cur = conn.cursor()
        if not all([firstname, lastname, email, gender, age, username, password]):
            st.warning("Please fill in all the required fields.")
            cur.close(); conn.close(); return False
        cur.execute("SELECT * FROM user WHERE email=%s", (email,))
        if cur.fetchone():
            st.warning("Email already exists. Choose a different email.")
            cur.close(); conn.close(); return False
        cur.execute("INSERT INTO user (firstname, lastname, email, gender, age, username, password) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                    (firstname, lastname, email, gender, age, username, hashed))
        conn.commit()
        cur.close(); conn.close()
        return True
    except Exception as e:
        st.error(f"DB error: {e}")
        return False


def authenticate(email, password):
    try:
        hashed = hash_password(password)
        conn = connect_to_database()
        cur = conn.cursor()
        cur.execute("SELECT password FROM user WHERE email=%s", (email,))
        row = cur.fetchone()
        cur.close(); conn.close()
        return bool(row and row[0] == hashed)
    except Exception as e:
        st.error(f"DB error: {e}")
        return False


def registration():
    st.title("Multiple Disease Diagnosis Expert System")
    colored_header(label="", description="Enter details to create Your Health Profile", color_name="red-70")
    with st.form("registration_form"):
        col1, col2 = st.columns(2)
        firstname = col1.text_input("First Name")
        lastname = col2.text_input("Last Name")
        email = col1.text_input("Email")
        gender = col2.selectbox("Gender", ["Male", "Female", "Other"])
        age = col1.number_input("Age", min_value=1, max_value=150)
        username = col2.text_input("Username")
        password = col1.text_input("Password", type="password")
        confirm = col2.text_input("Confirm Password", type="password")
        if st.form_submit_button("Create Health Profile"):
            if not password or password != confirm:
                st.warning("Passwords do not match or are empty")
            elif insert_user(firstname, lastname, email, gender, age, username, password):
                st.success("Registration successful! You can now go to the Login page.")
    st.write("\n")
    st.button("I already have a Health Profile", on_click=lambda: st.session_state.update(page="login"))


def home():
    """Render the home page with a menu and route to page modules."""
    # Use top tabs for navigation; Symptom-based Diagnosis first so it is the default
    tabs = st.tabs(["Symptom based Diagnosis", "Malaria Diagnosis", "Diabetes Diagnosis", "Disease Chatbot", "Log out"])

    # Symptom tab (default)
    with tabs[0]:
        symptome()

    # Malaria tab
    with tabs[1]:
        malaria()

    # Diabetes tab
    with tabs[2]:
        diabetes()

    # Chatbot tab
    with tabs[3]:
        chat_bot()

    # Log out tab
    with tabs[4]:
        if st.button("Log out"):
            st.session_state.page = "login"
            st.experimental_rerun()

    # Navigation is handled via tabs above; no `selected` routing required.


def login():
    st.title("Multiple Disease Diagnosis Expert System")
    colored_header(label="", description="Login to continue", color_name="red-70")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if not authenticate(email, password):
                st.warning("Invalid email or password")
            else:
                st.session_state.page = "home"
                st.experimental_rerun()
    st.button("Create Health Profile", on_click=lambda: st.session_state.update(page="register"))


def main():
    if "page" not in st.session_state:
        # Use SKIP_AUTH to bypass login during development/testing
        st.session_state.page = "home" if SKIP_AUTH else "login"
    if st.session_state.page == "register":
        registration()
    elif st.session_state.page == "login":
        login()
    elif st.session_state.page == "home":
        home()


if __name__ == "__main__":
    main()






