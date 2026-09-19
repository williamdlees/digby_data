# Rename the sample file using the current timestamp. 
# Copy to aws using aws s3 cp
# Create a file containing a link to the file on aws

import os
import time
import subprocess
import requests
import argparse

parser = argparse.ArgumentParser(description="Upload sample file to AWS S3 and create a link.")
parser.add_argument("--file", type=str, default="samples.zip", help="The sample file to upload (must be a .zip file).")
args = parser.parse_args()

if not args.file.endswith(".zip"):
    print("The sample file must be a .zip file.")
    exit(1)

bucket_link = "http://vdjbase-distribution.s3-website-us-east-1.amazonaws.com/"
bucket_name = "vdjbase-distribution"
archive_name = args.file.replace(".zip", "")

# Get the current timestamp

timestamp = time.strftime("%Y%m%d-%H%M%S")

# Rename the sample file

ts_filename = archive_name + "_" + timestamp + ".zip"
os.rename(args.file, ts_filename)

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

with open(f"link_to_{archive_name}.txt", "w") as f:
    f.write(bucket_link + ts_filename)
