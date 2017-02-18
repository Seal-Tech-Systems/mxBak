import csv
import re
from urllib import request
import ssl
import os
from .mxaudit import generate_info, write_info
from .mxbak import generate_backup
from .mxstill import generate_still

class Process(object):
    def __init__(self, opts):
        self._opts = opts
        self._input = self._get_input_data()
        if not os.path.exists(self._opts['output_dir']):
            os.makedirs(self._opts['output_dir'])
        if not os.path.exists(self._opts['images_dir']):
            os.makedirs(self._opts['images_dir'])
        if not os.path.exists(self._opts['configs_dir']):
            os.makedirs(self._opts['configs_dir'])
        output = self.process_list(self._input, self._opts)
        if self._opts['generateinfo']:
            write_info(output, self._opts['info_output_filename'])

    @property
    def opts(self):
        return self._opts

    def _get_input_data(self):
        result = []
        with open(self.opts['input']) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                r = {
                    'url': row['url'],
                    'login': row['login'],
                    'password': row['password'],
                }
                result.append(r)
        return result

    def process_list(self, l, opts):
        result = []
        for item in l:
            print('Processing %s' % item['url'])
            try:
                r = generate_info(item)
                result.append(r)
                print("Success: %s" % item['url'])

                if opts['backupstills']:
                    print('Backup still to %s' % self._opts['images_dir'])
                    x = self._opts['x']
                    y = self._opts['y']
                    q = self._opts['q']
                    generate_still(item, folder=self._opts['images_dir'], x=x, y=y, q=q)

                if opts['backupconfig']:
                    print('Backup still to %s' % self._opts['configs_dir'])
                    generate_backup(item, folder=self._opts['configs_dir'])
            except IOError as e:
                print("IO error '%s' while trying to process URL: %s" % (e, item['url']))
                result.append({'url': item['url'], 'status': 'IO ERROR: %s' % e})
            except BaseException as e:
                print("Unknown error '%s' while trying to process URL: %s" % (e, item['url']))
                raise e
        return result