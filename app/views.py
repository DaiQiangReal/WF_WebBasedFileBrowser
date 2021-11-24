'django.middleware.csrf.CsrfViewMiddleware'
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from app import Utils
from django.http import HttpResponse, Http404, FileResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import escape_uri_path
import tempfile, zipfile
from wsgiref.util import FileWrapper
import os
import json
import base64

# Create your views here.
userdata = None
rootpath=None

def needUserCookies(func):
    def wrapper(req):
        if isAuthenticated(req.COOKIES.get('username'), req.COOKIES.get('password')):
            return func(req)
        return HttpResponse("ERROR check your password!")
    return wrapper


def login(req):
    return render(req, "login.html")


def error(req):
    return HttpResponse("ERROR check your password!")


def isAuthenticated(username, password):
    global userdata
    if userdata == None:
        #with open("./app/userdata.conf") as config:
        #    userdata = eval(config.read())
        json_f=open('configuration.json','r')
        jsonObj=json.load(json_f)
        userdata={jsonObj["username"]:jsonObj["password"]}
    try:
        if userdata[username] == password:
            return True
    except Exception:
        return False


@csrf_exempt
def checkPassword(req):
    username = req.POST.get("username")
    password = req.POST.get("password")
    language=req.POST.get("language","en")
    if isAuthenticated(username, password):
        responseJson = {
            "ok": '/index',
        }
        response = HttpResponse(json.dumps(responseJson), content_type="application/json")
        response.set_cookie('username', username, 3600)
        response.set_cookie('password', password, 3600)
        response.set_cookie('language', language, 3600)
        return response
    else:
        responseJson = {
            "ok": '/error',
        }
        return HttpResponse(json.dumps(responseJson), content_type="application/json")


@needUserCookies
def main(req):
    global rootpath
    json_f=open('configuration.json','r')
    jsonObj=json.load(json_f)
    rootpath=jsonObj["rootpath"]
    Folder = Utils.Folder(rootpath)
    dataJson = Folder.getFolderJson()
    language=req.COOKIES.get('language')

    if language=="en":
        return render(req, "index_en-US.html", {"dataJson": dataJson})
    if language=="cn":
        return render(req, "index_zh-CN.html", {"dataJson": dataJson})

@csrf_exempt
@needUserCookies
def getDirContent(req):
    path = req.POST.get('path', None)
    if path is not None:
        Folder = Utils.Folder(path)
        dataJson = Folder.getFolderJson()
        return HttpResponse(dataJson, content_type="application/json")
    return HttpResponse(json.dumps({}), content_type="application/json")


@needUserCookies
def deleteFiles(req):
    deleteList = req.POST.get('deleteList', None).split(",")
    fileOperator = Utils.fileOperator()
    for file in deleteList:
        fileOperator.forceRemove(file)
    response = {
        "ok": True,

    }
    return HttpResponse(json.dumps(response), content_type="application/json")


@needUserCookies
def renameFiles(req):
    originPath = req.POST.get('originPath', None)
    newname = req.POST.get('newName', None)
    os.rename(originPath, os.path.split(originPath)[0] + "/" + newname)
    response = {
        "ok": True,

    }
    return HttpResponse(json.dumps(response), content_type="application/json")


@needUserCookies
def copyFiles(req):
    needCopyFileList = req.POST.get('needCopyFileList', None).split(",")
    targetPath = req.POST.get('targetPath', None)
    isMove = req.POST.get('isMove', False)
    fileOperator = Utils.fileOperator()

    fileOperator.copyFiles(needCopyFileList, targetPath, False if isMove != "true" else True)
    response = {
        "ok": True,
    }
    return HttpResponse(json.dumps(response), content_type="application/json")


@needUserCookies
def downloadFiles(req):
    downloadFileList = req.POST.get("downloadFileList").split(",")
    print(downloadFileList)
    fileOperator = Utils.fileOperator()
    return fileOperator.zipFilesInResponse(downloadFileList)


def mkdir(req):
    path = req.POST.get("path")
    fileOperator = Utils.fileOperator()
    fileOperator.mkdir(path)
    response = {
        "ok": True,
    }
    return HttpResponse(json.dumps(response), content_type="application/json")


@needUserCookies
def uploadFiles(req):
    response = {
        "ok": True,
    }
    try:
        files = req.FILES
        path = req.META.get("HTTP_PATH").encode('utf-8').decode("unicode_escape")
        if os.path.isfile(path) or (not os.path.exists(path)):
            path = os.path.dirname(path)

        for f in files:
            file = files[f]
            destination = open(path + "/" + file.name, 'wb+')
            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()
    except Exception:
        response = {
            "ok": "上传失败",
        }

    return HttpResponse(json.dumps(response), content_type="application/json")


@needUserCookies
def previewFiles(req):
    path = req.POST.get("path", None)
    ext = os.path.splitext(path)[1][1:].lower()
    imgExtList = ["jpg", "png", "bmp"]
    textExtList = ["txt", "ini", "inf", "py", "c", "cpp", "java", "conf"]
    if ext in imgExtList:
        with open(path, 'rb') as f:
            image_data = f.read()
        base64_data = base64.b64encode(image_data)
        s = base64_data.decode()
        imgBase64 = 'data:image/jpeg;base64,' + s
        response = {
            "file": imgBase64,
            "type": 'img'
        }
        return HttpResponse(json.dumps(response), content_type="application/json")

    if ext in textExtList:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception:
            try:
                with open(path, 'r', encoding='gb2312') as f:
                    text = f.read()
            except Exception:
                with open(path, 'r', encoding='ansi') as f:
                    text = f.read()
        response = {
            "file": text,
            "type": 'text'
        }
        return HttpResponse(json.dumps(response), content_type="application/json")
    response = {
        "file": "Unsupport file \n 不支持的文件类型",
        "type": 'error'
    }
    return HttpResponse(json.dumps(response), content_type="application/json")
