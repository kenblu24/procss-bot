import re
import praw


class DynReddit:
    def __init__(self, praw_instance, subreddit, url, blockid):
        self.reddit = praw_instance
        self.subreddit = self.reddit.subreddit(subreddit)
        self.url = url
        self.blockid = blockid
        self.raw_content = None
        self.page = None
        self.content_type = None

        if re.match(r'wiki\/', self.url):
            self.content_type = 'wiki'
            self.page = re.sub(r'wiki\/', '', self.url)
            self.raw_content = self.subreddit.wiki[self.page].content_md

    def find_content(self):
        blockid = str(self.blockid)
        pattern = r"(?:\[\]\(#begin_dynamic\?" + blockid + "\))(.+)(?:\[\]\(#end_dynamic\?" + blockid + "\))"  # Find delineators
        result = re.search(pattern, self.raw_content, re.DOTALL)
        if result.group(1):
            return result.group(1)  # return the first group, which is the content between the tags.
        else:
            return None

    def replace_content(self, raw_content):
        blockid = str(self.blockid)
        pattern = r"(?:\[\]\(#begin_dynamic\?" + blockid + "\))(.+)(?:\[\]\(#end_dynamic\?" + blockid + "\))"
        self.raw_content = self.raw_content.replace(re.match(pattern, self.raw_content).group(1), raw_content)

    def send_content(self):
        pass


