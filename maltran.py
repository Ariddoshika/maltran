#!/usr/bin/python3
#-*- coding:UTF-8 -*-

from __future__ import print_function
from platform import python_version
import sys

#check a version and quit if the version is less than 3
if python_version().startswith('2', 0, len(python_version())):
    print('Are you using python version {}\nPlease, use version 3.X of python'.format(python_version()))
    sys.exit()

import requests
import re
import time
import urlGET
import os
import shutil
from bs4 import BeautifulSoup as bs
from datetime import date, datetime
import urllib.request

WHITE, RED, YELLOW, GREEN, END = '\33[1;97m','\33[1;91m', '\33[1;93m', '\33[1;32m', '\33[0m'

if len(sys.argv) > 1:
    use = '''
{0}maltran v2.0{1}

github.com/MalwareReverseBrasil/maltran.git
Telegram: https://t.me/MalwareReverseBR
       
Usage: 
      python{2}3{1} maltran.py
    '''
    print(use.format(GREEN,END,WHITE))
    sys.exit()

banner = ('''
╔╦╗╔═╗╦  ┬ ┬┌─┐┬─┐┌─┐            
║║║╠═╣║  │││├─┤├┬┘├┤             
╩ ╩╩ ╩╩═╝└┴┘┴ ┴┴└─└─┘            
      ╔╦╗╦═╗┌─┐┌─┐┌─┐┬┌─┐    \t\t{}maltran.py version 2.0{}    
       ║ ╠╦╝├─┤├┤ ├┤ ││      \t\tTelegram: https://t.me/MalwareReverseBR   
       ╩ ╩╚═┴ ┴└  └  ┴└─┘    \t\thttps://github.com/MalwareReverseBrasil  
           ╔═╗╔╗╔┌─┐┬  ┬┌─┐┬ ┬┌─┐
           ╠═╣║║║├─┤│  │└─┐└┬┘└─┐
           ╩ ╩╝╚╝┴ ┴┴─┘┴└─┘ ┴ └─┘

malware-traffic-analysis.net
eNJoY ;)''')

site = 'http://malware-traffic-analysis.net/'
prefix = 'training-exercises.html'
target = site + prefix

url = urlGET.url_get(target)[0]
url2 = urlGET.url_get(site)[0]

def titles():

    '''
    get titles of menus
    :return: titles and number total of titles
    '''

    topic,msg = '', ''
    for numb, topics in enumerate(url2.findAll('h2')):
        if numb > 2: break
        topic += '\n' + topics.text

    topic = topic.split('\n')

    for i in topic: #remove item empty
        if i == '': topic.remove(i)

    j = 0
    for j, title_ in enumerate(topic[1::]):
        msg += '\n[{0}{1:02}{2}] --> {4}{3}{2}'.format(RED, j + 1,END,title_,WHITE)

    exit_option = ('\n[{0}{1:02}{2}] {0}Exit{2}'.format(RED, j + 2, END))
    msg += exit_option

    return topic[0], msg, j + 2, topic[1], topic[2]

def list_exercises():

    '''
    execute web scrapping to get list of exercises in target
    :return: list of exercises to choose 
    '''

    msg = ''
    i = 0
    for i,data in enumerate(url.findAll('li')):
        try:
            date = data.find('a',attrs={'class':'list_header'}).text
            exercise = data.find('a',attrs={'class':'main_menu'}).text[28::]
            msg += ('\n[{0}{1:02}{2}] {3} <--> {4}'.format(RED,i + 1,END,date,exercise))
        except AttributeError:
            break

    exit_option = ('\n[{0}{1:02}{2}] --> {0}Return Menu{2} or {0}Ctrl+C to Exit {2}'.format(RED, i + 1,END))
    msg += exit_option
    return i + 1,msg

def blog_posts_years():

    year_index, year_new = '', ''
    for year in url2.findAll('a', attrs={'href': re.compile('^20.*')}): #regex for get year
        year_index += '\n' + ((year.attrs)['href'])  # YYYY/index.html
        year_new += '\n' + ((year.text))  # YYYY

    #years = ['2013/index.html', '2014/index.html', '2015/index.html', '2016/index.html', '2017/index.html'.....]
    years = (year_index.split())

    # year = ['2013', '2014', '2015', '2016', '2017',....]
    year_ = year_new.split()
    year_.append('{}'.format('return'))

    list_year = ''
    for q in range(len(year_)):
        list_year += '[{0}{1}{2}]   '.format(RED,year_[q],END)

    return list_year, year_, years

