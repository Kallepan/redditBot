import praw
import pandas as pd
import os
import requests
import re

class RedditBot:
    # config_interpolation --> Dataset to be loaded from praw.ini
    def __init__(self, botID, config_interpolation):
        # constants
        self.limitForPosts = 50
        self.loadSubreddits()
        self.cwd = os.getcwd()
        self.topLimit = "day"
        # bot instance
        self.fetch_args();

        self.bot = praw.Reddit(botID, config_interpolation = config_interpolation)
        #self.bot.read_only = True
        
        print("Authenticated with: ", self.bot.user.me())

    def fetch_args(self):
        while True:
            try:
                limit_posts = int(input("Enter the amount of posts to fetch: "));
                self.limitForPosts = limit_posts;
                break;
            except:
                print("invalid entry!");
        while True:
            print("Enter the timeframe you want to look at")
            print("valid: 'day', 'week', 'month', 'year'")
            top_limit = input("Input: ")
            if(top_limit == "day" or top_limit == "week" or top_limit == "month" or top_limit == "year"):
                self.topLimit = top_limit;
                break;
        print("starting bot")

    def loadSubreddits(self):
        self.subreddits = []
        subredditsDF = pd.read_csv('subreddits.csv', sep = ";")
        for subreddit in subredditsDF['subreddits']:
            self.subreddits.append(subreddit)
        print("Loaded Subreddits");
    
    def fetchData(self):
        try:
            os.mkdir("pulls")
        except FileExistsError:
            pass;
        os.chdir("pulls")

        for subreddit in self.subreddits:
            cwd = os.getcwd()
            try:
                os.mkdir(str(subreddit))
                os.chdir(subreddit)
            except FileExistsError:
                os.chdir(subreddit)
            subreddit = self.bot.subreddit(subreddit)
            for post in subreddit.top(self.topLimit, limit = self.limitForPosts):
                if(".jpg" in post.url):
                    self.downloadImage(".jpg", post.url)
                else:
                    continue
            os.chdir(cwd)
            print(subreddit, " fetched...")
        os.chdir(self.cwd)
        print("Fetched Data")
        
    def downloadImage(self, ending, url):
        fileName = url.split("/")
        if(len(fileName) == 0):
            fileName = re.findall("/(.*?)", url)
        fileName = fileName[-1]
        if "." not in fileName:
            fileName += ending
        print("Downloaded: ", fileName)
        response = requests.get(url)
        with open(fileName, "wb") as file:
            file.write(response.content)

def main():
    reddit = RedditBot('BOT', 'basic')
    reddit.fetchData()

main()
#splitaudios();

