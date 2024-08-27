# Rename the sample file using the current timestamp. 
# Copy to aws using aws s3 cp
# Create a file containing a link to the file on aws

import os
import time
import subprocess

bucket_link = "http://vdjbase-distribution.s3-website-us-east-1.amazonaws.com/"
bucket_name = "vdjbase-distribution"

# Get the current timestamp

timestamp = time.strftime("%Y%m%d-%H%M%S")

# Rename the sample file

ts_filename = "samples_" + timestamp + ".zip"
os.rename("samples.zip", ts_filename)

# Copy the renamed file to aws

subprocess.call(["aws", "s3", "cp", ts_filename, "s3://" + bucket_name])

# Create a file containing a link to the file on aws

with open("link_to_sample.txt", "w") as f:
    f.write(bucket_link + ts_filename)
