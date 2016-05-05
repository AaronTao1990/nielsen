import json
from netcall import fetch_html
from scrapy.selector import Selector
from htmlutils import remove_tags
from optparse import OptionParser
import time


def get_proxy():
    ips = []
    def get_new_ips():
        api = 'http://api.zdaye.com/?api=201605051157596943&pw=123&checktime=1%D0%A1%CA%B1%C4%DA&gb=2'
        resp = fetch_html(api)
        for line in resp.split('\n'):
            ips.append('http://' + line)
    if not ips:
        get_new_ips()
    ip = ips[0]
    del ips[0]
    return ip

def load_tasks(filename):
    with open(filename, 'r') as f:
        for line in f.readlines():
            yield json.loads(line.strip('\n'))

def get_content(task, proxy):
    HEADERS = {
        'Host' : 'travel.qunar.com',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate, sdch',
        'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2',
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
    }

    try:
        response = None
        proxy = get_proxy()
        response = fetch_html(task['url'], headers=HEADERS, use_proxy=True, proxy_addr=proxy)
        #if proxy == 'no':
        #    response = fetch_html(task['url'], headers=HEADERS)
        #else:
        #    response = fetch_html(task['url'], headers=HEADERS, use_proxy=True, proxy_addr=proxy)
        selector = Selector(text=response)
        forward = ''.join(selector.xpath('//div[@id="b_foreword"]/node()').extract())
        scheduler = ''.join(selector.xpath('//div[@id="b_panel_schedule"]/node()').extract())
        content = remove_tags(forward+scheduler)
        if not content or len(content) == 0:
            content = remove_tags(''.join(selector.xpath('//div[@class="b_schedule"]/node()').extract()))
        if not content or len(content) ==0:
            return 'failed', content
        else:
            return 'success', content
    except Exception:
        return 'failed', ''



def main(filename, s_filename, f_filename, interval, proxy):
    s_f = open(s_filename, 'a')
    f_f = open(f_filename, 'a')
    for task in load_tasks(filename):
        status, content = get_content(task, proxy)
        if status == 'success':
            task['content'] = content
            s_f.write(json.dumps(task, ensure_ascii=False).encode('utf-8') + '\n')
        else:
            f_f.write(json.dumps(task, ensure_ascii=False).encode('utf-8') + '\n')
        time.sleep(int(interval))

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-o', '--orgin', dest='origin',
                      default='origin.txt',
                      help='source filename')
    parser.add_option('-s', '--success_filename', dest='s_filename',
                      default='success.txt',
                      help='success filename')
    parser.add_option('-f', '--failed_filename', dest='f_filename',
                      default='failed.txt',
                      help='failed filename')
    parser.add_option('-i', '--interval', dest='interval',
                      default='3',
                      help='interval')
    parser.add_option('-p', '--proxy', dest='proxy',
                      default='no',
                      help='proxy')
    (options, args) = parser.parse_args()
    main(options.origin, options.s_filename, options.f_filename, options.interval, options.proxy)
