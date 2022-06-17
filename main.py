# inspired by
# https://foosoft.net/projects/anki-connect/ 

import json
import urllib.request

kVERSION_NUMBER = 6
kREQUEST_LOCATION = 'http://localhost:8765'

def request(action, **params):
    return {'action': action, 'params': params, 'version': kVERSION_NUMBER}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request(kREQUEST_LOCATION, requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

