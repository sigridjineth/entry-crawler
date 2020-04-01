from selenium import webdriver
import time
import pandas as pd

title_list = []
author_list = []
view_list = []
like_list = []
comment_list = []

driver = webdriver.Chrome('/Users/jypsnewmac/Documents/GitHub/entry-crawler/chromedriver_mac64/chromedriver')


def article_scrapper():
	tables = driver.find_element_by_xpath("/html/body/section/section/section/section/div[3]/div")
	tables_projectbox = tables.find_elements_by_class_name("projectBox")

	for project in tables_projectbox:
		title = project.find_element_by_class_name("projectInfoName")
		if sorting_keyword(title.text):
			article_titleparser(title)
			article_authorparser(project)
			article_viewparser(project)
			article_likeparser(project)
			article_commentparser(project)


def article_titleparser(title):
	title_list.append(title.text)


def article_authorparser(project):
	tables_projectbox_author = project.find_element_by_class_name("projectInfoNameHigh")
	author_list.append(tables_projectbox_author.text)


def article_viewparser(project):
	tables_projectbox_infocontainer = project.find_element_by_class_name("projectInfoContainer")
	tables_projectbox_view = tables_projectbox_infocontainer.find_element_by_class_name("projectInfoViews")
	view_list.append(tables_projectbox_view.text)


def article_likeparser(project):
	tables_projectbox_like = project.find_element_by_class_name("projectInfoLikes")
	like_list.append(tables_projectbox_like.text)


def article_commentparser(project):
	tables_projectbox_comment = project.find_element_by_class_name("projectInfoComments")
	comment_list.append(tables_projectbox_comment.text)


# 협업과 관련된 키워드만 뽑아보기


def sorting_keyword(article_text):
	keyword = ["협업", "합작", "팀원", "모집", "구인", "합작원", "합작품", "멤버", "공용계정", "공용"]
	for trial in keyword:
		if trial in article_text:
			return True
	return False


# Pandas 활용 CSV 파일로 변환하기

def string_to_csv():
	data = {"title": title_list, "author": author_list, "comment": comment_list, "views": view_list, "likes": like_list}
	df = pd.DataFrame(data)
	print(df)
	df.to_excel('results_share.xlsx', sheet_name='results', encoding='euc-kr')


def main():
	for i in range(1, 500):
		driver.get("about:blank")
		driver.get("https://playentry.org/all#!/?sort=updated&rows=12&page="+str(i))
		time.sleep(10)
		article_scrapper()
		print("page " + str(i) + " done.")
		print("title:" + str(title_list) + "author: " + str(author_list) + "comment: " + str(comment_list)
			  + "view: " + str(view_list) + "like: " + str(like_list))
		driver.implicitly_wait(10)

	string_to_csv()
	driver.quit()


main()
