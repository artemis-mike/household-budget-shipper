#!/bin/sh

export $(cat .env | xargs)

if [ -z $SHIPPER_INTERVAL ]; then 
    SHIPPER_INTERVAL=30
fi

SECONDS_SINCE_LAST_RUN=$(expr $(date +%s) - $(cat lastRun.epoch))
THRESHOLD=$(expr $SHIPPER_INTERVAL \* 2)

if [ "$SECONDS_SINCE_LAST_RUN" -lt "$THRESHOLD" ]; then 
    exit 0; 
else
    exit 1;
fi
