# script for decoding data read out from
# HCal uHTR spy buffer

# A. Whitbeck - March 28, 2014
# K. Call - June 2014

#QIElinearization is from Totes, it contains an array. The index corresponds to the info
#from the QIE, R+M, each value of the array corresponds to the accumulated charge in
#microcolombs
from QIElinearization import *

#OptionParser is a library that facilitates reading options passed from the command-
#line 
from optparse import OptionParser

import os	#This provides access to OS dependant functionality
import sys	#We use this to exit out of the script early

import ROOT	#This provides the bindings to manipulate root object. We use to create the 
		#root file

from array import array #This module is imported to provide array functionality


#This function is a little more complicated since the TDC information is not aligned with the
#byte boundaries

#This function returns a list, the first element of which is a string "TDC", the following
#elements are the TDC values as integers in order
def organizeTDC( frame = [] ) :
 
	TDC = []
	TDC.append( "TDC" )
	#Take the last 2 bits of byte eight and stick them in front of the first 4 bits
	#of byte 1
	TDC.append( ( int( frame[ 8 ] , 16 ) & 3 ) << 4 | ( int( frame[ 1 ] , 16 ) >> 4 ) )

	#Take the first 6 bits of byte 8
	TDC.append( int( frame[ 8 ] , 16 ) >> 2 )

	#Take the last 6 bits of byte 9
	TDC.append( int( frame[ 9 ] , 16 ) & 63 )

	#Take the last 4 bits from byte 10 and stick them in front of the first 2 bits
	#from byte 9
	TDC.append( ( int( frame[ 10 ] , 16 ) & 15 ) << 2 | ( int( frame[ 9 ] , 16 ) >> 6 ) )

	#Take the last two bits from byte 11 and place them infront of the first 4 bits from
	#byte 10
	TDC.append( ( int( frame[ 11 ] , 16 ) & 3  ) << 4 | ( int( frame[ 10 ] , 16 ) >> 4 ) )

	#Take the first 6 bits from byte 11
	TDC.append( int( frame[ 11 ] , 16 ) >> 2 )

	return TDC

#This is an extremely straight forward function, it looks at bytes 2-7 then converts them
#from hexadecimal strings into ints.

#This function returns a list, the first element of which is a string "ADC", the following
#elements are ADC values as integers in order
def organizeADC( frame = [] ) :

	ADC = []
	ADC.append( "ADC" )
	ADC.append( int( frame[ 2 ] , 16 ) )
	ADC.append( int( frame[ 3 ] , 16 ) )
	ADC.append( int( frame[ 4 ] , 16 ) )
	ADC.append( int( frame[ 5 ] , 16 ) )
	ADC.append( int( frame[ 6 ] , 16 ) )
	ADC.append( int( frame[ 7 ] , 16 ) )
 
 	return ADC

#extractFrames is called from the function "decodeFiber" It is passed list list of all of the bunch crossings
def extractFrames( fiber = [] ) :

	frames = []	#We prepare an empty list to receive the extractedFrames
	frame = []	#This will hold the frame of data as we prepare it

	for bunchcrossing in fiber : #We loop over each of the bunch crossings in the fiber

		#The substring "BC" should be found in the first line of each bunchcrossing
		#If it is not present then there is an issue with the data and we skip over this bunchcrossing
		if bunchcrossing[0].find("BC") != -1:

			#We next check to make sure that the bunchcrossing has the expected number of lines
			if len(bunchcrossing) != 3:
				continue

			#In these next lines we slice the lines apart in order to extract the
			#data that we are interested in

			frame = [];
			frame.append(bunchcrossing[0][  9 : 11 ])
			frame.append(bunchcrossing[0][ 11 : 13 ])
			frame.append(bunchcrossing[0][ 15 : 17 ]) 
			frame.append(bunchcrossing[0][ 17 : 19 ]) 
			frame.append(bunchcrossing[1][  9 : 11 ])
			frame.append(bunchcrossing[1][ 11 : 13 ])
			frame.append(bunchcrossing[1][ 15 : 17 ])
			frame.append(bunchcrossing[1][ 17 : 19 ])
			frame.append(bunchcrossing[2][  9 : 11 ])
			frame.append(bunchcrossing[2][ 11 : 13 ])
			frame.append(bunchcrossing[2][ 15 : 17 ])
			frame.append(bunchcrossing[2][ 17 : 19 ])

			#Here we are transposing the position of some of the elements
			#We do this because the bytes are reported this way vs. the format
			#reported in the technical upgrade document
			frame[0],  frame[1]  = frame[1],  frame[0]
			frame[2],  frame[3]  = frame[3],  frame[2]
			frame[4],  frame[5]  = frame[5],  frame[4]
			frame[6],  frame[7]  = frame[7],  frame[6]
			frame[8],  frame[9]  = frame[9],  frame[8]
			frame[10], frame[11] = frame[11], frame[10]

			frames.append(frame)

	return frames

