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

if len(fileContents) != 1:
  print "We can only sort one file at a time. Please re-run with one CSV file"
  sys.exit(0)

headers = fileContents[0]['headers']
data = fileContents[0]['data']

sortCols = []
sortDescending = []
addingCols = True
textAddon = "" # For indicating that user is choosing ANOTHER sort column
while addingCols:
  colID = len(headers) + 5
  while colID >= len(headers) or colID < 0:
    print "\nEnter the" + textAddon + " header number to sort by"
    for j in range(len(headers)):
      if j in sortCols:
        continue
      print str(j + 1) + ' - ' + headers[j]
    colID = int(raw_input("> ")) - 1

    if colID >= len(headers) or colID < 0 or colID in sortCols:
      print "Invalid number. Try again..."
    else:
      # Check if descending
      choice = None
      while choice == None:
        text = raw_input("Ascending (enter \"a\") or Descending (enter \"d\"): ")
        if (text == "a"):
          choice = False
        elif (text == "d"):
          choice = True
        else:
          print "Invalid choice. Try again"
      sortDescending.append(choice)
  sortCols.append(colID)

  if len(sortCols) < len(headers):
    choice = None
    while choice == None:
      text = raw_input("Sort by another column (y/n)? ")
      if (text == "y"):
        choice = True
      elif (text = "n"):
        choice = False
      else:
        print "Invalid choice. Try again"
    
    if choice:
      addingCols = True
      textAddon = " next"
    else:
      addingCols = False

# Print sort message
sortMessage = 'Sorting '
for i in range(len(sortCols)):
  if sortDescending[i]:
    sortMessage += "descending by "
  else:
    sortMessage += "ascending by "
  sortMessage += headers[sortCols[i]]
  if i != len(sortCols) - 1:
    sortMessage += ' then '
print sortMessage


# Sort using a comparator
def comparator(a, b):
  for i in range(len(sortCols)):
    col = sortCols[i]
    descending = sortDescending[i]
    if a[col] < b[col]:
      if descending:
        return 1
      else:
        return -1
    elif a[col] > b[col]:
      if descending:
        return -1
      else:
        return 1
  return 0

sortedData = sorted(data, cmp=comparator)
write(headers, sortedData)