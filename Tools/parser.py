import requests
import settings
from bs4 import BeautifulSoup
from requests_xml import XMLSession

user_agent = settings.user_agent
url = settings.sitemap_url
urls_limit = settings.urls_limit
xml_selector = settings.xml_selector
no_success_urls = []
no_canonical_urls = []

session = XMLSession()
sitemap_req = session.get(url)
result = sitemap_req.xml.search('<loc>{}</loc>')

print("Найдено xml файлов в sitemap: ", len(result))
print("Будет выбран xml файл для парсинга номер ", xml_selector)


if xml_selector != 0:
    second_req = session.get(result[xml_selector][0])
    search_urls = second_req.xml.search('<loc>{}</loc>')
    print("Найдено ссылок для парсинга:", len(search_urls))
    print("Запуск парсинга ссылок из xml файла ", result[xml_selector][0])
    counter = 0
    for target_url in search_urls:
        if counter == urls_limit:
            print("Парсинг завершен. Проверено сссылок: ", counter)
            break
        counter += 1
        print("Парсинг url № ", counter)
        request = requests.Session()
        response = requests.get(target_url[0], headers=user_agent)

        status_code = response.status_code
        html = response.content
        if status_code != 200:
            print("Найден ответ без кода 200")
            no_success_urls.append({"url": target_url[0], "status_code": status_code})
        soup = BeautifulSoup(html, "html.parser")
        link_cntr = 0
        for y in soup.findAll('link',{"rel":"canonical"}):
            link_cntr += 1
            canonical_res = (y.get('href').split())
            if canonical_res[0] != target_url[0]:
                print("Найдено несовпадение канонической ссылки и запрошенного url")
                no_canonical_urls.append(target_url[0])
print(no_success_urls)
print(no_canonical_urls)

with open('no_success_urls.txt', 'w', encoding='utf-8') as f:
    for list_element in no_success_urls:
        value = "url: " + list_element["url"] + " status_code:" + str(list_element["status_code"])
        f.write(value)

with open('no_canonical_urls.txt', 'w', encoding='utf-8') as f:
    for list_element in no_canonical_urls:
        f.write(list_element)