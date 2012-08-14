import getpass
import json
import itertools
from restkit import Resource, BasicAuth, Connection, request
from socketpool import ConnectionPool

# Color sequence generated from HSB (140,30,100) to HSB (359,30,100) in a
# radial clock-wise direction on color wheel with constant S and B, 16 steps

DEFAULT_LINK_COLORS = ('b2ffcc',
                       'b2ffeb',
                       'b2f1ff',
                       'b2e4ff',
                       'b2dcff',
                       'b2d3ff',
                       'b2c5ff',
                       'b2b6ff',
                       'bcb2ff',
                       'c9b1ff',
                       'd6b1ff',
                       'e3b1ff',
                       'f6b1ff',
                       'ffb1f4',
                       'ffb1e2',
                       'ffb1ce',
                       'ffb1bc',
                       'ffb1b3')

color_cycle = itertools.cycle(DEFAULT_LINK_COLORS)

pool = ConnectionPool(factory=Connection)
serverurl="https://api.github.com"

msg = "This script will update the Link issue colors in a repository for use" \
      "with Huboard. Labels that start with Link will be updated."
print msg

repo = raw_input("Repository: ")
usr = raw_input("Username: ")
pwd = getpass.getpass("Password: ")
auth=BasicAuth(usr, pwd)

# Use your basic auth to request a token
# This is just an example from http://developer.github.com/v3/
authreqdata = { "scopes": [ "repo" ], "note": "admin script" }
resource = Resource('https://api.github.com/authorizations',
    pool=pool, filters=[auth])
response = resource.post(headers={ "Content-Type": "application/json" },
    payload=json.dumps(authreqdata))
token = json.loads(response.body_string())['token']


#Once you have a token, you can pass that in the Authorization header
#You can store this in a cache and throw away the user/password
#This is just an example query.  See http://developer.github.com/v3/
#for more about the url structure


resource = Resource('https://api.github.com/repos/%s/labels' % repo, pool=pool)
headers = {'Content-Type' : 'application/json' }
headers['Authorization'] = 'token %s' % token
response = resource.get(headers = headers)
labels = json.loads(response.body_string())
label_names = [n['name'] for n in labels]

for name in label_names:
    if name.startswith('Link <=> '):
        print "Updating Link %s" % name
        payload = {"name": name, "color": color_cycle.next() }
        print payload
        headers = {'Content-Type' : 'application/json' }
        headers['Authorization'] = 'token %s' % token
        resource = Resource('https://api.github.com/repos/%s/labels/%s' % (repo, name), pool=pool)
        response = resource.request('PATCH', payload=json.dumps(payload), headers=headers)




