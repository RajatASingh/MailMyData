import pandas as pd
import streamlit as st
import plotly.express as px
import io

import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

st.set_page_config(layout='wide')

import streamlit as st


import streamlit as st

import streamlit as st

st.markdown(
    """
    <style>
        /* Sidebar background color */
        [data-testid="stSidebar"] {
            background-color: #789DBC !important; 
        }

        /* Main app background and font */
        [data-testid="stAppViewContainer"] {
            background-color: #FEF9F2 !important; 
            font-family: "Roboto", sans-serif;
        }

        /* Change Streamlit top header background */
        header[data-testid="stHeader"] {
            background-color: #FEF9F2 !important; 
            padding: 10px !important;
        }

        /* Change text color inside the header */
        header[data-testid="stHeader"] * {
            color: black !important;
            font-weight: bold !important;
        }

        /* Change button background color to navy */
        [data-testid="stButton"] button {
            background-color: #789DBC !important;
            color: white !important; /* Ensures text is visible */
            border-radius: 8px !important;
            padding: 8px 16px !important;
        }

        /* Change button hover effect */
        [data-testid="stButton"] button:hover {
            background-color: 789DBC !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)





from streamlit_option_menu import option_menu 

# Initialize session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "email" not in st.session_state:
    st.session_state.email = ""
if "password" not in st.session_state:
    st.session_state.password = ""

def login_page():
    st.title("🔒 Please Log In")

    email = st.selectbox("Your mail ID", help="Enter your mail ID from which you need to send the mail" , options= ["rajat.singh@aarav.co"])
    password = st.text_input("Share your Password", type="password", help="My eyes are closed, can't see your password" , value= st.session_state.password)

    if st.button("Login"):
        if email and password:
            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(email, password)
                    st.session_state.logged_in = True  # Mark user as logged in
                    st.session_state.email = email  # Store email in session
                    st.session_state.password = password  # Store password in session
                    st.success("Login Successful! ✅")
                    st.rerun()
            except smtplib.SMTPAuthenticationError:
                st.error("Authentication failed. Check your email and password.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.error("Please enter both email and password.")

def main_app():
    with st.sidebar:
        selected = option_menu("Mail Sales", ["Sales Register", "Sales Analysis", "Logout"], 
            icons=["file-earmark-plus", "bar-chart-line", "box-arrow-right"], menu_icon="cast", default_index=0)

    st.title("📊 Excel Distributor")

    if selected == "Sales Register":
        upload_file = st.file_uploader("Upload your sales file", type=["xlsx", "csv"])
        if upload_file:
            st.write("File uploaded successfully! ✅")
            file_bytes = io.BytesIO(upload_file.getvalue())
            df = pd.read_excel(file_bytes) if upload_file.name.endswith(".xlsx") else pd.read_csv(file_bytes)
            st.session_state.df

            if st.button("Send Mail"):
                msg = MIMEMultipart()
                msg['Subject'] = 'Sales Analysis'
                msg['From'] = st.session_state.email
                msg['To'] = 'priya.kamat@aarav.co'
                body = """Hello Priya Tai kamat This is a testing mail do not say that you don't like it you have to like it."""
               
                msg.attach(MIMEText(body, 'plain')) 
                file_name = 'brown_foxSales.xlsx'
                df.to_excel(file_name , index=False)
                attachment = open(file_name , "rb")
                p = MIMEBase('application', 'octet-stream') 

                p.set_payload((attachment).read()) 
                encoders.encode_base64(p) 
                p.add_header('Content-Disposition', "attachment; filename= %s" % file_name)

                msg.attach(p)
                text = msg.as_string() 


                try:
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(st.session_state.email, st.session_state.password)  # Fixed this part
                        smtp.sendmail(st.session_state.email, 'asusbrown99@gmail.com', text)
                        st.success("Mail sent successfully! 📩")
                except Exception as e:
                    st.error(f"Failed to send email: {e}")
            st.dataframe(df.head())
            if "region" in df.columns:
                fig = px.histogram(data_frame=df, x="region", text_auto=True , color= "region")
                st.write(fig)
            else:
                st.error("Column 'Location' not found in the dataset.")

    elif selected == "Sales Analysis":

        upload_file = st.file_uploader("Upload your sales file for analysis", type=["xlsx", "csv"], key="analysis")
        if upload_file:
            df = pd.read_excel(upload_file, engine='openpyxl') if upload_file.name.endswith(".xlsx") else pd.read_csv(upload_file)
            
            

            if st.button("Send Mail"):
                st.write("Mail has been send ✅😁")
            
            column_for_graph = df.columns.tolist()
            select_column = st.selectbox('Select A column base on which you want to see sales' , options= column_for_graph)
            if select_column in df.columns:
                fig = px.histogram(data_frame=df, x= select_column, text_auto=True)
                st.write(fig)
            else:
                st.error("Column 'Location' not found in the dataset.")

    elif selected == "Logout":
        st.session_state.logged_in = False
        st.rerun()

if __name__ == "__main__":
    if not st.session_state.logged_in:
        login_page()
    else:
        main_app()
