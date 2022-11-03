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

from credientials import Credientials
# from exception import print


ssl._create_default_https_context = ssl._create_unverified_context #skip ssl certificate verification
account  = Credientials()
sender_address =  account.uid
sender_pass = account.pw

past = datetime.datetime.now() - datetime.timedelta(days=1)

WhenMailLastSent = past
status = None 
ContinousON = [past, past]
ContinousOFF = [past, past] 

#customable
address = 'https://www.obaksago.com:8443'
receiver  = 'geulligu89@naver.com'
term = 30 #sec
mail_term_when_down = 10 #min
sendEveryday = True
sendEveryweek = False

#이메일 보내는 함수 / void
def SendGmail(receiver, title, content): 
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver
    message['Subject'] = title

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
    global status

    try: 
        status_code = urllib.request.urlopen(address).getcode()

    except URLError: #아예 꺼지면 http 400, 500 오류 코드도 안옴 
        status = False
        errTime = datetime.datetime.now()
        errName = 'Connection refused. server failed.'
        print(errName, errTime)
        return [errTime, errName]

    if str(status_code)[0] == 4 or str(status_code)[0] == 5: #400, 500번대 오류 코드일시 
        status = False 
        errTime = datetime.datetime.now()
        errName = status_code
    print(errName, errTime)
    return [errTime, errName]


#자정인지
def ifMidnight():
    now = datetime.datetime.now()
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

    if (sendEveryday == True) and ((midnight_range[0] < now and now < midnight_range[1]) or (midnight_range[2] < now and now < midnight_range[3]) or (midnight_range[4] < now and now < midnight_range[5])): 
        return True

    else: return False


#켜진 상태, 보낼 시간됐는지 / boolean
def ONcheckTimeIfMail (): #매주 또는 매일 0:00시인지 확인. 절대적. no param
    if sendEveryday == True: 
        if ifMidnight(): return True
        else: return False

    elif sendEveryweek == True: 
        if datetime.datetime.now().weekday == 0:
            if ifMidnight(): return True
            else: return False
        else: return False


#꺼진 상태, 보낼 시간됐는지 / boolean
def OFFcheckTimeIfMail (to_compare): #보낸지 10분 이상 지났는지 확인. 상대적
    global WhenMailLastSent
    if (WhenMailLastSent < (to_compare - datetime.timedelta(minutes=mail_term_when_down))) or WhenMailLastSent == None: #to_compare - now가 10분 이상이거나 처음이거나
        WhenMailLastSent = datetime.datetime.now()
        return True

    else: return False


#메일 내용 생성 / [title,  content]
def createTitlteNContent(errTime, errName, first=False): #and global varible: address, mygit
    title, content = None, None

    if errTime == None and errName == None:
        title = "NOT error message, just notification about " + address

        content = address + " has been connected successfully for " + "minutes" + " to " + \
            ContinousON[0] + ContinousON[1] + \
            'sincerly ' + 'https://github.com/sungjun4403'

    elif errTime == None and errName == None and first == True: #Back Online
        title = address + "is Back Online!"

        content = address + " connection successed. Your web went down" + 'TIME' + "since" + 'TIME' + \
            'for ' + 'TIME' + 'minutes'

    elif errTime != None and errName != None and first == True: #First Failure
        title = 'ALERT! ERROR found on' + address 

        content = address + "failed" + "<br>" + \
            str(errName) + "found at " + str(errTime) + "<br>" + \
            'before failure, your web has been connected' + 'minutes continously' + "<br>" + \
            'sincerly ' + 'https://github.com/sungjun4403' 

    else: 
        title = 'RE-ALERT! ERROR found on ' + address

        content = address + "failed" + "<br>" + \
            str(errName) + "found at " + str(errTime) + "<br>" + \
            str(ContinousOFF[0]) + str(ContinousOFF[1]) + \
            'failed since' + 'minutes' + "<br>" + \
            'sincerly ' + 'https://github.com/sungjun4403' 


    return [title, content] 



if __name__ == '__main__': 
    alpha = True
    first = None

    while alpha:
        errTime, errName = StatusChecker(address)

        if status == True or (errTime == None): #웹 정상이고
            if WhenMailLastSent < (datetime.datetime.now() - datetime.timedelta(seconds=60)): 
                ContinousON[0] = datetime.datetime.now()
                first = True
            else: ContinousON[1] = datetime.datetime.now()

            if ONcheckTimeIfMail(): #보낼 시간 됐으면 
                title, content = createTitlteNContent(None, None)   #메일 내용 만들어서 
                SendGmail(receiver, title, content) #메일 보내기
                print('mail sent')
            elif ONcheckTimeIfMail() == True and first == True:
                title, content = createTitlteNContent(None, None, True)   #메일 내용 만들어서 
                SendGmail(receiver, title, content) #메일 보내기
                print('mail sent')
                first = None
            else: pass

        elif status == False: #웹 비정상인데    
            if ContinousON[1] < (datetime.datetime.now() - datetime.timedelta(seconds=60)):
                ContinousOFF[0] = datetime.datetime.now()
                first = True
            else: ContinousOFF[1] = datetime.datetime.now()

            if OFFcheckTimeIfMail(errTime): #10분 됐으면
                title, content = createTitlteNContent(errTime, errName)    #에러로 메일 내용 만들어서 
                SendGmail(receiver, title, content) #메일 보내기 
                print('mail sent')
            elif OFFcheckTimeIfMail(errTime) == True and first == True: #10분 됐으면
                title, content = createTitlteNContent(errTime, errName, True)    #에러로 메일 내용 만들어서 
                SendGmail(receiver, title, content) #메일 보내기 
                print('mail sent')
                first == None
            else: print('pass'); pass 
            
        else: time.sleep(5); continue #StatusChecker(address) 실패했을 때 

        time.sleep(term)



