from run import *
from ROOT import *

def plotADCvBX( fiber , fileName ) :

	nbx = len( fiber.eventList[0].bunch )

	ADCprofile = []
	ADCprofile.append( ROOT.TH2F("ADCprofile1",";BX;ADC",nbx,-0.5,nbx-.5,256,0,256) )
	ADCprofile.append( ROOT.TH2F("ADCprofile2",";BX;ADC",nbx,-0.5,nbx-.5,256,0,256) )
	ADCprofile.append( ROOT.TH2F("ADCprofile3",";BX;ADC",nbx,-0.5,nbx-.5,256,0,256) )
	ADCprofile.append( ROOT.TH2F("ADCprofile4",";BX;ADC",nbx,-0.5,nbx-.5,256,0,256) )

	for qie in range( 4 ) :

		for evt in fiber.eventList :

			for bx in range( nbx ) :

				ADCprofile[qie].Fill( bx , evt.bunch[bx].QIE[qie].ADC )

	c = ROOT.TCanvas("c","c",1000,1000)
	c.Divide(2,2)
	c.cd(1)
	ADCprofile[0].Draw()
	c.cd(2)
	ADCprofile[1].Draw()
	c.cd(3)
	ADCprofile[2].Draw()
	c.cd(4)
	ADCprofile[3].Draw()

	c.SaveAs( fileName + ".eps" )
	c.SaveAs( fileName + ".png")