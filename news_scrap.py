from bs4 import BeautifulSoup
import requests


def google_news_scrap():

    # Scrap from this page
    req = requests.get("https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtWnlHZ0pHVWlnQVAB?hl=fr&gl=FR&ceid=FR%3Afr")
    soup = BeautifulSoup(req.text, "html.parser")

    article_list = []
    article = soup.find_all("article")

    for a in article:
        article_list.append(a.get_text())

    title_list = []
    source_list = []
    for a in article_list:
        pos_amp = a.find("ampvideo")
        title = a[:pos_amp]
        title_list.append(title)

        source = a[pos_amp + 16:]
        if 'Il y a' in source:
            pos_source = source.find('Il y a')
        elif 'Hier' in source:
            pos_source = source.find('Hier')
        else:
            pos_source = - 1
        source = source[:pos_source]
        source_list.append(source)

    datetime_list = []
    datetimes = soup.find_all("time")
    for d in datetimes:          # Print all occurrences
        datetime_list.append(d['datetime'])

    return title_list, source_list, datetime_list


if __name__ == '__main__':
    titles, sources, datetimes = google_news_scrap()

    for i, elt in enumerate(titles):
        print(f"{elt} \n{sources[i]} \n{datetimes[i]} \n\n")