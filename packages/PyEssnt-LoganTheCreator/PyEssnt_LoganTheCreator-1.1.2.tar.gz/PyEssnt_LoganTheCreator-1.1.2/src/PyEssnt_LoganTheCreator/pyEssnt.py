from os import system,name,urandom
from time import sleep 
import sys
import hashlib
import string
import random
import socket
import ipaddress
import subprocess
try:
	hostName = socket.gethostname()
	__IP__ = socket.gethostbyname(hostName)
except:
	pass

def clearShell():
	system('cls')

def typestr(message, interval=""):
    for i in message:
        sys.stdout.write(i)
        sys.stdout.flush()
        if interval:
            sleep(float(interval))
        else:
            sleep(0.01)
def command(command):
    system(command)           
def list_directory():
    system('dir')
def wait(milliseconds):
    sleep(milliseconds)
def salt(chars, unencoded):
    salt = urandom(chars)
    if unencoded == True:
        return str(salt)
    elif unencoded == False:
        saltEncoded = str(salt)
        saltEncoded2 = saltEncoded.encode()
        return saltEncoded2
        
def hash(string,method=""):
    stringRaw = str(string).encode(encoding="utf-8")
    if method == "sha256":
        algorithm = hashlib.sha256()
    elif method == "md5":
        algorithm = hashlib.md5()
    else:
        raise ValueError("Invalid Algorithm")
    algorithm.update(stringRaw)
    return stringRaw,algorithm.hexdigest()

def ping_server(servername, count="4", verbose=True):
          if verbose == True:
            return system(f'ping {str(servername)} -n {count}')
          else:
              pingit = subprocess.call(["ping", f'{servername}','-n', f'{count}'])
              pingitsplit = str(pingit).strip()
              return pingitsplit
          

class Random:
    @staticmethod
    def string(case=""):
        if case == "lowercase":
            return random.choice(string.ascii_lowercase)
        elif case == "uppercase":
            return random.choice(string.ascii_uppercase)
        else:
            return random.choice(string.ascii_letters)
    def number(LowerNumber,HigherNumber):
        return random.randint(LowerNumber,HigherNumber)

    charList = ['!','@','#','$','%','^','&','*','*','(',')','-', '_','=','+','`','~',',','<','.','>',';',':','{','}','[',']','|']
    charRandom = random.choice(charList)


class Replace_Str:
    
    def __init__(self, strings) -> None:
        self.strings = strings
    
    def for_str(self, *args, replace_for="") -> str:
        new_string = self.strings
        for s in args:
            new_string = new_string.replace(s, replace_for)
        
        return new_string
    def replace_with_list(self,substrings, replacefor=''):
        passed_string = self.string
        for i in substrings:
            passed_string = passed_string.replace(i,replacefor)

                
        return passed_string

    
    


