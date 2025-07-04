# Rename the sample file using the current timestamp. 
# Copy to aws using aws s3 cp
# Create a file containing a link to the file on aws

import os
import time
import subprocess
import requests

bucket_link = "http://vdjbase-distribution.s3-website-us-east-1.amazonaws.com/"
bucket_name = "vdjbase-distribution"

# Get the current timestamp

timestamp = time.strftime("%Y%m%d-%H%M%S")

# Rename the sample file

ts_filename = "samples_" + timestamp + ".zip"
os.rename("samples.zip", ts_filename)

# Copy the renamed file to aws

subprocess.call(["aws", "s3", "cp", ts_filename, "s3://" + bucket_name])

url = bucket_link + ts_filename
url_valid = None
# Check if the URL is valid by sending a HEAD request

try:
    response = requests.head(url)
    if response.status_code == 200:
        url_valid = True
    else:
        print(f"URL is not valid. Status code: {response.status_code}")
        url_valid = False
except requests.exceptions.RequestException as e:
    print(f"Failed to validate the URL: {e}")
    url_valid = False

if not url_valid:
    os.rename(ts_filename, "samples.zip")
    exit(1)

# Create a file containing a link to the file on aws

with open("link_to_sample.txt", "w") as f:
    f.write(bucket_link + ts_filename)
