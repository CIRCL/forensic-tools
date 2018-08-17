#!/usr/bin/env python3
#
#   lol.py - Leak Origin Locator
#   Analyse leaked credentials to identify the compromised website.
#
#   Copyright (C) 2018  Michael Hamm
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.



import argparse
import os, sys, re, pprint, copy



MINWORD = 4                             # Ignore words with less than 4 characters
numOfHits = 5                           # How many passwords to show

PWD = { 'FRENCH' : ['AZERTY', 'ANNIVERSAIRE', 'BRUXELLES', 'MOTDEPASSE', 'SOLEIL', 'LOULOU', 'DOUDOU', 'COUCOU'],
        'GERMAN' : ['PASSWORT', 'QWERTZ'],
        'ENGLISH' : ['123456', '1234567', '12345678', 'PASSWORD', 'CANABIS', 'SECRET', 'QWERTY',
                    'ABC123', 'MONKEY', 'ILOVEYOU', 'LETMEIN', 'TRUSTNO'],
        'NAMES' : ['PIERRE', 'MANUEL', 'CAROLINE', 'LOUIS', 'MICHAEL']}



def loadData(fileName):
    if not os.path.exists(fileName):
        print('File %s not found!' % (fileName))
        sys.exit()
    with open(fileName) as f:
        data = f.read()
    f.close()
    return(data)



def extractPwd(data,noMostUsed=True):
    # Extract passwords, email addresses out of data
    # 1. Delete duplicate lines
    # 2. Ignore lines without email addresses (@)
    # 3. Sanitize words which are no email address
    # 4. Do (not) remove most common passwords
    lines = []
    passwords = []
    emails = []
    wordAdding = True
    
    for line in data.splitlines():
        if line in lines:
            continue
        else:
            lines.append(line)
        if '@' not in line:
            continue
        for words in re.split('[\s|:,;]',line):
            if '@' not in words:
                word = re.compile('[^A-Z\s]').sub('', words.upper())
                wordAdding = True

                for key in PWD:
                    if word in PWD[key] and noMostUsed == True:
                        wordAdding = False
                        break

                if len(word) >= MINWORD and wordAdding == True:
                    passwords.append(word)
            else:
                emails.append(words)
    return({'passwords':passwords, 'emails':emails})



def getWordCount(passwords):
    wordCount = {}
    for password in passwords:
        if len(password) >= MINWORD:
            if password not in wordCount:
                wordCount[password] = 1
            else:
                # Detected a hit
                # Longer words are more valuable
                wordCount[password] += len(password)
    return(wordCount)



def getWordSorted(wordCount, numOfHits):
    # Sort the passwords by number of occurences
    wordGrouped = {}

    for word in wordCount:
        if wordCount[word] not in wordGrouped:
            wordGrouped[wordCount[word]] = [word]
        else:
            wordGrouped[wordCount[word]].append(word)

    wordSorted = list(wordGrouped.items())
    wordSorted.sort(reverse=True)
    return(wordSorted[:numOfHits])



def getCorrelateEmailPwd(emails, wordSorted):
    domains = {}
    localParts = {}
    
    for words in wordSorted:
        for word in words[1]:
            for email in emails:
                domain = email.split('@')[1]
                localPart = email.split('@')[0]
                if word in domain.upper():
                    if domain.lower() not in domains:
                        domains[domain.lower()] = 1
                    else:
                        domains[domain.lower()] += 1
                if word in localPart.upper():
                    if localPart.lower() not in localParts:
                        localParts[localPart.lower()] = 1
                    else:
                        localParts[localPart.lower()] += 1

    domainsSorted = getWordSorted(domains, 4)
    localPartsSorted = getWordSorted(localParts, 2)
    return({'domains':domainsSorted, 'localParts':localPartsSorted})



def main():
    p = argparse.ArgumentParser(description='Leak origin Locator: Identify the origin of a credentials breach with Password Frequency Analyzis.')
    p.add_argument('-m', '--most', action='store_true', 
            help='Do not remove [M]ost used passwords from the analysis')
    p.add_argument('filename', help='Specify file name to analyse.')
    args = p.parse_args()
    fileName = args.filename

    print("Loading %s ..." % (fileName))
    data = loadData(fileName)
    print('%s characters loaded.' % (len(data)))

    if args.most:
        extractData = extractPwd(data,False)
    else:
        extractData = extractPwd(data)
    passwords = extractData['passwords']
    emails = extractData['emails']
    print('%s passwords extracted.' % (len(passwords)))

    wordCount = getWordCount(passwords)
    print('%s uniq passwords found.' % (len(wordCount)))

    wordSorted = getWordSorted(wordCount, numOfHits)
    print('\nCalculate weighting for interesting passwords:')
    pprint.pprint(wordSorted)

    print('\nCorrelating email domain names')
    correlateEmailPwd = getCorrelateEmailPwd(emails, wordSorted)
    pprint.pprint(correlateEmailPwd['domains'])
    print('\nCorrelating email local parts')
    pprint.pprint(correlateEmailPwd['localParts'])

    print('\nAnalysis completed.....\n\n')


if __name__ == "__main__":
    main()

