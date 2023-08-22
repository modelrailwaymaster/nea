import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase

port = 587
host = "smtp-mail.outlook.com"
password = "p18s2h2APoxuKzE"
sender_email = "henryowennea@outlook.com"
receiver_email = "henryowen2006@outlook.com"

message = MIMEMultipart("alternative")
message["Subject"] = "multipart test"
message["From"] = sender_email
message["To"] = receiver_email

text = """\
Hi,
how are you doing?
"""
html = """\
<html>
    <body>
    this is in the html
    <a href="www.google.com">link here</a>
    </body>
</html>
"""

# text only appears if the receiver cant format html

part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

message.attach(part1)
message.attach(part2)

# filename = "test.txt"

# with open(filename, "rb") as file:
#    part3 = MIMEBase("application", "octet-stream")
#    part3.set_payload(file.read())

# encoders.encode_base64(part3)
# part3.add_header("Content-Disposition", f"attachment; filename= {filename}",)

# message.attach(part3)

smtp = smtplib.SMTP(host=host, port=port)
status_code, response = smtp.ehlo()
print(status_code, response)
status_code, response = smtp.starttls()
print(status_code, response)
status_code, response = smtp.login(sender_email, password)
print(status_code, response)
smtp.sendmail(sender_email, receiver_email, message.as_string())
smtp.quit()
