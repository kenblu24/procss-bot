import praw
import prawcore.exceptions
import time
import re
import json

me = praw.Reddit('bot1')

def updateSubCount():
    targetsub = me.subreddit('MrnicunbtYonufoun1ss')
    targetpage = 'test'
    target = targetsub.wiki[targetpage]

    content = target.content_md

    tableMD = findContent(content, 1)
    table = tableMD_toList(tableMD)

    open('tablemd.txt','a').write('\r\n' + tableMD)

    # Updates subscriber counts for each valid subreddit in the table

    nomcol = colIndex(r'\/r\/\w+', table)  # find column with subreddit names
    cntcol = colIndex(r'-?(?:\d|,)+', table) # find column with subreddit subscribers
    subcount = 0
    for i in table:
        if re.match(r'\/r\/\w+',i[nomcol]): # if table row is subreddit entry
            subscribers = None
            while True:
                try:
                    subscribers = me.subreddit(re.search(r'(?:\/r\/)(\w+)',i[nomcol]).group(1)).subscribers
                    subcount+=1
                    print(i[nomcol])
                    break
                except (prawcore.exceptions.NotFound, prawcore.exceptions.Redirect) as InvalidURI:
                    time.sleep(3)
                    print(i[nomcol] + " does not exist!")
                    subscribers = -1
                    break
                except (prawcore.exceptions.Forbidden, prawcore.exceptions.BadRequest) as InsufficientPerms:
                    time.sleep(3)
                    print(i[nomcol] + " is not a subreddit or is locked away from you!")
                    subscribers = -0
                    break
            i[cntcol] = subscribers

    # Write table to md formatted table
    tableMD_updated = ''
    for i in table:
        for j in i:
            tableMD_updated += '|' + j
            if i.index(j) + 1 >= len(i):
                tableMD_updated += '|\r\n'
    open('tablemdupdated.txt','a').write('\r\n' + tableMD_updated)





def findContent(contentMD,id):
    id = str(id)
    pattern = r"(?:\[\]\(#begin_dynamic\?" + id + "\))(.+)(?:\[\]\(#end_dynamic\?" + id + "\))" #for id is an integer, matches between:    [](#begin_dynamic?id)   content   ()[#end_dynamic?id]
    result = re.search(pattern, contentMD, re.DOTALL)
    if result.group(1):
        return result.group(1) # return the first group, which is the content between your tags.
    else:
        return None

def tableMD_toList(tableMD):
    return [[j for j in i.split('|') if j] for i in re.split(r"(?:\r\n)+", tableMD) if i]



def colIndex(pattern, table):
    for i in table:
        for j in i:
            if re.match(pattern, j):
                return i.index(j)
    return None

updateSubCount()