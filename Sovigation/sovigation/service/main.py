# -*- coding: utf-8 -*-
from time import localtime, strftime
import time
import bs4
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
import pymysql
import threading

week = ['월', '화', '수', '목', '금', '토']


def parser(url, class_name):
    driver = webdriver.Chrome('C:\\Users\GENIE\PycharmProjects\Sovigation\driver\chromedriver')
    driver.get(url)
    source = driver.page_source
    bs = bs4.BeautifulSoup(source, 'lxml')
    entire = bs.find('table', class_=class_name)
    driver.close()
    return entire


def login(ID, password):
    driver = webdriver.Chrome('C:\\Users\GENIE\PycharmProjects\Sovigation\driver\chromedriver')
    # driver.implicitly_wait(3)
    driver.get("https://cyber.gachon.ac.kr/login.php")
    try:
        driver.find_element_by_name('username').send_keys(ID)
        driver.find_element_by_name('password').send_keys(password)
        driver.find_element_by_xpath('//*[@id="region-main"]/div/div/div[1]/div[2]/div[1]/form/div[3]/button').click()
        source = driver.page_source

        bs = bs4.BeautifulSoup(source, 'lxml')
        name = bs.find('li', class_='user_department hidden-xs')
        print(name)
        timeline = bs.find('div', class_='block block-upcomming block-coursemos ')
        title1 = timeline.find_all('h5')
        time1 = timeline.find_all('p')
        todo = bs.find('div', class_='block block-notification block-coursemos ')
        title2 = todo.find_all('h5')
        time2 = todo.find_all('p')
        conn = pymysql.connect(
            host='localhost', user='root', password='12345', charset='utf8', db='web')
        try:
            with conn.cursor() as cursor:
                sql = 'delete from service_LoginUser where userid=%s'
                cursor.execute(sql, ID)
                sql = 'delete from service_UserTodo where name=%s'
                cursor.execute(sql, ID)
                sql = 'delete from service_User_Info where name=%s'
                cursor.execute(sql, ID)
                sql = 'insert into service_LoginUser (userid, name) values(%s, %s)'
                cursor.execute(sql, (ID, name.text.encode('utf-8')))
            conn.commit()

            with conn.cursor() as cursor:
                for i in range(0, len(title1)):
                    sql = 'insert into service_UserTodo (name, todo, deadline) values(%s, %s, %s)'
                    cursor.execute(sql, (ID, title1[i].text.encode('utf-8'), time1[i].text.encode('utf-8')))
                    print(title1[i].text.encode('utf-8'))
                    print(time1[i].text.encode('utf-8'))
                for i in range(0, len(title2)):
                    sql = 'insert into service_User_Info (name, classes, todo) values(%s, %s, %s)'
                    cursor.execute(sql, (ID, title2[i].text.encode('utf-8'), time2[i].text.encode('utf-8')))
                    print(title2[i].text.encode('utf-8'))
                    print(time2[i].text.encode('utf-8'))
            conn.commit()
        finally:
            conn.close()

        driver.close()
    except UnexpectedAlertPresentException:
        # login failure
        print("login failure")
        driver.close()
        return False
    except AttributeError:
        # login failure
        print("login failure")
        driver.close()
        return False
    return True

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
        arr.append(list + 1)
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
            print(Ltd[i][j])
        print
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
        temp.append(i + 1)
        for j in range(0, 3):
            temp.append(td[i * 3 + j])
        temp.append(strftime("%y-%m-%d %H:%M:%S", localtime()))
        temp.append(week[i])
        arr.append(temp)

    for i in range(0, 6):
        for j in range(0, 6):
            print(arr[i][j])
        print
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
            print(arr[i][j])
        print
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
            print(arr[i][j])
        print
    return arr


def sqlsave():
    conn = pymysql.connect(host='localhost', user='root', password='12345', charset='utf8', db='web')
    try:

        Library = lib()
        for i in range(0, 5):
            with conn:
                cursor = conn.cursor()
                sql = 'update service_lib set whole= %s,used=%s,rest=%s,updated_at=%s where id=%s'
                cursor.execute(sql, (Library[i][4], Library[i][5], Library[i][6], Library[i][7], Library[i][0]))
            conn.commit()

        Create = cre()
        for i in range(0, 6):
            with conn:
                cursor = conn.cursor()
                sql = 'update service_fooda set prof= %s,first=%s,special=%s,updated_at=%s,week=%s where id=%s'
                cursor.execute(sql,
                               (Create[i][1], Create[i][2], Create[i][3], Create[i][4], Create[i][5], Create[i][0]))
            conn.commit()

        Beauty = bea()
        for i in range(0, 6):
            with conn:
                cursor = conn.cursor()
                sql = 'update service_foodb set prof= %s,first=%s,special=%s,updated_at=%s,week=%s where id=%s'
                cursor.execute(sql,
                               (Beauty[i][1], Beauty[i][2], Beauty[i][3], Beauty[i][4], Beauty[i][5], Beauty[i][0]))
            conn.commit()

        Vision = vis()
        for i in range(0, 6):
            cursor = conn.cursor()
            sql = 'update service_foodc set prof= %s,first=%s,special=%s,updated_at=%s,week=%s where id=%s'
            cursor.execute(sql,
                           (Vision[i][1], Vision[i][2], Vision[i][3], Vision[i][4], Vision[i][5], Vision[i][0]))
        conn.commit()
    finally:
        conn.close()


class crwaling(threading.Thread):
    def run(self):
        conn = pymysql.connect(
            host='localhost', user='root', password='12345', charset='utf8', db='web')
        try:
            with conn.cursor() as cursor:
                sql = 'TRUNCATE TABLE service_loginrequest'
                cursor.execute(sql, ())
                sql = 'TRUNCATE TABLE service_loginresult'
                cursor.execute(sql, ())
            conn.commit()
        finally:
            conn.close()
        while True:
            conn = pymysql.connect(host='localhost', user='root', password='12345', charset='utf8', db='web')
            try:
                with conn:
                    cursor = conn.cursor()
                    sql = 'select * from service_loginrequest'
                    cursor.execute(sql, ())
                rows = cursor.fetchall()
                if len(rows) == 0:
                    print
                    'sleep'
                    time.sleep(1)
                else:
                    for row in rows:
                        with conn:
                            cursor = conn.cursor()
                            if login(row[1], row[2]):
                                sql = 'insert into service_loginresult (name, result) values(%s, TRUE)'
                                print
                                'true'
                            else:
                                sql = 'insert into service_loginresult (name, result) values(%s, FALSE)'
                                print
                                'false'
                            cursor.execute(sql, (row[1]))
                    with conn:
                        cursor = conn.cursor()
                        sql = 'delete from service_loginrequest where name=%s'
                        cursor.execute(sql, (row[1]))
                conn.commit()
            finally:
                conn.close()


pr1 = crwaling()
#sqlsave()
pr1.start()