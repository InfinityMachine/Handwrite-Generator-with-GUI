#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os, re
import random
from BullshitGenerator import readJSON

data = readJSON.read_json_file("BullshitGenerator/data.json")
famousQuotes = data["famous"]  # a 代表前面垫话，b代表后面垫话
preQuotePadding = data["before"]  # 在名人名言前面弄点废话
afterQuoteText = data["after"]  # 在名人名言后面弄点废话
fillerText = data["bosh"]  # 代表文章主要废话来源

repetitionFactor = 2  # 重复因子


def shuffle_iterator(input_list):  # 随机获取指定的废话
    global repetitionFactor
    shuffled_pool = list(input_list) * repetitionFactor  # 随机打乱 [废话池 * 重复因子]
    while True:
        random.shuffle(shuffled_pool)
        for element in shuffled_pool:
            yield element  # 逐次返回废话


nextFillerSentence = shuffle_iterator(fillerText)  # 随机获取废话
nextFamousQuote = shuffle_iterator(famousQuotes)  # 随机获取名人名言


def getFamousQuote():  # 获取名人名言，替换其中的 a 和 b
    global nextFamousQuote
    quote = next(nextFamousQuote)
    quote = quote.replace("a", random.choice(preQuotePadding))
    quote = quote.replace("b", random.choice(afterQuoteText))
    return quote


def create_new_paragraph():  # 创建新段落
    newParagraph = "\r\n"
    newParagraph += "    "
    return newParagraph


def BullshitGenerator(theme, length):
    temp = "    "
    while len(temp) < length:
        branchProbability = random.randint(0, 100)  # 段落控制
        if branchProbability < 20:
            if (
                temp[-1] == "。"
                or temp[-1] == "！"
                or temp[-1] == "？"
                or temp[-1] == "”"
                or temp[-1] == "…"
            ):
                temp += create_new_paragraph()  # 20% 的概率插入新段落
        elif branchProbability < 40:
            temp += getFamousQuote()  # 40% 的概率插入名人名言
        else:
            temp += next(nextFillerSentence)  # 60% 的概率插入废话
    temp = temp.replace("x", theme)  # 替换主题
    # 删除末尾的字符，直到遇到句号
    while (
        temp != ""
        and temp[-1] != "。"
        and temp[-1] != "！"
        and temp[-1] != "？"
        and temp[-1] != "”"
        and temp[-1] != "…"
    ):
        temp = temp[:-1]
    if temp == "":
        temp = "    " + theme + "是一种怎样的存在？"
    return temp
