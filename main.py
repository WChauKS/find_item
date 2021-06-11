import requests
import yaml
import tweepy
from bs4 import BeautifulSoup

with open('config.yaml', 'r') as f:
    data = yaml.safe_load(f)


# scrapes the url and returns the items along with the tags
def scrape():
    page = requests.get(data['url'])
    soup = BeautifulSoup(page.content, 'html.parser')

    # get all items
    items = soup.find_all('h2')  # items were found in h2 tags
    return items


# collects item name and links into two dicts
# one is for all items, the other is for ones not saved previously
def get_relevent_items(cur, prev):
    # dict contains item name and its link
    found_items = {}
    new_items = {}
    for i in cur:
        tmp = i.text.lower()
        if data['item_of_interest'] in tmp:
            tmp = remove_strings(tmp)
            found_items[tmp] = data['site'] + i.find('a')['href']
            if tmp not in prev:
                new_items[tmp] = found_items[tmp]
    return found_items, new_items


# cleaning up the title of the item before storing and sending
def remove_strings(text):
    text = text.replace('\n', ' ')
    for rm in data['rm_strings']:
        text = text.replace(rm, '')
    return text


# saves all the items found in a dict format
def save_items(items):
    # overwrite the existing prev.txt file and save the current dict
    with open(data['filename'], 'w') as f:
        for k, v in items.items():
            print('{}: {}'.format(k, v), file=f)


# opens the saved file from the previous scrape
def open_prev():
    # read in prev.txt as a dictionary for checking if new items are added
    prev_items = {}
    with open(data['filename']) as f:
        # prev.txt is not formatted correctly (debugging or empty)
        try:
            for line in f:
                (k, v) = line.split(': ', 1)  # split line by ': ' one time
                prev_items[k] = v.replace('\n', '')
        except ValueError:
            # random, will be overwritten when saving
            prev_items['default'] = 'default'
    return prev_items


# auths with tweepy api and sends text to the user specified in config.py file
def dm_user(msg_contents):
    auth = tweepy.OAuthHandler(
        data['twitter']['consumer_key'],
        data['twitter']['consumer_secret']
    )
    auth.set_access_token(
        data['twitter']['access_token'],
        data['twitter']['access_token_secret']
    )
    api = tweepy.API(auth)
    # try:
    #     api.verify_credentials()
    #     print('Success!')
    # except:
    #     print('Failure')
    api.send_direct_message(api.get_user(data['user_id']).id_str, msg_contents)


if __name__ == '__main__':
    prev = open_prev()
    all_items = scrape()
    items, new_items = get_relevent_items(all_items, prev)
    save_items(items)
    if len(new_items) > 0:
        for i in new_items:
            dm_user(i + new_items[i])
            # print('New Item Found: '+i)
