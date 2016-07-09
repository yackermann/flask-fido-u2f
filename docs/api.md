**Post API Documentation**
---

* **Enroll**
    * [Get enroll](#get-enroll)
    * [Verify enroll](#verify-enroll)

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
            status :'failed', 
            error  :'Invalid key handle!'
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
