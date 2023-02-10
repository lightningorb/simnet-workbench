#!/bin/bash

# @Author: lnorb.com
# @Date:   2023-02-10 09:08:41
# @Last Modified by:   w
# @Last Modified time: 2023-02-10 12:14:00

# It can be tedious using long commands in Bash
# So here is a place to put commands.

# Let's do some cleaning up by removing the nodes and their volumes
./clusterlnd -H lnd docker 'rm -f alice bob carol btcd'
./clusterlnd -H lnd docker 'volume rm -f docker_bitcoin docker_lnd docker_shared'

# Clone lnd
./clusterlnd -H lnd lnd.clone

# Build lnd
# ./clusterlnd -H lnd docker 'rmi lnd'
# ./clusterlnd -H lnd lnd.build --tag=lnd

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


alias alice="./clusterlnd -H lnd lncli alice ${*}"
alias bob="./clusterlnd -H lnd lncli bob ${*}"
alias carol="./clusterlnd -H lnd lncli carol ${*}"
