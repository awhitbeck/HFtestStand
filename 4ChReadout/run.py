from event import *
import ROOT
from array import array 

"""
A run is a data structure meant to organize QIE10 data.
The structure is driven by how the data is read out.

A run consists of an array of event(s), which are defined
in event.py.  Each event is an array of bunches, each 
of which is a set of QIE data (4 channels).  The QIE 
data is defined in QIEdata.py.  

run :
--eventList = [] :
  --bunch = [] : ( is of type frame4channel )
    --QIE = [ QIEdata() , QIEdata() , QIEdata() , QIEdata() ] :
      --QIEdata.TDCE
        QIEdata.capID
        QIEdata.ADC
        QIEdata.LE_TDC
        QIEdata.TE_TDC
"""

class run :

    def __init__( self , inputFile = "internalChargeInjection_00A.txt" , fiber_ = 4):

        self.data = []
        self.eventList = []
        self.fiber = fiber_
        keep = False

        dataFile = open("internalChargeInjection_00A.txt")
        
        for line in dataFile : 

            if line[0:-1] == "" and keep : 
                keep = False

                self.eventList.append( event( self.data ) )
                self.data = []

            if keep :
                self.data.append( line[8:19] )

            if line.find("Reading Fiber:"+str(self.fiber) ) != -1 :

                keep = True

    def saveToROOT( self , fileName = "randomFileName.root" ) :

        if len( self.eventList ) == 0 :
            return 

        nbx = len(self.eventList[0].bunch)

        capID1 = array( 'i' , [0]*nbx )
        capID2 = array( 'i' , [0]*nbx )
        capID3 = array( 'i' , [0]*nbx )
        capID4 = array( 'i' , [0]*nbx )

        TDCE1 = array( 'i' , [0]*nbx )
        TDCE2 = array( 'i' , [0]*nbx )
        TDCE3 = array( 'i' , [0]*nbx )
        TDCE4 = array( 'i' , [0]*nbx )

        ADC1 = array( 'i' , [0]*nbx )
        ADC2 = array( 'i' , [0]*nbx )
        ADC3 = array( 'i' , [0]*nbx )
        ADC4 = array( 'i' , [0]*nbx )

        LE_TDC1 = array( 'i' , [0]*nbx )
        LE_TDC2 = array( 'i' , [0]*nbx )
        LE_TDC3 = array( 'i' , [0]*nbx )
        LE_TDC4 = array( 'i' , [0]*nbx )

        TE_TDC1 = array( 'i' , [0]*nbx )
        TE_TDC2 = array( 'i' , [0]*nbx )
        TE_TDC3 = array( 'i' , [0]*nbx )
        TE_TDC4 = array( 'i' , [0]*nbx )

        tree = ROOT.TTree( "fiber" + str(self.fiber) , "fiber" + str(self.fiber) )
        
        ADC1branch = tree.Branch("ADC_Channel1",ADC1,"ADC_Channel1 ["+str(nbx)+"]/I")
        ADC2branch = tree.Branch("ADC_Channel2",ADC2,"ADC_Channel2 ["+str(nbx)+"]/I")
        ADC3branch = tree.Branch("ADC_Channel3",ADC3,"ADC_Channel3 ["+str(nbx)+"]/I")
        ADC4branch = tree.Branch("ADC_Channel4",ADC4,"ADC_Channel4 ["+str(nbx)+"]/I")
                      
        capID1branch = tree.Branch("capID_Channel1",capID1,"capID_Channel1 ["+str(nbx)+"]/I")
        capID2branch = tree.Branch("capID_Channel2",capID2,"capID_Channel2 ["+str(nbx)+"]/I")
        capID3branch = tree.Branch("capID_Channel3",capID3,"capID_Channel3 ["+str(nbx)+"]/I")
        capID4branch = tree.Branch("capID_Channel4",capID4,"capID_Channel4 ["+str(nbx)+"]/I")
                      
        TDCE1branch = tree.Branch("TDCE_Channel1",TDCE1,"TDCE_Channel1 ["+str(nbx)+"]/I")
        TDCE2branch = tree.Branch("TDCE_Channel2",TDCE2,"TDCE_Channel2 ["+str(nbx)+"]/I")
        TDCE3branch = tree.Branch("TDCE_Channel3",TDCE3,"TDCE_Channel3 ["+str(nbx)+"]/I")
        TDCE4branch = tree.Branch("TDCE_Channel4",TDCE4,"TDCE_Channel4 ["+str(nbx)+"]/I")
                      
        LE_TDC1branch = tree.Branch("LE_TDC_Channel1",LE_TDC1,"LE_TDC_Channel1 ["+str(nbx)+"]/I")
        LE_TDC2branch = tree.Branch("LE_TDC_Channel2",LE_TDC2,"LE_TDC_Channel2 ["+str(nbx)+"]/I")
        LE_TDC3branch = tree.Branch("LE_TDC_Channel3",LE_TDC3,"LE_TDC_Channel3 ["+str(nbx)+"]/I")
        LE_TDC4branch = tree.Branch("LE_TDC_Channel4",LE_TDC4,"LE_TDC_Channel4 ["+str(nbx)+"]/I")
                      
        TE_TDC1branch = tree.Branch("TE_TDC_Channel1",TE_TDC1,"TE_TDC_Channel1 ["+str(nbx)+"]/I")
        TE_TDC2branch = tree.Branch("TE_TDC_Channel2",TE_TDC2,"TE_TDC_Channel2 ["+str(nbx)+"]/I")
        TE_TDC3branch = tree.Branch("TE_TDC_Channel3",TE_TDC3,"TE_TDC_Channel3 ["+str(nbx)+"]/I")
        TE_TDC4branch = tree.Branch("TE_TDC_Channel4",TE_TDC4,"TE_TDC_Channel4 ["+str(nbx)+"]/I")

        for evt in self.eventList : 
                
            ADC1branch.SetAddress( ADC1 )
            ADC2branch.SetAddress( ADC2 )
            ADC3branch.SetAddress( ADC3 )
            ADC4branch.SetAddress( ADC4 )
            
            capID1branch.SetAddress( capID1 )
            capID2branch.SetAddress( capID2 )
            capID3branch.SetAddress( capID3 )
            capID4branch.SetAddress( capID4 )
            
            TDCE1branch.SetAddress( TDCE1 )
            TDCE2branch.SetAddress( TDCE2 )
            TDCE3branch.SetAddress( TDCE3 )
            TDCE4branch.SetAddress( TDCE4 )
            
            LE_TDC1branch.SetAddress( LE_TDC1 )
            LE_TDC2branch.SetAddress( LE_TDC2 )
            LE_TDC3branch.SetAddress( LE_TDC3 )
            LE_TDC4branch.SetAddress( LE_TDC4 )
            
            TE_TDC1branch.SetAddress( TE_TDC1 )
            TE_TDC2branch.SetAddress( TE_TDC2 )
            TE_TDC3branch.SetAddress( TE_TDC3 )
            TE_TDC4branch.SetAddress( TE_TDC4 )

            if len( evt.bunch ) != nbx :
                print "run::saveToROOT - ERROR: event doesn't has a different number of bunches!"
                continue

            for bx in range( nbx ) : # evt.bunch :
                
                #print bx
                #bx.printData()
                #bx.QIE[0].printQIE()

                if len( evt.bunch[bx].QIE ) < 4 : 
                    print "run::saveToROOT - ERROR: bunch doesn't have info for all QIEs"
                    continue

                ADC1[bx]= evt.bunch[bx].QIE[0].ADC
                ADC2[bx]= evt.bunch[bx].QIE[1].ADC 
                ADC3[bx]= evt.bunch[bx].QIE[2].ADC 
                ADC4[bx]= evt.bunch[bx].QIE[3].ADC 

                capID1[bx]= evt.bunch[bx].QIE[0].capID 
                capID2[bx]= evt.bunch[bx].QIE[1].capID 
                capID3[bx]= evt.bunch[bx].QIE[2].capID 
                capID4[bx]= evt.bunch[bx].QIE[3].capID 

                TDCE1[bx]= evt.bunch[bx].QIE[0].TDCE 
                TDCE2[bx]= evt.bunch[bx].QIE[1].TDCE 
                TDCE3[bx]= evt.bunch[bx].QIE[2].TDCE 
                TDCE4[bx]= evt.bunch[bx].QIE[3].TDCE 

                LE_TDC1[bx]= evt.bunch[bx].QIE[0].LE_TDC 
                LE_TDC2[bx]= evt.bunch[bx].QIE[1].LE_TDC 
                LE_TDC3[bx]= evt.bunch[bx].QIE[2].LE_TDC 
                LE_TDC4[bx]= evt.bunch[bx].QIE[3].LE_TDC 

                TE_TDC1[bx]= evt.bunch[bx].QIE[0].TE_TDC 
                TE_TDC2[bx]= evt.bunch[bx].QIE[1].TE_TDC 
                TE_TDC3[bx]= evt.bunch[bx].QIE[2].TE_TDC 
                TE_TDC4[bx]= evt.bunch[bx].QIE[3].TE_TDC 

            print ADC1

            tree.Fill()

        rootFile = ROOT.TFile(fileName,"UPDATE")
        tree.Write()
        rootFile.Close()
