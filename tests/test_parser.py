import requests
import settings
from bs4 import BeautifulSoup
from requests_xml import XMLSession


def test_status_code_200():
    no_success_urls = []
    result = XMLSession().get(settings.sitemap_url).xml.search('<loc>{}</loc>')
    if settings.xml_selector != 0:
        second_req = XMLSession().get(result[settings.xml_selector][0])
        search_urls = second_req.xml.search('<loc>{}</loc>')
        counter = 0
        for target_url in search_urls:
            if counter == settings.urls_limit:
                break
            counter += 1
            request = requests.Session()
            response = request.get(target_url[0], headers=settings.user_agent)
            status_code = response.status_code
            if status_code != 200:
                no_success_urls.append({"url": target_url[0], "status_code": status_code})
                with open('no_success_urls.txt', 'w', encoding='utf-8') as f:
                    for list_element in no_success_urls:
                        value = "url: " + list_element["url"] + " status_code:" + str(list_element["status_code"])
                        f.write(value)
    assert status_code == 200
    return status_code


def test_canonical_url(urls):
    no_canonical_urls = []
    result = XMLSession().get(settings.sitemap_url).xml.search('<loc>{}</loc>')
    link_cntr = 0
    counter = 0
    for target_url in XMLSession().get(result[settings.xml_selector][0]).xml.search('<loc>{}</loc>'):
        if counter == settings.urls_limit:
            break
        counter += 1
    for y in BeautifulSoup(urls.content, "html.parser").findAll('link', {"rel": "canonical"}):
        link_cntr += 1
        canonical_res = (y.get('href').split())
        if canonical_res[0] != target_url[0]:
            no_canonical_urls.append(target_url[0])
            with open('no_canonical_urls.txt', 'w', encoding='utf-8') as f:
                for list_element in no_canonical_urls:
                    f.write(list_element)
    assert canonical_res[0] == target_url[0]
    return canonical_res