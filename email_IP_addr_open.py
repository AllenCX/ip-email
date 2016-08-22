
# coding: utf-8

# In[1]:

import smtplib
from email.mime.text import MIMEText
import uuid
import socket
import re, subprocess
from threading import Timer
import sched,time


# In[ ]:

MAIL_TO_LIST = ['xxxxxx@xxx.com']
MAIL_HOST = "smtp.xxxxx.com"
MAIL_USER = 'xxxx'
MAIL_PWD = 'xxxxx'
MAIL_POSTFIX = "xxx.xxx"

# In[25]:

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
    ifconfig  = subprocess.check_output('ifconfig', shell=True)
    ifconfig = str(ifconfig)
    ipList = re.findall('\d+\.\d+\.\d+\.\d+', ifconfig)
    ipList = "\n".join(ipList)
    return ipList

def get_mac_addr():
    node = uuid.getnode()
    mac = uuid.UUID(int = node).hex[-12:]
    return mac

def assemble_message():
    send_time = time.strftime('%Y%m%d %H:%M:%S',time.localtime())
    
    ip_addr = get_local_IP()
    machine_name = socket.gethostname()
    mac_addr = get_mac_addr()
    msg = 'ip address:\n' + ip_addr + '\n\n'+ 'mac address:\n' + mac_addr
    msg = msg + '\n' + send_time
    return msg


# In[28]:

def send_mail_clock(d=0, h=0, m=0, s=30):
    
    #caculate the interval, interval == 0 means send the message once and quit
    interval = d*24*3600 + h*3600 + m*60 + s
    
    msg = assemble_message()
    machine_name = socket.gethostname()
    sub = 'This the ip of your {0}'.format(machine_name)
    if interval == 0:
        i = 0
        SEND_FLAG = False
        if send_mail(MAIL_TO_LIST, sub, msg):
            print(time.strftime('%Y%m%d %H:%M:%S',time.localtime()))
            print("Email has been sent! Here below is the content!")
            print('='*80)
            print(msg)
            print('='*80)
            print('Stopped!')
            return
        else:
            #retry at most 20 times until success
            print('[{0}] Failed! Try again 10 seconds later!'.format(i))
            
            while(i<20 and SEND_FLAG == False):
                i += 1
                time.sleep(10)
                msg = assemble_message()
                SEND_FLAG = send_mail(MAIL_TO_LIST, sub, msg)
                #if i < 3: SEND_FLAG = False
                if SEND_FLAG == True:
                    print(time.strftime('%Y%m%d %H:%M:%S',time.localtime()))
                    print("Email has been sent! Here below is the content!")
                    print('='*80)
                    print(msg)
                    print('='*80)
                    print('Stopped!')
                    return
                else:
                    print('[{0}] Failed! Try again 10 seconds later!'.format(i))
            print('After trying 20 times, still cannot send the email!')
            return
        
    if send_mail(MAIL_TO_LIST, sub, msg):
        print(time.strftime('%Y%m%d %H:%M:%S',time.localtime()))
        print("Email has been sent! Here below is the content!")
        print('='*80)
        print(msg)
        print('='*80)
    else:
        print('failed!')    
    #automatically run the function to send message
    scheduler.enter(interval, 1, send_mail_clock, argument=(d,h,m,s))
    scheduler.run()


# In[29]:

if __name__ == '__main__':
    scheduler = sched.scheduler()
    #run once and quit
    send_mail_clock(0,0,0,0)
    print('Fuction out!')

