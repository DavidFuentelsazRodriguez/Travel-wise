from bs4 import BeautifulSoup
import requests
import re

BASE_URL = 'https://www.viator.com'
URL = f'{BASE_URL}/es-ES/Spain-tourism/d67-r1238050151644556-s322637112?m=27910&supag=1238050151644556&supsc=kwd-77378197139969&supai=77378206570439&supdv=c&supnt=nt:o&suplp=3222&supli=170&supti=kwd-77378197139969&tsem=true&supci=kwd-77378197139969&supkw=lugares%20para%20visitar%20en%20espa%C3%B1a&msclkid=9d27fd23912f19d924fc9a4a29aa1ee7'

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
        activity_name = activity.find('span', class_='title__h6oh').get_text()
        price_element = activity.find('strong', class_='currentPrice__Llbs') or activity.find('div', class_='currentPrice__Llbs')
        price = price_element.find('span').get_text() if price_element else 0
        duration = activity.find('li', {'data-automation': 'sem-lander-product-list-card-duration'})
        duration = duration.get_text() if duration else None
        activity_url = BASE_URL + activity.find('a', class_='productCard__A2Ct clickable__DG3l inspiration__n1kn')['href']
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

    city = soup.find('a', class_='crumbLink__et23')
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
    content = fetch_page_content(URL)
    if not content:
        return []

    soup = BeautifulSoup(content, 'html.parser')
    activities_div = soup.find_all('div', class_='productCardWrapper__FQeo')
    activities = []

    for activity in activities_div:
        details = parse_activity_details(activity)
        if not details:
            continue

        additional_details = fetch_activity_additional_details(details['url'])
        activity_data = {
            **details,
            **additional_details
        }
        activities.append(activity_data)

    return activities

