'''
sends email of your web status

code will check your web every 30secs (global varible: 'term')

email if: your web fails (10min term), every week or day 0:00 

email example: 
    title: 
        obaksago.com:8443 failed to connect

    content: 
        1. reason mail sent
        2. error * found
        3. failed since *, * minutes
        4. how long web connected successfully before failure
        5. my github address
'''

#email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#request check
from urllib.error import URLError
import urllib.request
import ssl

#time cal
import datetime
import time

import credientials


ssl._create_default_https_context = ssl._create_unverified_context
account  = credientials.Credientials()
sender_address =  account.uid
sender_pass = account.pw

status = None 

#customable
address = 'https://www.obaksago.com:8443'
term = 30 #sec
mail_term_when_down = 10 #min
sendEveryday = True
sendEveryweek = True

#이메일 보내는 함수 / void
def SendGmail(receiver, title, content): 
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver
    message['Subject'] = "! " + title + " connection failed!"   #The subject line

    #The body and the attachments for the mail
    message.attach(MIMEText(content, 'plain'))

    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver, text)
    session.quit()


#http response 보는 함수 / [errTime, errName]
def StatusChecker(address): 
    errName = None; errTime = None
    
    try: 
        status_code = urllib.request.urlopen(address).getcode()

    except URLError: #아예 꺼지면 http 400, 500 오류 코드도 안옴 
        status = False
        errTime = datetime.datetime.now()
        errName = 'Connection refused. server failed.'
        return [errTime, errName]

    if str(status_code)[0] == 4 or str(status_code)[0] == 5: #400, 500번대 오류 코드일시 
        status = False 
        errTime = datetime.datetime.now()
        errName = status_code
    return [errTime, errName]


#켜진 상태, 보낼 시간됐는지 / boolean
def ONcheckTimeIfMail (): #매주 또는 매일 0:00시인지 확인. 절대적. no param
    now = datetime.time.now()
    midnight_range = []

    dt = datetime.datetime.today() - datetime.timedelta(days=1)
    midnight = datetime.datetime.combine(dt, datetime.datetime.min.time())
    midnight_range.append(midnight - datetime.timedelta(seconds=30))
    midnight_range.append(midnight + datetime.timedelta(seconds=30))
    dt = datetime.datetime.today()
    midnight = datetime.datetime.combine(dt, datetime.datetime.min.time())
    midnight_range.append(midnight - datetime.timedelta(seconds=30))
    midnight_range.append(midnight + datetime.timedelta(seconds=30))
    dt = datetime.datetime.today() + datetime.timedelta(days=1)
    midnight = datetime.datetime.combine(dt, datetime.datetime.min.time())
    midnight_range.append(midnight - datetime.timedelta(seconds=30))
    midnight_range.append(midnight + datetime.timedelta(seconds=30))

    if (sendEveryday == True) and (): pass

    return None

#꺼진 상태, 보낼 시간됐는지 / boolean
def OFFcheckTimeIfMail (to_compare): #보낸지 10분 이상 지났는지 확인. 상대적
    now = datetime.datetime.now()


    #to_compare - now가 10분 이상이면 메일 보내기 



if __name__ == '__main__': 
    alpha = True

    midnight_range = []

    dt = datetime.datetime.today() - datetime.timedelta(days=1)
    midnight = datetime.datetime.combine(dt, datetime.datetime.min.time())
    midnight_range.append(midnight - datetime.timedelta(seconds=30))
    midnight_range.append(midnight + datetime.timedelta(seconds=30))
    dt = datetime.datetime.today()
    midnight = datetime.datetime.combine(dt, datetime.datetime.min.time())
    midnight_range.append(midnight - datetime.timedelta(seconds=30))
    midnight_range.append(midnight + datetime.timedelta(seconds=30))
    dt = datetime.datetime.today() + datetime.timedelta(days=1)
    midnight = datetime.datetime.combine(dt, datetime.datetime.min.time())
    midnight_range.append(midnight - datetime.timedelta(seconds=30))
    midnight_range.append(midnight + datetime.timedelta(seconds=30))

    for i in range (0, len(midnight_range), 1):
        print(midnight_range[i])

    # while alpha:
    #     errTime, errName = StatusChecker(address)

    #     if status == True: 
    #         ONcheckTimeIfMail()
    #         SendGmail()

    #     elif status == False:
    #         OFFcheckTimeIfMail()
    #         SendGmail()
        
    #     else: continue
    







    # alpha = True
    # while alpha:
    #     status = StatusChecker(address)
    #     ContinuousTime = datetime.datetime.now() - datetime.timedelta(firstTime)

    #     if status[0]: 
    #         firstTime = 0
    #         pass
    #     elif status[0] == False:
    #         if LatestSentTime == 0: 
    #             firstTime = datetime.datetime.now()
    #             content = contentProvider(status)
    #             SendGmail('geulligu89@naver.com', content, address)
    #             LatestSentTime = status[1]

    #         elif ifTenMinPassed(LatestSentTime, datetime.datetime.now()): 
    #             content = contentProvider(status)
    #             content += timeMinus(firstTime, datetime.datetime.now())
    #             SendGmail('geulligu89@naver.com', content, address)
    #             LatestSentTime = status[1]
        
    #     time.sleep(term)

    # SendGmail('geulligu89@naver.com', content)
        

##시간 연산
# def ifTenMinPassed(main, sub): 
#     return main < sub - datetime.timedelta(minutes=1)  #10분 지났는지 

# #에러 이름, 에러 시간, 연속으로 꺼지 시간 조합해서 메일 내용 만드는 함수
# def contentProvider(status): 
#     content = 'server failed at ' + str(status[1])[:-7] + ' / ' + str(status[2])
#     return content

# def timeMinus(bigger, smaller): 
#     lst = str(smaller.date()).split('-')
#     lst += str(smaller.time()).split(':')
#     print(lst)
#     bigger - datetime.timedelta(lst[0], lst[1], lst[2], lst[3], lst[4], lst[5])
