from frame4channel import *

class event :

	def __init__( self , data = [] ) :

		self.bunch = []

		if len( data ) % 3 != 0 :
			print "ERROR: not enough lines in this event..."
		else:
			for i in range( 0 , len( data ) , 3 ) :
				bunchString = [ data[i] , data[i+1] , data[i+2] ]
				self.bunch.append( frame4channel( bunchString ) )
				self.bunch[-1].convertData()
				#print " - - - - - - - - - - - - - - "


	def printEvent( self ):

		for bx in self.bunch :
			print bx.rawData


		
