
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import csv
import pandas as pd
import MySQLdb
# host='localhost'
# user='root'
# passwd=''
# db='test'
# conn=MySQLdb.connect(host,user,passwd,db,charset='utf8')
# cursor = conn.cursor()
boser=webdriver.Chrome()
boser.maximize_window()
wait=WebDriverWait(boser , 10)
def getlogin():
    boser.get('https://www.tianyancha.com/login')
    user = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#web-content > div > div > div > div.position-rel.container.company_container > div > div.in-block.vertical-top.float-right.right_content.mt50.mr5.mb5 > div.module.module1.module2.loginmodule.collapse.in > div.modulein.modulein1.mobile_box.pl30.pr30.f14.collapse.in > div.pb30.position-rel > input"))
    )
    password=wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#web-content > div > div > div > div.position-rel.container.company_container > div > div.in-block.vertical-top.float-right.right_content.mt50.mr5.mb5 > div.module.module1.module2.loginmodule.collapse.in > div.modulein.modulein1.mobile_box.pl30.pr30.f14.collapse.in > div.pb40.position-rel > input'))
    )
    submit = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR , '#web-content > div > div > div > div.position-rel.container.company_container > div > div.in-block.vertical-top.float-right.right_content.mt50.mr5.mb5 > div.module.module1.module2.loginmodule.collapse.in > div.modulein.modulein1.mobile_box.pl30.pr30.f14.collapse.in > div.c-white.b-c9.pt8.f18.text-center.login_btn'))
    )
    user.send_keys('15109157091')
    password.send_keys('lm1425560783')
    submit.click()
    getSearch()
def getSearch():
    user = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR , "#home-main-search"))
    )
    submit = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR ,
                                    '#web-content > div > div.mainV3_tab1_enter.position-rel > div.mainv2_tab1.position-rel > div > div.main-tab-outer > div:nth-child(2) > div > div:nth-child(1) > div.input-group.inputV2 > div > span'))
    )
    key='佛山市顺德区'
    user.send_keys(key)
    submit.click()
    html=boser.page_source
    geturl(html)
    getUrlNext()
def getUrlNext():
    for i in range(2,5):
        boser.get(r'https://www.tianyancha.com/search/p%s?key=佛山市顺德区'% i)
        html=boser.page_source
        geturl(html)
def geturl(html):
    try:
        reg=r'<a href=".*?" target="_blank" tyc-event-click="" tyc-event-ch="CompanySearch.Company" style="word-break: break-all;font-weight: 600;" class="query_name sv-search-company f18 in-block vertical-middle"><span>(.*?)</span></a>'
        names=re.findall(reg,html,re.S)
        reg=r'<a title=".*?" class="legalPersonName hover_underline" target="_blank" href=".*?">(.*?)</a>'
        daibiao=re.findall(reg,html,re.S)
        reg=r'<div class="title overflow-width" style="border-right: none">.*?<span title=".*?">(.*?)</span></div>'
        days = re.findall(reg,html,re.S)
        reg=r'<span class="sec-c3">联系电话：</span><span class="overflow-width over-hide vertical-bottom in-block" style="max-width:500px;">(.*?)</span>'
        phones = re.findall(reg , html , re.S)
        reg=r'<div class="add"><span class="sec-c3">.*?</span><span>：</span><span class="overflow-width over-hide vertical-bottom in-block" style="max-width:500px;">(.*?)</span>'
        location=re.findall(reg,html,re.S)
        for i in range(20):
            data={
                'name':names[i].replace('<em>','').replace('</em>',''),
                'daibiao':daibiao[i],
                'day':days[i].replace('<em>','').replace('</em>',''),
                'phone':phones[i].replace('<em>','').replace('</em>',''),
                'location': location[i].replace('<em>', '').replace('</em>','')
            }
            print(data)
            # cursor.execute("insert into tianyancha(name,daibiao,day,phone,location) values('{}','{}','{}','{}','{}')".format(data['name'],data['daibiao'],data['day'],data['phone'],data['location']))
            # print(data['daibiao'],'成功存入数据库')
            # conn.commit()

    except:
        return None
def main():
    getlogin()

if __name__ == '__main__':
    main()
