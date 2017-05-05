import re
import time

import pickle

import praw
import prawcore.exceptions

from DynReddit import DynReddit

def get_table():
    table = table_markdown_tolist(wiki_supporters.find_content())

def update_subscriber_counts():
    name_column = 0
    subs_column = 2
    total_subreddit_count = 0
    total_subscriber_count = 0
    for i in table:
        if re.match(r'\/r\/\w+', i[name_column]):  # if table row is subreddit entry
            subscribers = None
            while True:
                try:
                    subscribers = praw_1.subreddit(re.search(r'(?:\/r\/)(\w+)', i[name_column]).group(1)).subscribers
                    total_subreddit_count += 1
                    total_subscriber_count += subscribers
                    print(i[name_column] + " " + str(subscribers))
                    break
                except (prawcore.exceptions.NotFound, prawcore.exceptions.Redirect) as InvalidURI:
                    time.sleep(3)
                    print(i[name_column] + " does not exist!")
                    subscribers = -1
                    break
                except (prawcore.exceptions.Forbidden, prawcore.exceptions.BadRequest) as InsufficientPerms:
                    time.sleep(3)
                    print(i[name_column] + " is not a subreddit or is locked away from you!              Error!")
                    subscribers = -0
                    break
            i[subs_column] = str(subscribers)


def table_markdownify(table):
    table_markdown = None
    for i in table:
        for j in i:
            table_markdown += '|' + j
            if i.index(j) + 1 >= len(i):
                table_markdown += '|\r\n'
    return table_markdown


def table_markdown_tolist(table_markdown):
    return [[j for j in i.split('|') if j] for i in re.split(r"(?:\r\n)+", table_markdown) if i]


def regex_column_index(pattern, table):
    for i in table:
        for j in i:
            if re.match(pattern, j):
                return i.index(j)
    return None

def load_wikitable():
    with open('wikitable') as f:
        temp = pickle.load('wikitable')
        table = temp[0]
        total_subreddit_count = temp[1]
        total_subscriber_count = temp[2]
        wikitable_timestamp = temp[3]

def save_wikitable():
    with open('wikitable', 'wb') as f:
        pickle.dump((table, total_subreddit_count, total_subscriber_count, wikitable_timestamp), f)

def table_add_entry(name, info):
    try:
        table.index('/r/' + name in)

def response(error):
    if error == 'comment_add':
        pass
    pass




praw_1 = praw.Reddit('bot1')

wiki_supporters = DynReddit(praw_1, 'MrnicunbtYonufoun1ss', 'wiki/test', 1)
table = None  # table_markdown_tolist(wiki_supporters.find_content())
total_subreddit_count = 0
total_subscriber_count = 0
wikitable_timestamp = time.time()

def comment_spin():
    pass

def post_spin():
    pass

def void():
    get_table()

void()