#The function is a reformulation of the decodeEvent function
def decodeFiber( fiber = [] ) :

	frames = extractFrames(fiber[1:])	#The first element is number

	table = []

	for i in frames : 
	
		#We need to check that the extractFrames function was able to get all of the
		#bytes out that we expected
		if len( i ) == 12  :
		
			#int( ) used in this case converts the string into an integer,
			#we have explicitly told it in this case that it is recorded in
			#hexadecimal
			
			#We shift right two places, then take the 2 right most bits
			capid = ( int( i[1], 16 ) >> 2 ) & 3

			#We shift right one place, then take the single right most bit
			ce    = ( int( i[1] , 16 ) >> 1) & 1

			#We take the right most bit
			bc0   = ( int( i[1] , 16 ) ) & 1

			#We call organizeTDC in order to extract the TDC information from
			#the event
			TDC = organizeTDC(i)
			#We do the same with organizeADC
			ADC = organizeADC(i)

			#We stick 4 element lists containing the TDC and ADC lists
			#and the capid, ce, and bc0 into the table
			table.append( [TDC,ADC,capid,ce,bc0] )

	return table

def linearize( ADCs = [] ) :

	charge = []

	for ADC in ADCs : 

		charge.append( bin_charge[ ADC ] )

	return charge

#This marks start of execution, all of the previous code defined functions that will be used here

parser = OptionParser() #We create the option parser object

#We tell the OptionParser what options we expect and what to do with them.

#You provide two formats that the option can take, single dash with a single letter,
#and double dash with a word, you provide the name of the variable in which to place the
#value of the parameter passed, and short description of the option which can then be reported
#by invoking the "-h" option ("--help" as well.)

#This option is used to identify the filename to be read. It assumes that the file extension is
# "txt" therefore this part should be obmitted. It will write the ouput file to the same name,
# but with the "root" extension
parser.add_option("-f", "--file", dest="filename",
                  help="read data from <file>.txt and write to <file>.root")

#We now parse the arguments passed at the command-line. This is done by invoking the
#parse_args() function of the parser object. It reads the options from the argument vector
#sys.argv[:]

#There are two variables returned, "options" an object containing the the value of all of the #objects identified, and "args" which contain the strings left over from the command line after
#the options have been parsed out.
(options, args) = parser.parse_args()

#First we check whether a filename has been provided
if not options.filename:
	print("You must specify a filename.")
	print("Please provide the name of the data file without the txt extension.")
	sys.exit(2)

try:
	txtFile = open( options.filename + ".txt" )
except IOError:
	print("Cannot open "+options.filename+".txt")
	print("Check that you have provided the filename without the txt extension.")
	sys.exit()

print "Decoding: "+options.filename+".txt" 

events = []			#This creates events and formattedEvents as empty lists
formattedEvents = []

#We will use the following variables as we iterate through the file
#At the end of the iterations we will have the variable events which is a list of "event"s
#Which contain fibers, which contain bunchCrossings
fEventParse = False	#We are currently parsing an event
fFiberParse = False	#We are currently parsing a Fiber
bunchCrossing = []	#We will build our bunch crossing in here
event = []		#We will build our event in here
curfiber = []		#We will build our fiber in here
linenumber = -1		#We use this to track which line in a group of three we expect to be on
eventNumber = 0		#We use these two variable to extraxt the event and fiber number
fiberNumber = 0

