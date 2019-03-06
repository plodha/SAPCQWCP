import csv
import io
import urllib.request
# 19:31.17
# 19:35.08 after 100 items: 19.35.08
# time: 3.45m = 225s
# time_per_item:    2.25
# time_per_950:     2137,5s = 35m
from bs4 import BeautifulSoup

import functions

# todo code_cleanup, getconent(unimportant)

# import functions.py as function
# delete csv content

filename = 'Questions3.CSV'
with open(filename, 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

# create csv and header
with open(filename, 'a', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(["Title", "All Tags", "Tags (separated with comma)", "Creation Date", "Status", "Link"])

no_of_pages = 10
count_items = 1
for ii in range(no_of_pages):
    url = "https://answers.sap.com/tags/73554900100800000266?page=" + str(
        ii) + "&pageSize=100&sort=active&filter=unanswered"
    content = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(content, "lxml")
    Questions = soup.find_all("li", {"class": "dm-contentListItem"})

    for res in Questions:
        Title = res.find("div", {"class": "dm-contentListItem__title"})
        Tags = res.find("div", {"class": "dm-tags__list"})
        Date = res.find("span", {"class": "dm-user__date"})
        Closed = res.find("span", {"class": "dm-badge--closed"})

        # get content
        title_text = (Title.text).strip('\n')
        tags_text = functions.tags_format(tags_text=Tags.text)
        date_text = functions.convertDate(date=Date.text)
        url_text = functions.convertHtml_link(html_link=str(Title.contents[1]))
        # hyperlink_text = '=HYPERLINK("http://www.Google.com\";\"Google")'  #was working but too slowly
        closed_text = "-"

        if Closed is not None:
            closed_text = "closed"

        # detailview of the question
        content2 = urllib.request.urlopen(url_text).read()
        soup2 = BeautifulSoup(content2, "lxml")
        Questions2 = soup2.find_all("div", {"class": "dm-tags__content"})

        detail_tags = (Questions2[0].text).split('\n\n\n')
        detail_user_tags = functions.detail_user_tags_format(detail_tags[2])

        all_tags = tags_text
        if len(detail_user_tags) != 0:
            all_tags = all_tags + ", " + detail_user_tags

        '''if 'Special Tax Depreciation Calculation for 30% in First Year Config' in title_text:
            print('stop:', detail_user_tags)
            test6789 = len(detail_user_tags)'''

        # output on console dd
        print("Count:", str(count_items))
        print("URL:", url_text)
        print("Title:", title_text)
        print("All Tags: ", all_tags),
        print("SAP Tags over: ", tags_text),
        print("User Tags: ", detail_user_tags),
        print("Date: ", date_text),
        print("Closed: ", closed_text),
        print("-----------------------------------------------------------------------")

        # wrtie to CSV
        with io.open(filename, 'a', encoding="utf-8", newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';')
            spamwriter.writerow([title_text, all_tags, date_text, closed_text, url_text])

        count_items = count_items + 1

        # if count_items ==0:
        #  print("ffds")

print('Check for duplicates in Excel')
