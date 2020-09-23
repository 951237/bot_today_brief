import requests
from bs4 import BeautifulSoup
from noti import send


# 뷰티플 숩 객체 만들기
def create_soup(p_url):
    # 유저에이전트 설정 - what is my user-agent 검색
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/84.0.4147.125 Safari/537.36"
        }

    # 링크 정보 받아오기
    res = requests.get(p_url, headers=headers)
    res.raise_for_status()  # 정보가 없으면 프로그램 종료

    soup = BeautifulSoup(res.text, "lxml")
    return soup


def today_english():
    try:
        result = []
        result.append("===== 오늘의 영어회화 =====")
        URL = "https://www.hackers.co.kr/?c=s_eng/eng_contents/I_others_english"
        soup = create_soup(URL)
        # 오늘의 회화 주제
        title = soup.find("div", attrs={"class": "conv_titleTxt"
                                        }).get_text().strip().replace("\n", "")
        # 회화 지분 선택(영어, 한글)
        texts = soup.find_all("div", attrs={"class": "conv_txt"})
        kor_texts = texts[0].find_all('span', attrs={"class": "conv_sub"})  # 한글 지문
        eng_texts = texts[1].find_all('span', attrs={"class": "conv_sub"})  # 영어 지문
        result.append(title)
        # 영어지문 출력
        result.append('영어 대화')
        for txt in eng_texts:
            result.append(txt.get_text())
        # result.append()

        # 한글 지문 출력
        result.append('한글 대화')
        for txt in kor_texts:
            result.append(txt.get_text())

        return result
    except:
        error = ["오류 : 오늘의 영어"]
        return error


def today_weather(p_region, p_url):
    result = []
    result.append(f"===== 오늘의 {p_region} 날씨 =====")
    soup = create_soup(p_url)
    div = soup.find("div", attrs={"class": "today_weather"})  # 날씨 전체 구쳑 선택
    weather_area = div.find("div", attrs={"class": "weather_area"})  # 오늘의 날씨 요약 선택

    try:
        # 날씨 한줄 정리
        summary = weather_area.find("p", {"class": "summary"}).get_text().strip().replace('\n', " / ")
        # 날씨 상태
        current_degree = weather_area.find("strong", attrs={"class": "current"}).get_text()  # 현재온도
        degree_feel = weather_area.find("dd", attrs={"class": "desc_feeling"}).get_text()  # 체감온도
        desc_rainfall = weather_area.find("dd", attrs={"class": "desc_rainfall"}).get_text()  # 강수확률
        newline = '\n'
        result.append(f'날씨 요약 : {summary}{newline}현재 온도 : {current_degree} /  체감온도 : {degree_feel} / 강수확률 : {desc_rainfall}')

    except:
        return ["오류 : 오늘의 날씨 기본정보"]

    try:
        ttl_areas = div.find_all('div', attrs={"class": "ttl_area"})  # 세부날씨 정보
        charts = div.find_all('div', attrs={"class": "chart"})  # 세부날씨 수치

        # 미세먼지
        dust = ttl_areas[0].find("em", {"class": "level_text"}).get_text()
        value = charts[0].find("strong", {"class": "value"}).get_text()

        # 초미세먼지
        cho_dust = ttl_areas[1].find("em", {"class": "level_text"}).get_text()
        cho_value = charts[1].find("strong", {"class": "value"}).get_text()

        # 자외선
        sun = ttl_areas[2].find("em", {"class": "level_text"}).get_text()
        sun_value = charts[2].find("strong", {"class": "value"}).get_text()

        newline = '\n'

        result.append(f'미세먼지 : {dust}({value}) / 초미세먼지 : {cho_dust}({cho_value}) / 자외선 : {sun}({sun_value}){newline}')
        return result

    except:
        return ["오류 : 오늘의 날씨 세부정보"]


# 열독률 높은 뉴스 - 예전 크롤링 기법
def today_news():
    try:
        result = []
        result.append("===== 이시간 주요 뉴스 =====")
        URL = "https://news.daum.net"
        soup = create_soup(URL)  # 뷰티플 숩 객체 만들기

        box_headline = soup.find("div", {"class": "box_headline"})
        lis = box_headline.select('ul > li')
        i = 1

        for li in lis:
            content = li.find_all('strong')
            txt = content[0].text.strip().replace('\n', " / ")
            link = li.find('a').get('href')
            result.append(f'{i}. {txt} / {link}')
            i += 1
        result.append("")

        return result

    except:
        return ["오류 : 오늘의 뉴스"]


if __name__ == "__main__":
    # URL[0] : 새솔동, URL[1] : 안산시 사동
    URL = {'새솔동': 'https://n.weather.naver.com/today/02590140', '안산': 'https://n.weather.naver.com/today/02271103'}
    for k, v in URL.items():
        weather_data = today_weather(k, v)
        weather = ("\n".join(str(i) for i in weather_data))
        send(weather)

    english_data = today_english()
    english = ("\n".join(str(i) for i in english_data))  # 리스트를 한줄로 출력 "" : 한줄로 이어서, "\n" 줄바꿈으로 출력
    send(english)

    news_data = today_news()
    news = ("\n\n".join(str(i) for i in news_data))
    send(news)