fiberNumbers = []	#We use this to track the fiber numbers in the file

nbx = 0;		#We use these variables to count the number of bunchcrossings in an event
tnbx = 0;



#We iterate over every line in the in the opened file
for line in txtFile :


	#First we check if we are currently parsing an event
	if not fEventParse:

		#we check the line to see if it contains the substring "START EVENT"

		#If it contains the string start event, then we will mark that we are parsing
		#an event then continue looking at the lines
		if line.find("START EVENT") != -1:
			fEventParse = True
			event = []	#We make sure that the event list is clear
			eventNumber = int(filter(str.isdigit, line))
			event.append(eventNumber), #The first element of the event list is the event number
			tnbx = 0

			#print "Event: "+str(eventNumber)

		#It does not matter if we found "Start Event" or not,
		#we continue to the next line
		continue
	
	#The simplest way to identify if we have started parsing another event is to check if
	#another event has started while we think that we are currently parsing an event
	else:

		if line.find("START EVENT") != -1:
			
			#We need to check if we still think that we are parsing a fiber, if so we close it out
			if fFiberParse:
				event.append(curfiber)
				fFiberParse = False
				curfiber = []
				tnbx = 0		#We reset the bunch crossing counter for this fiber
				linenumber = -1
				
			#Now we stuff the current event into the events lists
			events.append(event)

			#and clear out the event list, in preparation for this new event
			event = []

			#and start the next event
			eventNumber = int(filter(str.isdigit,line))
			event.append(eventNumber) #The first element of the event list is the event number

			#print "Event: "+str(eventNumber)

			#We continue to the next line
			continue

	#Next we check if we are currently parsing a fiber
	if not fFiberParse:

		#we check the line to see if it contains the substring "Reading Fiber"
		if line.find("Reading Fiber") != -1:
			fFiberParse = True
			linenumber = 0	#We expect the next line to be the
					#first number in a group of three

			curfiber = []	#We make sure that the fiber list is empty
			fiberNumber = int(filter(str.isdigit,line[line.find("Fiber"):])) #The number after fiber
			tnbx = 0;	#We reset our counter for the number of bunchcrossing			

			#We stick the fiber number in as the first element of the list
			curfiber.append(fiberNumber)

			#print "Fiber: "+str(eventNumber)

			#We then add the fiber number to the list of fibers in this data file
			fiberfound = False
			for i in fiberNumbers:
				if i == fiberNumber:
					fiberfound = True
					break

			if not fiberfound:
				fiberNumbers.append(fiberNumber)

		#It does not matter if the substring was found or not,
		#we continue to the next line
		continue

	#If we have reached this point then both the fEventParse and fFiberParse flags are set
	#We will now extact the lines in groups of three.

	if linenumber == 0:
		
		#The first line should include the substring "CAP"
		if line.find("CAP") != -1:
			bunchCrossing = []		#We make sure that the list is empty
			bunchCrossing.append(line)	#We stick the first line into bunchCrossing
			linenumber = 1

		#The file is not following the format that we expect, or we have exhausted the
		#bunchcrossings in the event, we signal that the fiber is finished parsing
		else:
			linenumber = -1		#We mark that we are no longer in
							#valid group of three lines
			fFiberParse = False;		#We mark that we are no longer parsing a fiber
			event.append(curfiber)		#We stuff the fiber into the event
			tnbx = 0

		continue

	elif linenumber == 1:

		#The second line should include the substring "ADC"
		if line.find("ADC") != -1:
			bunchCrossing.append(line)
			linenumber = 2

		#The file is not following the format that we expect, we mark the fiber ended and
		#continue
		else:
			bunchCrossing = []
			linenumber = -1
			fFiberParse = False
			event.append(curfiber)	#We stuff the fiber into the event
			tnbx = 0

		continue

	elif linenumber == 2:

		#The third line should include the substring "TDC"
		if line.find("TDC") != -1:
			bunchCrossing.append(line)
			curfiber.append(bunchCrossing)	#We stuff the bunchCrossing into the fiber list

			tnbx = tnbx + 1

			if tnbx > nbx:
				nbx = tnbx

			#print "TNBX: "+str(tnbx)
			#print "NBX: "+str(nbx)

			linenumber = 0
			bunchCrossing = []

		#The file is not following the format that we expect, we mark the fiber ended and continue
		else:
			bunchCrossing = []
			linenumber = -1
			fFiberParse = False
			event.append(curfiber)	#We stuff the fiber into the event
			tnbx = 0

		continue

	#This code should never execute
	elif linenumber == -1:

		print "Check you code linenumber = -1"

