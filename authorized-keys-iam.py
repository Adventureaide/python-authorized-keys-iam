#!/usr/bin/python3
"""
Authorized Keys IAM

This script will pull the public SSH keys from IAM for the user that is trying
to login and then validate if that is the correct ssh key.

Usage:
  authorized-keys-iam <-h | --version>
  authorized-keys-iam auth <user>
  authorized-keys-iam sync-users

Options:
  -h --help    Show this screen
  --version    Show version.

"""
from docopt import docopt

import boto3
import sys
import re
import pwd
import shlex

import pprint

pp = pprint.PrettyPrinter()

def print_user_keys(user):
  client = boto3.client('iam')
  response = client.list_ssh_public_keys(UserName=user)
  for key in response['SSHPublicKeys']:
    keyid = key['SSHPublicKeyId']
    response = client.get_ssh_public_key(UserName=user, SSHPublicKeyId=keyid, Encoding='SSH')
    print(response["SSHPublicKey"]["SSHPublicKeyBody"])

def get_missing_users():
  missing = list()

  client = boto3.client('iam')
  iam_users = client.list_users()["Users"]
  system_users = map(lambda x: x.pw_name, pwd.getpwall())
  for user in iam_users:
    if user not in system_users:
      missing.push(user)

  return missing

def add_user(user):
  call("/usr/sbin/adduser " + shlex.quote(user))

if __name__ == '__main__':
  arguments = docopt(__doc__, version="Authorized Keys IAM 0.1")
  if arguments["auth"]:
    user = arguments["<user>"]
    print_user_keys(user)
  elif arguments["sync-users"]:
    map(add_user, get_missing_users())
