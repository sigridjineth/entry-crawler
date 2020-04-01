from selenium import webdriver
import time
import pandas as pd

# pandas로 각종 컬럼에 대한 정의가 들어가는 곳
title_list = []
author_list = []
view_list = []
like_list = []
date_list = []

# selenium 사용을 위한 웹 드라이버 설정
driver = webdriver.Chrome('/Users/jypsnewmac/Documents/GitHub/entry-crawler/chromedriver_mac64/chromedriver')

# 엔트리 공유하기의 '엔트리 이야기' 게시글 크롤링


def article_scrapper():
    table = driver.find_element_by_xpath("/html/body/section/section/section/div[2]/div/table/tbody")
    table_tr = table.find_elements_by_tag_name("tr")

    for tr in table_tr:
        if sorting_keyword(tr.text):
            article_titleparser(tr)
            article_authorparser(tr)
            article_viewparser(tr)
            article_dateparser(tr)
            article_likeparser(tr)


def article_titleparser(tr):
    title = tr.find_element_by_class_name("discussTitleWrapper")
    title_list.append(title.text)


def article_authorparser(tr):
    author = tr.find_element_by_class_name("discussWriter")
    author_list.append(author.text)


def article_viewparser(tr):
    view = tr.find_element_by_class_name("discussViewCount")
    view_list.append(view.text)


def article_likeparser(tr):
    like = tr.find_element_by_class_name("discussLikeCount")
    like_list.append(like.text)


def article_dateparser(tr):
    date = tr.find_element_by_class_name("discussDate")
    date_list.append(date.text)

# 협업과 관련된 키워드만 뽑아보기


def sorting_keyword(article_text):
    keyword = ["협업", "합작", "팀원", "모집", "구인", "합작원", "합작품", "멤버", "공용계정", "공용"]
    for trial in keyword:
        if trial in article_text:
            return True
    return False


# Pandas 활용 CSV 파일로 변환하기

def string_to_csv():
    data = {"title": title_list, "author": author_list, "dates": date_list, "views": view_list, "likes": like_list}
    df = pd.DataFrame(data)
    print(df)
    df.to_excel('results_free.xlsx', sheet_name='results', encoding='euc-kr')


# 크롤러 실행하기

def main():
    for i in range(1, 250):
        driver.get("https://playentry.org/ds#!/free?sort=created&rows=1000&page=" + str(i))
        time.sleep(10)
        article_scrapper()
        print("page " + str(i) + " done.")
        driver.implicitly_wait(10)

    string_to_csv()
    driver.quit()


main()
