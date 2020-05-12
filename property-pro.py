import requests
from bs4 import BeautifulSoup as soup
from time import sleep
from random import randint
import csv


# csvFile = open('test.csv', 'w+', newline='')

# try:
#     writer = csv.writer(csvFile)
#     writer.writerow((Title, Locations, Beds, Baths,
#                      Toilets, Price, Last, Updated, Added))


csv_file = open('test.scrape.csv', 'w')
csv_writer = csv.writer(csv_file)
# csv_writer.writerow(['Title', 'PID', 'Price', 'Location', 'Beds', 'Baths', 'Toilets', 'Description', 'Agent', 'Added', 'Last Updated', 'Link'])
csv_writer.writerow(['Title', 'PID','Price', 'Location', 'Beds', 'Baths', 'Toilets', 'Agent', 'Added', 'Last Updtaed', 'Link'])

container_count = 0

n_pages = 0
for page in range(0, 4):
    n_pages += 1

    res = requests.get(
        'https://www.propertypro.ng/property-for-sale/flat-apartment/in/lagos/?search=Ikoyi+%2C+Lagos&bedroom=3&min_price=&max_price=200000000&page=' + str(page))

    page_soup = soup(res.text, 'html.parser')

    containers = page_soup.findAll(
        "div", {"class": "col-lg-8 col-md-8 col-sm-7 col-xs-12 prop-meta-data text-left"})

    container_count = container_count + len(containers)

    container = containers[0]
    if container != []:
        for container in containers:
            title = title = container.a.h2.text
            # find property-aminities
            amenities = container.findAll('div')[1].span
            # get the description
            description_box = container.findAll(
                "p", {"class": "pro-description readmore"})
            description_text = description_box[0].text
            # description_clean = description_text.replace('[email\xa0protected]', 'email-protected')
            # description_email = description_box[0].findAll("a",{"class":"__cf_email__"})
            # description_clean = desctipion_strip.replace(':', '|')
            # description_clean2 = description_clean.replace(',','|')
            # description_clean3 = description_clean2.replace('?','|')
            # description_clean4 = description_clean3.replace('...','|')
            
            # property date updated and added
            prop_date_box = container.findAll(
                "", {"class": "prop-date pull-left"})
            prop_date_txt = prop_date_box[0].text
            if (len(prop_date_txt) > 20):
                update_add_split = prop_date_txt.split(',')
                date_added = update_add_split[0]
                date_updated = update_add_split[1]
            else:
                update_add_split = prop_date_txt
                date_added = update_add_split
                date_updated = 'N/A'

            # agent
            agent_box = container.findAll("small", {"class": "agent-title"})
            agentxt = agent_box[0].text
            # get link of property
            link_string = container.div.a.get('href')
            # # get PID
            pidbox = container.findAll(
                "", {"class": "title prop-sub-title d-none d-sm-block"})
            pidtxt = pidbox[0].text
            pidlist = pidtxt.split('(')[-1]
            pid2 = pidlist.strip(')')
            pid1 = pid2.split(':')[-1:]
            pid = pid1[0]

            title = container.a.h2.text
            price = container.findAll('span')[1].text
            location = container.h3.text
            beds1 = amenities.findAll('span')[0].text
            beds = beds1.strip('bed')
            baths1 = amenities.findAll('span')[1].text
            baths = baths1.strip('bath')
            toilets1 = amenities.findAll('span')[2].text
            toilets = toilets1.strip('toilet')
            description = description_text
            agent = agentxt.strip('Marketed By')
            link = 'https://www.propertypro.ng' + link_string

            print('Title:' + title)
            print('PID:' + pid)
            print('Price:' + 'N ' + price)
            print('Location:' + location)
            print('Beds:' + beds)
            print('Baths:' + baths)
            print('Toilets:' + toilets)
            print('Description:' + description)
            print('Agent:' + agent)
            print('Link:' + link)
            print('Added:' + date_added)
            print('Updated:' + date_updated)
            

            print('::::::::::::::::::::::::::::::::::::::::')
            # csv_writer.writerow([title, pid, price, location, beds, baths, toilets, description, agent, date_added, date_updated, link]).endcode('utf-8')
            csv_writer.writerow([title,pid, price, location, beds, baths, toilets, agent, date_added, date_updated, link])

    else:
        break

    sleep(randint(1, 2))

print('You scraped {} pages containing {} properties.'.format(
    n_pages, container_count))

csv_file.close()
