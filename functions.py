from datetime import datetime, timedelta

from dateutil.parser import parse

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
        days_to_subtract = date[:1]

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
    tags_text = (tags_text.replace(',SAP S/4HANA,', ''))

    # remove first comma
    if tags_text[:1] == ',':
        tags_text = tags_text[1:i]

    i = len(tags_text)
    i = i - 1
    # remove the last comma
    if tags_text[-1:] == ',':
        tags_text = tags_text[0:i]

    # add space between comma
    tags_text = (tags_text).replace(',', ', ')

    return tags_text;


def convertHtml_link(html_link):
    # <a href="/questions/703307/error-in-main-shdimpparmvnt-shd-308-column-name-al.html" title="Error in MAIN_SHDIMP/PARMVNT_SHD 308-column name already exists">Error in MAIN_SHDIMP/PARMVNT_SHD 308-column name already exists</a>
    # https://answers.sap.com/questions/703910/sap-r3-to-s4-migration-schedule.html
    html_link = (html_link).replace('<a href="/', 'https://answers.sap.com/')
    sep = '" title='
    html_link = html_link.split(sep, 1)[0]

    return html_link;

def detail_user_tags_format(detail_user_tags):
    detail_user_tags = detail_user_tags.replace('|', ',', )
    detail_user_tags = detail_user_tags.replace('\n', '', )
    detail_user_tags = detail_user_tags.replace('SAP S/4HANA, ', '')
    detail_user_tags = detail_user_tags.replace('SAP S/4HANA,', '')
    detail_user_tags = detail_user_tags.replace('SAP S/4HANA', '')
    detail_user_tags = detail_user_tags.replace('  ', '')

    return detail_user_tags;