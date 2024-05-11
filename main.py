import streamlit as st
import mysql.connector
import hashlib
from streamlit_option_menu import option_menu
from symptom_module import symptome
from bot_module import chat_bot
from malaria_module import malaria
from diabetes_module import diabetes
from streamlit_extras.colored_header import colored_header


# Function to establish a connection to the MySQL database
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="disease"
    )

# Function to hash a password using SHA-256
def hash_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

# Function to insert a user into the MySQL database
def insert_user(firstname, lastname, email, gender, age, username, password):
    try:
        # Hash the password
        hashed_password = hash_password(password)

        # Establish a connection to the MySQL database
        connection = connect_to_database()

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Check if any required field is empty
        if not all([firstname, lastname, email, gender, age, username, password]):
            st.warning("Please fill in all the required fields.")
            return False

        # Check if the email already exists
        existing_query = "SELECT * FROM user WHERE email=%s"
        cursor.execute(existing_query, (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            st.warning("Email already exists. Choose a different email.")
            return False

        # Query to insert a new user with hashed password
        insert_query = "INSERT INTO user (firstname, lastname, email, gender, age, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (firstname, lastname, email, gender, age, username, hashed_password))

        # Commit the changes to the database
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return True

    except mysql.connector.Error as err:
        st.error(f"MySQL Error: {err}")
        return False

# Function to check credentials against MySQL database
def authenticate(email, password):
    try:
        # Hash the provided password
        hashed_password = hash_password(password)

        # Establish a connection to the MySQL database
        connection = connect_to_database()

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Query to retrieve a hashed password for the given email
        query = "SELECT password FROM user WHERE email=%s"
        cursor.execute(query, (email,))
        stored_password_tuple = cursor.fetchone()

        # Check if the email exists and if the hashed password matches
        if stored_password_tuple and hashed_password == stored_password_tuple[0]:
            return True

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return False

    except mysql.connector.Error as err:
        st.error(f"MySQL Error: {err}")
        return False

# Streamlit app for registration
def registration():
    st.title("Multiple Disease Diagnosis Expert System")
    colored_header(
        label="",
        description="Enter details to create Your Health Profile",
        color_name= "red-70",
        ) 

    # Using st.form to organize input fields
    with st.form(key="registration_form"):
        # Input fields for firstname, lastname, email, gender, and age
        col1, col2 = st.columns(2)
        firstname = col1.text_input("First Name", key="firstname", placeholder="Enter your first name")
        lastname = col2.text_input("Last Name", key="lastname", placeholder="Enter your last name")
        email = col1.text_input("Email", key="email", placeholder="Enter your email address")
        gender = col2.selectbox("Gender", ["Male", "Female", "Other"], key="gender")
        age = col1.number_input("Age", min_value=1, max_value=150, key="age", placeholder="Enter your age")
        username = col2.text_input("Username", key="username", placeholder="Choose a username")
        password = col1.text_input("Password", type="password", key="password", placeholder="Enter your password")
        confirm_password = col2.text_input("Confirm Password", type="password", key="confirm_password", placeholder="Confirm your password")

      
       
        # Validate input fields
        if st.form_submit_button("Create Health Profile"):
            # Check if passwords match
            if not all([password, confirm_password]) or password != confirm_password:
                st.warning("Passwords do not match. Please enter them again.")
            else:
                # Insert user into MySQL database
                if insert_user(firstname, lastname, email, gender, age, username, password):
                    st.success("Registration successful! You can now go to the Login page.")
                    
    # Add some space
    st.write("\n")
    st.write("\n")

    # Buttons to go to the other page
    st.button("I already have a Health Profile", on_click=lambda: st.session_state.update(page="login"))

    
    
def home():
    with st.sidebar:
        selected = option_menu('Multiple Disease Diagnosis Expert System',
                               [
                                'Symptom-based Diagnosis',
                                'Malaria Diagnosis',
                                'Diabetes Diagnosis',
                                'Disease Chatbot',
                                'Log out',
                                ],
                               icons=['person-lines-fill', 'bug',  'droplet-half', 'robot',
                                      'exit', ],
                               default_index=0,
                               styles={"nav-link": { "--hover-color": "#989898"},
                                       }
                               )
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
        
    if selected == 'Symptom-based Diagnosis':
        symptome()  
    if selected == 'Disease Chatbot':
        chat_bot()  
    if selected == 'Malaria Diagnosis':
        malaria()         
    if selected == 'Diabetes Diagnosis':
        diabetes()      
    if selected == 'Log out':
        st.session_state.page = "login"  
        st.rerun()    
    
    
    
    
    
# Streamlit app for login
def login():    

    st.title("Multiple Disease Diagnosis Expert System")
    colored_header(
        label="",
        description=" &nbsp;Login to continue with the Multiple Disease Diagnosis Expert System...",
        color_name= "red-70",
        ) 
    #Sst.write("\n")
    
  
    # Using st.form to organize input fields
    with st.form(key="login_form"):
        # Input fields for email and password
        email = st.text_input("Email", key="login_email", placeholder="Enter your email address")
        password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")

        # Validate input fields
        if st.form_submit_button("Login to profile"):
            # Authenticate user against MySQL database
            if not all([email, password]) or not authenticate(email, password):
                st.warning("Invalid email or password. Please try again.")
            else:
                #st.success("Login successful! Redirecting to the dashboard")
                st.session_state.page = "home"  
                st.rerun()
                
                
    # Add some space
    st.write("\n")
    st.write("\n")

    # Buttons to go to the other page
    st.button("Create Health Profile", on_click=lambda: st.session_state.update(page="register"))
    
    
   # import json
    #from streamlit_lottie import st_lottie
    #def load_lottiefile(filepath: str):
     ##      return json.load(f)
    #lottiedoc = load_lottiefile("C:\\Users\\User\\Downloads\\Animation.json")
    #st_lottie(
     #   lottiedoc,
      #  speed=1, 
    # loop=True,
     #   quality="h
    #)
    
    
# Main Streamlit app
def main():
    # Set background color using st.markdown
    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "login"

    
  
    # Depending on the page, call the appropriate function
    if st.session_state.page == "register":
        registration()
        
    elif st.session_state.page == "login":
        login()     
         
    elif st.session_state.page == "home":
        home()     
    
        

if __name__ == "__main__":
    main()



import streamlit as st
import mysql.connector
import hashlib
from streamlit_option_menu import option_menu
from symptom_module import symptome
from bot_module import chat_bot
from malaria_module import malaria


# Function to establish a connection to the MySQL database
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="disease"
    )

# Function to hash a password using SHA-256
def hash_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

# Function to insert a user into the MySQL database
def insert_user(firstname, lastname, email, gender, age, username, password):
    try:
        # Hash the password
        hashed_password = hash_password(password)

        # Establish a connection to the MySQL database
        connection = connect_to_database()

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Check if any required field is empty
        if not all([firstname, lastname, email, gender, age, username, password]):
            st.warning("Please fill in all the required fields.")
            return False

        # Check if the email already exists
        existing_query = "SELECT * FROM user WHERE email=%s"
        cursor.execute(existing_query, (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            st.warning("Email already exists. Choose a different email.")
            return False

        # Query to insert a new user with hashed password
        insert_query = "INSERT INTO user (firstname, lastname, email, gender, age, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (firstname, lastname, email, gender, age, username, hashed_password))

        # Commit the changes to the database
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return True

    except mysql.connector.Error as err:
        st.error(f"MySQL Error: {err}")
        return False

# Function to check credentials against MySQL database
def authenticate(email, password):
    try:
        # Hash the provided password
        hashed_password = hash_password(password)

        # Establish a connection to the MySQL database
        connection = connect_to_database()

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Query to retrieve a hashed password for the given email
        query = "SELECT password FROM user WHERE email=%s"
        cursor.execute(query, (email,))
        stored_password_tuple = cursor.fetchone()

        # Check if the email exists and if the hashed password matches
        if stored_password_tuple and hashed_password == stored_password_tuple[0]:
            return True

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return False

    except mysql.connector.Error as err:
        st.error(f"MySQL Error: {err}")
        return False

# Streamlit app for registration
def registration():
    st.title("Enter details to create Your Health Profile ")
    st.write("\n")

    # Using st.form to organize input fields
    with st.form(key="registration_form"):
        # Input fields for firstname, lastname, email, gender, and age
        col1, col2 = st.columns(2)
        firstname = col1.text_input("First Name", key="firstname", placeholder="Enter your first name")
        lastname = col2.text_input("Last Name", key="lastname", placeholder="Enter your last name")
        email = col1.text_input("Email", key="email", placeholder="Enter your email address")
        gender = col2.selectbox("Gender", ["Male", "Female", "Other"], key="gender")
        age = col1.number_input("Age", min_value=1, max_value=150, key="age", placeholder="Enter your age")
        username = col2.text_input("Username", key="username", placeholder="Choose a username")
        password = col1.text_input("Password", type="password", key="password", placeholder="Enter your password")
        confirm_password = col2.text_input("Confirm Password", type="password", key="confirm_password", placeholder="Confirm your password")

        # Set the style for the input fields to make text brighter
        input_fields_style = """
        <style>
            div[data-baseweb="input"] input {
                color: #FFFFFF !important;  /* Set the desired text color */
            }
        </style>
        """
        st.markdown(input_fields_style, unsafe_allow_html=True)

        # Validate input fields
        if st.form_submit_button("Create Health Profile"):
            # Check if passwords match
            if not all([password, confirm_password]) or password != confirm_password:
                st.warning("Passwords do not match. Please enter them again.")
            else:
                # Insert user into MySQL database
                if insert_user(firstname, lastname, email, gender, age, username, password):
                    st.success("Registration successful! You can now go to the Login page.")
                    
    # Add some space
    st.write("\n")
    st.write("\n")

    # Buttons to go to the other page
    st.button("I already have a Health Profile", on_click=lambda: st.session_state.update(page="login"))
    
    

    
    
    
# Streamlit app for login
def login():
    
    st.title("Multiple Disease Diagnosis Expert System")
    colored_header(
        label="",
        description="Authenticate to access the Multiple Disease Diagnosis Expert System",
        color_name= "red-70",
        )
    
    st.write("\n")

    # Using st.form to organize input fields
    with st.form(key="login_form"):
        # Input fields for email and password
        email = st.text_input("Email", key="login_email", placeholder="Enter your email address")
        password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")

        # Validate input fields
        if st.form_submit_button("Login"):
            # Authenticate user against MySQL database
            if not all([email, password]) or not authenticate(email, password):
                st.warning("Invalid email or password. Please try again.")
            else:
                #st.success("Login successful! Redirecting to the dashboard")
                st.session_state.page = "home"  
                st.experimental_rerun()
                
                
    # Add some space
    st.write("\n")
    st.write("\n")

    # Buttons to go to the other page
    st.button("Create Health Profile", on_click=lambda: st.session_state.update(page="register"))

   




# Main Streamlit app
def main():
    # Set background color using st.markdown
    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "login"

    
  
    # Depending on the page, call the appropriate function
    if st.session_state.page == "register":
        registration()
        
    elif st.session_state.page == "login":
        login()     
         
    elif st.session_state.page == "home":
        home()    
        
        
        
        

    
   