def blog_posts_months(new_page):

    month_ = ['January', 'February', 'March', 'April',
              'May', 'June', 'July', 'August',
              'September', 'October', 'November', 'December']

    get_months,msg = '',''

    for num, malspam in enumerate(new_page.findAll('li')):
        try:

            topic = malspam.find('a', attrs={'class': 'main_menu',
                                             'href': re.compile(r'.*/\d\d/.*')}).text

            #get malspam date -> YYYY-MM-DD
            date_ = malspam.find('a', attrs={'class': 'list_header',
                                             'href': re.compile(r'.*/\d\d/.*')}).text

            msg += ('\n[{0}{1:03}{2}] {3} <--> {4}'.format(RED,num + 1,END, date_, topic))

            date_convert = datetime.strptime(date_, '%Y-%m-%d').date()  # convert string to date
            get_months += '\n' + month_[date_convert.month - 1]  # get month (mmmm) in list months

        except AttributeError:
            break

        month_unrepeat = Rrepeat(get_months.split())


        list_month = '{2}[{0}{1:02}{2}] <-->  {4}{3}{2}\n'.format(RED, 0, END, 'Show All',GREEN)

        for numb, k in enumerate(month_unrepeat[::-1]):  # print list of months of the year
            list_month += '[{0}{1:02}{2}] <-->  {3}\n'.format(RED,numb + 1,END, k)

    exit_option = ('\n[{0}{1:03}{2}] --> {0}Return Menu{2} or {0}Ctrl+C to Exit {2}'.format(RED, num + 1, END))
    exit_option2 = ('[{0}{1:02}{2}] <-->  {0}Return Menu{2} or {0}Ctrl+C to Exit {2}\n'.format(RED, numb + 2, END))

    msg += exit_option
    list_month += exit_option2

    return list_month, numb + 1, month_, month_unrepeat[::-1], msg, num + 1

def Rrepeat(list_):
    '''
    remove duplicates months of year
    :param list_: list of months with values duplicate 
    :return: remove duplicates list
    '''

    t = []
    [t.append(item) for item in list_ if not t.count(item)]
    return t


def options_down():

    '''
    show options after choosing exercises
    :return: list of options to download or view files
    '''

    show = '[{}{:02}{}] --> Show associated files'
    down = '[{}{:02}{}] --> Downloads all associated files'
    down_exercise = '[{}{:02}{}] --> Downloads exercises associated files'
    down_answers = '[{}{:02}{}] --> Downloads answers associated files'
    back = '[{}{:02}{}] --> Return the list of exercises'
    back2 = '[{}{:02}{}] --> Return the list of malspam'
    lists = [show, down, down_exercise, down_answers, back]
    lists1 = [show, down,back2]

    list_big, list_small = '', ''


    # for num, list1 in enumerate(lists):
    #     print(list1.format(RED, num + 1, END))
    # print ('')

    for num, list1 in enumerate(lists):
        list_big += '\n' + list1.format(RED,num + 1, END)


    for num2, list2 in enumerate(lists1):
        list_small += '\n' + list2.format(RED,num2 + 1, END)

    return list_big, list_small


def option_1(date_exercise, link_exercise):

    '''
    execute option 1: show associated files
    :param date_exercise: xxxx-xx-xx  
    :param link_exercise: prefix xxxx/xx/xx/index.html 
    :return: show exercises and answers associated
    '''

    #cut link_exercise: xxxx/xx/xx/index.html ->>> xxxx/xx/xx/
    date_exercise_2 = link_exercise[:11]

    target = site + date_exercise_2
    verify_page2 = urlGET.url_get(target + 'page2.html')[1]
    verify_page6 = urlGET.url_get(target + 'page6.html')[1]
    result = ''

    if verify_page2.status_code == 200:
        if verify_page6.status_code == 200: #page6
            page = target + 'page6.html'

            for exercises in urlGET.url_get(page)[0].findAll('li'):
                try:
                    files_all = exercises.find('a', attrs={'class': 'menu_link'})['href']
                    result += '\n' + files_all
                except TypeError:
                    pass

        else: #page2
            page = target + 'page2.html'

            for exercises in urlGET.url_get(page)[0].findAll('li'):
                try:
                    files_all = exercises.find('a', attrs={'class': 'menu_link', 'href': re.compile('^' + date_exercise + '.*')})['href']
                    result += '\n' + files_all
                except TypeError:
                    pass
    else: #index

        page = site + link_exercise

        for exercises in urlGET.url_get(page)[0].findAll('li'):
            try:
                files_all = exercises.find('a', attrs={'class': 'menu_link', 'href': re.compile('^' + date_exercise + '*')})['href']
                result += '\n' + files_all
            except TypeError:
                pass

    return result

