oauth-example-python
====================

This sample shows how to obtain a Bullhorn OAuth access token without having a browser and user in the loop.

Normally, A third-party application using Bullhorn OAuth would detect an un-authorized user and redirect the user's browser to Bullhorn's OAuth servers where the user would log in, then be redirected back to the third-party app.

Sometimes this flow is not possible, for example when the application is a scheduled job or anything else that either does not have a Web UI or needs to log in on behalf of a special user unattended.

The general strategy here is similar to the standard OAuth flow: obtain an access token, and from that obtain an authorization code.  Here, however, instead of sending the response from the access token request directly to a browser for redirection, we pull, in our code, the "Location" header off of the HTTP response from the access token request (this is the redirect).  This "Location" header contains a URL with a query string containing the access token.  Once we have this, we can turn around and make the request for an authorization code using the access token.

So instead of the browser propagating the access token from OAuth to our third-party app for us, we simply examine the HTTP response ourselves in code.
