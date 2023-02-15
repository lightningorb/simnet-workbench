#!/bin/bash

rsync -azv ../lnd/peer/brontide*.go ubuntu@lnd:~/lnd/peer/

./simnet-workbench -H lnd test 'github.com/lightningnetwork/lnd/peer'
