#!/bin/bash
# set this variable to point to your ingress host
#HOST=dfl-tv.fritz.box

curl -X PUT http://$HOST/py-key-value-store/doc/eins -d '{"foo": "ich war hier"}' -H 'Content-Type: application/json'
curl -X PUT http://$HOST/py-key-value-store/doc/zwo -d '{"foo": "ich war hier"}' -H 'Content-Type: application/json'

curl http://$HOST/py-key-value-store/doc/zwo | jq .
curl http://$HOST/py-key-value-store/doc/ | jq .

curl http://$HOST/py-key-value-store/health/ | jq .
