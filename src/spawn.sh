#!/bin/bash

# @Author: lnorb.com
# @Date:   2023-02-10 09:08:41
# @Last Modified by:   w
# @Last Modified time: 2023-02-10 10:57:37

# It can be tedious using long commands in Bash
# So here is a place to put commands.

# Let's do some cleaning up by removing the nodes and their volumes
./clusterlnd -H lnd docker 'rm -f alice bob carol btcd '
./clusterlnd -H lnd docker 'volume rm -f docker_bitcoin docker_lnd docker_shared simnet_lnd_alice simnet_lnd_bob simnet_lnd_bot simnet_lnd_carol'

./clusterlnd -H lnd docker 'build --tag=myrepository/lnd-dev -f dev.Dockerfile .'


#                   ┌───────┐
#      ┌────────────┤ alice ├─────────────┐
#      │            └───────┘             │
#      │                                  │
#      │                                  │
#      │                                  │
#      │                                  │
#      │                                  │
#      │                                  │
#      │                                  │
#  ┌───┴───┐                          ┌───┴───┐
#  │ carol ├──────────────────────────┤  bob  │
#  └───────┘                          └───────┘

# Create alice
./clusterlnd -H lnd lnd.start --name alice

# Create bob and connect him to alice
./clusterlnd -H lnd lnd.start --name bob    --channels alice

# Create carol and connect her to bob and alice
./clusterlnd -H lnd lnd.start --name carol  --channels bob,alice
