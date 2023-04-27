import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

def isOK():
    url = "http://zsbbm.masu.edu.cn/login"
    try:
        response = requests.get(url, timeout=15)  # 设置超时时间为5秒
        if response.status_code == 200:
            print('访问成功')
            return True
        else:
            print('访问失败')
            return False
    except requests.exceptions.Timeout:
        print('请求超时')
        return False
def get_score_page():
    url = "http://zsbbm.masu.edu.cn/score" # 查询地址
    header={
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "Cookie":"b-user-id=a5a771fd-xxxxxxxxxxxxao85kbbncdpd3a7ee1kteu04", # cookie 通过网页抓包获取
        "Connection":"keep-alive",
        "Host":"zsbbm.masu.edu.cn"
    }
    resp=requests.post(url=url,headers=header).content
    content = resp.decode("utf-8")
    # with open("index.html",'w') as f:
    #     f.write(content)
    #print(content)
    return content
def get_score(html_page):
    # html_page=""
    # with open("index.html","r") as f:
    #     html_page=f.read()
    soup = BeautifulSoup(html_page,'html.parser')
    table = soup.find('table') # 获取表格元素
    # 获取表头数据
    headers = [th.text for th in table.select('thead th')]
    # 获取表格数据
    rows = table.select('tbody tr')
    data=[]
    for row in rows:
        data = [td.text for td in row.select('td')]
    # 将headers和data合并成一个字典
    score_dict={headers[i]: data[i] for i in range(len(headers))}
    print(score_dict)
    return score_dict
def send_email(score_dict):
    data = score_dict
    # 设置发件人邮箱和密码
    sender_email = 'xxxxxxxxx@qq.com'
    sender_password = 'fxxxxxxxxxxxxxxx' #邮箱授权码
    # 设置收件人邮箱
    receiver_email = 'wangyuqi@wyq.icu'
    # 设置邮件主题和内容
    subject = '成绩单'
    content = '<table>'
    for key, value in data.items():
        content += f'<tr><td>{key}</td><td>{value}</td></tr>'
    content += '</table>'
    msg = MIMEText(content, 'html', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = formataddr(('Sender', sender_email))
    msg['To'] = receiver_email
    # 发送邮件
    try:
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, [receiver_email], msg.as_string())
        print('邮件发送成功')
    except Exception as e:
        print('邮件发送失败')
        print(str(e))
    finally:
        server.quit()
if __name__ == '__main__':
    while(True):
        if(isOK()):
            send_email(get_score(get_score_page()))
            break
