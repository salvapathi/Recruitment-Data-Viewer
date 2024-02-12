import streamlit as st
import mysql.connector
import pandas as pd
import subprocess

# Function to get recruitment data based on selected search criteria
def get_recruitment_data(criteria_value, search_criteria):
    mysql_host = "localhost"
    mysql_user = "root"
    mysql_password = "iscs_user"
    mysql_database = "iscs"

    connection = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )

    cursor = connection.cursor()

    if search_criteria == "Recruiter":
        query = "SELECT * FROM Recruitment WHERE Recruiter = %s;"
    elif search_criteria == "Mobile_No":
        query = "SELECT * FROM Recruitment WHERE Mobile_No = %s;"
    elif search_criteria == "Technology":
        query = "SELECT * FROM Recruitment WHERE Technology = %s;"

    cursor.execute(query, (criteria_value,))
    
    rows = cursor.fetchall()

    # Extracting column names from the cursor description
    column_names = [desc[0] for desc in cursor.description]

    cursor.close()
    connection.close()

    return rows, column_names

# Function to validate phone number
def validate_phone_number(phone_number):
    if not phone_number.isdigit() or len(phone_number) != 10:
        return False
    return True

# Streamlit UI
def main():
    # Set page title and background color
    st.set_page_config(
        page_title="Recruitment Data Viewer",
        page_icon=":bar_chart:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Add a background color to the entire app
    st.markdown(
    """
    <style>
        body {
            background-color: #720D9B;
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
        }
        .st-bh {
            background-color: #1E88E5;
            color: white;
            padding: 1rem;
            border-radius: 0.5rem;
        }
        .st-eb {
            background-color: #ffffff;
            padding: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .dataframe {
            background-color: #ffffff;
            border-collapse: collapse;
            margin-top: 1rem;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        th, td {
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #1E88E5;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True
)

    st.title("ISCS Recruitment Data Viewer")

    # Dropdown to select search criteria
    search_criteria = st.selectbox("Select Search Criteria:", ["Recruiter", "Mobile_No", "Technology"])

    # Input for selected criteria
    criteria_value = st.text_input(f"Enter {search_criteria}:")

    # Validate phone number if Mobile_No is selected
    if search_criteria == "Mobile_No" and criteria_value and not validate_phone_number(criteria_value):
        st.warning("Please enter a valid 10-digit phone number.")

    # Debugging information
    st.write(f"{search_criteria} Entered: {criteria_value}")

    # Button to fetch data
    if st.button("Fetch Data"):
        if criteria_value:
            recruitment_data, column_names = get_recruitment_data(criteria_value, search_criteria)

            # Displaying the data in a DataFrame with custom styles
            if recruitment_data:
                df = pd.DataFrame(recruitment_data, columns=column_names)
                st.dataframe(df.style.set_properties(**{'background-color': '#1abc9c', 'color': 'black'}), height=500)  # Adjust the height of the DataFrame
            else:
                st.warning("No data found for the given criteria.")
        else:
            st.warning("Please enter a value for the selected search criteria.")

if __name__ == "__main__":
    # Install Ngrok authtoken
    subprocess.run(["C:/Users/DELL/AppData/Roaming/npm/ngrok.cmd", "authtoken", "2c7p2kLhZ8kcRfIsbSg1lzVWOqV_84ytnNJmQVngJaowK2CvZ"])

    # Use Ngrok to expose the Streamlit app to the internet
    subprocess.Popen(["C:/Users/DELL/AppData/Roaming/npm/ngrok.cmd", "http", "8501"])

    # Run the Streamlit app
    main()


