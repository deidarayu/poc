#!/usr/bin/env python
# coding=utf-8

import json
import sys
import urllib2

from lxml import etree

def get_api_url(wp_url):
    res = urllib2.urlopen(wp_url)
    data = etree.HTML(res.read())
    print data 
    u = data.xpath('//link[@rel = "https://api.w.org/"]/@href')[0]
     
    if 'rest_route' in u:
        print 'may not work!'
    return u

def get_posts(api_base):
    res = urllib2.urlopen(api_base + 'wp/v2/posts')
    posts = json.loads(res.read())

    for post in posts:
        print '- Post ID: {0}, Title: {1}, Url: {2}'.format(post['id'], post['title']['rendered'],post['link'])


def update_post(api_base, post_id, post_content):
    data = json.dumps({
        'content' : post_content
    })
    url = api_base + 'wp/v2/posts/{post_id}/?id={post_id}abc'.format(post_id = post_id)
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    res = urllib2.urlopen(req).read()
    
    print 'post update. Check it out at {0}'.format(json.loads(res)['link'])

def usage():
    print 'view blog'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    if 2 < len(sys.argv) < 4:
        print 'Please provide a file with post content with a post id'
        sys.exit(1)

    print 'discovering api endpoint'
    print sys.argv[1]
    api_url = get_api_url(sys.argv[1])
    print 'API lives at: {0}'.format(api_url)

    if len(sys.argv) < 3:
        print 'Getting available posts'
        get_posts(api_url)

        sys.exit(0)


    print 'updating post {0}'.format(sys.argv[2])
    with open(sys.argv[3], 'r') as content:
        new_content = content.readlines()

    update_post(api_url, sys.argv[2], ''.join(new_content))

    print 'update complete'



