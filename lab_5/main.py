import email
import imaplib
import poplib
import smtplib
import ssl
import os
from email import encoders
from email import header
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from tkinter import filedialog
import tkinter as tk


username='valerian.labpr@outlook.com'
password= 'qwerty12345'

smtp_port=587
smtp_host='smtp.office365.com'

host = 'outlook.office365.com'
path='D:/univer/PR/lab5/downloads/'
attach_path='D:/univer/PR/lab5/attachments/'
def send_mail():
    message=MIMEMultipart()
    message['From'] = 'valerian.labpr@outlook.com'
    print("adresa unde doriti sa trimiteti emailul:")
    send_list=[]
    while True:
        addr=input()
        if addr=='/next':
            break
        else:
            send_list.append(addr)
    message['To'] =', '.join( send_list)
    #message['To'] = input()
    message['Subject'] = input('Subiectul:')
    body = input('Textul emailului:')
    attach_flag=input("Doriti sa atasati un fisier?\nDa: 1\nNu: 2\n")
    if attach_flag == '1':
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        attachment= open(file_path,'rb')
        attachment_pack=MIMEBase('application','octet-stream')
        attachment_pack.set_payload((attachment).read())
        encoders.encode_base64(attachment_pack)
        attachment_pack.add_header('Content-Disposition','attachment; filename= '+file_path.split('/')[-1])
        message.attach(attachment_pack)
    else:
      pass

    message.attach(MIMEText(body, 'plain'))
    text = message.as_string()

    try:
        tie=smtplib.SMTP(smtp_host,smtp_port)
        tie.starttls()
        tie.login(username,password)
        print("conected to smtp server\n")

        print(f"Sending email to - {message['From']}")
        tie.sendmail(username,send_list,text)
        print("email succesfully sent")

    except:
        print("ERROR")




#send_mail()
# Connect securely with SSL
def get_imap():
    imap = imaplib.IMAP4_SSL(host)
    imap.login(username, password)
    imap.select('Inbox')
    typ, data = imap.search(None, 'ALL')
    sbject=''
    sender=''
    for num in data[0].split():
        typ, msg_data = imap.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            fileName = part.get_filename()
            if bool(fileName):
                filePath = os.path.join(attach_path, fileName)
                if not os.path.exists('D:/univer/PR/lab5/attachments/'):
                    os.makedirs('D:/univer/PR/lab5/attachments/')
                if not os.path.isfile(filePath):
                    fp = open(filePath, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
                subject = str(msg).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
                #print(f'Downloaded {fileName} from email titled {subject}')

        print(f'Email: {num}: {msg["Subject"]}')

    print ("Doriti sa deaschideti un anumit email?")
    flag=input("Da: 1\nNu:2\n")
    if flag=='1':
        selected=input("Introduceti indexul mesajului dorit:")
        selected=int(selected)
        message_id = data[0].split()[selected]
        status, msg_data = imap.fetch(message_id, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
        sbject = msg.get('Subject')
        sender = msg.get('From')
        body = ''
        filename=''
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    body += part.get_payload(decode=True).decode('utf-8')
                if part.get_content_type() == 'su':
                    body += part.get_payload(decode=True).decode('utf-8')
                if part.get_content_type() == 'application/octet-stream':
                    filename = part.get_filename()


        else:
            # If the message is not multipart, just get the payload
            body += msg.get_payload(decode=True).decode('utf-8')

        # Print the body of the message
        print(f'#######################   Texutl emailului: #########################\n{body}')
        print(f'#######################   atasamente:##############################\n{filename}')
    elif flag =='2':
        pass
    if flag=='1':
        print("Doriti sa raspundeti la acest email?\n")
        flag_res = input("Da: 1\nNu:2\n")
        if flag_res=='1':

            # Connect to the SMTP server and send the reply message
            reply_msg = MIMEMultipart()
            reply_subject = f"Re: {sbject}"
            reply_body = input("Tastati raspunsul:\n")
            reply_body = MIMEText(reply_body)
            reply_msg['To'] = sender
            reply_msg['From'] = username
            reply_msg['Subject'] = reply_subject
            reply_msg.attach(reply_body)
            attach_flag = input("Doriti sa atasati un fisier?\nDa: 1\nNu: 2\n")
            if attach_flag == '1':
                root = tk.Tk()
                root.withdraw()
                file_path = filedialog.askopenfilename()
                attachment = open(file_path, 'rb')
                attachment_pack = MIMEBase('application', 'octet-stream')
                attachment_pack.set_payload((attachment).read())
                encoders.encode_base64(attachment_pack)
                attachment_pack.add_header('Content-Disposition', 'attachment; filename= ' + file_path.split('/')[-1])
                reply_msg.attach(attachment_pack)
            else:
                pass  # message= f'Subiect:{subject}\n\n {body}'

            #reply_msg.attach(MIMEText(reply_body, 'plain'))
            text = reply_msg.as_string()

            try:
                tie = smtplib.SMTP(smtp_host, smtp_port)
                tie.starttls()
                tie.login(username, password)
                print("conected to smtp server\n")

                #print(f"Sending email to - {message['From']}")
                tie.sendmail(username, sender, text)
                print("email succesfully sent")
                tie.quit()
            except:
                print("ERROR")
        else:
            pass

def get_pop3():
    pop=poplib.POP3_SSL(host,995)
    pop.user(username)
    pop.pass_(password)

    if not os.path.exists(path):
        os.makedirs(path)

    nr_message = len(pop.list()[1])
    for i in range(nr_message):
        response = pop.retr(i + 1)
        raw_message = response[1]
        message = b'\r\n'.join(raw_message).decode('utf-8')
        # Parse the message using the email library
        parsed_message = email.message_from_string(message)

        for part in parsed_message.walk():
            if part.get_content_disposition() == 'attachment':
                filename = part.get_filename()
                filepath = os.path.join(path, filename)
                with open(filepath, 'wb') as f:
                    f.write(part.get_payload(decode=True))
                    print(f"  Attachment saved: {filepath}")
        subject = parsed_message['Subject']
        filename = f"{i + 1}_{subject}.eml"
        filepath = os.path.join(path, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(message)
        # Print the subject line of the message
        print(f"Message {i + 1}: {parsed_message['Subject']}")

#get_pop3()
def run():
    print('##########################################################################\n'
          '################             LABORATOR 5          ########################\n'
          '################                                  ########################\n'
          '##########################################################################\n')

    print('Ce doriti sa efectuati?\n\n'
          'Verificare inbox-ului prin IMAP:  1\n'
          'Verificarea inbox-ului prin POP3:  2\n'
          'Trimiterea unui email: 3')
    while True:
        print('Ce doriti sa efectuati?\n')
        case = int(input())
        if case==1:
            get_imap()
        elif case==2:
            get_pop3()
        elif case==3:
            send_mail()


if __name__=='__main__':
    run()