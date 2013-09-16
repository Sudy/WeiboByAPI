#!/usr/bin/env python
#-*- coding:utf-8 -*-
import urllib
import base62
import threading  
import xmlrpclib
import json
import time


result_file = open("resultfile","w")

class WeiboThread(threading.Thread):
    #The timer class is derived from the class threading.Thread  
    def __init__(self,mutex):  
        threading.Thread.__init__(self)

        self.thread_stop = False
        self.access_token = "your access_token"
        #try up to five times to get a url seed
        self.base_url = "https://api.weibo.com/2/statuses/show_batch.json?access_token=" \
                    + self.access_token + "&ids="
        self.server = xmlrpclib.ServerProxy("http://192.168.3.48:8000")
        self.mutex = mutex
    

    def run(self):
        #when thereis not and stop
        while not self.thread_stop:
            url = self.base_url
            seeds = self.server.getSeed()
            print seeds
            if 0 == len(seeds):
                print "thread stop!"
                self.stop()
                continue

            for item in seeds:
                url += str(base62.url_to_mid(item.strip())) + ","
            self.get_weibo_by_id(url,0)
            time.sleep(3)


    def get_weibo_by_id(self,url,try_time):

        if try_time > 5:
            print "try url ",url,"for more than",try_time
            return
        
        weibo_json = ""        
        
        try:    
            raw_data = urllib.urlopen(url).read()
            weibo_json = json.loads(raw_data)
        except:
            time.sleep(5)
            self.get_weibo_by_id(url,try_time + 1)
            
        result = ""
        for status in weibo_json["statuses"]:
            try:
                if status.has_key("deleted"):
                    continue
                result +=  status['mid'] + "\t" + status["text"] + "\t" + str(status['user']['id']) + "\t" +\
                    status['user']['location'] + "\t" + status['created_at'] +'\n'
            except:
                continue 
        self.mutex.acquire()
        result_file.write(result.encode('utf8'))
        result_file.flush()
        self.mutex.release()
    def get_comment_by_weibo(self,weiboid):
        pass    
               
    
    def stop(self):
        self.thread_stop = True

if __name__ == '__main__':
    g_mutex = threading.Lock()
    for i in range(0,5):
        wThread = WeiboThread(g_mutex)
        wThread.start()