def option_2(date_exercise, link_exercise, title_exercise):

    '''
    execute option 2: downloads all assotiated files 
    :param date_exercise: xxxx-xx-xx
    :param link_exercise: prefix xxxx/xx/xx/index.html
    :param title_exercise: title exercise choice
    :return: downloads files and show files
    '''

    date_exercise_2 = link_exercise[:11]
    target = site + date_exercise_2
    verify_page2 = urlGET.url_get(target + 'page2.html')[1]
    verify_page6 = urlGET.url_get(target + 'page6.html')[1]
    result = ''
    folder_name = title_exercise

    if verify_page2.status_code == 200:
        if verify_page6.status_code == 200:  # page6
            print('Download in progress...\nWait...')
            page = target + 'page6.html'

            #added in new version maltran: create folder

            try:
                os.makedirs(folder_name, mode=0o777)
            except FileExistsError as err:
                print(err)
                pass

            for exercises in urlGET.url_get(page)[0].findAll('li'):
                try:
                    files_all = exercises.find('a', attrs={'class': 'menu_link'})['href']
                    result += '\n' + files_all

                    try:

                        f = urllib.request.urlopen(target + files_all)
                        data = f.read()
                        with open(files_all, "wb") as code:
                            code.write(data)

                        #move exercises to folder
                        source = os.getcwd() + '/' + files_all
                        destination = os.getcwd() + '/' + folder_name + '/'
                        try:
                            shutil.move(source, destination)
                        except shutil.Error:
                            print('file already exists')

                    except FileNotFoundError:
                        pass

                except TypeError:
                    pass

        else:  # page2
            print('Download in progress...\nWait...')
            page = target + 'page2.html'

            try:
                os.makedirs(folder_name, mode=0o777)
            except FileExistsError as err:
                print(err)
                pass

            for exercises in urlGET.url_get(page)[0].findAll('li'):
                try:
                    files_all = exercises.find('a', attrs={'class': 'menu_link', 'href': re.compile('^' + date_exercise + '*')})['href']
                    result += '\n' + files_all

                    try:
                        f = urllib.request.urlopen(target + files_all)
                        data = f.read()
                        with open(files_all, "wb") as code:
                            code.write(data)

                        source = os.getcwd() + '/' + files_all
                        destination = os.getcwd() + '/' + folder_name + '/'
                        try:
                            shutil.move(source, destination)
                        except shutil.Error:
                            print('file already exists')

                    except FileNotFoundError:
                        pass

                except TypeError:
                    pass
    else:  # index
        print('Download in progress...\nWait...')
        page = site + link_exercise

        try:
            os.makedirs(folder_name, mode=0o777)
        except FileExistsError as err:
            print(err)
            pass

        for exercises in urlGET.url_get(page)[0].findAll('li'):
            try:
                files_all = exercises.find('a', attrs={'class': 'menu_link', 'href': re.compile('^' + date_exercise + '*')})['href']
                result += '\n' + files_all

                try:
                    f = urllib.request.urlopen(target + files_all)
                    data = f.read()
                    with open(files_all, "wb") as code:
                        code.write(data)

                    source = os.getcwd() + '/' + files_all
                    destination = os.getcwd() + '/' + folder_name + '/'
                    try:
                        shutil.move(source, destination)
                    except shutil.Error:
                        print('file already exists')

                except FileNotFoundError:
                    pass

            except TypeError:
                pass

    result += '\n\n{0}password is: infected{1}\n{2}Downloads Successful{1} \n'.format(RED,END,GREEN)
    return result

