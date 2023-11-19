#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Author  : Linzjian666
# @Time    : 2023/11/11 11:45
# @Function: Generate argumentative article(Bullshit in fact)

import os, re
import random
import requests, json

def 读JSON文件(fileName=""):
    import json
    if fileName!='':
        strList = fileName.split(".")
        if strList[len(strList)-1].lower() == "json":
            with open(fileName,mode='r',encoding="utf-8") as file:
                return json.loads(file.read())

data = 读JSON文件("data.json")
名人名言 = data["famous"]
前面垫话 = data["before"]
后面垫话 = data['after']
废话 = data['bosh']

重复度 = 2

def 洗牌遍历(列表):
    global 重复度
    池 = list(列表) * 重复度
    while True:
        random.shuffle(池)
        for 元素 in 池:
            yield 元素

下一句废话 = 洗牌遍历(废话)
下一句名人名言 = 洗牌遍历(名人名言)

def 来点名人名言():
    global 下一句名人名言
    xx = next(下一句名人名言)
    xx = xx.replace(  "a",random.choice(前面垫话) )
    xx = xx.replace(  "b",random.choice(后面垫话) )
    return xx

def 另起一段():
    xx = " "
    xx += "\r\n\r\n"
    return xx

def 狗屁不通生成器(theme):
    tmp = str()
    tmp += "《x》\r\n\r\n"
    while ( len(tmp) < 1500 ) :
        分支 = random.randint(0,100)
        if 分支 < 5:
            tmp += 另起一段()
        elif 分支 < 20 :
            tmp += 来点名人名言()
        else:
            tmp += next(下一句废话)
    tmp = tmp.replace("x",theme)
    return tmp

def 狗屁稍通生成器(theme):
    api_key = 'CHATNIO-API-KEY'
    prompt = [
        {"role": "user", "content": f"请以“{theme}”为主题题写一篇议论性文章，1200字左右，可以举一些名人名言和名人事迹进行论证，题目可自拟，请在认真思考后输出，只输出文章标题和文章内容而不输出其他内容，输出标题格式：《文章标题》"}
    ]
    data = {
        "model": "gpt-3.5-turbo-16k",
        "messages": prompt
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.post("https://api.chatnio.net/v1/chat/completions", data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        tmp = response_data['choices'][0]['message']['content']
    else:
        tmp = f"Error: {response.status_code} {response.text}"
    return tmp


if __name__ == "__main__":
    print("欢迎使用议论性文章生成器!!\r\n工作模式:\r\n1.狗屁不通生成器\r\n2.狗屁稍通生成器(实验性,由AI驱动)")
    mode = input("请选择(1/2):")
    while mode not in ['1', '2']:
        print("无效的输入，请重新选择1或2")
        mode = input("请选择(1/2):")
    theme = input("请输入文章主题:")
    tmp = str()
    if mode == '1':
        tmp += 狗屁不通生成器(theme)
    elif mode == '2':
        print("AI玩命生成文章ing，请稍等...")
        tmp += 狗屁稍通生成器(theme)
    os.system("cls")
    print("生成内容如下:\r\n\r\n"+tmp+"\r\n\r\n")
    with open('output.txt', 'w', encoding='utf-8') as f:
            f.write(tmp)
    input("已写入文件output.txt,请按任意键退出...")
