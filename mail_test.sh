#!/bin/bash

EMAIL_ADDRESS="chen.stephen151@gmail.com"
EMAIL_SUBJECT="test"

echo "" | mail -s "$EMAIL_SUBJECT" "$EMAIL_ADDRESS"
