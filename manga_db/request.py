# coding=utf-8
__author__ = 'BaiYa'

import urllib2
import time

def request(url, data=None):
    return urllib2.urlopen(url, data)

class DefaultErrorHandler(urllib2.HTTPDefaultErrorHandler):
    """用来保证请求中记录Http状态
    """
    def http_error_default(self, req, fp, code, msg, headers):
        result = urllib2.HTTPError(
			req.get_full_url(), code, msg, headers, fp)
        result.status = code
        return result

class Request(object):
    """a sample is the url i want to download
    """
    url = None
    contentLength = 0
    etag = None
    lastModified = None
    data = None
    path = None

    def __init__(self, url, contentLength=0, etag=None, lastModified=None):
        self.url = url
        self.contentLength = contentLength
        self.etag = etag
        self.lastModified = lastModified
        self.status = 200
        self.file = file

    def __repr__(self):
        return repr("Http Status=%s; Length=%s; Last Modified Time=%s; eTag=%s" % (self.status, self.contentLength, self.lastModified, self.etag))

    def request(self):
        request = urllib2.Request(self.url)
        # request.add_header('User-Agent', "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en)")
        if self.lastModified:
            request.add_header('If-Modified-Since', self.lastModified)
        if self.etag:
            request.add_header('If-None-Match', self.etag)
        self.requestTime = time.gmtime()
        conn = urllib2.build_opener(DefaultErrorHandler()).open(request)

        if hasattr(conn, 'headers'):
            print(conn.headers)
            # save ETag, if the server sent one
            self.etag = conn.headers.get('ETag')
            # save Last-Modified header, if the server sent one
            self.lastModified = conn.headers.get('Last-Modified')
            self.contentLength = conn.headers.get("content-length")

            if hasattr(conn, 'status'):
                self.status = conn.status
                print "status=%d" % self.status

            self.header = conn.headers
            self.data = conn.read()

        if (self.status == 304):
            print "the content is same, so return nothing!"

        if not self.contentLength:
            self.contentLength = len(self.data)

        conn.close()

if __name__ == '__main__':
    url = 'http://www.jide123.com/manhua/11784/285367.html'
    sample = Request(url)
    sample.request()
    print sample
    sample.request()
    print sample