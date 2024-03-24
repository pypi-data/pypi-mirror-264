from mail_sender import create_sender, config_file_list
from email.mime.text import MIMEText

yahoo = 'daw30410@yahoo.com'
gmail = 'dwillcoxster@gmail.com'
fs = 'financial-secretary@community-ucc.org'

sender = create_sender(yahoo)

msg = MIMEText("This is a test message", 'plain')
msg['Subject'] = 'Test: cc to fs, bcc to gmail and yahoo, with split, v2'
# msg['to'] = gmail
msg['bcc'] = ','.join([yahoo, gmail])
msg['cc'] = 'david@urbanatroop104.org'

sender.send_message(msg)
