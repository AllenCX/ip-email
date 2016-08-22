
# coding: utf-8

# In[58]:

import smtplib
from email.mime.text import MIMEText
import uuid
import socket


# In[59]:

MAIL_TO_LIST = ['445631326@qq.com']
MAIL_HOST = "smtp.163.com"
MAIL_USER = 'gdga51'
MAIL_PWD = '135asdfghjkl'
MAIL_POSTFIX = "163.com"


# In[62]:

def send_mail(to_list, sub, content):
    me = MAIL_USER + '@' + MAIL_POSTFIX
    msg = MIMEText(content, _subtype='plain')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ';'.join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(MAIL_HOST)
        server.login(MAIL_USER, MAIL_PWD)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(str(e))
        return False
    
def get_local_IP():
    ip = socket.gethostbyname(socket.gethostname())
    return ip

def get_mac_addr():
    node = uuid.getnode()
    mac = uuid.UUID(int = node).hex[-12:]
    return mac


# In[63]:

if __name__ == '__main__':
    msg = get_local_IP()
    machine_name = socket.gethostname()
    mac_addr = get_mac_addr()
    title = 'This the ip of your {0}'.format(machine_name)
    if send_mail(MAIL_TO_LIST, title, msg):
        print('success!')
    else:
        print('failed!')    


# In[ ]:



