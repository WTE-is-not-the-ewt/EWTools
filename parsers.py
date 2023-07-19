import execjs
from os import environ
from lxml import etree
from urllib.parse import urlparse

scripts = execjs.compile(open('script.js', encoding='utf-8').read()) # 以 node 为环境编译爬虫所需 JavaScript 代码
# 为转换 JavaScript Object 为 dict，需要 JavaScript 环境
environ["EXECJS_RUNTIME"] = "JScript" # JavaScript Object 在 node 环境会报编码错误，转用 Windows 自带 JScript 环境
script_eval = execjs.eval # 转换函数别名
