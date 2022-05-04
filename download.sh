#!/bin/bash
downloadPath=$1
savePath=$2
curl -X GET -u Shroom:ichbin1pilz "https://friz-nc.uk/remote.php/dav/files/Shroom/${downloadPath}" --output $savePath
