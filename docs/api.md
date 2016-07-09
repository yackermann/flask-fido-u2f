**Post API Documentation**
---

* **Enroll**
    * [Get enroll](#get-enroll)
    * [Verify enroll](#verify-enroll)

* **Sign**
    * [Get challenge](#get-challenge)
    * [Verify signature](#verify-signature)

Enroll
___

**Gets enroll**
----
Get U2F enroll seed

* **URL**

    * `/enroll`

* **Method:**

     * `GET`
    
*  **URL Params**

    * None

* **Data Params**

    * None

* **Success Response:**

    * **Code:** 200 OK

        ```javascript
        {
            authenticateRequests: [], 
            registerRequests: [
                {
                    appId:     "https://example.com", 
                    challenge: "5STI1s4eaOcMnqqmqYWm5RrprZa6iW4XtoxCDyuZma4", 
                    version:   "U2F_V2"
                }
            ]
        }
        ```
 
* **Error Response:**

    * **Code:** 401 UNAUTHORIZED

        ```javascript
        {
            status : "failed", 
            error  : "Unauthorized!"
        }
        ```

* **Sample Call:**

    ```javascript
        fetch('/enroll', {
            method  : 'GET',
            credentials : 'same-origin',
            headers : {
                'Accept'       : 'application/json',
                'Content-Type' : 'application/json'
            }
        }).then(function (response) {
            return response.json();
        }).then(function (response) {
            var enroll = response.registerRequests;
            var sign   = response.authenticateRequests;
            // Getting AppID
            var appid = enroll[0].appId;
           
            // Formating Challenge
            u2f.register(appid, enroll, sign, function(deviceResponse) {
                console.log(deviceResponse)
            })
        }).catch(function (err) {
            console.log({ 'status': 'failed', 'error': err });
        })
    ```


**Verify enroll**
----
Verifies U2F enroll

* **URL**

    * `/enroll`

* **Method:**

     * `POST`
    
*  **URL Params**

    * None

* **Data Params**

    ```javascript
    {
        registrationData : "BQR2ihOxMrhGyzeI6gmzO3jw1KbstHRlwTqBYptJ...",
        challenge        : "GHMvJOZKv-BPHULgS8kajjWIzztYfCxTYmOR0bwA...",
        clientData       : "eyJ0eXAiOiJuYXZpZ2F0b3IuaWQuZmluaXNoRW5y..."
        appId            : "https://example.com", 
        version          : "U2F_V2", 
    }
    ```

* **Success Response:**

    * **Code:** 201 CREATED

        ```javascript
        {
            status  : "ok", 
            message : "Successfully enrolled new U2F device!"
        }
        ```
 
* **Error Response:**

    * **Code:** 400 BAD REQUEST
        ```javascript
        {
            status :"failed", 
            error  :"Invalid key handle!"
        }
        ```
    
    * **Code:** 401 UNAUTHORIZED
        ```javascript
        {
            status : "failed", 
            error  : "Unauthorized!"
        }
        ```

* **Sample Call:**
    ```javascript
        fetch('/enroll', {
            method  : 'GET',
            credentials : 'same-origin',
            headers : {
                'Accept'       : 'application/json',
                'Content-Type' : 'application/json'
            }
        }).then(function (response) {
            return response.json();
        }).then(function (response) {
            var enroll = response.registerRequests;
            var sign   = response.authenticateRequests;
            // Getting AppID
            var appid = enroll[0].appId;
           
            // Formating Challenge
            u2f.register(appid, enroll, sign, function(deviceResponse) {
                fetch('/enroll', {
                    method  : 'POST',
                    credentials : 'same-origin',
                    body : JSON.stringify(deviceResponse),
                    headers : {
                        'Accept'       : 'application/json',
                        'Content-Type' : 'application/json'
                    }
                }).then(function (response) {
                    return response.json();
                }).then(function (response) {
                    console.log(response);
                }).catch(function (err) {
                    console.log({ 'status': 'failed', 'error': err });
                })
            })
        }).catch(function (err) {
            console.log({ 'status': 'failed', 'error': err });
        })
    ```

Sign
---

**Get challenge**
----
Gets U2F signature challenge

* **URL**

    * `/sign`

* **Method:**

     * `GET`
    
*  **URL Params**

    * None

* **Data Params**

    * None

* **Success Response:**

    * **Code:** 200 OK

        ```javascript
        {
            authenticateRequests: [
                {
                    challenge : "YYuWW3wJIBqUl-T-Xh1KhtxdE7wtG7lFNEG...", 
                    keyHandle : "Jo_q_IxHKq5AzEheueRVrzltnVDOqjbGD2Z...",
                    appId     : "https://example.com", 
                    version   : "U2F_V2"
                },
                {
                    challenge : "243tDJmbm5mDj_1gMRjpwtI_c9cgUgtF79Y...", 
                    keyHandle : "bmmSN2Ur8vT4LpoQuVLx5avRfo17ZZzVjxr...",
                    appId     : "https://example.com", 
                    version   : "U2F_V2"
                }
                ...
            ]
        }
        ```
 
* **Error Response:**
    
    * **Code:** 401 UNAUTHORIZED
        ```javascript
        {
            status : "failed", 
            error  : "Unauthorized!"
        }
        ```

* **Sample Call:**
    ```javascript
        fetch('/sign', {
            method  : 'GET',
            credentials : 'same-origin',
            headers : {
                'Accept'       : 'application/json',
                'Content-Type' : 'application/json'
            }
        }).then(function (response) {
            return response.json();
        }).then(function (response) {
            var keys = response.authenticateRequests;
            var challenge = keys[0].challenge;
            var appId = keys[0].appId;
            u2f.sign(appId, challenge, keys, function(deviceResponse) {
                console.log(deviceResponse)
            })
        }).catch(function (err) {
            console.log({ 'status': 'failed', 'error': err });
        })
    ```

**Verify signature**
----
Verifies users signature

* **URL**

    * `/sign`

* **Method:**

     * `POST`
    
*  **URL Params**

    * None

* **Data Params**

    ```javascript
    {
        clientData    : "eyJ0eXAiOiJuYXZpZ2F0b3IuaWQuZ2V0QXaNzZ...",
        keyHandle     : "Jo_q_IxHKq5AzEheueRVrzltnVDOqjbGD2ZGoj...",
        signatureData : "AQAAAIowRgIhAOIualn9io4K7WaqoJOXFOQrQU..."
    }
    ```

* **Success Response:**

    * **Code:** 200 OK

        ```javascript
        {
            status  : "ok", 
            message : "Successfully verified your second factor!"
        }
        ```
 
* **Error Response:**

    * **Code:** 400 BAD REQUEST
        ```javascript
        {
            status : "failed", 
            error  : "Invalid signature!"
        }
        ```
    
    * **Code:** 401 UNAUTHORIZED
        ```javascript
        {
            status : "failed", 
            error  : "Unauthorized!"
        }
        ```

* **Sample Call:**
    ```javascript
        fetch('/sign', {
            method  : 'GET',
            credentials : 'same-origin',
            headers : {
                'Accept'       : 'application/json',
                'Content-Type' : 'application/json'
            }
        }).then(function (response) {
            return response.json();
        }).then(function (response) {
            var keys = response.authenticateRequests;
            var challenge = keys[0].challenge;
            var appId = keys[0].appId;
            u2f.sign(appId, challenge, keys, function(deviceResponse) {
                fetch('/sign', {
                    method  : 'POST',
                    credentials : 'same-origin',
                    body : JSON.stringify(deviceResponse),
                    headers : {
                        'Accept'       : 'application/json',
                        'Content-Type' : 'application/json'
                    }
                }).then(function (response) {
                    return response.json();
                }).then(function (response) {
                    console.log(response);
                }).catch(function (err) {
                    console.log({ 'status': 'failed', 'error': err });
                })
            })
        }).catch(function (err) {
            console.log({ 'status': 'failed', 'error': err });
        })
    ```
