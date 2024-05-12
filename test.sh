#!/bin/bash

# Loop to create 10 user profiles
for i in {1..10}
do
    username="user$i"
    adduser --disabled-password --gecos "" $username
    echo "User $username created successfully."
done
