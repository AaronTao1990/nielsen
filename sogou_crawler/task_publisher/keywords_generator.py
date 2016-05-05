from optparse import OptionParser
import redis
import logging

logger = logging.getLogger(__name__)

redis_config = {
    'host' : '10.111.0.12',
    'port' : 6380,
    'ntasks' : 'ntasks'
}


class KeywordsGenerator(object):

    def __init__(self, filename, target):
        self.redis_cli = redis.Redis(host=redis_config['host'], port = redis_config['port'])
        self.filename = filename
        self.target = target

    def __get_items(self):
        with open(self.filename, 'r') as f:
            for line in f.readlines():
                line = line.strip('\n')
                yield line

    def publish_tasks(self):
        try:
            for task in self.__get_items():
                self.redis_cli.sadd(self.target, task)
        except Exception, e:
            logger.error('exception : %s' % e)

def main(filename, target, args):
    generator = KeywordsGenerator(filename, target)
    generator.publish_tasks()

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-f', '--filename', dest='filename',
                      default='source.txt',
                      help='filename')
    parser.add_option('-t', '--target', dest='target',
                      default='ntasks',
                      help='target')
    (options, args) = parser.parse_args()
    main(options.filename, options.target, args)

