# Lemon Questionnaire Platform
> 简易问卷平台。
- 后端：Flask + mysql
- 前端：Vue + element-ui + echarts
## 功能

- 用户注册、登录，用户注册时需要填写邮箱并验证，用户名、密码要求在6字节以上，email的格式验证，并保证用户名和email在系统中唯一。
- 用户登录后可以设计问卷，一个问卷由标题、问卷说明和多个问卷项目组成，提供一个界面来动态设计，题目类型包含：
  - 单选
  - 多选
  - 文本填写（单行/多行）
  - 数字填写（整数/小数）
  - 评分（特殊的单选形式）
- 问卷设计完成后生成填写链接，通过分享链接由他人填写，分享时可以设定填写周期和填写方式，填写方式支持以下几种：
  - 仅限登录用户
  - 无需登录，一人总共可填写n次
  - 无需登录，一人每天可填写n次
  - 备注：将通过ip地址确定未登录用户
- 保存填写结果并可以在问卷分析界面展示填写结果
- 管理问卷界面可以发布问卷/删除问卷/查看分析

## 结构
```bash
.
├── README.md
├── app.py
├── config.py
├── database.py
├── lemon.sql	# MySQL database initialization
├── main.py		# entrance of app
├── pages		# route and logic for different features
│   ├── __init__.py
│   ├── account.py
│   ├── analyze.py
│   ├── design.py
│   ├── fill.py
│   ├── home.py
│   └── manage.py
├── requirements.txt
├── static		# third-party js / css library
│   ├── css
│   │   ├── element-ui@2.13.2.css
│   │   └── fonts
│   │       ├── element-icons.ttf
│   │       └── element-icons.woff
│   └── js
│       ├── echarts@4.1.0.js
│       ├── element-ui@2.13.2.js
│       ├── vue@2.6.11.js
│       └── vue@2.6.11.min.js
└── templates	# used for rendering pags
    ├── analyze.html
    ├── design.html
    ├── fill.html
    ├── index.html
    ├── login.html
    └── manage.html
```

## 运行

- 在MySQL执行`lemon.sql`
- 按`requirements.txt`配置环境
- 在`config.py`中配置好MySQL连接（用户名/密码/服务器/端口等等）
- 执行`python main.py`可以运行
- 部署在服务器请自行配置gunicorn等工具

## 截图
### 首页

<img src="screenshots/home1.png" alt="home1" style="zoom:50%;" />

<img src="screenshots/home2.png" alt="home2" style="zoom:50%;" />

### 登录

<img src="screenshots/login1.png" alt="login1" style="zoom:50%;" />

<img src="screenshots/login2.png" alt="login2" style="zoom:50%;" />

### 设计

![design](screenshots/design1.png)

![design2](screenshots/design2.png)

### 管理

![manage1](screenshots/manage1.png)

![manage2](screenshots/manage2.png)

![manage3](screenshots/manage3.png)

### 填写

![fill1](screenshots/fill1.png)

![fill2](screenshots/fill2.png)

![fill3](screenshots/fill3.png)

### 分析

![analyze1](screenshots/analyze1.png)

![analyze2](screenshots/analyze2.png)

![analyze3](screenshots/analyze3.png)

![analyze4](screenshots/analyze4.png)

![analyze5](screenshots/analyze5.png)