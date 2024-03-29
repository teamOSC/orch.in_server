#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask, flask.views
app = flask.Flask(__name__)

from flask import render_template
from flask import request
import json,urllib2

@app.route('/api/<category>/<limit>')
def main(category,limit):
    url = 'http://www.reddit.com/r/%s/.json?limit=%s'%(category,limit)
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'readonly bot for orch.in website and app')]
    response = opener.open(url)

    arr = []

    jsondata = json.loads(response.read())
    for i in jsondata["data"]["children"]:
        f = i["data"]["url"]
        #if images
        if  f[-4:] in [".jpg",".png",".gif"]:
            d={}
            d['title'] = i["data"]["title"]
            d['type'] = 'image'
            d['url'] = f
            arr.append(d)
        elif "http://imgur.com/" in f:
            f = "http://i."+f.split('/')[2]+"/"+f.split('/')[3]+".jpg"
            d ={}
            d['title'] = i["data"]["title"]
            d['type'] = 'image'
            d['url'] = f
            arr.append(d)
            
        #youtube videos
        elif "youtube.com/watch" in f or "vimeo.com" in f:
            d = {}
            d['title'] = i["data"]["title"]
            d['url'] = f
            d['type'] = 'video'
            arr.append(d)

    return json.dumps(arr)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')

