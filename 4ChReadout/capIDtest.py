from run import *
from ROOT import *


def capIDtest( fiber , fileName ) :

	nbx = len( fiber.eventList[0].bunch )

	capIDdiff = []
	capIDdiff.append( ROOT.TH1F("capIDdiff",";capID_{0} - capID{1};Events (a.u.)" , 8 , -3.5 , 3.5 ) )
	capIDdiff.append( ROOT.TH1F("capIDdiff",";capID_{0} - capID{2};Events (a.u.)" , 8 , -3.5 , 3.5 ) )
	capIDdiff.append( ROOT.TH1F("capIDdiff",";capID_{0} - capID{3};Events (a.u.)" , 8 , -3.5 , 3.5 ) )

	for evt in fiber.eventList :

		for bx in range( nbx ) :

			capIDdiff[0].Fill( evt.bunch[bx].QIE[0].capID - evt.bunch[bx].QIE[1].capID )
			capIDdiff[1].Fill( evt.bunch[bx].QIE[0].capID - evt.bunch[bx].QIE[2].capID )
			capIDdiff[2].Fill( evt.bunch[bx].QIE[0].capID - evt.bunch[bx].QIE[3].capID )

	c = ROOT.TCanvas("c","c",1200,400)
	c.Divide(3)
	c.cd(1)
	capIDdiff[0].Draw()
	c.cd(2)
	capIDdiff[1].Draw()
	c.cd(3)
	capIDdiff[2].Draw()

	c.SaveAs( fileName + ".eps" )
	c.SaveAs( fileName + ".png")