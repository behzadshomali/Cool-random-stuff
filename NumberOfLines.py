
# This piece of code will return the number 
# of lines of the files with the indeed 
# extensions. It will search recursively 
# based on its initial address.

import os
import pprint


def numbers_in_dir(base, depth=None, showFilesName=True, currentDepth=0):
	currentDepth += 1
	for fileName in os.listdir(base):
		if not os.path.isdir(base+fileName):

			# Two following lines are extracting
			# extensions from file name
			splitted = fileName.split('.')
			ext = splitted[len(splitted)-1]
			if len(splitted) > 1 and ext in extensions:
				# Check whether file name contains
				# extension and also we're looking for or not
				if showFilesName:
					print('\033[96m' + base, end='')
					print(''.join(splitted[:-1]) + '\033[92m' + '.' + ext) # Pick a different color for extension
				with open(base+fileName, 'r+', encoding = "ISO-8859-1") as f:
					for line in f:
						if line != '\n': # Prevents counting empty lines
							extensionsLinesNumber.setdefault(fileName.split('.')[1], 0)
							extensionsLinesNumber[fileName.split('.')[1]] += 1
		elif os.path.isdir(base+fileName+'/'):
			if depth == None or currentDepth < depth:
				numbers_in_dir(base+fileName+'/', depth, showFilesName, currentDepth)





# Initialization
extensions = ['sh', 'cpp', 'c', 'py', 'txt']
extensionsLinesNumber = {}


baseAddress = input('Enter the indeed directory: ')
baseAddress = './' if baseAddress == '' else baseAddress

try:
	depth = int(input('Enter the indeed depth: '))
except ValueError:
	depth = None


showFilesName = input('Do you want to see the file addresses? ')
showFilesName = True if 'y' in  showFilesName else False



# Starting the program
numbers_in_dir(baseAddress, depth=depth, showFilesName=showFilesName)


# Printing the results
print('\033[96m', '\033[1m')
pprint.pprint(extensionsLinesNumber)