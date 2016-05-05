import re
import HTMLParser

TAG_RE = re.compile(r'<[^>]+>')

def decodehtml(text):
    h= HTMLParser.HTMLParser()
    return h.unescape(text)

def remove_tags(text):
    result = TAG_RE.sub('', text)
    return decodehtml(result)

def main():
    temp = '<html>afdsf</html>'
    print remove_tags(temp)

if __name__ == '__main__':
    main()
