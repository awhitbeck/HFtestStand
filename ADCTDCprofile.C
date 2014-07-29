void ADCTDCprofile(char* fileName = "test_summer14_testBeam" , int fiber = 2, 
		   int chan = 6){

  gROOT->ProcessLine(".L ~/tdrstyle.C");
  setTDRStyle();
  gStyle->SetPadTickY(0);

  TCanvas *c1 = new TCanvas("c1","ADC/TDC profile",600,600);

  char inputFile[256];
  sprintf(inputFile,"%s.root",fileName);
  TFile* f = new TFile(inputFile , "READ" );
  char fiberName[256];
  sprintf(fiberName,"fiber%i",fiber);
  TTree* t = f->Get(fiberName);

  //get ADC vs BX histo
  char temp[256];
  sprintf(temp,"hBX_ADC%i",chan-1);
  TH2F *ADC2 = f->Get(temp);
  TH1F *ADC = (TH1F*) ADC2->ProfileX("ADC");
  ADC->GetYaxis()->SetRangeUser(0,256);
  ADC->SetMarkerColor(2);
  ADC->SetMarkerStyle(8);
  ADC->GetYaxis()->SetTitle("ADC code");
  ADC->GetXaxis()->SetTitle("Bunch Crossing");

  //get TDC vs BX histo
  sprintf(temp,"hBX_TDC%i",chan-1);
  TH2F* TDC2 = f->Get(temp);
  TH1F* TDC = (TH1F*) TDC2->ProfileX("TDC");
  TDC->SetMarkerColor(4);
  TDC->SetMarkerStyle(8);

  //scale hint1 to the pad coordinates
  Float_t rightmax = 70.;
  Float_t scale = 256./rightmax;
  TDC->Scale(scale);

  ADC->Draw("");
  TDC->Draw("same");

  //draw an axis on the right side
  TGaxis *axis = new TGaxis(21,0,
			    21,256,0,rightmax,510,"+L");
  axis->SetLineColor(kBlue);
  axis->SetTextColor(kBlue);
  axis->SetTitle("TDC code");
  axis->Draw();

  char outputFile[256];
  sprintf(outputFile,"%s_fiber%i_chan_%i.png",fileName,fiber,chan);
  c1->SaveAs(outputFile);


}
