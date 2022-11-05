import requests
from bs4 import BeautifulSoup
import random
import csv
import time
import random_user_agent
from random_user_agent import *

headers_list = [{
	'authority': 'httpbin.org',
	'cache-control': 'max-age=0',
	'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
	'sec-ch-ua-mobile': '?0',
	'upgrade-insecure-requests': '1',
	'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'sec-fetch-site': 'none',
	'sec-fetch-mode': 'navigate',
	'sec-fetch-user': '?1',
	'sec-fetch-dest': 'document',
	'accept-language': 'en-US,en;q=0.9',
} # , {...}
]
headers = random.choice(headers_list)
#headers = random_user_agent.headers
proxies = {'http': 'http://192.210.159.128'}
def get_list_of_pages_soup(from_page,to_page):
    list_of_links_to_agents = []
    end_of_range = to_page + 1
    for strona in range(from_page,end_of_range):
        time.sleep(3)
        #print(strona)
        page_number = strona
        url = f'https://www.zillow.com/professionals/real-estate-agent-reviews/denver-co/?page={page_number}'
        print(url)
        print(headers)
        #print(url)
        r = requests.get(url, headers=headers)
        print(r.status_code)
        soup = BeautifulSoup(r.content, 'html.parser')
        print(soup.text)
        agents_table = soup.find_all("tbody", {"class": "StyledTableBody-c11n-8-50-1__sc-8i1s74-0 iohaIx"})[0]
        set_of_single_agents = agents_table.find_all("tr")
        for tr in set_of_single_agents:
            second_half_of_link = tr.find('a')['href']
            link_to_single_agent = 'https://www.zillow.com/'+second_half_of_link
            list_of_links_to_agents.append(link_to_single_agent)
    return list_of_links_to_agents
#list_of_links_to_agents = get_list_of_pages_soup(1,2)
list_of_dict = []
list_of_links_to_agents = get_list_of_pages_soup(1,10)

i = 1
try:
    for link in list_of_links_to_agents:
        time.sleep(3)
        url = link
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        info_div = soup.find("div", {"class": "sc-fzomuh kwRcsK"})
        childrens = info_div.children
        list_of_info_div_childrens = []

        for child in childrens:
            list_of_info_div_childrens.append(child)
        hip_team_info = list_of_info_div_childrens[0].text.split()[0]

        if hip_team_info == 'Lead':
            team_dependence = 'Lead'
            team_name = list_of_info_div_childrens[0].text

        elif hip_team_info == 'Member':
            team_dependence = 'Member'
            team_name = list_of_info_div_childrens[0].text.split('of ')[1].strip()

        else:
            team_dependence = 'NONE'
            team_name = 'NO TEAM INFO'

        name = info_div.find("div",{"class":"ctcd-title"}).find('h1').text.strip()


        personal_info_div = soup.find('div', {"class":"Flex-c11n-8-39-0__n94bjd-0 igzmLa"})
        cell_phone_number = 'BRAK'
        if team_dependence == 'NONE' or team_dependence == 'Lead':
            phone_number = personal_info_div.find_all('div', {"class":"Flex-c11n-8-39-0__n94bjd-0 sc-fzolEj dmgWTu"})
            list_of_personal_data = []
            for aaa in phone_number:
                list_of_personal_data.append(aaa.text)
            cell_phone_number = list_of_personal_data[1][11:]
        if team_dependence == 'Member':

            try:
                imie = name.split()[0]
                nazwisko = name.split()[1]
                url_num = f'https://www.realtor.com/realestateagents/agentname-{imie}%20{nazwisko}'

                r_realtor = requests.get(url_num, headers=headers)
                #print(r_realtor.status_code)
                soup_realtor = BeautifulSoup(r_realtor.content, 'html.parser')
                list_agents = soup_realtor.find('ul', {"class": "jsx-2317458496"})
                l_list_agents = list_agents.find_all("div", {"class":"jsx-2317458496"})
                if len(l_list_agents) > 1:
                    phone_number = personal_info_div.find_all('div', {"class":"Flex-c11n-8-39-0__n94bjd-0 sc-fzolEj dmgWTu"})
                    list_of_personal_data = []
                    for aaa in phone_number:
                        list_of_personal_data.append(aaa.text)
                    cell_phone_number = list_of_personal_data[1][11:]
                else:
                    cell_phone_number = soup_realtor.find("div", {"class":"jsx-3970352998 agent-phone hidden-xs hidden-xxs"}).text.strip()



            except:
                phone_number = personal_info_div.find_all('div', {"class":"Flex-c11n-8-39-0__n94bjd-0 sc-fzolEj dmgWTu"})
                list_of_personal_data = []
                for aaa in phone_number:
                    list_of_personal_data.append(aaa.text)
                cell_phone_number = list_of_personal_data[1][11:]

        webside = 'NONE'
        facebook = "NONE"
        linkedin = "NONE"
        twitter = "NONE"

        links_in_personal_data_div = personal_info_div.find_all('a')
        for plink in links_in_personal_data_div:
            if plink.text == 'Website':
                webside = plink['href']
            if plink.text == 'Facebook':
                facebook = plink['href']
            if plink.text == 'LinkedIn':
                linkedin = plink['href']
            if plink.text == 'Twitter':
                twitter = plink['href']
            print('Nowy lead -----------')
            print('Name -  '+ name)
            print('Team name -  ' +team_name)
            print('Phone -  '+ cell_phone_number)
            print('zillow.com profile -  '+ url)
            print('Webside -  '+ webside)
            print('Facebook -  '+ facebook)
            print('LinkedIn -  '+ linkedin)
            print('Twitter -  '+ twitter)
            data_dict = {'Name':name, 'Team name':team_name, 'Phone':cell_phone_number, 'zillow.com profile':url, 'Webside':webside, 'Facebook':facebook, 'LinkedIn':linkedin, 'Twitter':twitter}
            print(data_dict)
        list_of_dict.append(data_dict)
        i = i +1
        print(i)

except:
    pass

nr_pliku = 1
fieldnames1 = ['Name', 'Team name', 'Phone', 'zillow.com profile', 'Webside', 'Facebook', 'LinkedIn', 'Twitter']

with open(f'realtor_leads_{nr_pliku}.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames1)
    writer.writeheader()
    for dict in list_of_dict:
        writer.writerow(dict)



