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
        params = urllib.urlencode(kwargs)
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
    def request_as(self, path, **kwargs):
        return self.request_json('webman/3rdparty/AudioStation/webUI/%s' % path, **kwargs)

    def audio(self):
        return self.request_as('audio.cgi')

    def browse_audio(self, target = 'musiclib_root', server = 'musiclib_root'):
        '''
        Basic method for audio browsing.

        server - musiclib_root for files or musiclib_music_aa for data
        target - musiclib_music_file for files, musiclib_music_aa for data

        '''
        return self.request_as(
            'audio_browse.cgi',
            action = 'browse',
            target = target,
            server = server,
            category = '',
            keyword = '',
            start = 0,
            sort = 'title',
            dir = 'ASC',
            limit = 100,
        )

if __name__ == '__main__':
    import sys
    syno = AudioStation(sys.argv[1], sys.argv[2], 'localhost')
    if not syno.login():
        print 'Failed login'
        sys.exit(1)
    print syno.browse_audio()