def option_3(date_exercise, link_exercise, title_exercise):

    '''
    execute option 3: show associated exercises files and downloads
    :param date_exercise: xxxx-xx-xx  
    :param link_exercise: prefix xxxx/xx/xx/index.html 
    :return: downloads associated exercises files
    '''

    date_exercise_2 = link_exercise[:11]
    target = site + date_exercise_2
    verify_page2 = urlGET.url_get(target + 'page2.html')[1]
    verify_page6 = urlGET.url_get(target + 'page6.html')[1]
    result = ''
    folder_name = title_exercise

    if verify_page2.status_code == 200:
        if verify_page6.status_code == 200:  # page6
            print('Download in progress...\nWait...')
            page = target + 'page6.html'

            try:
                os.makedirs(folder_name, mode=0o777)
            except FileExistsError as err:
                print(err)
                pass

            for exercises in urlGET.url_get(page)[0].findAll('a'):
                if 'href' in exercises.attrs:
                    if not 'answers' in exercises.attrs['href'] and date_exercise in exercises.attrs['href']:

                        files_all = exercises.attrs['href']
                        result += '\n' + files_all

                        try:
                            f = urllib.request.urlopen(target + files_all)
                            data = f.read()
                            with open(files_all, "wb") as code:
                                code.write(data)

                            source = os.getcwd() + '/' + files_all
                            destination = os.getcwd() + '/' + folder_name + '/'
                            try:
                                shutil.move(source, destination)
                            except shutil.Error:
                                print('file already exists')

                        except FileNotFoundError:
                            pass

        else:  # page2
            print('Download in progress...\nWait...')
            page = target + 'page2.html'

            try:
                os.makedirs(folder_name, mode=0o777)
            except FileExistsError as err:
                print(err)
                pass

            for exercises in urlGET.url_get(page)[0].findAll('a'):
                if 'href' in exercises.attrs:
                    if not 'answers' in exercises.attrs['href'] and date_exercise in exercises.attrs['href']:

                        files_all = exercises.attrs['href']
                        result += '\n' + files_all

                        try:
                            f = urllib.request.urlopen(target + files_all)
                            data = f.read()
                            with open(files_all, "wb") as code:
                               code.write(data)

                            source = os.getcwd() + '/' + files_all
                            destination = os.getcwd() + '/' + folder_name + '/'
                            try:
                                shutil.move(source, destination)
                            except shutil.Error:
                                print('file already exists')

                        except FileNotFoundError:
                            pass

    else:  # index
        print('Download in progress...\nWait...')
        page = site + link_exercise
        regular_expression = '^' + date_exercise + '*!answers*'
        print(regular_expression)

        try:
            os.makedirs(folder_name, mode=0o777)
        except FileExistsError as err:
            print(err)
            pass

        for exercises in urlGET.url_get(page)[0].findAll('a'):
            if 'href' in exercises.attrs:
                if not 'answers' in exercises.attrs['href'] and date_exercise in exercises.attrs['href']:

                    files_all = exercises.attrs['href']
                    result += '\n' + files_all

                    try:
                        f = urllib.request.urlopen(target + files_all)
                        data = f.read()
                        with open(files_all, "wb") as code:
                            code.write(data)

                        source = os.getcwd() + '/' + files_all
                        destination = os.getcwd() + '/' + folder_name + '/'
                        try:
                            shutil.move(source, destination)
                        except shutil.Error:
                            print('file already exists')

                    except FileNotFoundError:
                        pass

    result += '\n\n{0}password is: infected{1}\n{2}Downloads Successful{1} \n'.format(RED, END, GREEN)
    return result


