#!/usr/bin/env python
import requests
import sys
import pickle
import os.path
import time

API = "REDACTED"

class TS(object):
    """TumblrScrape
    Using a random API on the internet REDACTED
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
        #self.update()

    def _getPost(self, URI):
        return URL.split('/')[4]

    def _pickleLoad(self):
        with open("{}.scrapedata".format(self.blogURI), "rb") as f:
            self.downloaded, self.queue = pickle.load(f)

    def _pickleSave(self):
        try:
            with open("{}.scrapedata".format(self.blogURI), "wb") as f:
                pickle.dump([self.downloaded, self.queue], f)
        except KeyboardInterrupt:
            with open("{}.scrapedata".format(self.blogURI), "wb") as f:
                pickle.dump([self.downloaded, self.queue], f)
            print("Interrupted!")
            sys.exit()

    def update(self):
        postNum = len(self.downloaded)
        if not self.queue:
            self.fillQueue()
        if not self.queue:
            print "Already Updated!"
            print "Current post is {}".format(len(self.downloaded) - 1)
            return
        totalLen = len(self.queue)
        for i in self.queue[::-1]:
            fileType = i['imgurl'].split('.')[-1]
            filename = "{0:05d}_{1}.{2}".format(postNum, self.blogURI, fileType)
            print("Saving {} @ {}".format(filename, i['imgurl'])),
            postNum += 1
            try:
                with open(filename, 'wb') as f:
                    r = requests.get(i['imgurl'])
                    f.write(r.content)
                    print(" OK!")
            except KeyboardInterrupt:
                with open(filename, 'wb') as f:
                    r = requests.get(i['imgurl'])
                    f.write(r.content)
                    print(" OK!")
                self.downloaded.append(i)
                self.queue.pop()
                self._pickleSave()
                print("Interrupted!")
                sys.exit()

            self.downloaded.append(i)
            self.queue.pop()
            self._pickleSave()
        self._pickleSave()
        assert(len(self.queue) == 0)

    def fillQueue(self):
        print "Filling Queue"
        if self.downloaded:
            lastPost = self.downloaded[-1]['posturl']
        else:
            lastPost = None
        currOffset = 0
        while True:
            print("Fill is at {}".format(len(self.queue)))
            r = requests.post(API.format(self.blogURI, currOffset))
            if len(r.json()) == 0:
                break
            for i in r.json():
                #print i['posturl']
                #print lastPost
                if i['posturl'] == lastPost:
                    break
                else:
                    self.queue.append(i)
            else:
                currOffset += 20
                continue
            break
        self._pickleSave()

def main():
    if len(sys.argv) != 2:
        print("Usage: python {} <tumblrblogtitle>", sys.argv[0])
        return

    x = TS(sys.argv[1])
    x.update()

if __name__ == '__main__':
    main()
