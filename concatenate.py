#!/usr/bin/python

import traceback
import csv as csvOperator
import collections

# Import arguments
import sys
arguments = sys.argv[1:]

# Read files
fileContents = []
for i in range(len(arguments)):
  try:
    filename = arguments[i]
    with open(filename) as file:
      csvfile = csvOperator.reader(file, delimiter=',')
      
      csv = {}
      csv['data'] = []
      csv['headers'] = None
      for row in csvfile:
        if (csv['headers'] == None):
          csv['headers'] = row
        else:
          csv['data'].append(row)
      fileContents.append(csv)
  except:
    print "I couldn't read the file: " + arguments[i] + "\nError: ", sys.exc_info()[0]
    traceback.print_exc(file=sys.stdout)
    sys.exit(0)

# Define writer
def write(header, data):
  print "\nEnter a filename to write to:"
  filename = raw_input()
  # Add extension if necessary
  if not filename.endswith('.csv'):
    filename += '.csv'
  with open(filename, 'w') as csvfile:
    writer = csvOperator.writer(csvfile, delimiter=',', quotechar='|', quoting=csvOperator.QUOTE_MINIMAL)
    # Write header
    writer.writerow(header)
    # Data
    for row in data:
      writer.writerow(row)
    print "\nData written to " + filename

# Make sure all headers match
headerCounts = {}
# Add first file's headers
for i in range(len(fileContents[0]['headers'])):
  headerCounts[fileContents[0]['headers'][i]] = 1
# Verify the rest of the files
for i in range(1, len(fileContents)):
  headers = fileContents[i]['headers']
  for header in headers:
    if header in headerCounts:
      headerCounts[header] += 1
    else:
      # Error! Found a header that doesn't match with the first file
      print "Error: all CSV headers need to match."
      sys.exit(0)
for key in headerCounts:
  if not headerCounts[key] == len(fileContents):
    # Not all files have this header
    print "Error: all CSV headers need to match."
    sys.exit(0)

# Compile data such that columns are matched
headers = fileContents[0]['headers']
allData = fileContents[0]['data']
for i in range(1, len(fileContents)):
  currHeaders = fileContents[i]['headers']
  currData = fileContents[i]['data']
  for row in currData:
    newRow = []
    # Add each column in order
    for header in headers:
      index = currHeaders.index(header)
      newRow.append(row[index])
    allData.append(newRow)

write(headers, allData)