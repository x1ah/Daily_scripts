[百度贴吧自动签到小脚本.](https://xiahei.github.io/2016/06/18/sign-Baidu-Tieba/)
>由于贴吧登陆新增验证码机制，账号密码登陆签到已失效，改为用cookies，浏览器复制自己的cookies保存到此目录下新建的`cookies`文件中运行`python baidu_cookies_login.py`即可.



## 命令行版
- 依赖:
    - `BeautifulSoup`
        - `pip install bs4`
    - `requests`
        - `pip install requests`
    - `prettytable`
        - `pip install prettytable`

>以下均失效
- 使用
    - clone 代码，`python baidu.py`输入用户名，密码即可。

- `baidu_server.py` for 服务器
    - 添加手机号，密码，crontab(`01 8 * * * . /etc/profile;/usr/bin/python ***/Baidu/baidu_server.py >> ~/baidulog.txt`).

- result:
![res](http://ww4.sinaimg.cn/large/005NaGmtjw1f4yn4wrnxqj30yl08zaef.jpg)
![res](http://ww2.sinaimg.cn/large/005NaGmtjw1f4yn4j1um9j30p007h0w5.jpg)

## GUI版
- `tiebaGUI/` 为 GUI 版，太过简陋。依赖与上一致。
    - `python Gtieba.py`

GUI:
![tieba](http://ww3.sinaimg.cn/large/005NaGmtjw1f4ymy4xytbj30cn0k8tf1.jpg)
