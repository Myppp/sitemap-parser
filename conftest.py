import pytest
import settings
import requests
from requests_xml import XMLSession


@pytest.fixture()
def urls():
    session = XMLSession()
    sitemap_req = session.get(settings.sitemap_url)
    result = sitemap_req.xml.search('<loc>{}</loc>')
    if settings.xml_selector != 0:
        second_req = session.get(result[settings.xml_selector][0])
        search_urls = second_req.xml.search('<loc>{}</loc>')
        counter = 0
        for target_url in search_urls:
            if counter == settings.urls_limit:
                break
            counter += 1
            request = requests.Session()
            response = request.get(target_url[0], headers=settings.user_agent)
    return response
