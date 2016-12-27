Objective: Enable anyone to look up (via SMS) lawyers by name - against the list of registered lawyers in Kenya.

# Components

## SMS listener
A Twistd web service that receives messages from Twilio.
* Location: "./sms_proxy"
* Start: twistd -y site.py
* Stop:  kill -9 `cat twistd.pid`
* Log location: "sms_proxy/logs"


## Query API
Queries Cloudsearch and returns results matching the query "name"
* Location: "./api"
* API endpoint: "/lsk"
* Expected http method: "GET"
* Expected http parameters: "name" (name of lawyer to query) and "channel" (source of request e.g. sms/web)
* Start:  twistd -y site.py
* Stop:   kill -9 "cat twistd.pid"
* Sample query:

```
$ curl -XGET -i "http://localhost:6060/lsk?name=jack&channel=sms"
HTTP/1.1 200 OK
Transfer-Encoding: chunked

Found 7 results matching your query. Refine your query by providing more names?
Bunde Omondi Jack - P.105/5857/05 - Active 
Mwangi Jack Benson Kinyua - P.105/9438/12 - Active 
Masese Jack Reuben - P.105/1347/84 - Active 
Odhiambo Jack Oronga - P.105/8841/11 - Active 
Ojiambo Jack Ncruba Nambiro - P.105/6309/06 - Active 
Ouma Jack Busalile Mwimali - P.105/7841/10 - Active 
Wandai Jack Matheka - P.105/7103/08 - Active 

```
