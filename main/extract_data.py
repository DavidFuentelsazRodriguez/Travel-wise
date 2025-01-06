from bs4 import BeautifulSoup
import requests
import re

BASE_URL = 'https://www.viator.com'
URL_TEMPLATE = f'{BASE_URL}/es-ES/Spain/d67-ttd'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
    'Referer': 'https://www.google.com/',
}

def fetch_page_content(url):
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.text
        else:
            print(f'HTTP Error: {response.status_code} for URL: {url}')
            return None
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
        return None

def parse_activity_details(activity):
    try:
        activity_name = activity.find('h2', class_='title__mrvv title4__AK3w').get_text()
        price = activity.find('span', class_='moneyView__wf0H defaultColor__k7nd').get_text()
        duration = activity.find('li', {'data-automation': 'ttd-product-list-card-duration'})
        duration = parse_duration(duration.get_text()) if duration else None
        activity_url = BASE_URL + activity.find('a', {'data-automation': 'ttd-product-list-card'})['href']
        return {
            'name': activity_name,
            'price': price,
            'duration': duration,
            'url': activity_url
        }
    except AttributeError:
        return None

def fetch_activity_additional_details(activity_url):
    content = fetch_page_content(activity_url)
    if not content:
        return {}

    soup = BeautifulSoup(content, 'html.parser')

    city = soup.find('span', class_='location__C9GX')
    city = city.get_text() if city else None

    recommendation_rate = soup.find('span', class_='recommendationLabel__EZ1b')
    regex = r"\b(100|\d{1,2})\b"
    recommendation_rate = re.findall(regex, recommendation_rate.get_text())[0] if recommendation_rate else None

    badge_of_excellence = bool(soup.find('span', class_='badgeOfExcellenceInner__WVG4'))

    general_description = soup.find('div', {'class': '', 'lang': 'es-x-mtfrom-en'})
    if general_description and general_description.findChild():
        general_description = general_description.findChild().get_text()
    else:
        general_description = 'Unknown'

    return {
        'city': city,
        'recommendation_rate': recommendation_rate,
        'badge_of_excellence': badge_of_excellence,
        'description': general_description
    }

def extract_activities():
    activities = []
    page_number = 1

    while page_number < 5:
        url = URL_TEMPLATE if page_number == 1 else f"{URL_TEMPLATE}/{page_number}"
        content = fetch_page_content(url)
        if not content:
            break

        soup = BeautifulSoup(content, 'html.parser')
        activities_div = soup.find('div', class_='productListProductsAndSortByContainer__kSLc')
        if not activities_div:
            print(f"No se encontró el contenedor de actividades en la página {page_number}.")
            break

        activities_card = activities_div.find_all('div', class_='productListCardWithDebug__GUoq')
        if not activities_card:
            print(f"No se encontraron tarjetas de actividades en la página {page_number}. Finalizando.")
            break

        for activity in activities_card:
            details = parse_activity_details(activity)
            if not details:
                continue

            additional_details = fetch_activity_additional_details(details['url'])
            activity_data = {
                **details,
                **additional_details
            }
            activities.append(activity_data)

        page_number += 1

    return activities

def parse_duration(duration):
    pattern = r"De \d+ a \d+ horas"
    if re.match(pattern, duration):
        return None
    return duration

