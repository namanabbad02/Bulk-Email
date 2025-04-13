# from flask import Flask, request, render_template
# import pandas as pd
# import os
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import smtplib
# import webbrowser
# import threading

# app = Flask(__name__)
# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
        # try:
        #     email = request.form['email']
        #     password = request.form['password']
        #     subject = request.form['subject']
        #     body_template = request.form['body']
        #     file = request.files['file']

        #     if not email or not password or not subject or not body_template or not file:
        #         return "All fields are required."

        #     filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        #     file.save(filepath)

        #     # Read CSV with tab separator
        #     df = pd.read_csv(filepath, sep='\t')

        #     if 'name' not in df.columns or 'email' not in df.columns:
        #         return "CSV must contain 'name' and 'email' columns."

#             server = smtplib.SMTP('smtp.gmail.com', 587)
#             server.starttls()
#             server.login(email, password)

#             for index, row in df.iterrows():
#                 name = row['name']
#                 to_email = row['email']

#                 msg = MIMEMultipart()
#                 msg['From'] = email
#                 msg['To'] = to_email
#                 msg['Subject'] = subject

#                 body = body_template.format(name=name)
#                 msg.attach(MIMEText(body, 'plain'))
#                 server.send_message(msg)

#             server.quit()
#             return "Emails sent successfully!"

#         except Exception as e:
#             return f"An error occurred: {str(e)}"

#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)
#     # Open browser in a separate thread after 1 sec
#     # threading.Timer(1.0, lambda: webbrowser.open('http://localhost:5000')).start()
#     # app.run(debug=False)

import threading
import webview
from flask import Flask, request, render_template
import pandas as pd
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         try:
#             email = request.form['email']
#             password = request.form['password']
#             subject = request.form['subject']
#             body_template = request.form['body']
#             file = request.files['file']

#             if not email or not password or not subject or not body_template or not file:
#                 return "All fields are required."

#             filepath = os.path.join(UPLOAD_FOLDER, file.filename)
#             file.save(filepath)

#             df = pd.read_csv(filepath, sep ='\t')  # assumes comma-separated

#             if 'name' not in df.columns or 'email' not in df.columns:
#                 return "CSV must contain 'name' and 'email' columns."

#             server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#             server.login(email, password)

#             for index, row in df.iterrows():
#                 name = row['name']
#                 to_email = row['email']

#                 msg = MIMEMultipart()
#                 msg['From'] = email
#                 msg['To'] = to_email
#                 msg['Subject'] = subject

#                 body = body_template.format(name=name)
#                 msg.attach(MIMEText(body, 'plain'))
#                 server.send_message(msg)

#             server.quit()
#             return "Emails sent successfully!"

#         except Exception as e:
#             return f"An error occurred: {str(e)}"

#     return render_template('index.html')
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            subject = request.form['subject']
            body_template = request.form['body']
            file = request.files['file']
            attachment = request.files.get('attachment')  # Optional file

            if not email or not password or not subject or not body_template or not file:
                return "All fields are required."

            # Save CSV file
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            # Save attachment if exists
            attachment_path = None
            if attachment and attachment.filename:
                attachment_path = os.path.join(UPLOAD_FOLDER, attachment.filename)
                attachment.save(attachment_path)

            # Read CSV
            df = pd.read_csv(filepath, sep='\t')  # default to tab-separated

            if 'name' not in df.columns or 'email' not in df.columns:
                return "CSV must contain 'name' and 'email' columns."

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(email, password)

            for index, row in df.iterrows():
                name = row['name']
                to_email = row['email']

                msg = MIMEMultipart()
                msg['From'] = email
                msg['To'] = to_email
                msg['Subject'] = subject

                body = body_template.format(name=name)
                msg.attach(MIMEText(body, 'plain'))

                # Attach file if present
                if attachment_path:
                    from email.mime.base import MIMEBase
                    from email import encoders

                    with open(attachment_path, "rb") as f:
                        mime = MIMEBase('application', 'octet-stream')
                        mime.set_payload(f.read())
                        encoders.encode_base64(mime)
                        mime.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment_path)}"')
                        msg.attach(mime)

                server.send_message(msg)

            server.quit()
            return "Emails sent successfully!"

        except Exception as e:
            return f"An error occurred: {str(e)}"

    return render_template('index.html')



def start_flask():
    app.run()

if __name__ == '__main__':
    threading.Thread(target=start_flask).start()
    webview.create_window("Bulk Email Sender", "http://127.0.0.1:5000")