#This is the end of the for loop, at this point we need to clean things up
#as the last fiber of the last event may not yet be saved

else:
	if fEventParse:

		if fFiberParse:
			event.append(curfiber)

		events.append(event)

dataTrees = {}						

#We create a TTree object for each of the fiber numbers identified in the datafile, 
#note that the the name and the title have been set identically
for number in fiberNumbers:
	dataTrees[number] = ROOT.TTree("fiber"+str(number),"fiber"+str(number))

#We open the root file
dataFile = ROOT.TFile(options.filename+".root","UPDATE")

#The following commands create arrays of singned int with the given initial values
ADC1 = array( 'i' , [1,2,3,4,5] )
ADC2 = array( 'i' , [1,2,3,4,5] )
ADC3 = array( 'i' , [1,2,3,4,5] )
ADC4 = array( 'i' , [1,2,3,4,5] )
ADC5 = array( 'i' , [1,2,3,4,5] )
ADC6 = array( 'i' , [1,2,3,4,5] )

TDC1 = array( 'i' , [1,2,3,4,5] )
TDC2 = array( 'i' , [1,2,3,4,5] )
TDC3 = array( 'i' , [1,2,3,4,5] )
TDC4 = array( 'i' , [1,2,3,4,5] )
TDC5 = array( 'i' , [1,2,3,4,5] )
TDC6 = array( 'i' , [1,2,3,4,5] )

#The following commands create arrays of floats with the given initial values
Q1 = array( 'f' , [1,2,3,4,5] )
Q2 = array( 'f' , [1,2,3,4,5] )
Q3 = array( 'f' , [1,2,3,4,5] )
Q4 = array( 'f' , [1,2,3,4,5] )
Q5 = array( 'f' , [1,2,3,4,5] )
Q6 = array( 'f' , [1,2,3,4,5] )

CAPID = array( 'i' , [0,0,0,0] )
CAPIDerror = array( 'i' , [] )
BC0 = array( 'i' , [] )

#We will set up these variables as dicts, it will allow us to refer to the individual branches by fiber number

ADC1branch = {}
ADC2branch = {}
ADC3branch = {}
ADC4branch = {}
ADC5branch = {}
ADC6branch = {}

TDC1branch = {}
TDC2branch = {}
TDC3branch = {}
TDC4branch = {}
TDC5branch = {}
TDC6branch = {}

Q1branch = {}
Q2branch = {}
Q3branch = {}
Q4branch = {}
Q5branch = {}
Q6branch = {}

CAPIDbranch = {}
CAPIDerrorbranch = {}
BC0branch = {}

#print "NBX: "+str(nbx)

