from QIEdata import *

class frame4channel : 


	def __init__( self , bunch = [] ):

		self.rawData = [] # indexed by bytes 
		self.QIE = [ ] #QIEdata() , QIEdata() , QIEdata() , QIEdata() ]

		if len( bunch ) != 3 :
			print "error! bunch doesn't have enough lines"
		elif bunch[0][3:5] != "BC" :
			print "error! comma character missing",bunch[0][3:5] 
		else :
			self.rawData.append( bunch[0][3:5]  )
			self.rawData.append( bunch[0][1:3]  )
			self.rawData.append( bunch[0][9:11] )
			self.rawData.append( bunch[0][7:9]  )
			self.rawData.append( bunch[1][3:5]  )
			self.rawData.append( bunch[1][1:3]  )
			self.rawData.append( bunch[1][9:11] )
			self.rawData.append( bunch[1][7:9]  )
			self.rawData.append( bunch[2][3:5]  )
			self.rawData.append( bunch[2][1:3]  )
			self.rawData.append( bunch[2][9:11] )
			self.rawData.append( bunch[2][7:9]  )

	def convertData( self ) :

		#print self.rawData 

		if len( self.rawData ) != 12 :
			print "frame4channel::convertData - ERROR: data doesn't contain enough information (or too much!)"
			return 
			
		# QIE 0 --------
		TDCE   = ( int( self.rawData[1] , 16 ) & 16 ) / 16
		capID  = ( int( self.rawData[2] , 16 ) & 3 )
		ADC = int( self.rawData[3] , 16 )
		LE_TDC = int( self.rawData[7] , 16 ) & 3 << 4 
		LE_TDC = LE_TDC | int( self.rawData[8] , 16 ) & 3 << 2
		LE_TDC = LE_TDC | int( self.rawData[9] , 16 ) & 3
		TE_TDC = int( self.rawData[10] , 16 ) & 15

		#print "TDCE",TDCE,"capID",capID,"ADC",ADC,"LE_TDC",LE_TDC,"TE_TDC",TE_TDC

		temp = QIEdata( TDCE , capID , ADC , LE_TDC , TE_TDC )
		#temp.printQIE()
		self.QIE.append( temp )

		# QIE 1 --------
		TDCE   = ( int( self.rawData[1] , 16 ) & 32 ) / 32
		capID  = ( int( self.rawData[2] , 16 ) & 12 ) >> 2
		ADC = int( self.rawData[4] , 16 )
		LE_TDC = int( self.rawData[7] , 16 ) & 12 << 2 
		LE_TDC = LE_TDC | int( self.rawData[8] , 16 ) & 12 
		LE_TDC = LE_TDC | int( self.rawData[9] , 16 ) & 12 >> 2
		TE_TDC = ( int( self.rawData[10] , 16 ) & 240 ) >> 4

		temp = QIEdata( TDCE , capID , ADC , LE_TDC , TE_TDC )
		#temp.printQIE()
		self.QIE.append( temp )

		# QIE 2 --------
		TDCE   = ( int( self.rawData[1] , 16 ) & 64 ) / 64
		capID  = ( int( self.rawData[2] , 16 ) & 48 ) >> 4
		ADC = int( self.rawData[5] , 16 )
		LE_TDC = int( self.rawData[7] , 16 ) & 48   
		LE_TDC = LE_TDC | int( self.rawData[8] , 16 ) & 48 >> 2
		LE_TDC = LE_TDC | int( self.rawData[9] , 16 ) & 48 >> 4
		TE_TDC = ( int( self.rawData[11] , 16 ) & 15 )

		temp = QIEdata( TDCE , capID , ADC , LE_TDC , TE_TDC )
		#temp.printQIE()
		self.QIE.append( temp )

		# QIE 3 --------
		TDCE   = ( int( self.rawData[1] , 16 ) & 128 ) / 128
		capID  = ( int( self.rawData[2] , 16 ) & 192 ) >> 6
		ADC = int( self.rawData[6] , 16 )
		LE_TDC = int( self.rawData[7] , 16 ) & 192 >> 2
		LE_TDC = LE_TDC | int( self.rawData[8] , 16 ) & 192 >> 4
		LE_TDC = LE_TDC | int( self.rawData[9] , 16 ) & 192 >> 6
		TE_TDC = ( int( self.rawData[11] , 16 ) & 240 )

		temp = QIEdata( TDCE , capID , ADC , LE_TDC , TE_TDC )
		#temp.printQIE()
		self.QIE.append( temp )

		#self.printData()

	def printData( self ) :

		print self.rawData
		self.QIE[0].printQIE()
		self.QIE[1].printQIE()
		self.QIE[2].printQIE()
		self.QIE[3].printQIE()
		
