import urllib, urllib2, urlparse

# This sample shows how to obtain a Bullhorn OAuth access token
# without the user/browser flow.  This style of OAuth authentication
# can be used when building scheduled jobs or other code that needs
# to log in without user intervention.

# Change the values for the following global variables to test out
# this code.  Code can then be run directly, e.g.:
# [user@host]: python oauth_example.py

# Bullhorn OAuth client ID
client_id = "client_id_here"
# Bullhorn OAuth secret
client_secret = 'client_secret_here'
# Bullhorn OAuth service endpoint.  Don't forget to change
# host to auth9 if using a sandbox environment
base_url = 'https://auth.bullhornstaffing.com/oauth'
# put login credentials here
username = ""
password = ""

class AuthCodeRedirectHandler(urllib2.HTTPRedirectHandler):
    """
    A bare bones redirect handler that pulls the auth code sent back
    by OAuth off the query string of the redirect URI given in the
    Location header.  Does no checking for other errors or bad/missing
    information.
    """
    def http_error_302(self, req, fp, code, msg, headers):
        """handler for 302 responses that assumes a properly constructed
        OAuth 302 response and pulls the auth code out of the header"""
        qs = urlparse.urlparse(headers["Location"]).query
        print(qs)
        auth_code = urlparse.parse_qs(qs)['code'][0]
        return auth_code

def build_auth_code_request(username, password):
    auth_data = urllib.urlencode({
        "client_id": client_id,
        "response_type": "code",
        "username": username,
        "password": password,
        "action": "Login"
    })
  
    req = urllib2.Request(url=base_url + "/authorize", data=auth_data)
    return req


def get_access_token(code):
    """
    Gets an OAuth access token given an OAuth authorization code
    """
    access_token_params = urllib.urlencode({
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code
    })
    
    req = urllib2.Request(base_url + '/token', access_token_params)
    f = urllib2.urlopen(req)
    return f.read()


if __name__ == "__main__":
    req = build_auth_code_request(username, password)
    opener = urllib2.build_opener(AuthCodeRedirectHandler)

    auth_code = opener.open(req) 
    print(auth_code)

    access_token = get_access_token(auth_code)

    print(access_token)