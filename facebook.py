# -*- coding: utf-8 -*-
import os
from time import time
from threading import Thread
from pathlib import Path
from queue import Queue
import urllib.request
from urllib.parse import urlencode
from urllib.error import URLError
import json
import socket
import re

def main():
    uid = "1388945647849340";
    url = "https://www.facebook.com/" + uid + "/about";
    headers = {
        "Cookie": "datr=27n1WMx3roL2jXpBruEKcoPf; dats=1; locale=zh_CN; sb=Lbr1WA7sdvQ4aA28nm2e-HKb; pl=n; lu=gAOQBBz51gYwiEcboCg3Zgqg; c_user=100016496230996; xs=2%3AOHVroqGu2x5MAQ%3A2%3A1492498990%3A-1; fr=0jcWxjJ6Mq2KVqbiL.AWVlNpeWYp9cMpzJBI09sCZ0Cpg.BY3FSf.s-.AAA.0.0.BY9rEn.AWUaVpaJ; presence=EDvF3EtimeF1492562202EuserFA21B16496230996A2EstateFDutF1492562202568CEchFDp_5f1B16496230996F2CC; act=1492562210873%2F3; wd=1920x973"}
    req = urllib.request.Request(url, headers=headers, method="GET")
    companylist = ""
    phone = ""
    web = ""
    name = ""
    email = ""
    people = ""
    companyinfo = ""
    category = ""
    address = ""
    j = {}
    about = urllib.request.urlopen(req, timeout=10).read().decode("utf-8");

    obj = re.search(r"_xdl\">(?P<h1user>.+?)</div>", about)
    if (obj):
        obj = re.search(r"URL=/(?P<h1user>.+?)/", about)
        if (obj):
            name = obj.group("h1user");
        j["name"] = name
        obj = re.search(r"呼叫 +(?P<h1user>.+?)</div>", about)
        if (obj):
            phone = obj.group("h1user");
        obj = re.search(r"this, &quot;http:\\\\/\\\\/(?P<h1user>.+?)\\\\", about)
        if (obj):
            web = obj.group("h1user")
        obj = re.search(r"\"mailto:(?P<h1user>.+?)\"", about)
        if (obj):
            email = obj.group("h1user")
        obj = re.search(r"<div class=\"_3-8w\">(?P<h1user>.+?)</div", about)
        if (obj):
            des = obj.group("h1user")
        obj = re.search(r"简介</div><div class=\"_3-8w\">(?P<h1user>.+?)</div", about)
        if (obj):
            companyinfo = obj.group("h1user")
        obj = re.search(r"about_category\">(?P<h1user>.+?)</a", about)
        if (obj):
            category = obj.group("h1user")
        email = email.replace("&#064;", "@")
        j["phone"] = phone
        j["email"] = email
        j["web"] = web
        j["companyinfo"] = companyinfo
        j["category"] = category
        j["address"] = address
    else:
        req = urllib.request.Request("https://www.facebook.com/" + uid, headers=headers, method="GET")
        content = urllib.request.urlopen(req, timeout=10).read().decode("utf-8");
        obj = re.findall(r"/pages/(?P<h1user>.+?)/", content)
        if (obj):
            address = urllib.request.unquote(obj[-2])
        print(address)
        obj = re.search(r"URL=/(?P<h1user>.+?)\?", content)

        if (obj):
            name = obj.group("h1user");
        obj = re.search(r"&lst=(?P<h1user>.+?)\",", content)
        if (obj):
            url1 = "https://www.facebook.com/" + name + "/about?section=contact-info&lst=" + obj.group("h1user")
            print(url1)
            req = urllib.request.Request(url1, headers=headers, method="GET")
            contact = urllib.request.urlopen(req, timeout=10).read().decode("utf-8");

            obj = re.search(r"联系方式</span></div>(?P<h1user>.+?)</ul", contact)
            if (obj):
                people = obj.group("h1user")
                # if people.count("无联系信息可显示")==1:
                #    people=""
                repeople = ""
                repeople = re.search(r"^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$", people)
                if (repeople):
                    email = repeople.group(0)
                repeople = re.search(r"^1(3|4|5|7|8)\d{9}$", people)
                if (repeople):
                    phone = repeople.group(0)
            j["web"] = web
            j["companyinfo"] = companyinfo
            j["category"] = category
            j["phone"] = phone
            j["email"] = email
            j["name"] = name
            j["address"] = address
    print(json.dumps(j))


if __name__ == "__main__":
    main()
