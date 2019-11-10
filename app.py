from flask import Flask, request, render_template, flash, redirect, url_for
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True


app.secret_key='secret123'
 
@app.route('/')
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html')
 
    elif request.method == 'POST':
        mailer = Mailer()
        name = request.form['name']
        user_email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        print(name, user_email, subject, message)
        
        mailer.send(subject=subject, name=name, user_email=user_email, message=message)

        flash('Message sent', 'success')
        return redirect(url_for('contact')) # This can have a standard 'Thank you' message .

class Mailer:
    def __init__(self):
        self.PASSWORD = os.environ.get('EMAIL_PASSWORD')
        self.SMTP = app.config['MAIL_SERVER']
        self.PORT = app.config['MAIL_PORT']
        self.FROM_ADDR = os.environ.get('EMAIL_USER')
        self.TO_ADDR = os.environ.get('EMAIL_USER')
 
    def send(self, **kwargs):
        try:
            msg = MIMEMultipart()
 
            # Email fields
            toaddr = self.TO_ADDR
            msg['From'] = self.FROM_ADDR
            msg['To'] = toaddr
            msg['Subject'] = kwargs.get('subject')
 
            # Content of the email
            user_name = kwargs.get('name')
            user_email = kwargs.get('user_email')
            user_message = kwargs.get('message')
 
            #set email template
            html = self.template(user_name, user_email, user_message)
           
            msg.attach(MIMEText(html.encode('utf-8'), 'html', 'utf-8'))
            server = smtplib.SMTP(self.SMTP, self.PORT)
            server.starttls()
            server.login(self.FROM_ADDR, self.PASSWORD)
            text = msg.as_string()
            server.sendmail(self.FROM_ADDR, toaddr, text)
            server.quit()
 
            return None
        except Exception as e:
            print(e)
            pass
 
    def template(self, user_name, user_email, user_message):
        html = """
       From: {} -- {}
       Message:
       {}
       """.format(user_name, user_email, user_message)
        return html

if __name__ == '__main__':
    app.run(debug=True)