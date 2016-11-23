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


##### Join on Column
# Collect key headers
keyColIndices = []
for i in range(len(arguments)):
  headers = fileContents[i]['headers']
  colID = len(headers) + 5
  while colID >= len(headers) or colID < 0:
    print "\nEnter the join column number (" + arguments[i] + ")"
    for j in range(len(headers)):
      print str(j + 1) + ' - ' + headers[j]
    colID = int(raw_input()) - 1

    if colID >= len(headers) or colID < 0:
      print "Invalid number. Try again..."
  keyColIndices.append(colID)

# Get all row keys and initialize rows to [key]
rowDict = collections.OrderedDict()
for i in range(len(fileContents)):
  data = fileContents[i]['data']
  keyIndex = keyColIndices[i]
  for row in data:
    rowDict[row[keyIndex]] = [row[keyIndex]]

# Create full header
newHeader = []
# Get name of key column from first csv file
newHeader.append(fileContents[0]['headers'][keyColIndices[0]])
# Add rest of headers, excluding key columns
for i in range(len(fileContents)):
  header = fileContents[i]['headers']
  keyIndex = keyColIndices[i]
  
  for j in range(len(header)):
    if j == keyIndex:
      continue
    newHeader.append(header[j])

# Add data to rows
for i in range(len(fileContents)):
  data = fileContents[i]['data']
  keyIndex = keyColIndices[i]
  usedKeys = set()
  for row in data:
    key = row[keyIndex]
    usedKeys.add(key)
    for j in range(len(row)):
      if j == keyIndex:
        continue
      rowDict[key].append(row[j])

  # Insert "null" for unused keys
  nullUsed = False
  for k,v in rowDict.items():
    if not k in usedKeys:
      # Found an unused key
      for _ in range(len(data[0]) - 1):
        rowDict[k].append('null')
        nullUsed = True
  if nullUsed:
    print "Note: \"null\" was inserted where the join did not match (this is an outer join)"

# Convert to list of rows
write(newHeader, rowDict.values())