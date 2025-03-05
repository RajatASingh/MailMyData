import pandas as pd
import streamlit as st
import plotly.express as px

import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

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

    st.title("📊 Sales Dashboard")

    if selected == "Sales Register":
        upload_file = st.file_uploader("Upload your sales file", type=["xlsx", "csv"])
        if upload_file:
            st.write("File uploaded successfully! ✅")
            df = pd.read_excel(upload_file) if upload_file.name.endswith(".xlsx") else pd.read_csv(upload_file)

            if st.button("Send Mail"):
                msg = MIMEMultipart()
                msg['Subject'] = 'Sales Analysis'
                msg['From'] = st.session_state.email
                msg['To'] = 'asusbrown99@gmail.com'
                body = """Hello Brown_Fox /n/n Happy to share the file with you about your sales as on today"""
               
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
            st.dataframe(df)
    elif selected == "Sales Analysis":
        st.subheader("Sales Data Visualization")
        upload_file = st.file_uploader("Upload your sales file for analysis", type=["xlsx", "csv"], key="analysis")
        if upload_file:
            df = pd.read_excel(upload_file) if upload_file.name.endswith(".xlsx") else pd.read_csv(upload_file)
            if "Location" in df.columns:
                fig = px.histogram(data_frame=df, x="Location", text_auto=True)
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
