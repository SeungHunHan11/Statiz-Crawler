import os
from bs4 import BeautifulSoup
from html_table_parser import parser_functions

import pandas as pd
import sys
import parser
import requests
import datetime

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
chrome_driver='C:/chromedriver'

from selenium import webdriver
import sys
from pathlib import Path

from getch import pause



prompt_key=0
teamlinkP="http://www.statiz.co.kr/stat.php?mid=stat&re=1&ys=2010&ye=2020&se=0&te=LG&tm=&ty=0&qu=auto&po=0&as=&ae=&hi=&un=&pl=&da=1&o1=WAR&o2=OutCount&de=1&lr=0&tr=&cv=&ml=1&pa=0&si=&cn=&sn=100"
teamlinkB="http://www.statiz.co.kr/stat.php?mid=stat&re=0&ys=2010&ye=2020&se=0&te=LG&tm=&ty=0&qu=auto&po=0&as=&ae=&hi=&un=&pl=&da=1&o1=WAR_ALL_ADJ&o2=TPA&de=1&lr=0&tr=&cv=&ml=1&pa=0&si=&cn=&sn=100"

start_year=0
end_year=0
teamlinkstat=""
teamlist = ["LG", "두산", "삼성", "NC", "키움", "SSG", "한화", "롯데", "KIA", "kt"]
teamcode = """
LG 두산 삼성 NC 키움 SSG 한화 롯데 KIA kt
"""

welcome="""
고려대학교 통계학과 동아리 PAINS

스탯티즈 자료 자동 추출 프로그램 V.2

                     주의사항
        
1. 오류 발생시 V3 등 컴뷰터 백신 프로그램을 일시정지 해보세요
2. 오류 발생시 종료 후 다시 실행 해보세요.

기타 문의 및 건의사항은 

painsports1905@gmail.com
으로 보내주세요!

"""

