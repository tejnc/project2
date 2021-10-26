## flask-mongoengine

##### Learning mongoengine and using it to create api using flask and python

## For registration api (url: <server_address>/user/register):
* passing parameters are 
    1. name
    2. gender
    3. phone_number
    4. province
    5. district
    6. town
    7. email
    8. password

    ##### And they are returned in the format:
    
            [
                {
                    "address"{
                        "district":"...",
                        "province":"....",
                        "town": "....."
                    },
                    "email":".....@....",
                    "gender":"....",
                    "name":"......",
                    "phone_number":"......",
                }
            ]
        

## For login api (url: <server_address>/login):
* parmeters are
    1. email
    2. password
    
`Note: You need to login again after 45 minutes.`

## For listing users(url: <server_address>/users/<page>/<limit>):
* You must be logged in and authorized.
* Pagination included

## For updating user(url: <server_address>/user/<id>):
* method: PUT

## For deleting user(url: <server_address>/user/<id>):
* method: DELETE




