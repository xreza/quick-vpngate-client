"""
Oliver McLaughlin 11/18/20
XReza 1/15/2021
This program acts as a simple text-based client for the openvpn service.
It only prints the top 10 results with host name, score, and ping.

The user then inputs a number (0-9) and the openvpn profile is downloaded
to temp and then used.
"""
import os
import csv
import urllib.request
import base64

# Make a request to url, get csv info
response = urllib.request.urlopen("http://www.vpngate.net/api/iphone/")

# Decode the response and split by newline to agree with csv.reader
response = response.read().decode('utf-8').split('\n')

# Read in the csv info and make new object
reader = csv.reader(response, delimiter=',')

# Get rid of irrelevant headers
reader.__next__()
reader.__next__()

# Set current 
current = reader.__next__()

# b64 representations of openvpn profiles
profiles = []

# Loop through first 99 results
for i in range(99):
    
    # Print results in "[num]    name        Score       ping" fashion
    print("[" + str(i) + "]\t" +
          current[0] +
          " [" + current[6] + "]" +
          "\t\tScore: " + current[2] +
          "\t\tPing: " + current[3])

    # Append openvpn profile data to array
    profiles.append(current[14])
    
    # Get next result
    current = reader.__next__()

# Choose a profile
choice = int(input("Choose a profile: "))

# If invalid keep asking
while choice < 0 or choice > 10:
    choice = int(input("Choose a profile: "))

# Write file to /tmp/
with open('/tmp/profile.opvn', 'w') as f:
    f.write(base64.b64decode(profiles[choice]).decode('ascii'))

# Open openvpn with new profile
os.system("sudo openvpn /tmp/profile.opvn")
