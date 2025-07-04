# Find files on AWS that are no longer referenced in the digby_data repos
# Offer to delete them

import os
import subprocess

bucket_link = "http://vdjbase-distribution.s3-website-us-east-1.amazonaws.com/"
bucket_name = "vdjbase-distribution"

digby_data_repos = ['digby_data', 'digby_private_data']
repo_prefix = 'd:/research'

links_in_use = []

# search all subdirectories in the repos for files named 'link_to_*.txt'
# extract the links from the files and add them to the list

for repo in digby_data_repos:
    repo_path = os.path.join(repo_prefix, repo)
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.startswith('link_to_') and file.endswith('.txt'):
                with open(os.path.join(root, file), 'r') as f:
                    links_in_use.append(f.read().strip().replace(bucket_link, ''))

# get the list of files in the bucket using aws s3 ls

subprocess.call(["aws", "s3", "ls", "s3://" + bucket_name, "--no-paginate"], stdout=open("aws_files.txt", "w"))

with open("aws_files.txt", "r") as f:
    aws_files = f.readlines()

aws_files = [x.split(' ')[-1].strip() for x in aws_files if x.strip() and not x.startswith('PRE')]

all_found = True
for link in links_in_use:
    if link not in aws_files:
        print(f"Current link {link} not found in AWS bucket")
        all_found = False
if all_found:   
    print("All current links are found in the AWS bucket.")

files_to_delete = []

print('Files to retain:')
for file in aws_files:
    if file not in links_in_use:
        files_to_delete.append(file)
    else:
        print(file)

if not files_to_delete:
    print("All files are current.")
    exit(0)


print('Files to delete:')
for file in files_to_delete:
    print(file)

print('Delete files from AWS bucket? (y/n)')
delete_files = input().strip().lower()

if delete_files == 'y':
    for file in files_to_delete:
        print(f"Deleting {file}")
        subprocess.call(["aws", "s3", "rm", "s3://" + bucket_name + "/" + file])

