#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a datafilter module '

__author__ = 'Shea Jin'
import sys
sys.path.append('../')  # 新加入的
from lxml import etree
import re
import time
from Futurism_Craw.config import *

#数据清洗模块
class Data_Filter():

    def __init__(self):
        pass

    def get_futurism_infos(self,json):
        '''
        对接受来的json数据，按照格式生成可插入数据库的list
        :param json:
        :return:
        '''
        if json:
            for page_num in range(PER_PAGE):

                if json[page_num]:
                    item = json[page_num]
                    #文章标题
                    title = item.get('title').get('plain_text')
                    #文章正文
                    content = item.get('content').get('rendered')
                    #文章url
                    article_url = item.get('link')
                    #文章作者
                    author = item.get('author_detailed').get('display_name')
                    #文章发布时间
                    release_time = item.get('modified')
                    release_time = release_time.replace('T',' ')
                    #爬取时间
                    craw_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    #文章来源网站
                    source_sit_url = 'https://futurism.com'

                    img_url = item.get('featured_image').get('url')

                    # print(img_url)
                    content_list = self.content_parse(content)
                    # content_list = self.content_parse_only_text(content)

                    pure_text = self.pure_text_resolve(content_list)
                    print(pure_text)
                    #对content_list进行处理，得到纯文本

                    article_text = [
                        {
                            'type': LINK,
                            'text': source_sit_url
                        },
                        {
                            'type': LINK,
                            'text': article_url
                        },
                        {
                            'type': IMAGE,
                            'imageUrl': img_url
                        },
                        {
                            'type': TITLE,
                            'text': title
                        },
                        {
                            'type': TEXT,
                            'text': author
                        }]

                    article_text = article_text + content_list

                    article_text.append({
                        'type': TEXT,
                        'text': release_time
                    })
                    article_text.append({
                        'type': TEXT,
                        'text': craw_time
                    })

                    article_text.append({
                        'type': TEXT,
                        'text': pure_text
                    })
                    # print(article_text)
                    print(page_num)
                    yield article_text


    def pure_text_resolve(self,content_list):
        temp = ''
        for content in content_list:
            if content['type'] == TEXT:
                temp = temp + content['text']

        return temp


    def content_parse(self, content):
        '''
        对正文进行解析，最后返回正文解析的数组字典
        :param content: 正文
        :return:
        '''
        print('正文解析content_parse')
        # 去除里面的a标签和span标签和em标签
        content = re.sub(r'(<\/?a.*?>)|(<\/?span.*?>)|(<\/?em.*?>)', '', content)

        content_html = etree.HTML(content)
        youtubu = content_html.xpath('//iframe/@src')
        #临时字符串temp
        temp = ''
        text_list = []
        # 如果里面没有youtub 的视频
        if len(youtubu) == 0:
            str_text = content_html.xpath('//body//text()')
            print('无YouTube视频，//body//text()方法：%s' % str_text)
            for str in str_text:
                if str.startswith('https://') or str.startswith('http://'):
                    text_list.append(temp)
                    text_list.append(str)
                    temp = ''
                elif str.startswith('READ MORE') or str.startswith('Futurism fans') or str.startswith('More on'):
                    break
                else:
                    temp = temp + str
        else:
            #去除iframe标签，并添加标记token_vedio_http
            content_iframe = re.sub(r'(<\/?iframe.*?>)', 'token_vedio_http', content)

            content_html = etree.HTML(content_iframe)

            iframe_xpath = content_html.xpath('//body//text()')
            i = 0
            for str in iframe_xpath:
                if 'token_vedio_http' in str:
                    text_list.append(temp)
                    text_list.append(youtubu[i])
                    temp = ''
                    i = i + 1
                elif str.startswith('READ MORE') or str.startswith('Futurism fans') or str.startswith('More on'):
                    break
                else:
                    temp = temp + str

        text_list.append(temp)
        print('正文解析list为:%s' % text_list)

        return self.build_content(text_list)


    def build_content(self,text_list):
        '''
        构造结构数据
        :param text_list:
        :return:
        '''
        content_list = []
        content_dic = {}
        for build in text_list:
            if build.startswith('http'):
                content_dic['type'] = VEDIO
                content_dic['resUrl'] = build
            else:
                content_dic['type'] = TEXT
                content_dic['text'] = build

            # print(content_dic)
            content_list.append(content_dic)
            content_dic = {}
        print('正文解析组合后[dic]为:%s' % content_list)

        return content_list