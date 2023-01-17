#!/bin/bash
curl -u $SHROOM_USER:$SHROOM_PASSWORD -T $1 https://friz-nc.uk/remote.php/dav/files/$SHROOM_USER/
