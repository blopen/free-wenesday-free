<<<<<<< HEAD
#!/bin/bash

####API
APIKEY="IdOB74VGLBdyafLEJEaDbKr0ucE4oWROC94qLjYRFDdIRxusEjZryBRaNSOBs4a7"
APISECRET="bTpX1dsKhOgWudEXft9ihOOCU2id7eG6QFe2P22nujrDaklck9Ze9nClxVMi5x7f"

RECVWINDOW=5000 # 5 seconds

####GET ACCOUNT BALACE

TM=$(( $(date -u +%s) *1000))

GET_BALANCE_QUERY="recvWindow=$RECVWINDOW&timestamp=$TM"

GET_BALANCE_SIG=$(echo -n "$GET_BALANCE_QUERY" | openssl dgst -sha256 -hmac $APISECRET)

echo $GET_BALANCE_SIG
GET_BALANCE_SIG="$(echo $GET_BALANCE_SIG | cut -f2 -d" ")"
echo $GET_BALANCE_SIG

=======
#!/bin/bash

####API
APIKEY="IdOB74VGLBdyafLEJEaDbKr0ucE4oWROC94qLjYRFDdIRxusEjZryBRaNSOBs4a7"
APISECRET="bTpX1dsKhOgWudEXft9ihOOCU2id7eG6QFe2P22nujrDaklck9Ze9nClxVMi5x7f"

RECVWINDOW=5000 # 5 seconds

####GET ACCOUNT BALACE

TM=$(( $(date -u +%s) *1000))

GET_BALANCE_QUERY="recvWindow=$RECVWINDOW&timestamp=$TM"

GET_BALANCE_SIG=$(echo -n "$GET_BALANCE_QUERY" | openssl dgst -sha256 -hmac $APISECRET)

echo $GET_BALANCE_SIG
GET_BALANCE_SIG="$(echo $GET_BALANCE_SIG | cut -f2 -d" ")"
echo $GET_BALANCE_SIG

>>>>>>> bb5139a261576f42443de9c7549cfb80c1f47869
curl -H "X-MBX-APIKEY: $APIKEY" -X GET "https://api.binance.com/api/v3/account?recvWindow=$RECVWINDOW&timestamp=$TM&signature=$GET_BALANCE_SIG" 