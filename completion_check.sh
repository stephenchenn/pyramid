#!/bin/bash

NOHUP_OUT_FILE="nohup.out"
SLEEP_TIME=3600  # time to wait between checks, in seconds
EMAIL_ADDRESS="chen.stephen151@gmail.com"
EMAIL_SUBJECT="Nohup operation completed"
EMAIL_MESSAGE="pyramid completed"

# Check if nohup.out exists and is readable
if [[ ! -r $NOHUP_OUT_FILE ]]; then
    echo "ERROR: $NOHUP_OUT_FILE is not readable or does not exist"
    exit 1
fi

while true; do
    # Sleep for SLEEP_TIME seconds
    sleep $SLEEP_TIME
    
    # Get the last line of the nohup.out file
    lastline=$(tail -n 1 "$NOHUP_OUT_FILE")

    # If the last line is 'done', then the nohup operation is complete
    if [[ $lastline == "done" ]]; then
        # Send email notification
        echo "$EMAIL_MESSAGE" | mail -s "$EMAIL_SUBJECT" "$EMAIL_ADDRESS"
        echo "Nohup operation completed"
        break
    fi
done
