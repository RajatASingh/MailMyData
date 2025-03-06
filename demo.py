import smtplib
import os
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Read data and convert to HTML table
df = pd.read_excel("SalesData.xlsx")

html_table = df.to_html(index=False)  # Removes the default index column

# SMTP Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "rajat.singh@aarav.co"
EMAIL_RECEIVER = "siddhesh.ambre@aarav.co"
EMAIL_PASSWORD = "R@9967366993"  # Securely fetch the password

# Email Subject
subject = "Revised Prices for FY 2025-26"

# HTML Email Content
html_content = f"""\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Price Revision Notice</title>
    <style> 
        h1 {{ font-size: 50px; color: brown; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ border: 1px solid black; padding: 10px; text-align: left; }}
        th {{ background-color: #98D8EF; }}
    </style>
</head>
<body>
<p>Dear Sir/ Ma’am,</p>
<p>We are proposing revised prices for the new financial year 2025-26. These prices are effective from <b>April 1st, 2025.</b></p>

{html_table}  <!-- This inserts the HTML table dynamically -->

<p><b>Applicable GST extra.</b></p>
<p>The revised prices being communicated would be valid for FY 2025-26.</p>

<p>Thank you!</p>

<p>For <b>Aarav Fragrances & Flavors Pvt Ltd.</b></p>
<p><b>Siddhesh Ambre</b></p>

<h3>This is a demo</h3>
</body>
</html>
"""

# Setting Up the Email
msg = MIMEMultipart()
msg["From"] = EMAIL_SENDER
msg["To"] = EMAIL_RECEIVER
msg["Subject"] = subject
msg.attach(MIMEText(html_content, "html"))

try:
    # Connect to SMTP Server
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()  # Secure connection
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)  # Login

    # Send Email
    server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

    # Close Server
    server.quit()
    print("✅ Email sent successfully!")

except Exception as e:
    print(f"❌ Error: {e}")
