import csv
import time
import os

import requests
import json
import random

import config

def get_request(main_video_id, root, pn):
    url = f'https://api.bilibili.com/x/v2/reply/reply?oid=' + main_video_id +'&type=1&root=' + root + \
          f'&ps=' + config.PAGE_COMMENTS_NUM + '&pn=' + str(pn) + \
          f'&web_location=333.788'
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        'cookie': config.COOKIE
    }
    try:
        rs = requests.get(url, headers=header)
    except:
        print("[Failed]Maybe have been blocked......")
        return
    datad = json.loads(rs.text)
    return datad


def get_all_sub_comments(main_video_id, main_comment_id, sub_comments_num):
    gotten_comments_num = 0
    cur_page = 1
    while gotten_comments_num < sub_comments_num:
        sleep_interval = random.random() * 10
        time.sleep(sleep_interval)
        if sleep_interval > 9.9:    # 1% sleep prevent blocking.
            time.sleep(60)  # Sleep 60s
        data = get_request(main_video_id, main_comment_id, cur_page)  # Get json
        for i in data['data']['replies']:
            comment_id = ''
            create_time = i['ctime']  # Comment creat time
            video_id = ''
            content = i['content']['message']  # Content
            print(content)  # Log content
            user_id = i['member']['mid']
            nickname = i['member']['uname']
            avatar = ''
            sub_comment_count = ''
            last_modify_ts = ''
            like_num = i['like']  # Like number
            at_user_lists = i['content']['members']
            at_users_nickname = ''
            if at_user_lists:
                for j in at_user_lists:
                    at_users_nickname = at_users_nickname + j['uname']
            with open(config.OUTPUT_CSV_NAME, "a", newline='', encoding='UTF8') as wr_csvfile:
                writer = csv.writer(wr_csvfile)
                writer.writerow([comment_id, create_time, video_id, content, user_id, nickname, avatar,
                                 sub_comment_count, last_modify_ts, like_num, at_users_nickname])
        cur_page = cur_page + 1
        gotten_comments_num = gotten_comments_num + int(config.PAGE_COMMENTS_NUM)


def read_csv_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as rd_file:
        next(rd_file)  # Skip header
        csv_reader = csv.reader(rd_file)
        for row in csv_reader:
            yield row
    rd_file.close()


def process_data(csv_file):
    for row in csv_file:
        [comment_id, create_time, video_id, content, user_id, nickname, avatar, sub_comment_count, last_modify_ts] = row
        with open(config.OUTPUT_CSV_NAME, "a", newline='', encoding='UTF8') as wr_csvfile:
            writer = csv.writer(wr_csvfile)
            writer.writerow([comment_id, create_time, video_id, content, user_id,
                             nickname, avatar, sub_comment_count, last_modify_ts])
        print('Current main comment:' + comment_id + ', with ' + sub_comment_count + ' sub comments.')
        if int(sub_comment_count) > 0:
            print('[' + comment_id + ']Start crawling...')
            get_all_sub_comments(video_id, comment_id, int(sub_comment_count))
            print('[' + comment_id + ']Crwal successfully.')


def sub_comment_crawler(input, output, cookie):

    if input == '' or not os.path.isfile(input):
        print('[Input]No such file or directory')
        return
    else:
        config.INPUT_CSV_NAME = input
    
    if cookie == '':
        print('No cookie.')
        return
    else:
        config.COOKIE = cookie
    
    if output == '':
        config.OUTPUT_CSV_NAME = config.INPUT_CSV_NAME.rstrip('.csv') + '_with_sub_comment.csv'
    else:
        config.OUTPUT_CSV_NAME = output

    # Write csv header
    with open(config.OUTPUT_CSV_NAME, "a", newline='', encoding='UTF8') as wr_file:
        wr_file.write('comment_id,create_time,video_id,content,'
                      'user_id,nickname,avatar,sub_comment_count,'
                      'last_modify_ts,like_num,at_users_nickname\n')
    wr_file.close()
    rd_csv_file = read_csv_file(config.INPUT_CSV_NAME)
    process_data(rd_csv_file)