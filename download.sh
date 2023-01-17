#!/bin/bash
downloadPath=$1
savePath=$2
curl -X GET -u $SHROOM_USER:$SHROOM_PASSWORD "https://friz-nc.uk/remote.php/dav/files/${SHROOM_USER}/${downloadPath}" --output $savePath
