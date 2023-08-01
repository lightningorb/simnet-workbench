#!/bin/bash

# @Author: lnorb.com
# @Date:   2023-02-10 09:08:41
# @Last Modified by:   w
# @Last Modified time: 2023-02-10 12:46:55

# Clone lnd
./simnet-workbench -H lnd lnd.clone

# this is completely aribrary, e.g you want to build changes a file
# rsync -azv ../lnd/peer/brontide.go ubuntu@lnd:~/lnd/peer/

# if lnd.conf exists, then sync it to the repo
if test -e src/lnd.conf; then
    rsync -azv src/lnd.conf ubuntu@lnd:~/lnd/sample-lnd.conf;
fi

# sync the dev dockerfile, with our modifications
rsync -azv src/dev.Dockerfile ubuntu@lnd:~/lnd/;

# Let's do some cleaning up by removing the nodes and their volumes
./simnet-workbench -H lnd docker 'rm -f alice bob carol btcd'
./simnet-workbench -H lnd docker 'volume rm -f docker_bitcoin docker_lnd docker_shared'

# Build lnd
./simnet-workbench -H lnd docker 'rmi lnd'
./simnet-workbench -H lnd lnd.build --tag=lnd

# Create alice
./simnet-workbench -H lnd lnd.start --name alice

# Create bob and connect him to alice
./simnet-workbench -H lnd lnd.start --name bob    --channels alice

# Create carol and connect her to bob and alice
./simnet-workbench -H lnd lnd.start --name carol  --channels bob,alice

alias alice="./simnet-workbench -H lnd lncli alice ${*}"
alias bob="./simnet-workbench -H lnd lncli bob ${*}"
alias carol="./simnet-workbench -H lnd lncli carol ${*}"