for i in fiberNumbers:
	
	ADC1branch[i] = dataTrees[i].Branch("ADC_Channel1",ADC1,"ADC_Channel1 ["+str(nbx)+"]/I")
	ADC2branch[i] = dataTrees[i].Branch("ADC_Channel2",ADC2,"ADC_Channel2 ["+str(nbx)+"]/I")
	ADC3branch[i] = dataTrees[i].Branch("ADC_Channel3",ADC3,"ADC_Channel3 ["+str(nbx)+"]/I")
	ADC4branch[i] = dataTrees[i].Branch("ADC_Channel4",ADC4,"ADC_Channel4 ["+str(nbx)+"]/I")
	ADC5branch[i] = dataTrees[i].Branch("ADC_Channel5",ADC5,"ADC_Channel5 ["+str(nbx)+"]/I")
	ADC6branch[i] = dataTrees[i].Branch("ADC_Channel6",ADC6,"ADC_Channel6 ["+str(nbx)+"]/I")

	TDC1branch[i] = dataTrees[i].Branch("TDC_Channel1",TDC1,"TDC_Channel1 ["+str(nbx)+"]/I")
	TDC2branch[i] = dataTrees[i].Branch("TDC_Channel2",TDC2,"TDC_Channel2 ["+str(nbx)+"]/I")
	TDC3branch[i] = dataTrees[i].Branch("TDC_Channel3",TDC3,"TDC_Channel3 ["+str(nbx)+"]/I")
	TDC4branch[i] = dataTrees[i].Branch("TDC_Channel4",TDC4,"TDC_Channel4 ["+str(nbx)+"]/I")
	TDC5branch[i] = dataTrees[i].Branch("TDC_Channel5",TDC5,"TDC_Channel5 ["+str(nbx)+"]/I")
	TDC6branch[i] = dataTrees[i].Branch("TDC_Channel6",TDC6,"TDC_Channel6 ["+str(nbx)+"]/I")

	Q1branch[i] = dataTrees[i].Branch("Q_Channel1",Q1,"Q_Channel1 ["+str(nbx)+"]/F")
	Q2branch[i] = dataTrees[i].Branch("Q_Channel2",Q2,"Q_Channel2 ["+str(nbx)+"]/F")
	Q3branch[i] = dataTrees[i].Branch("Q_Channel3",Q3,"Q_Channel3 ["+str(nbx)+"]/F")
	Q4branch[i] = dataTrees[i].Branch("Q_Channel4",Q4,"Q_Channel4 ["+str(nbx)+"]/F")
	Q5branch[i] = dataTrees[i].Branch("Q_Channel5",Q5,"Q_Channel5 ["+str(nbx)+"]/F")
	Q6branch[i] = dataTrees[i].Branch("Q_Channel6",Q6,"Q_Channel6 ["+str(nbx)+"]/F")

	CAPIDbranch[i] = dataTrees[i].Branch("CAPID", CAPID, "CAPID ["+str(nbx)+"]/I" )
	CAPIDerrorbranch[i] = dataTrees[i].Branch("CAPIDerror", CAPIDerror, "CAPIDerror ["+str(nbx)+"]/I" )
	BC0branch[i] = dataTrees[i].Branch("BC0", BC0, "BC0 ["+str(nbx)+"]/I" )

#The TH2F object creates a 2-D histogram
#pulseShape2D = []
#pulseShape2D.append( ROOT.TH2F("pulse2D_ch1","pulse2D_ch1",nbx,0,nbx,2000,0,7000) )
#pulseShape2D.append( ROOT.TH2F("pulse2D_ch2","pulse2D_ch2",nbx,0,nbx,2000,0,7000) )
#pulseShape2D.append( ROOT.TH2F("pulse2D_ch3","pulse2D_ch3",nbx,0,nbx,2000,0,7000) )
#pulseShape2D.append( ROOT.TH2F("pulse2D_ch4","pulse2D_ch4",nbx,0,nbx,2000,0,7000) )
#pulseShape2D.append( ROOT.TH2F("pulse2D_ch5","pulse2D_ch5",nbx,0,nbx,2000,0,7000) )
#pulseShape2D.append( ROOT.TH2F("pulse2D_ch6","pulse2D_ch6",nbx,0,nbx,2000,0,7000) )


