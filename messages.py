import urllib2
import json
import os

url = 'https://android.googleapis.com/gcm/send'
#Get an API KEY from Google and set it up into heroku environment variable
apiKey = os.environ['GCM_API_KEY']
myKey = "key=" + apiKey
#regid ='registraion_id'


class GCM():
    def send(self, registration, message ):
        # make header
        headers = {'Content-Type': 'application/json', 'Authorization': myKey}
        # make json data
        data = {}
        data['registration_ids'] = (registration,)
        data['data'] = {'data': message }
        json_dump = json.dumps(data)        
        # print json.dumps(data, indent=4)
        req = urllib2.Request(url, json_dump, headers)
        result = urllib2.urlopen(req).read()
        print result
        print json.dumps(result)
        
        return True
