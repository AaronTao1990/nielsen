import urllib2, urllib, json
import StringIO
import gzip
import logging

def uncompress(data):
    try:
        stream = StringIO.StringIO(data)
        gzipper = gzip.GzipFile(fileobj=stream)
        return gzipper.read()
    except Exception, e:
        print e

def api_request(url, headers, body=None, timeout=5, use_proxy=False, proxy_addr=None):
    opener = None
    if use_proxy:
        opener = urllib2.build_opener(urllib2.ProxyHandler({'http':proxy_addr}))
    else:
        opener = urllib2.build_opener(urllib2.BaseHandler())
    urllib2.install_opener(opener)

    #if body:
    #    if headers.get('Content-Type', None) == 'application/json':
    #        body = json.dumps(body)
    #    else:
    #        body = urllib.urlencode(body)
    request = urllib2.Request(url, body, headers)
    try:
        f = urllib2.urlopen(request, timeout=timeout)
        coding = f.info().get('Content-Encoding')
        if coding == 'gzip':
            result = uncompress(f.read())
        else:
            result = f.read()
    except Exception, e:
        import traceback
        logging.error('exception while trying to fetch url : %s, reason : %s' % (url, traceback.format_exc()))
        return None
    else:
        return result

def fetch_html(url, headers={}, body=None, timeout=10, retry_count=2, use_proxy=False, proxy_addr=None):
    for i in range(retry_count):
        resp = api_request(url, headers, body, timeout, use_proxy, proxy_addr)
        if resp:
            return resp
    return None

def main():
    #url = 'http://www.baidu.com'
    url = 'http://ic.snssdk.com/2/article/v31/stream/?iid=3569306836&ac=WIFI&os_version=9.2.1&aid=26&app_name=explore_article&channel=App%20Store&device_platform=iphone&idfa=44AA66F4-5CF3-4A89-9A6F-C1383DED9485&device_id=6776405896&vid=7E75BBB6-5A47-43FA-803E-A0CD8308D885&openudid=53fb0e7b6132c8406f8e5dad7cf5ecac09876e35&device_type=iPhone%206&abflag=1&idfv=7E75BBB6-5A47-43FA-803E-A0CD8308D885&ssmix=a&ab_version=&resolution=750*1334&ab_client=a1,b1,e1,f1&version_code=5.1.1&LBS_status=authroize&category=subv_funny&city=%E5%8C%97%E4%BA%AC&count=20&detail=1&image=1&last_refresh_sub_entrance_interval=1454556495&latitude=39.99682629305991&list_entrance=main_tab&loc_mode=1&loc_time=1454556272&longitude=116.3328902518888&min_behot_time=0'
    html = fetch_html(url)
    print html

if __name__ == "__main__":
    main()