#We iterate over each of the events in the data file
for event in events :

	#We then iterate over each of the fibers in the data file, we skip the first element, since it is a number
	for fiber in event[1:]:

		fiberNumber = int(fiber[0])	#This is the fiber number

		#We extract the information from the fiber
		#This returns a list than contains the ADCs, TDCs, capid and ce for each bunchcrossing
		formattedFiber = decodeFiber(fiber)

		ADC = []
		TDC = []
		capid = []
		ce = []
		bc0 = []
	
		#We take the table returned from decodeFiber and break out the integer values
		#to place in the ADC and TDC lists.
		for bunchCrossing in formattedFiber : 

			ADC.append( bunchCrossing[1][1:7] )
			TDC.append( bunchCrossing[0][1:7] )
			capid.append(bunchCrossing[2])
			ce.append(bunchCrossing[3])
			bc0.append(bunchCrossing[4])

		#Here we create arrays of signed integers they are composed of the
		#sequence of values for each ADC through the event

		#Note the use of zip(* ), in a sense this a transpose operation
		#We need to check that the vector is valid, it may not be if there was an issue with the data
		if ADC:
			ADC1 = array ( 'i' , list(zip(*ADC)[0]) )
			ADC2 = array ( 'i' , list(zip(*ADC)[1]) )
			ADC3 = array ( 'i' , list(zip(*ADC)[2]) )
			ADC4 = array ( 'i' , list(zip(*ADC)[3]) )
			ADC5 = array ( 'i' , list(zip(*ADC)[4]) )
			ADC6 = array ( 'i' , list(zip(*ADC)[5]) )
		else:
			continue

		TDC1 = array ( 'i' , list(zip(*TDC)[0]) )
		TDC2 = array ( 'i' , list(zip(*TDC)[1]) )
		TDC3 = array ( 'i' , list(zip(*TDC)[2]) )
		TDC4 = array ( 'i' , list(zip(*TDC)[3]) )
		TDC5 = array ( 'i' , list(zip(*TDC)[4]) )
		TDC6 = array ( 'i' , list(zip(*TDC)[5]) )

		#The Q arrays are similar to the ADC arrays but have be changed into units of charge
		Q1 = array( 'f', linearize( list(zip(*ADC)[0]) ))
		Q2 = array( 'f', linearize( list(zip(*ADC)[1]) ))
		Q3 = array( 'f', linearize( list(zip(*ADC)[2]) ))
		Q4 = array( 'f', linearize( list(zip(*ADC)[3]) ))
		Q5 = array( 'f', linearize( list(zip(*ADC)[4]) ))
		Q6 = array( 'f', linearize( list(zip(*ADC)[5]) ))

#		for ch in range( 6 ) :
#			Qtemp = linearize( list(zip(*ADC)[ch]) )
#			for i in range ( len( Qtemp ) )  : 
#				pulseShape2D[ch].Fill( i , Qtemp[i] )

		ADC1branch[fiberNumber].SetAddress( ADC1 )
		ADC2branch[fiberNumber].SetAddress( ADC2 )
		ADC3branch[fiberNumber].SetAddress( ADC3 )
		ADC4branch[fiberNumber].SetAddress( ADC4 )
		ADC5branch[fiberNumber].SetAddress( ADC5 )
		ADC6branch[fiberNumber].SetAddress( ADC6 )

		TDC1branch[fiberNumber].SetAddress( TDC1 )
		TDC2branch[fiberNumber].SetAddress( TDC2 )
		TDC3branch[fiberNumber].SetAddress( TDC3 )
		TDC4branch[fiberNumber].SetAddress( TDC4 )
		TDC5branch[fiberNumber].SetAddress( TDC5 )
		TDC6branch[fiberNumber].SetAddress( TDC6 )

		Q1branch[fiberNumber].SetAddress( Q1 )
		Q2branch[fiberNumber].SetAddress( Q2 )
		Q3branch[fiberNumber].SetAddress( Q3 )
		Q4branch[fiberNumber].SetAddress( Q4 )
		Q5branch[fiberNumber].SetAddress( Q5 )
		Q6branch[fiberNumber].SetAddress( Q6 )


		CAPID = array( 'i' , capid )
		CAPIDerror = array( 'i' , ce)
		BC0 = array( 'i' , bc0 )


		CAPIDbranch[fiberNumber].SetAddress( CAPID )
		CAPIDerrorbranch[fiberNumber].SetAddress( CAPIDerror )
		BC0branch[fiberNumber].SetAddress( BC0 )

		dataTrees[fiberNumber].Fill()

#pulseShape = []

for i in fiberNumbers:
	dataTrees[i].Write()

#for ch in range( 6 ) :
#	pulseShape.append( pulseShape2D[ch].ProfileX("pulse1D_ch"+str(ch) ) )
#	pulseShape2D[ch].Write()
#	pulseShape[ch].Write()

dataFile.Close()

print "Completed Extraction for "+options.filename+".txt"
