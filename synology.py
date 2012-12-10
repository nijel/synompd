import urllib
import urllib2
import urlparse
import httplib
import cookielib
import json

class SynoBase(object):
    def __init__(self, username, password, host, port = 8800, protocol = 'http'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.protocol = protocol
        self.cj = cookielib.CookieJar()
        self.processor = urllib2.HTTPCookieProcessor(self.cj)
        self.opener = urllib2.build_opener(self.processor)
        self.opener.addheaders = [('User-agent', 'Python-Synology')]

    def request(self, path, **kwargs):
        url = '%s://%s:%s/%s' % (
            self.protocol,
            self.host,
            self.port,
            path
        )
        if len(kwargs) > 0:
            params = urllib.urlencode(kwargs)
        else:
            params = None
        return self.opener.open(url, params)

    def request_json(self, path, **kwargs):
        response = self.request(path, **kwargs)
        return json.load(response)

    def login(self):
        response = self.request_json(
            'webman/login.cgi',
            username = self.username,
            passwd = self.password
        )
        return response['success']

class AudioStation(SynoBase):
    pass

if __name__ == '__main__':
    import sys
    syno = AudioStation(sys.argv[1], sys.argv[2], 'localhost')
    if not syno.login():
        print 'Failed login'
        sys.exit(1)

