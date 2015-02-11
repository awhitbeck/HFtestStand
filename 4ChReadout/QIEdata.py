class QIEdata :

	def __init__( self , 
			      TDCE_ = -1 ,
			      capID_ = -1 , 
			      ADC_ = -1 , 
			      LE_TDC_ = -1 , 
			      TE_TDC_ = -1 
			      ) : 

		self.TDCE = TDCE_
		self.capID = capID_
		self.ADC = ADC_
		self.LE_TDC = LE_TDC_
		self.TE_TDC = TE_TDC_

	def setData (self , 
			      TDCE_ ,
			      capID_ , 
			      ADC_ , 
			      LE_TDC_ , 
			      TE_TDC_ 
			      ) :

		self.TDCE = TDCE_
		self.capID = capID_
		self.ADC = ADC_
		self.LE_TDC = LE_TDC_
		self.TE_TDC = TE_TDC_

	def printQIE( self ) :

		print "TDCE",self.TDCE,"capID",self.capID,"ADC",self.ADC,"LE_TDC",self.LE_TDC,"TE_TDC",self.TE_TDC

