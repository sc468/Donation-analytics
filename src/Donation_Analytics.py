# https://github.com/InsightDataScience/donation-analytics
#import numpy as np
import datetime
import AVL_Tree as AVL
import sys

itcontFileLocation = sys.argv[1]
percentileFileLocation = sys.argv[2]
outputFileLocation = sys.argv[3]

#Extract percentile
percentile = 0
with open(percentileFileLocation) as percentFile:
    percentile = int(percentFile.readline())

#Parameter items: input line spliced by '|'
#Output: Dictionary data with values for output
def readData (items):
    data = {}
    data['CMTE_ID'] = items[0]
    data['NAME'] = items[7]

    #Check if ZIP_CODE is valid
    try:
        data['ZIP_CODE'] = items[10][0:5]
    except:
        #print ('INVALID ZIP CODE')
        #print(str(items) + '\n')
        return None

    #Check if TRANSACTION_DT is valid, and extract year
    try:
        data['TRANSACTION_YR'] = datetime.datetime.strptime(items[13], '%m%d%Y').year
    except ValueError:
        #print('INCORRECT DATE FORMAT')
        return None

    data['TRANSACTION_AMT'] = float(items[14])
    data['OTHER_ID']  = items[15]
    data['ID'] = str(data['NAME'])+str(data['ZIP_CODE'])

    return data

#Parameter data: Dictionary formed from readData()
#Output: True for erroneous inputs, False otherwise
def checkError (data):
    try:
        #Not individual contributor
        if not data['OTHER_ID'] =='':
            #print ('OTHER_ID NOT BLANK')
            #print(str(items) + '\n')
            return True

        #Empty items
        if data['CMTE_ID'] == '' or data['NAME'] == '' or \
        data['ZIP_CODE'] == '' or data['TRANSACTION_AMT'] == '':
            #print ('EMPTY DATA FIELD')
            #print(str(items) + '\n')
            return True

        #Check if zipcode is numeric
        if not str.isnumeric(data['ZIP_CODE']):
            return True

        #Moved to readData
        #TRANSACTION_DT is an invalid date (e.g., malformed)
        #try:
        #    datetime.datetime.strptime(data['TRANSACTION_DT'], '%m%d%Y')
        #except ValueError:
        #    print('INCORRECT DATE FORMAT')
        #    return True

    except:
        return True

    return False

#Parameter data: Dictionary from readData()
#Output: Requested string output from challenge
def processData(data):
    output = []

    outputKey = str(data['CMTE_ID']) + str(data['ZIP_CODE']) + \
    str(data['TRANSACTION_YR'])

    output = str(data['CMTE_ID']) + '|' + str(data['ZIP_CODE']) + '|' + \
    str(data['TRANSACTION_YR']) + '|'

    #Add percentile to output
    appendContributionList(outputKey, round(data['TRANSACTION_AMT']))
    percentileOutput = findPercentile(outputKey)
    output= output + str(int(percentileOutput)) + '|'

    #Add total number of dollars to output
    if not outputKey in contributionDollar:
        contributionDollar [outputKey] = data['TRANSACTION_AMT']
    else:
        contributionDollar[outputKey] +=data['TRANSACTION_AMT']
    output = output + str(round(contributionDollar[outputKey])) + '|'

    #Add number of contributions to output
    if not outputKey in contributionNumber:
        contributionNumber [outputKey] = 1
    else:
        contributionNumber[outputKey] +=1
    output = output + str(contributionNumber[outputKey]) + '\n'

    #print ('Output = ', output)
    return output

#Parameter outputKey: ID with CMTE_ID, ZIP_CODE and TRANSACTION_YR
#Parameter amount: Donation amount
#Goal: Store donation amount for outputKey in dictionary
def appendContributionList(outputKey, amount):
    if not outputKey in contributionList:
        contributionList [outputKey] = AVL.Tree()
    contributionList [outputKey].add(amount)
    return

#Parameter outputKey: ID with CMTE_ID, ZIP_CODE and TRANSACTION_YR
#Output: Percentile contribution for outputKey
def findPercentile(outputKey):
    return contributionList [outputKey].findPercentile(percentile)

##############################################################################
#------------------MAIN CODE----------------------------------------------

donorIDs = {}
contributionNumber = {}
contributionDollar = {}
contributionList = {}

#Read itcont and output to outputFile
outputFile = open(outputFileLocation, 'w+')
itcontFile = open(itcontFileLocation, 'r')
with open(itcontFileLocation, 'r') as itcontFile:
    with open(outputFileLocation, 'w+') as outputFile:
        for line in itcontFile:
            items = line.split('|')

            #Read items into dictionary
            data = readData(items)

            #Check for errors in items
            if checkError(data):
                continue

            #Check if repeat donor
            #If not repeat donor, store ID to check later
            if data['ID'] not in donorIDs:
                donorIDs[data['ID']]= 1
                #print ('Not Repeat Donor')
                #print(str(data) + '\n')
                continue
            #If repeat donor, process data and write to output
            else:
                #print ('Repeat Donor!')
                output = processData(data)
                outputFile.write(output)
