from run import *
from plotADCvBX import *
from capIDtest import *
from ROOT import *

#dataFile = open("internalChargeInjection_00A.txt")

fiber3 = run("internalChargeInjection_00A.txt",3)
fiber4 = run("internalChargeInjection_00A.txt",4)
fiber6 = run("internalChargeInjection_00A.txt",6)

#fiber3.saveToROOT("test.root")
#fiber4.saveToROOT("test.root")
#fiber6.saveToROOT("test.root")

#rootFile = ROOT.TFile("test.root","READ")
#rootTree = rootFile.Get("fiber4")
#rootTree.Show(0)

plotADCvBX( fiber3 , "internalChargeInjectionTest_fiber3" )
plotADCvBX( fiber4 , "internalChargeInjectionTest_fiber4" )

capIDtest( fiber3 , "capIDtest_fiber3" )
capIDtest( fiber4 , "capIDtest_fiber4" )