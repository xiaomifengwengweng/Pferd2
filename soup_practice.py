import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
def get_page_content(request_url):
    # 得到页面的内容
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html=requests.get(request_url,headers=headers,timeout=10)
    content = html.text
    #print(content)
    # 通过content创建BeautifulSoup对象
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
    return soup

#分析页面信息
def analysis(soup):
    df = pd.DataFrame(columns=['投诉编号', '投诉品牌', '投诉车系', '投诉车型', '问题简述', '典型问题', '投诉时间', '投诉状态'])
    temp = soup.find('div', class_ = 'tslb_b')
    tr_list = temp.find_all('tr')
    for tr in tr_list:
        td_list = tr.find_all('td')
        #投诉编号	投诉品牌	投诉车系	投诉车型	问题简述	典型问题	投诉时间	投诉状态
        if len(td_list) > 0:
            投诉编号, 投诉品牌, 投诉车系, 投诉车型, 问题简述, 典型问题, 投诉时间, 投诉状态 = \
            td_list[0].text, td_list[1].text, td_list[2].text, td_list[3].text, td_list[4].text, td_list[5].text, td_list[6].text, td_list[7].text
            #print(投诉编号, 投诉品牌, 投诉车系, 投诉车型, 问题简述, 典型问题, 投诉时间, 投诉状态)
            temp_dict = {}
            temp_dict['投诉编号'] = 投诉编号
            temp_dict['投诉品牌'] = 投诉品牌
            temp_dict['投诉车系'] = 投诉车系
            temp_dict['投诉车型'] = 投诉车型
            temp_dict['问题简述'] = 问题简述
            temp_dict['典型问题'] = 典型问题
            temp_dict['投诉时间'] = 投诉时间
            temp_dict['投诉状态'] = 投诉状态
            df = df.append(temp_dict, ignore_index=True)
    return df

# 请求URL
url_base = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-0-0-0-0-0-'
result = pd.DataFrame(columns=['投诉编号', '投诉品牌', '投诉车系', '投诉车型', '问题简述', '典型问题', '投诉时间', '投诉状态'])
for i in range(3):
    url = url_base + str(i+1) +'.shtml'
    soup = get_page_content(url)
    result = result.append(analysis(soup))

time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
filename = 'car_complain' + str(time) +'.xlsx'
result.to_excel(filename, index=False)
