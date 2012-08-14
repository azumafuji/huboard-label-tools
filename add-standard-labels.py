import getpass
import json
from restkit import Resource, BasicAuth, Connection, request
from socketpool import ConnectionPool

# Color sequence from ColorBrewer http://colorbrewer2.org/
# Diverging 6 color BrBG scheme

DEFAULT_LABELS = (('0 - Backlog', '8C510A'),
                  ('1 - On Deck', 'D8B365'),
                  ('2 - Analysis', 'F6E8C3'),
                  ('3 - Developing', 'C7EAE5'),
                  ('4 - Acceptance', '5AB4AC'),
                  ('5 - Production Close', '01665E'),)

pool = ConnectionPool(factory=Connection)
serverurl="https://api.github.com"

msg = "This script will create the default labels %s in your specified " \
      "repository if they do not yet exist." % (', '.join(lab[0] for lab in DEFAULT_LABELS))
print msg

repo = raw_input("Repository: ")
usr = raw_input("Username: ")
pwd = getpass.getpass("Password: ")
# Add your username and password here, or prompt for them
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

resource = Resource('https://api.github.com/user/repos', pool=pool)
resource = Resource('https://api.github.com/orgs/lillyoi/repos', pool=pool)

resource = Resource('https://api.github.com/repos/%s/labels' % repo, pool=pool)
headers = {'Content-Type' : 'application/json' }
headers['Authorization'] = 'token %s' % token
response = resource.get(headers = headers)
labels = json.loads(response.body_string())
label_names = [n['name'] for n in labels]

for dl,color in DEFAULT_LABELS:
    payload = {"name": dl, "color": color}
    headers = {'Content-Type' : 'application/json' }
    headers['Authorization'] = 'token %s' % token

    if dl not in label_names:
        print "Adding %s" % dl
        resource = Resource('https://api.github.com/repos/%s/labels' % repo, pool=pool)
        response = resource.post(payload=json.dumps(payload), headers=headers)
    else:
        print "Updating colors for %s" % dl
        resource = Resource('https://api.github.com/repos/%s/labels/%s' % (repo, dl), pool=pool)
        response = resource.request('PATCH', payload=json.dumps(payload), headers=headers)



