# coding=utf-8
__author__ = 'BaiYa'

import urllib2
import time
from DBStore import *
import Logger

def request(url):
    Logger.info(str('request start url: %s' % url))
    query_request = session.query(Request).filter(Request.url==url).first()
    last_modified = None
    etag = None
    if query_request:
        last_modified = query_request.last_modified
        etag = query_request.etag

    httpRequest = HttpRequest(url=url, lastModified=last_modified, etag=etag)
    httpRequest.request()

    if httpRequest.status == 304:
        pass
    elif httpRequest.status != 200:
        pass
    else:
        last_modified = httpRequest.lastModified
        etag = httpRequest.etag
        if query_request:
            query_request.last_modified = last_modified
            query_request.etag = etag
        else:
            query_request = Request(url=url, etag=etag, last_modified=last_modified)
            session.add(query_request)

        session.commit()
    Logger.info(str('request status: %d' % httpRequest.status))
    Logger.info(str('request stop url: %s' % url))
    return httpRequest


class DefaultErrorHandler(urllib2.HTTPDefaultErrorHandler):
    """用来保证请求中记录Http状态
    """
    def http_error_default(self, req, fp, code, msg, headers):
        result = urllib2.HTTPError(
			req.get_full_url(), code, msg, headers, fp)
        result.status = code
        return result

class HttpRequest(object):
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
            # print(conn.headers)
            # save ETag, if the server sent one
            self.etag = conn.headers.get('ETag')
            # save Last-Modified header, if the server sent one
            self.lastModified = conn.headers.get('Last-Modified')
            self.contentLength = conn.headers.get("content-length")

            if hasattr(conn, 'status'):
                self.status = conn.status

            self.header = conn.headers
            self.data = conn.read()

        if (self.status == 304):
            pass

        if not self.contentLength:
            self.contentLength = len(self.data)

        conn.close()

if __name__ == '__main__':
    url = 'http://www.jide123.com/manhua/11784/285367.html'
    sample = HttpRequest(url)
    sample.request()
    print sample
    sample.request()
    print sample