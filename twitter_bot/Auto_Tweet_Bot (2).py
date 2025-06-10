import tweepy
from datetime import datetime
import requests
import os,csv
from time import sleep,time


Google_Sheer_URL = "https://docs.google.com/spreadsheets/d/1Fb0CwN-4avNZDQG7xXUMdQiGPnMNtVO3mrKrzfSQioE/edit#gid=0"

def get_tweepy_client_api():
    consumer_key = 'udsVDgJBZAasdsfp2MBjGn7xBM'
    consumer_secret = 'FckPZLrF7YkDPasdfgrwED0rZV6OJQiZb1BqEd2GU97BBHdW2'
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAK1pwgEAAAdfBKwR%2Fz%2B6r%2F5%2F2iBU%2BJz7tKJ0KfY%3DEpGzDgfdfTwh82gEKWGIy06qrZ6f26ot8sTL8ht9PifVStHOpwZ"
    access_token = '1666140507389698048-mr4KkC9iXoM1WVldfgdfgvb1VNhDby'
    access_token_secret = 'qGobYv3dfgKVY6wpQ1AgIltUEDugX9XdYhhNAbZbxzuE'
    client = tweepy.Client(bearer_token,consumer_key,consumer_secret,access_token,access_token_secret)
    return client


def get_sheet_data(sheet_url):
    url_1 = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
    res = requests.get(url_1)
    with open('file.csv','w+',encoding='utf-8')as f:
        f.write(res.text)
        f.seek(0)
        a=list(csv.DictReader(f,delimiter=','))

    os.remove('file.csv')
    return a

def main():
    data = get_sheet_data(Google_Sheer_URL)
    client = get_tweepy_client_api()

    with open('row.txt','r') as fp:
        row_num = int(fp.read().strip())-1
    row = data[row_num]
    text=row['Tweets'][:279]


    if not text:
        return False
    res = client.create_tweet(text=row['Tweets'][:279])
    with open('row.txt','w') as fp:
        fp.write(str(row_num+2))
    if not res.errors:
        return True
    else:
        print(res.errors)

def get_last_tweet_time():
    try:
        with open("last_tweet_time.txt", "r") as file:
            last_tweet_time = float(file.read())
            return last_tweet_time
    except FileNotFoundError:
        return None

if __name__ == "__main__":
    while True:
        try:
            with open('delay_between_tweets.txt','r') as file:
                delay = int(file.read())
        except FileNotFoundError:
            delay = 85


        last_tweet_time= get_last_tweet_time()
        if (last_tweet_time is None) or (float(time() - last_tweet_time) >= float(delay*60)):
            try:
                r = main()
                if r:
                    print('successfully tweeted\n')
                elif r is None:
                    pass
                else:
                    with open('row.txt','r') as fp:
                        row_num = int(fp.read().strip())-1
                    print(f'please check row number {row_num} bot did not find any text there')
            except Exception as e:
                print('something went wrong')
                print(e)
        sleep(60)
