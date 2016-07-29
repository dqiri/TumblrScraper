#!/usr/bin/env python
import requests
import sys
import pickle
import os.path

API = "REDACTED Contact me for details"

class TS(object):
    """TumblrScrape
    Using a random API on the internet (REDACTED)
    --- A tumblr slideshow maker --- I was able to find out how it
    worked and how it got the convoluted Tumblr URL. This class will
    create the basic data structure to get the URL, the image, and make
    it so that it can be updated using pickle structures
    @assert blog will have static posts or there will be unexpected behavior
    such as mismatched posts. I mean if someone goes and deletes a post,
    it would cause some trouble."""
    def __init__(self, blogURI):
        """Initializes the class
        @param blogURI str the tumblr site you want to scrape,
            e.g. <blogURI>.tumblr.com"""
        self.blogURI = blogURI
        self.downloaded = []
        self.queue = []
        if os.path.isfile("{}.scrapedata".format(blogURI)):
            """Use pickle to unpack file"""
            self._pickleLoad()
            self.update()

    def _getPost(self, URI):
        print("hello")
        return URL.split('/')[4]

    def _pickleLoad(self):
        with open("{}.scrapedata".format(self.blogURI), "rb") as f:
            self.downloaded, self.queue = pickle.load(f)

    def _pickleSave(self):
        with open("{}.scrapedata".format(self.blogURI), "wb") as f:
            pickle.dump([self.downloaded, self.queue])

    def update(self):
        #self.fillQueue()
        postNum = len(self.downloaded)
        for i in self.queue[::-1]:
            fileType = i['imgurl'].split('.')[-1]
            filename = "{0:05d}_{1}.{2}".format(postNum, self.blogURI, fileType)
            print(filename, i['imgurl'])
            postNum += 1
            with open(filename, 'wb') as f:
                r = requests.get(i['imgurl'])
                print("Saving",i['imgurl'],filename)
                f.write(r.content)
            self.downloaded.append(i)
        self.queue = []
        self._pickleSave()

    def fillQueue(self):
        if self.downloaded:
            lastPost = self.downloaded[0]['posturl']
        else:
            lastPost = None
        currOffset = 0
        while True:
            r = requests.post(API.format(self.blogURI, currOffset))
            if len(r.json()) == 0:
                break
            for i in r.json():
                if i['posturl'] == lastPost:
                    break
                else:
                    self.queue.append(i)
            else:
                currOffset += 20
                continue
            break
        self._pickleSave()

    def fillQueueFirstTime(self):
        currOffset = 0
        print("Posting",API.format(self.blogURI, currOffset))
        r = requests.post(API.format(self.blogURI, currOffset))
        prevPost = None
        for i in r.json():
            postURL = i['posturl']
            #print(postURL, i['imgurl'])
            if not prevPost or prevPost != postURL:
                prevPost = postURL
                currOffset += 1
            self.queue.append(i)
        print currOffset
        while len(r.json()) > 0:
            print("Posting",API.format(self.blogURI, currOffset))
            r = requests.post(API.format(self.blogURI, currOffset))
            for i in r.json():
                postURL = i['posturl']
                #print(postURL, i['imgurl'])
                if not prevPost or prevPost != postURL:
                    prevPost = postURL
                    currOffset += 1
                self.queue.append(i)
            print currOffset
        self._pickleSave()
