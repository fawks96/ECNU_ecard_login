# coding=utf-8
import urllib2
import cookielib
import xlrd
import urllib
import sys
import pytesseract
from PIL import Image
reload(sys)
sys.setdefaultencoding("utf-8")
# 防止中文报错


CaptchaUrl = "http://www.ecard.ecnu.edu.cn/util/rand"
PostUrl = "http://www.ecard.ecnu.edu.cn/weblogin"
# 验证码地址和post地址

#存储账号名和密码的文件
data = xlrd.open_workbook('a.xlsx')

table = data.sheets()[0]

nrows = table.nrows

for i in range(1,nrows):
    list = table.row_values(i)
    studentId = str(list[0])[0:11]
    studentPwd = list[2]
    pwdlen = len(studentPwd)
    studentPwd = studentPwd[pwdlen-6:pwdlen]

    if studentPwd[5] == 'X':
        studentPwd = studentPwd[:5] + '0'

    cookie = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    # 将cookies绑定到一个opener cookie由cookielib自动管理

    # 用户名和密码
    picture = opener.open(CaptchaUrl).read()
    # 用openr访问验证码地址,获取cookie
    local = open('image.jpg', 'wb')
    local.write(picture)
    local.close()
    # 保存验证码到本地

    image = Image.open('image.jpg')
    SecretCode = pytesseract.image_to_string(image)

    #SecretCode = raw_input('输入验证码： ')
    # 打开保存的验证码图片 输入
    postData = {
        'username':studentId,
        'password':studentPwd,
        'code':SecretCode,
    }
    # 根据抓包信息 构造表单
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
    }
    # 根据抓包信息 构造headers
    data = urllib.urlencode(postData)
    # 生成post数据 ?key1=value1&key2=value2的形式
    request = urllib2.Request(PostUrl, data, headers)

    #cookie:<Cookie JSESSIONID=1C46D4CB6A3D1D873B8E6303F4CAFC7A for www.ecard.ecnu.edu.cn/>
    '''
    try:
        response = opener.open(request)
        result = response.read()
        print result
        # 打印登录后的页面
    except urllib2.HTTPError,e:
        print e
    '''
    host_url = "http://www.ecard.ecnu.edu.cn"
    sub_url = "/head/"
    tail_url = "_1.jpg"
    #用户头像url
    head_url = host_url + sub_url + studentId + tail_url;
    print head_url
    try:
        get_response = opener.open(request)
    except urllib2.HTTPError,e:
        print ('fuck1')
        continue
    try:
        get_response2 = opener.open(head_url)
    except urllib2.HTTPError, e:
        print ('fuck2')
        continue
    #print(get_response.read().decode())
    #print(get_response2.read())
    local2 = open(studentId+'.jpg', 'wb')
    local2.write(get_response2.read())
    local2.close()