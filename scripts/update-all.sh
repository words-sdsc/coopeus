#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

$DIR/neon-to-postgis.py 
$DIR/unavco-to-postgis.py 

