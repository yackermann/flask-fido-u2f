Flask-FIDO-U2F 
==============

Implements easy to use U2F managing plugin

## Arguments:

`app`:
 * (Flask) - A Flask application

`enroll_route`:
 * (String) - A route for device enrollment

`sign_route`:
 * (String) - A route for device verification(signature)

`devices_route`:
 * (String) - A route for device management(View, Deletion)

`facets_route`:
 * (String) - A route for FIDO Facets 
    

## Session variables:

`session['u2f_enroll_authorized']:`
 * (Boolean) - A session variable that enables access to Enrollment API.

`session['u2f_sign_required']:`
 * (Boolean) - A session variable that enables access to Verification API.

`session['u2f_allow_device_management']:`
 * (Boolean) - A session variable that enables access to Device management API


## Flask application config variables:

`app.config['U2F_APPID']`

 + (String) - A configuration key that holds application ID. 

 * MAKE SURE NO TRAILING SLASHES IN THE APPID!!!!!

 * Additional info.

    + "The AppIDis a URL carried as part of the protocol message sent by the server and indicates the target for this credential.

 * For more information, refer to page 3 of https://fidoalliance.org/specs/fido-appid-and-facets-ps-20150514.pdf

`app.config['U2F_FACETS_ENABLED']`

 * (Boolean) - A configuration key that enables FIDO U2F support. If enabled, U2F_FACETS_LIST must be set.

`app.config['U2F_FACETS_LIST']`

 + (List) - Defines a list of FIDO application facets. For example Google facets:

    ```javascript
    [
      "https://accounts.google.com",
      "https://myaccount.google.com",
      "https://security.google.com",
      "android:apk-key-hash:FD18FA800DD00C0D9D7724328B6...",
      "android:apk-key-hash:Rj6gA3QDA2ddyQyi21JXly6gw9...",
      "ios:bundle-id:com.google.SecurityKey.dogfood"
    ]
    ```
 + For more information, refer to page 5 of https://fidoalliance.org/specs/fido-appid-and-facets-ps-20150514.pdf