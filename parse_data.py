import requests
from bs4 import BeautifulSoup


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'}


def get_league_table():
    url = 'https://www.premierleague.com/tables'
    response = requests.get(url, headers=headers).text

    with open('templates/index.html', 'w', encoding='utf-8') as file:
        file.write(response)

    with open('templates/index.html', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    clubs = soup.find_all('tr', attrs={'data-filtered-entry-size': '20'})

    data = []

    for club in clubs:
        club_image = club.find('td', class_='team').find('img')['srcset'][0:-3]
        matches_info = club.find_all('td', class_=None)
        goal_dif = club.find_all('td', class_='hideSmall')
        last_matches_list = club.find('td', class_='form hideMed').find_all('abbr', class_='form-abbreviation')
        next_opponent_image = club.find('td', class_='nextMatchCol').find('img')['srcset'].split(',')[1][0:-3]
        last_matches = ''
        for match in last_matches_list:
            last_matches += f'{match.text} '

        data.append(
            [
                club_image,
                club.find('span', class_='long').text,
                matches_info[0].text,
                matches_info[1].text,
                matches_info[2].text,
                matches_info[3].text,
                goal_dif[0].text,
                goal_dif[1].text,
                matches_info[4].text.strip(),
                club.find('td', class_='points').text,
                last_matches,
                next_opponent_image
            ]
        )
    return data


def get_previous_match():
    url = 'https://www.skysports.com/manchester-united-results'

    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')
    last_match = soup.find('div', class_='fixres__body').find('div', class_='fixres__item')

    url = last_match.find('a', class_='matches__item matches__link')['href']
    detailed_response = requests.get(url, headers=headers).text
    detailed_soup = BeautifulSoup(detailed_response, 'lxml')
    match_details = detailed_soup.find('div', class_='sdc-site-match-header__detail')
    match_details = ' '.join(match_details.text.split()).replace('.', '\n')

    match_info = detailed_soup.find_all('h4', class_='sdc-site-match-header__team')
    data = [match_details]
    for team in match_info:
        logo = team.find('img')['src']
        score = team.find('span', class_='sdc-site-match-header__team-score-block').text
        data.append([logo, int(score)])
    return data


def get_previous_matches():
    url = 'https://www.skysports.com/manchester-united-results'
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')
    teams1 = soup.find_all('span', class_='matches__item-col matches__participant matches__participant--side1')[1:6]
    teams2 = soup.find_all('span', class_='matches__item-col matches__participant matches__participant--side2')[1:6]
    scores = soup.find_all('span', class_='matches__teamscores')[1:6]
    dates = soup.find_all('h4', class_='fixres__header2')[1:6]
    leagues = soup.find_all('h5', class_='fixres__header3')[1:6]
    data = []
    for i in range(5):
        data.append(
            [
                f"{teams1[i].text.strip()} {'-'.join(scores[i].text.split())} {teams2[i].text.strip()}",
                dates[i].text,
                leagues[i].text
            ]
        )
    return data


def get_upcoming_matches():
    url = 'https://www.skysports.com/manchester-united-fixtures'
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')
    teams1 = soup.find_all('span', class_='matches__item-col matches__participant matches__participant--side1')[:5]
    teams2 = soup.find_all('span', class_='matches__item-col matches__participant matches__participant--side2')[:5]
    times = soup.find_all('span', class_='matches__date')[:5]
    dates = soup.find_all('h4', class_='fixres__header2')[:5]
    leagues = soup.find_all('h5', class_='fixres__header3')[:5]
    data = []
    for i in range(5):
        data.append(
            [
                f'{teams1[i].text.strip()} {times[i].text.strip()} {teams2[i].text.strip()}',
                dates[i].text,
                leagues[i].text
            ]
        )
    return data