def option_4(date_exercise, link_exercise, title_exercise):

    '''
    execute option 3: show associated exercises files and downloads
    :param date_exercise: xxxx-xx-xx  
    :param link_exercise: prefix xxxx/xx/xx/index.html 
    :return: downloads associated exercises files
    '''

    date_exercise_2 = link_exercise[:11]
    target = site + date_exercise_2
    verify_page2 = urlGET.url_get(target + 'page2.html')[1]
    verify_page6 = urlGET.url_get(target + 'page6.html')[1]
    result = ''
    folder_name = title_exercise

    if verify_page2.status_code == 200:
        if verify_page6.status_code == 200:  # page6
            print('Download in progress...\nWait...')
            page = target + 'page6.html'

            try:
                os.makedirs(folder_name, mode=0o777)
            except FileExistsError as err:
                #print(err)
                pass

            for exercises in urlGET.url_get(page)[0].findAll('li'):
                try:
                    files_all = \
                        exercises.find('a', attrs={'class': 'menu_link',
                                                   'href': re.compile('^' + date_exercise + '.*answers.*')})['href']
                    result += '\n' + files_all

                    try:
                        f = urllib.request.urlopen(target + files_all)
                        data = f.read()
                        with open(files_all, "wb") as code:
                            code.write(data)

                        source = os.getcwd() + '/' + files_all
                        destination = os.getcwd() + '/' + folder_name + '/'
                        try:
                            shutil.move(source, destination)
                        except shutil.Error:
                            print('file already exists')

                    except FileNotFoundError:
                        pass

                except TypeError:
                    pass

        else:  # page2
            print('Download in progress...\nWait...')
            page = target + 'page2.html'

            try:
                os.makedirs(folder_name, mode=0o777)
            except FileExistsError as err:
                print(err)
                pass

            for exercises in urlGET.url_get(page)[0].findAll('li'):
                try:
                    files_all = \
                        exercises.find('a', attrs={'class': 'menu_link',
                                                   'href': re.compile('^' + date_exercise + '.*answers.*')})['href']
                    result += '\n' + files_all

                    try:
                        f = urllib.request.urlopen(target + files_all)
                        data = f.read()
                        with open(files_all, "wb") as code:
                            code.write(data)

                        source = os.getcwd() + '/' + files_all
                        destination = os.getcwd() + '/' + folder_name + '/'
                        try:
                            shutil.move(source, destination)
                        except shutil.Error:
                            print('file already exists')

                    except FileNotFoundError:
                        pass

                except TypeError:
                    pass
    else:  # index
        print('Download in progress...\nWait...')
        page = site + link_exercise

        try:
            os.makedirs(folder_name, mode=0o777)
        except FileExistsError as err:
            print(err)
            pass

        for exercises in urlGET.url_get(page)[0].findAll('li'):
            try:
                files_all = \
                    exercises.find('a', attrs={'class': 'menu_link',
                                               'href': re.compile('^' + date_exercise + '.*answers.*')})['href']
                result += '\n' + files_all

                try:
                    f = urllib.request.urlopen(target + files_all)
                    data = f.read()
                    with open(files_all, "wb") as code:
                        code.write(data)

                    source = os.getcwd() + '/' + files_all
                    destination = os.getcwd() + '/' + folder_name + '/'
                    try:
                        shutil.move(source, destination)
                    except shutil.Error:
                        print('file already exists')

                except FileNotFoundError:
                    pass

            except TypeError:
                pass

    if result == '':
        shutil.rmtree(folder_name,ignore_errors=True)
        result = '\n\n{}There is no answer file{}\n'.format(GREEN, END)

    else:
        result += '\n\n{0}password is: infected{1}\n{2}Downloads Successful{1} \n'.format(RED, END, GREEN)
    return result

