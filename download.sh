#!/bin/bash
downloadPath=$1
savePath=$2
curl -X GET -u Shrooms:SecretShrooms1!2@ "https://friz-nc.mooo.com/remote.php/dav/files/Shrooms/${downloadPath}" --output $savePath