if __name__ == "__main__":


    print(welcome)

    os.system('pause')

    prompt="""
    
    원하는 기능을 입력해주세요
    
    1. 선수 기록 확인
    2. 팀기록 확인
    3. 종료
    
    숫자를 입력해주세요:
    
    """

    while prompt_key !=3:

        try:
            print(prompt)
            prompt_key = int(input())

            if prompt_key == 1:

                height=input("\n\n선수 이름을 입력하시오 (한글은 스페이스바를 눌러가며 타이핑 해주세요): ")


                url="http://www.statiz.co.kr/player.php?name="+height+"&search="

                request = requests.get(url)

                soup = BeautifulSoup(request.text, "html.parser")

                error=soup.find("div",{"id":"con_expa1"})

                while error != None:

                    height = input("\n존재하지 않는 선수입니다.\n\n 선수 이름을 다시 입력하시오 (한글은 스페이스바를 눌러가며 타이핑 해주세요): ")

                    url = "http://www.statiz.co.kr/player.php?name=" + height + "&search="

                    request = requests.get(url)
                    soup = BeautifulSoup(request.text, "html.parser")
                    error = soup.find("div", {"id": "con_expa1"})

                    if error == None:
                        break

                data = soup.find("table", {"class": "table table-striped"})

                if data != None:

                    table = parser_functions.make2d(data)
                    df = pd.DataFrame(data=table[1:], columns=table[0])
                    print(df)
                    player = input("\n어느 선수를 선택하시겠습니까? (숫자 입력) : \n\n\n\n")

                    linkplayer = linkpars=soup.select('td>a')
                    selectplayer = int(player) - 1

                    url2 = linkplayer[selectplayer]['href']
                    url2="http://www.statiz.co.kr/"+url2
                    url2

                    request2 = requests.get(url2)
                    soup2 = BeautifulSoup(request2.text, "html.parser")
                    data2 = soup2.find("table",{"class": "table table-striped table-responsive table-condensed no-space table-bordered"})
                    table2 = parser_functions.make2d(data2)
                    df2 = pd.DataFrame(data=table2[1:], columns=table2[0])

                    "\n\n"
                    print(df2)

                else:
                    url2 = url

                    url2 = url2[0:35] + "opt=1&" + url2[35:]

                    request2 = requests.get(url2)
                    soup2 = BeautifulSoup(request2.text, "html.parser")
                    data2 = soup2.find("table",{"class": "table table-striped table-responsive table-condensed no-space table-bordered"})
                    table2 = parser_functions.make2d(data2)
                    df2 = pd.DataFrame(data=table2[1:], columns=table2[0])

                    "\n\n"
                    print(df2)


                save = input("이 자료를 저장하시겠습니까? Y/N\n\n\n").upper()

                while save != "Y" or "N":
                    if save == "Y":
                        file_name = input("자료의 저장 이름을 정해주세요: ")
                        df2.to_csv(os.path.abspath(Path.home()) + "\\" + file_name + ".csv", encoding="utf-8-sig")
                        print('C:/Users/유저이름 경로로'+file_name+'csv 파일 저장이 완료되었습니다!\n\n')
                        break
                    elif save == "N":
                        break
                    else:
                        save = input("잘못된 입력입니다 다시 입력해주세요 Y/N\n").upper()

            elif prompt_key==2:

                print(teamcode)
                team = input("\n검색하고자 하는 팀 이름을 입력해주세요: ")

                while team not in teamlist:
                    team = input("\n존재하지 않는 팀입니다. \n 검색하고자 하는 팀 이름을 다시 입력해주세요: ")
                    if team in teamlist:
                        break

                start_year = input("\n검색하고자하는 연도 범위의 시작 연도를 입력해주세요: ")
                end_year = input("\n검색하고자하는 연도 범위의 끝 연도를 입력해주세요: ")


                ##연도 설정할때 문자 입력해도 오류나게

                while int(start_year) and int(end_year) not in list(range(1982, datetime.today().year+1)) or int(end_year)<int(start_year):

                        print("\n검색 가능한 범위가 아닙니다. 다시 입력해주세요\n")

                        start_year = input("\n검색하고자하는 연도 범위의 시작 연도를 입력해주세요: ")
                        end_year = input("\n검색하고자하는 연도 범위의 끝 연도를 입력해주세요: ")

                        if int(start_year) and int(end_year) in list(range(1982, datetime.today().year+1)) and int(end_year)>=int(start_year):
                            break


                BP=100

                BP = int(input("\n타자의 기록을 검색하고자 하면 0 투수의 기록을 검색하고자 하면 1을 입력해주세요: "))

                if BP == 0:
                    teamlinkstat = teamlinkB[:50] + str(start_year) + teamlinkB[54:58] + str(end_year) + teamlinkB[62:71] + team + teamlinkB[73:]
                elif BP == 1:
                    teamlinkstat = teamlinkP[:50] + str(start_year) + teamlinkP[54:58] + str(end_year) + teamlinkP[62:71] + team + teamlinkP[73:]

                request = requests.get(teamlinkstat)
                soup3 = BeautifulSoup(request.text, "html.parser")
                data3 = soup3.find("table", {"class": "table table-striped table-responsive table-condensed no-space table-bordered"})
                table3 = parser_functions.make2d(data3)
                df3 = pd.DataFrame(data=table3[1:], columns=table3[0])

                "\n\n"
                print(df3)

                save = input("\n이 자료를 저장하시겠습니까? Y/N\n\n\n").upper()

                while save != "Y" or "N":
                    if save == "Y":
                        file_name = input("\n자료의 저장 이름을 정해주세요: ")

                        df3.to_csv(os.path.abspath(Path.home()) + "\\" + file_name + ".csv", encoding="utf-8-sig")
                        print('\nC:/Users/유저이름 경로로  '+file_name+'  csv 파일 저장이 완료되었습니다!\n\n')
                        break
                    elif save == "N":
                        break
                    else:
                        save = input("\n잘못된 입력입니다 다시 입력해주세요 Y/N\n").upper()


            elif prompt_key == 3:

                sys.exit("\n프로그램을 종료합니다")

        except ValueError:

            try:

                print("\n올바른 입력이 아닙니다.\n1에서 3의 숫자를 입력해주세요")
                print(prompt)
                prompt_key = int(input())

            except ValueError:

                print('제발 숫자를 입력해주세요!!!')



##pyinstaller --icon=C:\Users\icako\PycharmProjects\pythonProject4\icon.ico --onefile --add-binary "chromedriver.exe";"." statiz.py