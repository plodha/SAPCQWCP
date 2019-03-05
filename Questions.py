from bs4 import BeautifulSoup

import urllib.request
from datetime import datetime, timedelta
from dateutil.parser import parse
import csv
import io

#roij

#import functions.py as function
# delete csv content
with open('Questions.CSV', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

# create csv and header
with open('Questions.CSV', 'a', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(["Title", "Tags (separated with comma)", "Creation Date", "Status","Link"])

no_of_pages=10
count_items = 1
for ii in range(no_of_pages):
    url = "https://answers.sap.com/tags/73554900100800000266?page=" + str(ii) + "&pageSize=100&sort=active&filter=unanswered"
    content = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(content, "lxml")
    Questions = soup.find_all("li", {"class": "dm-contentListItem"})


    # @todo add seconds and minute and minutes
    def convertDate(date):
        days_to_subtract = 0

        if "hour ago" in date:
            days_to_subtract = 0

        elif "hours ago" in date:
            days_to_subtract = 0

        elif "yesterday" in date:
            days_to_subtract = 1

        elif "days" in date:
            days_to_subtract = date [:1]

        else:
            # convert date into a proper date format
            dt = parse(date)
            d = dt.strftime('%d/%m/%Y')
            return d;

        d = datetime.today() - timedelta(days=int(days_to_subtract))
        d = d.strftime('%d/%m/%Y')
        return d;

    def tags_format(tags_text):
        i = len(tags_text)
        tags_text = (tags_text).replace('\n', ',')
        tags_text = (tags_text.replace(',SAP S/4HANA,', '')).strip('\n')

        # remove first comma
        if tags_text[:1] == ',':
            tags_text = tags_text[1:i]

        i = len(tags_text)
        i = i-1
        # remove the last comma
        if tags_text[-1:] == ',':
            tags_text = tags_text[0:i]

        # add space between comma
        tags_text = (tags_text).replace(',', ', ')

        return tags_text;

    def convertHtml_link (html_link):
        # <a href="/questions/703307/error-in-main-shdimpparmvnt-shd-308-column-name-al.html" title="Error in MAIN_SHDIMP/PARMVNT_SHD 308-column name already exists">Error in MAIN_SHDIMP/PARMVNT_SHD 308-column name already exists</a>
        # https://answers.sap.com/questions/703910/sap-r3-to-s4-migration-schedule.html
        html_link = (html_link).replace('<a href="/','https://answers.sap.com/')
        sep = '" title='
        html_link = html_link.split(sep, 1)[0]

        return html_link;


    for res in Questions:
        Title = res.find("div", {"class": "dm-contentListItem__title"})
        Tags = res.find("div", {"class": "dm-tags__list"})
        Date = res.find("span", {"class": "dm-user__date"})
        Closed = res.find("span", {"class": "dm-badge--closed"})

        # get content
        title_text = (Title.text).strip('\n')
        # debug
        if "Purchase order type : Output management with BRF+" in title_text:
            print ("stop")

        tags_text = tags_format(tags_text=Tags.text)
        date_text = convertDate(date=Date.text)
        closed_text ="-"

        if Closed is not None:
            closed_text = "closed"

        url_text = convertHtml_link(html_link = str(Title.contents[1]))
        hyperlink_text = '=HYPERLINK("http://www.Google.com\";\"Google")'

        # output on console
        print("Count:", str(count_items))
        print("URL:", url_text)
        print("Title:", title_text)
        print("TAGS: ", tags_text),
        print("Date: ", date_text),
        print("Closed: ", closed_text),
        print("-----------------------------------------------------------------------")

        # wrtie to CSV
        with io.open('Questions.CSV', 'a', encoding="utf-8", newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';')
            spamwriter.writerow([title_text, tags_text, date_text, closed_text, url_text])

        count_items = count_items+1



<<<<<<< HEAD
print('Check for duplicates in Excel')
=======
print('Check for duplicates in Excel')
>>>>>>> origin/master
