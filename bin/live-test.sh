#!/bin/sh

make start-testserver
make jstest
make stop-testserver
