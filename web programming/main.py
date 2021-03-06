#-*- coding: utf-8 -*-
from time import localtime,strftime
import bs4
from selenium import webdriver
import pymysql

week = ['월', '화', '수', '목', '금', '토']


def parser(url, class_name):
    driver = webdriver.Chrome('C:\\driver\\chromedriver')
    driver.get(url)
    source = driver.page_source
    bs = bs4.BeautifulSoup(source, 'lxml')
    entire = bs.find('table', class_=class_name)
    driver.close()
    return entire


def login(url):
    driver = webdriver.Chrome('C:\\driver\\chromedriver')
    driver.implicitly_wait(3)
    driver.get(url)
    driver.find_element_by_name('username').send_keys('')
    driver.find_element_by_name('password').send_keys('')
    driver.find_element_by_xpath('//*[@id="region-main"]/div/div/div[1]/div[2]/div[1]/form/div[3]/button').click()
    source = driver.page_source
    bs = bs4.BeautifulSoup(source, 'lxml')
    timeline = bs.find('div', class_='block block-upcomming block-coursemos ')
    title1 = timeline.find_all('h5')
    time1 = timeline.find_all('p')

    Title1 = []
    for list in title1:
        Title1.append(list.text.encode('utf-8'))
    Time1 = []
    for list in time1:
        Time1.append(list.text.encode('utf-8'))
    for list in Title1:
        print(list)
    for list in Time1:
        print(list)
    todo = bs.find('div', class_='block block-notification block-coursemos ')
    title2 = todo.find_all('h5')
    time2 = todo.find_all('p')

    Title2 = []
    for list in title2:
        Title2.append(list.text.encode('utf-8'))
    Time2 = []
    for list in time2:
        Time2.append(list.text.encode('utf-8'))
    for list in Title2:
        print(list)
    for list in Time2:
        print(list)
    driver.close()


def lib():
    # 도서관
    library = parser("http://dlibadm.gachon.ac.kr/GACHON_CENTRAL_BOOKING/"
                     "webbooking/statusList.jsp;jsessionid=551C36DA908D0B356F7793D0A73660F6", "tbl_type")
    Ltdlist = library.find_all('td')
    # 도서관 좌석현황 확인
    temp = []
    for list in Ltdlist:
        temp.append(list.text)
    temp.pop(0)
    temp.pop(0)
    temp.pop(4)
    Ltd = []
    for list in range(0, 5):
        arr = []
        arr.append(list+1)
        arr.append('중앙도서관')
        if (list == 0):
            arr.append(1)
        else:
            arr.append(2)
        arr.append(temp[list * 4 + 0])
        arr.append(temp[list * 4 + 1])
        arr.append(temp[list * 4 + 2])
        arr.append(temp[list * 4 + 3])
        arr.append(strftime("%y-%m-%d %H:%M:%S", localtime()))
        Ltd.append(arr)
    for i in range(0, 5):
        for j in range(0, 8):
            print Ltd[i][j]
        print ''
    return Ltd


def cre():
    # 창조관
    create = parser("http://www.gachon.ac.kr/etc/food.jsp?gubun=A", "data")
    tdlist = create.find_all('td')
    # 창조관
    td = []
    for list in tdlist:
        td.append(list.text)

    td.pop(19)
    td.pop(15)
    td.pop(11)
    td.pop(7)
    td.pop(3)

    arr = []
    for i in range(0, 6):
        temp = []
        temp.append(i+1)
        for j in range(0, 3):
            temp.append(td[i * 3 + j])
        temp.append(strftime("%y-%m-%d %H:%M:%S", localtime()))
        temp.append(week[i])
        arr.append(temp)

    for i in range(0, 6):
        for j in range(0, 6):
            print arr[i][j]
        print ''
    return arr


def bea():
    # 아름관
    beauty = parser("http://www.gachon.ac.kr/etc/food.jsp?gubun=B", "data")
    tdlist = beauty.find_all('td')
    # 아름관
    td = []
    for list in tdlist:
        td.append(list.text)

    td.pop(19)
    td.pop(15)
    td.pop(11)
    td.pop(7)
    td.pop(3)

    arr = []
    for i in range(0, 6):
        temp = []
        temp.append(i + 1)
        for j in range(0, 3):
            temp.append(td[i * 3 + j])
        temp.append(strftime("%y-%m-%d %H:%M:%S", localtime()))
        temp.append(week[i])
        arr.append(temp)

    for i in range(0, 6):
        for j in range(0, 6):
            print arr[i][j]
        print ''
    return arr


def vis():
    # 비전타워
    vision = parser("http://www.gachon.ac.kr/etc/food.jsp?gubun=C", "data")
    tdlist = vision.find_all('td')
    # 비전타워
    td = []
    for list in tdlist:
        td.append(list.text)

    td.pop(18)
    td.pop(14)
    td.pop(10)
    td.pop(6)
    # td.pop(3)

    arr = []

    for i in range(0, 6):
        temp = []
        temp.append(i + 1)
        for j in range(0, 3):
            temp.append(td[i * 3 + j])
        temp.append(strftime("%y-%m-%d %H:%M:%S", localtime()))
        temp.append(week[i])
        arr.append(temp)

    for i in range(0, 6):
        for j in range(0, 6):
            print arr[i][j]
        print ''
    return arr


login("https://cyber.gachon.ac.kr/login.php")


conn = pymysql.connect(
    host='localhost', user='root', password='12345', charset='utf8', db='web')
try:

    Library = lib()
    for i in range(0, 5):
        with conn.cursor() as cursor:
            sql = 'update sovigation_lib set whole= %s,used=%s,rest=%s,updated_at=%s where id=%s'
            cursor.execute(sql, (Library[i][4], Library[i][5], Library[i][6], Library[i][7], Library[i][0]))
        conn.commit()

    Create = cre()
    for i in range(0, 6):
        with conn.cursor() as cursor:
            sql = 'update sovigation_foodc set prof= %s,first=%s,special=%s,updated_at=%s,week=%s where id=%s'
            cursor.execute(sql, (Create[i][1], Create[i][2], Create[i][3], Create[i][4], Create[i][5], Create[i][0]))
        conn.commit()

    Beauty = bea()
    for i in range(0, 6):
        with conn.cursor() as cursor:
            sql = 'update sovigation_foodc set prof= %s,first=%s,special=%s,updated_at=%s,week=%s where id=%s'
            cursor.execute(sql, (Beauty[i][1], Beauty[i][2], Beauty[i][3], Beauty[i][4], Beauty[i][5], Beauty[i][0]))
        conn.commit()

    Vision = vis()
    for i in range(0, 6):
        with conn.cursor() as cursor:
            sql = 'update sovigation_foodc set prof= %s,first=%s,special=%s,updated_at=%s,week=%s where id=%s'
            cursor.execute(sql, (Vision[i][1], Vision[i][2], Vision[i][3], Vision[i][4], Vision[i][5], Vision[i][0]))
        conn.commit()
finally:
    conn.close()
