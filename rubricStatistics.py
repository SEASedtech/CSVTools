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
if len(fileContents) != 1:
  print "You can only run this script on one CSV file"
  sys.exit(0)

headers = fileContents[0]['headers']
data = fileContents[0]['data']

newHeader = ['Rubric Name', 'Avg Points', 'Num Graded', 'Num to Grade', 'Total Students', 'Percent Graded'] # Each column is a rubric item
rows = [] # Each row is a rubric item

for i in range(len(headers)):
  header = headers[i]
  # Skip columns that aren't for rubric items
  if not header.startswith('Rubric Points: '):
    continue

  # Get rubric item name
  rubricName = header[len('Rubric Points: '):].split('(max ')[0].strip()
  avgPoints = 0.0
  numGraded = 0
  totalStudents = len(data)

  for student in data:
    points = student[i]
    if points.startswith('null'):
      # Null (not graded)
      continue

    try:
      avgPoints += float(int(points))
      numGraded += 1
    except ValueError:
      continue

  avgPoints /= float(totalStudents)
  numToGrade = totalStudents - numGraded
  percentGraded = (float(numGraded) / float(totalStudents)) * 100

  rows.append([rubricName, avgPoints, numGraded, numToGrade, totalStudents, percentGraded])

# Convert to list of rows
write(newHeader, rows)