#!/bin/bash

resp1=$(curl -s -X POST http://localhost:8081/admin/select-winners --cookie session=.eJwlzjEOwjAMQNG7eO5gO4nj9DIosR3BBErphLg7ldifvv4HbnPFcYf9vc7Y4PZw2MGL88iNPApZap2pMYYOk9GNaNoYTUjC1ZsSRWHMVN1r1c4yTdD4cuxXASljKtRxzHLBkISdcvcsRsLacgqVYiozITayiuGwwXnE-s-8wtcTvj9LvzA4.YCv3FA.1ualoe2bcGVLI--ih_O8n67QA0o)

if [ "$resp1" = '"Success"' ]; then
    resp2=$(curl -s -X POST http://localhost:8081/admin/reset-daily-points --cookie session=.eJwlzjEOwjAMQNG7eO5gO4nj9DIosR3BBErphLg7ldifvv4HbnPFcYf9vc7Y4PZw2MGL88iNPApZap2pMYYOk9GNaNoYTUjC1ZsSRWHMVN1r1c4yTdD4cuxXASljKtRxzHLBkISdcvcsRsLacgqVYiozITayiuGwwXnE-s-8wtcTvj9LvzA4.YCv3FA.1ualoe2bcGVLI--ih_O8n67QA0o)
    
    if [ "$resp2" = '"Success"' ]; then
        echo "Success"
    else
        echo "Error reseting daily points"
    fi
else
    echo "Error selecting winners"
fi