import requests
from bs4 import BeautifulSoup
from noti import send


# 뷰티플 숩 객체 만들기
def create_soup(p_url):
    # 유저에이전트 설정 - what is my user-agent 검색
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"
        }

    # 링크 정보 받아오기
    res = requests.get(p_url, headers=headers)
    res.raise_for_status()  # 정보가 없으면 프로그램 종료

    soup = BeautifulSoup(res.text, "lxml")
    return soup


def today_english():
    send("===== 오늘의 영어회화 =====")
    URL = "https://www.hackers.co.kr/?c=s_eng/eng_contents/I_others_english"
    soup = create_soup(URL)
    # 오늘의 회화 주제
    title = soup.find("div", attrs={"class": "conv_titleTxt"
                                    }).get_text().strip().replace("\n", "")
    # 회화 지분 선택(영어, 한글)
    texts = soup.find_all("div", attrs={"class": "conv_txt"})
    kor_texts = texts[0].find_all('span', attrs={"class": "conv_sub"})  # 한글 지문
    eng_texts = texts[1].find_all('span', attrs={"class": "conv_sub"})  # 영어 지문
    send(title)
    # 영어지문 출력
    send('영어 대화')
    for txt in eng_texts:
        send(txt.get_text())
    # send()

    # 한글 지문 출력
    send('한글 대화')
    for txt in kor_texts:
        send(txt.get_text())


def today_weather():
    send("===== 오늘의 날씨 =====")
    URL = "https://n.weather.naver.com/today/02590140"  # 네이버 날씨
    soup = create_soup(URL)
    div = soup.find("div", attrs={"class": "today_weather"})  # 날씨 전체 구쳑 선택
    weather_area = div.find("div",
                            attrs={"class": "weather_area"})  # 오늘의 날씨 요약 선택
    # 날씨 한줄 정리
    summary = weather_area.find("p", {"class": "summary"
                                      }).get_text().strip().replace('\n', " / ")
    # 날씨 상태
    current_degree = weather_area.find("strong", attrs={
        "class": "current"
        }).get_text()  # 현재온도
    degree_height = weather_area.find("strong", attrs={
        "class": "degree_height"
        }).get_text()  # 최고온도
    degree_low = weather_area.find("strong", attrs={
        "class": "degree_low"
        }).get_text()  # 최저온도
    degree_feel = weather_area.find("strong", attrs={
        "class": "degree_feel"
        }).get_text()  # 체감온도
    newline = '\n'
    send(
        f'날씨 요약 : {summary}{newline}오늘의 온도 : {degree_height} / {degree_low} / 체감온도 {degree_feel}')

    ttl_areas = div.find_all('div', attrs={"class": "ttl_area"})  # 세부날씨 정보
    charts = div.find_all('div', attrs={"class": "chart"})  # 세부날씨 수치

    # 미세먼지
    dust = ttl_areas[1].find("em", {"class": "level_text"}).get_text()
    value = charts[0].find("strong", {"class": "value"}).get_text()

    # 초미세먼지
    cho_dust = ttl_areas[2].find("em", {"class": "level_text"}).get_text()
    cho_value = charts[1].find("strong", {"class": "value"}).get_text()

    # 자외선
    sun = ttl_areas[3].find("em", {"class": "level_text"}).get_text()
    sun_value = charts[2].find("strong", {"class": "value"}).get_text()

    send(f'미세먼지 : {dust}({value}) / 초미세먼지 : {cho_dust}({cho_value}) / 자외선 : '
         f'{sun}({sun_value}) ')


# 열독률 높은 뉴스 - 예전 크롤링 기법
def today_new():
    send("===== 오늘의 뉴스 =====")
    URL = "https://news.daum.net"
    soup = create_soup(URL)  # 뷰티플 숩 객체 만들기
    all_pop_cmts = soup.findAll('div', {'class': 'pop_news pop_cmt'})[0]
    title = all_pop_cmts.find('h3')
    lis = all_pop_cmts.select('ol > li')
    send(title.text)

    for li in lis[:5]:
        content = li.find_all('span')
        rank = content[0].text
        source = content[1].text
        link = li.find('a').get('href')
        txt = li.text.strip().replace("                    ", "").replace("\n",
                                                                          "  ").replace(
            "         ", " :").replace("       ", " /")
        send(f'{txt} / {link}')
    send()


if __name__ == "__main__":
    # today_weather()
    # today_english()
    today_new()

