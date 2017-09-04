'''
'''

import json

class Params(object):

    def __init__(self, data={}):
        self.data = data

    def __str__(self):
        return json.dumps(self.data, indent=2)

    def add(self, data, key):
        if key not in self.data:
            self.data[key] = {'byId': {}, 'allIds': []}

        pk = '{}'.format(data['id'])

        self.data[key]['byId'][pk] = data
        if pk not in self.data[key]['allIds']:
            self.data[key]['allIds'].append(pk)

    def get_conf(self, id_conf=None, dtype=None):
        if id_conf is not None:
            return self.data['configurations']['byId'][id_conf]
        elif dtype:
            for id_conf in self.data['configurations']['byId']:
                if self.data['configurations']['byId'][id_conf]['device_type'] == dtype:
                    return self.data['configurations']['byId'][id_conf]
        return {}

    def get_exp(self, id_exp=None):
        if id_exp is not None:
            return self.data['experiments']['byId'][id_exp]
        return {}

    def get_camp(self, id_camp):
        if id_camp is not None:
            return self.data['campaings']['byId'][id_camp]
        return {}
