# WF 文件管理器 (Web File Explorer)
![python](https://img.shields.io/badge/Python-3.5+-green.svg)
![build](https://img.shields.io/badge/build-passed-green.svg)
![FrameWork](https://img.shields.io/badge/Django-2.0+-green.svg)  
--------
Contact me | 
--------- |
DaiQiang: daiqianghaha@foxmail.com | 

一款美观易用性强快速部署的网页文件管理器，符合Google Material Design，采用Python语言 Django 框架编写。  
A user-friendly install easily WebBased File Browser programed with Python Django with Material Design Interface.   
### [ English](../README.md) | 中文文档
## 登录界面
![login](./README/login.png "登录界面") 
## 文件预览
![preview](./README/preview_EN.gif "文件预览")
## 拖动快速移动复制文件
![drag](./README/drag_EN.gif "拖动快速移动复制文件")
## 快速重命名
![rename](./README/rename_EN.gif "快速重命名")
## 删除文件
![delete](./README/delete_EN.gif "删除文件")

# 优点

* 快速配置，一键部署，立即启动项目，python解释运行无需编译
* CSRF token 验证技术，防止跨站请求伪造（CSRF）攻击
* 异步动态加载技术，可瞬间渲染上万文件
* 文件预览功能 快速查看文本文件、项目代码和各种格式的图片文件
* 多文件快速压缩打包下载
* 可自定义背景图等风格

# 安装说明
1. 下载项目所有文件
2. 终端或命令行运行
 `pip install Django`  
 如果同时安装了python3和python2 请运行  
    `pip3 install Django`

3. 修改app目录下的`userdata.conf` 配置用户名和密码  
修改app目录下的`rootpath.conf` 配置需要管理的路径根目录
4. 终端运行
`python3 manage.py runserver 0.0.0.0:5210`

0.0.0.0 和5210 可根据需要更换成自定义的IP和端口

5. 浏览器访问 0.0.0.0:5201 即可管理文件
