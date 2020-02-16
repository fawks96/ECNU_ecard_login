# ECNU_ecard_login
An automated login script for ecnu ecard system (www.ecard.ecnu.edu.cn) with a user facial attractiveness grading feature.


## 原理
查看网络请求容易得知登录方式为向地址 www.ecard.ecnu.edu.cn/weblogin 发送`username`、`password`、`code`三个字段值（下方 Form data 处）。

![Request](https://github.com/fawks96/ECNU_ecard_login/blob/master/Request.jpg?raw=true)

利用urllib库向网站发送该三个字段值即可。

其中`code`为验证码字段。查看网络请求容易得知该验证码图片的获取地址为 www.ecard.ecnu.edu.cn/util/rand。

![Request2](https://github.com/fawks96/ECNU_ecard_login/blob/master/Request2.png?raw=true)

通过向该地址发送请求获取验证码图片，然后使用`pytesseract`库将验证码图片OCR解析为具体数值。


## 使用
将`login.py`中的`studentId`和`studentPwd`设为目标账号密码即可。默认通过文件批量传入。
