#!/bin/bash

# @Author: lnorb.com
# @Date:   2023-02-10 09:08:41
# @Last Modified by:   w
# @Last Modified time: 2023-02-10 12:46:55

# Let's do some cleaning up by removing the nodes and their volumes
./simnet-workbench docker 'rm -f alice bob carol btcd'
./simnet-workbench docker 'volume rm -f docker_bitcoin docker_lnd docker_shared'

# Create alice
./simnet-workbench lnd.start --name alice

# Create bob and connect him to alice
./simnet-workbench lnd.start --name bob    --channels alice

# Create carol and connect her to bob and alice
./simnet-workbench lnd.start --name carol  --channels bob,alice

alias alice="./simnet-workbench lncli alice ${*}"
alias bob="./simnet-workbench lncli bob ${*}"
alias carol="./simnet-workbench lncli carol ${*}"