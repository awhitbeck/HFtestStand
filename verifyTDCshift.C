


void verifyTDCshift(TString fileName = "verifyTDCshift_Channel6.root", int chan = 5){

  gROOT->ProcessLine(".L ~/tdrstyle.C");
  setTDRStyle();

  TFile* f = new TFile(fileName);

  char temp[256];
  sprintf(temp,"hBX_ADC%i",chan);

  TH2F* ADC = f->Get(temp);
  ADC->SetMarkerColor(2);

  sprintf(temp,"hBX_TDC%i",chan);
  TH2F* TDC = f->Get(temp);
  TDC->SetMarkerColor(4);

  ADC->Draw();
  TDC->Draw("SAME");

}