def main():

    os.system('clear')
    print(banner.format(YELLOW, END))
    try:
        print('{}\t\t\t\t'.format(YELLOW) + titles()[0] + '{}'.format(END))
    except IndexError:
        print('{}This is embarrassing, excuse-me.\nPlease, check your internet connection.{}'.format(RED, END))
        sys.exit()
    print(titles()[1])

    while True:
        try:
            select_menu = int(input('\nChoose what you want to do: '))
            if select_menu not in range(1,titles()[2] + 1):
                print('{0}Select a number between 01 and {1:02}{2}'.format(RED,titles()[2],END))
                pass

            if select_menu == titles()[2]:  # exit environment
                print('\nBye!\n')
                break

            if select_menu == 1:  # choise exercises
                os.system('clear')
                print('{}'.format(GREEN) + titles()[3] + '{}'.format(END))
                time.sleep(1)
                print(list_exercises()[1])

                while True:
                    try:
                        select_exercise = int(input('\nSelect an exercise: '))
                        if select_exercise not in range(1, list_exercises()[0] + 1):
                            print('{0}Select a number between 01 and {1:02}{2}'.format(RED,list_exercises()[0],END))
                            pass

                        if select_exercise == list_exercises()[0]:  # return environment
                            os.system('clear')
                            print(banner.format(YELLOW, END))
                            print('{}\t\t\t\t'.format(YELLOW) + titles()[0] + '{}'.format(END))
                            print(titles()[1])
                            break

                        for num, list1 in enumerate(url.findAll('li')):
                            try:
                                if select_exercise == num + 1:
                                    choice = list1.find('a', attrs={'class': 'main_menu'}).text[
                                             28::]  # title of exercise selected
                                    date = list1.find('a', attrs={'class': 'list_header'}).text  # date xxxx-xx-xx
                                    prefix_choice = list1.find('a', attrs={'class': 'main_menu'})[
                                        'href']  # prefix xxxx/xx/xx/index.html

                                    os.system('clear')
                                    print('\nYou chose the exercise {0}{2}{1}'.format(YELLOW, END, choice))
                                    print(options_down()[0])
                                    print('')

                                    while True:
                                        try:
                                            select_down = int(input('Select an option: '))

                                            if select_down not in range(1, 6):
                                                print('{}Select a number between 01 and 05{}'.format(RED, END))
                                                pass

                                            if select_down == 1:
                                                print(option_1(date, prefix_choice))
                                                print('')

                                            if select_down == 2:
                                                print(option_2(date, prefix_choice, choice))
                                                print('')

                                            if select_down == 3:
                                                print(option_3(date, prefix_choice, choice))
                                                print('')

                                            if select_down == 4:
                                                print(option_4(date, prefix_choice, choice))
                                                print('')

                                            if select_down == 5:
                                                os.system('clear')
                                                print('{}'.format(GREEN) + titles()[3] + '{}'.format(END))
                                                print(list_exercises()[1])
                                                break

                                        except ValueError:
                                            print('{}Enter only with numbers.{}'.format(RED, END))
                                            pass

                            except AttributeError:
                                break

                    except ValueError:
                        print('{}Enter only with numbers.{}'.format(RED, END))
                        pass

            if select_menu == 2:

                os.system('clear')
                print('{}'.format(GREEN) + titles()[4] + '{}\n'.format(END))
                time.sleep(1)
                print(blog_posts_years()[0], end="")

                while True:

                    select_year = input('--> Choose a Year: {}'.format(RED))
                    if select_year not in blog_posts_years()[1]:
                        print('\n{}Please, choose one of the above years!{}'.format(RED,END), end=" ")
                        pass

                    elif select_year.lower() == 'return':
                        os.system('clear')
                        print('{}'.format(END),end='')
                        print(banner.format(YELLOW, END))
                        print('{}\t\t\t\t'.format(YELLOW) + titles()[0] + '{}'.format(END))
                        print(titles()[1])
                        break

                    else:
                        index_year = blog_posts_years()[1].index(select_year)

                        # years[4] = 2017/index.html; number of 0 : len(years)
                        new_page = urlGET.url_get(site + blog_posts_years()[2][index_year])[0]

                        os.system('clear')
                        print('  {0}[{1}  {2}{3}{1}  {0}]{1}\n'.format(RED, END, GREEN, select_year))
                        print(blog_posts_months(new_page)[0])

                        while True:
                            try:
                                select_month_mal = int(input('--> Choose a Month: '))
                                if select_month_mal not in range(0, int(blog_posts_months(new_page)[1]) + 2):
                                    print('Select a number between 00 and {:02}'.format((blog_posts_months(new_page))[1] + 1))
                                    pass

                                elif select_month_mal == 0:
                                    os.system('clear')
                                    print(blog_posts_months(new_page)[4])  #show all files malspam
                                    val_total = blog_posts_months(new_page)[5]

                                    while True:
                                        try:
                                            select_post_all = int(input('\nSelect a post: '))
                                            if select_post_all not in range(1, val_total + 1):
                                                print(
                                                    '{0}Select a number between 01 and {1:02}{2}'.format(RED, val_total,
                                                                                                         END))
                                                pass

                                            if select_post_all == val_total: #return menu
                                                os.system('clear')
                                                print('  {0}[{1}  {2}{3}{1}  {0}]{1}\n'.format(RED, END, GREEN,select_year))
                                                print(blog_posts_months(new_page)[0]) #show months
                                                print('')
                                                break

                                            topic_malspam_all, date_malspam_all = '',''
                                            for num_malspam_all, malspam_all in enumerate(new_page.findAll('li')):
                                                try:
                                                    if select_post_all == num_malspam_all + 1:
                                                        topic_malspam_all = malspam_all.find('a', attrs={'class': 'main_menu',
                                                                                     'href': re.compile(
                                                                                         r'.*/\d\d/.*')}).text

                                                    # get malspam date -> MM/DD/index.html
                                                        date_malspam_all = malspam_all.find('a', attrs={'class': 'list_header',
                                                                                     'href': re.compile(
                                                                                         r'.*/\d\d/.*')})['href']


                                                        print('\nYou chose {0}{2}{1}'.format(YELLOW, END, topic_malspam_all))
                                                        url_malspam_all = site + select_year + '/' + date_malspam_all
                                                        page_malspam_all = urlGET.url_get(url_malspam_all)[0]

                                                        os.system('clear')
                                                        print(options_down()[1])
                                                        print('')

                                                        while True:

                                                            try:
                                                                select_down_malspam_all = int(input('Select an option: '))
                                                                print('')

                                                            except ValueError:
                                                                print('{}Enter only with numbers.{}'.format(RED, END))
                                                                pass

                                                            if select_down_malspam_all not in range(1, 4):
                                                                print('{}Select a number between 01 and 03{}'.format(RED, END))
                                                                pass

                                                            if select_down_malspam_all == 3: #return the list malspam
                                                                os.system('clear')
                                                                print(blog_posts_months(new_page)[4])  # show all files malspam
                                                                break

                                                            if select_down_malspam_all == 1: #show files

                                                                msg_malspam_all, msg_malspam2_all = '', ''
                                                                for child_all in page_malspam_all.select('a[href^="2"]'):
                                                                    msg_malspam_all += '\n' + (child_all['href'])

                                                                msg_malspam2_all = Rrepeat(msg_malspam_all.split())

                                                                for child2_all in msg_malspam2_all:
                                                                    print(child2_all)
                                                                print('')

                                                            if select_down_malspam_all == 2: #download files

                                                                folder_malspam_all = topic_malspam_all

                                                                print('Download in progress...\nWait...')
                                                                try:
                                                                    os.makedirs(folder_malspam_all, mode=0o777)
                                                                except FileExistsError as err:
                                                                    print(err)
                                                                    pass

                                                                msg_all_down, msg_all_down2 = '', ''
                                                                for child_all_down in page_malspam_all.select('a[href^="2"]'):
                                                                    msg_all_down += '\n' + (child_all_down['href'])

                                                                msg_all_down2 = Rrepeat(msg_all_down.split())

                                                                # date_malspam_all original -> YYYY/MM/DD/index.html
                                                                url_all_down = site + select_year + '/' + date_malspam_all[:6]  # date3 -> YYYY/MM/DD/

                                                                result_down_all = ''
                                                                for child_all_down2 in msg_all_down2:

                                                                    try:
                                                                        result_down_all += '\n' + child_all_down2
                                                                        f = urllib.request.urlopen(url_all_down + child_all_down2)
                                                                        data = f.read()
                                                                        with open(child_all_down2, "wb") as code:
                                                                            code.write(data)

                                                                        source = os.getcwd() + '/' + child_all_down2
                                                                        destination = os.getcwd() + '/' + folder_malspam_all + '/'
                                                                        try:
                                                                            shutil.move(source, destination)
                                                                        except shutil.Error:
                                                                            print('file already exists')

                                                                    except FileNotFoundError:
                                                                        pass

                                                                result_down_all += '\n\n{0}password is: infected{1}\n{2}Downloads Successful{1} \n'.format(
                                                                    RED, END, GREEN)
                                                                print(result_down_all)

                                                except AttributeError:
                                                    break

                                        except ValueError:
                                            print('{}Enter only with numbers.{}'.format(RED, END))
                                            pass


                                elif select_month_mal == blog_posts_months(new_page)[1] + 1:
                                    os.system('clear')
                                    #return year menu
                                    print(blog_posts_years()[0], end="")
                                    break

                                else:

                                    month_corresp = blog_posts_months(new_page)[2].index(
                                        blog_posts_months(new_page)[3][(select_month_mal) - 1]) + 1
                                    new_month_corresp = str('{:02}'.format(month_corresp))

                                    msg2, topic2 = '', ''
                                    num2 = 0
                                    for malspam2 in new_page.findAll('li'):
                                        try:
                                            topic2 = malspam2.find('a', attrs={'class': 'main_menu',
                                                                               'href': re.compile(
                                                                                   '^' + new_month_corresp + '/.*')}).text
                                            date2 = malspam2.find('a', attrs={'class': 'list_header',
                                                                              'href': re.compile(
                                                                                  '^' + new_month_corresp + '/.*')}).text
                                            num2 += 1
                                            msg2 += ('\n[{0}{1:02}{2}] {3} <--> {4}'.format(RED,num2,END, date2, topic2))

                                        except AttributeError:
                                            pass

                                    exit_option = ('\n[{0}{1:02}{2}] --> {0}Return Menu{2} or {0}Ctrl+C to Exit {2}\n'.format(RED, num2 + 1,END))
                                    msg2 += exit_option
                                    os.system('clear')
                                    print('{0}[{1}  {2}{3} {4}{1}  {0}]{1}'.format(RED,
                                                                                END,
                                                                                GREEN,
                                                                                blog_posts_months(new_page)[3][(select_month_mal) - 1],
                                                                                select_year))
                                    print(msg2)

                                    while True:
                                        try:
                                            select_post = int(input('\nSelect a post: '))
                                            if select_post not in range(1, num2 + 2):
                                                print('{0}Select a number between 01 and {1:02}{2}'.format(RED, num2 + 1,
                                                                                                           END))
                                                pass

                                        except ValueError:
                                            print('{}Enter only with numbers.{}'.format(RED, END))
                                            pass

                                        if select_post == num2 + 1:
                                            os.system('clear')
                                            print('  {0}[{1}  {2}{3}{1}  {0}]{1}\n'.format(RED,END,GREEN, select_year))
                                            print(blog_posts_months(new_page)[0])
                                            break

                                        num3 = 0
                                        date3,topic3 = '',''

                                        for malspam3 in new_page.findAll('li'):

                                            topic3 = malspam3.find('a', attrs={'class': 'main_menu',
                                                                               'href': re.compile(
                                                                                   '^' + new_month_corresp + '/.*')})
                                            if topic3 != None:
                                                num3 += 1

                                                if select_post == num3:

                                                    topic3 = malspam3.find('a', attrs={'class': 'main_menu',
                                                                                       'href': re.compile(
                                                                                           '^' + new_month_corresp + '/.*')}).text
                                                    date3 = malspam3.find('a', attrs={'class': 'list_header',
                                                                                      'href': re.compile(
                                                                                          '^' + new_month_corresp + '/.*')})['href']
                                                    break

                                        print('\nYou chose {0}{2}{1}'.format(YELLOW, END, topic3))
                                        url_malspam = site + select_year + '/' + date3
                                        page_malspam = urlGET.url_get(url_malspam)[0]

                                        print(options_down()[1])
                                        print('')

                                        while True:

                                            try:
                                                select_down_malspam = int(input('Select an option: '))
                                                print('')

                                                if select_down_malspam not in range(1, 4):
                                                    print('{}Select a number between 01 and 03{}'.format(RED, END))
                                                    pass

                                                if select_down_malspam == 1: #show files of month selected

                                                    msg_malspam, msg_malspam2 = '', ''
                                                    for child in page_malspam.select('a[href^="2"]'):
                                                        msg_malspam += '\n' + (child['href'])

                                                    msg_malspam2 = Rrepeat(msg_malspam.split())

                                                    for child2 in msg_malspam2:
                                                        print(child2)
                                                    print('')

                                                if select_down_malspam == 2: #download_files

                                                    folder_malspam = topic3

                                                    print('Download in progress...\nWait...')
                                                    try:
                                                        os.makedirs(folder_malspam, mode=0o777)
                                                    except FileExistsError as err:
                                                        print(err)
                                                        pass

                                                    msg_malspam_down, msg_malspam2_down = '', ''
                                                    for child_down in page_malspam.select('a[href^="2"]'):
                                                        msg_malspam_down += '\n' + (child_down['href'])

                                                    msg_malspam2_down = Rrepeat(msg_malspam_down.split())

                                                    #date3 original -> YYYY/MM/DD/index.html
                                                    url_malspam_down = site + select_year + '/' + date3[:6] #date3 -> YYYY/MM/DD/

                                                    result_down = ''
                                                    for child2_down in msg_malspam2_down:

                                                        try:
                                                            result_down += '\n' + child2_down
                                                            f = urllib.request.urlopen(url_malspam_down + child2_down)
                                                            data = f.read()
                                                            with open(child2_down, "wb") as code:
                                                                code.write(data)

                                                            source = os.getcwd() + '/' + child2_down
                                                            destination = os.getcwd() + '/' + folder_malspam + '/'
                                                            try:
                                                                shutil.move(source, destination)
                                                            except shutil.Error:
                                                                print('file already exists')

                                                        except FileNotFoundError:
                                                            pass

                                                    result_down += '\n\n{0}password is: infected{1}\n{2}Downloads Successful{1} \n'.format(RED, END, GREEN)
                                                    print(result_down)

                                                if select_down_malspam == 3:
                                                    os.system('clear')
                                                    print('{0}[{1}  {2}{3} {4}{1}  {0}]{1}'.format(RED,
                                                                                               END,
                                                                                               GREEN,
                                                                                               blog_posts_months(new_page)[3][(select_month_mal) - 1],
                                                                                               select_year))
                                                    print(msg2)
                                                    break

                                            except ValueError:
                                                print('{}Enter only with numbers.{}'.format(RED, END))
                                                pass

                            #except for select_month_mal
                            except ValueError:
                                print('{}Enter only with numbers.{}'.format(RED,END))
                                pass

        #except for first try, select_menu
        except ValueError:
             print('{}Enter only with numbers.{}'.format(RED,END))
             pass
    return

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\nBye\n')
        sys.exit()
    except SystemExit:
        pass