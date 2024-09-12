from ROOT import *
import ROOT
import array, math, sys
import os

def is_float_try(str):
    try:
        float(str)
        return True
    except ValueError:
        return False
        
def getHist(filename,var,histname):
        f=open(filename)
        print("File:",filename)
        start=False
        binning=array.array('d')
        lastx=-1
        ys=[]
        for line in f.readlines():
            if "BEGIN" in line and var in line:
              start=True
            if start:
              if "END" in line: break
              s=line.split("	")
              if len(s)==7 and is_float_try(s[0]):
                print(l)
                binning.append(float(s[0]))
                lastx=float(s[1])
                ys+=[float(s[2])]
        binning.append(lastx)
        hist=TH1F(histname,histname,len(binning)-1,binning)
        i=1
        for y in ys:
          hist.SetBinContent(i,y)
          i+=1
        return hist
        
if __name__=="__main__":
  print("start ROOT")
  #gROOT.Reset()
  gROOT.SetStyle("Plain")
  gROOT.SetBatch(True)
  gStyle.SetOptStat(0)
  gStyle.SetOptFit(0)
  gStyle.SetTitleOffset(1.2,"Y")
  gStyle.SetPadLeftMargin(0.15)
  gStyle.SetPadBottomMargin(0.15)
  gStyle.SetPadTopMargin(0.05)
  gStyle.SetPadRightMargin(0.05)
  gStyle.SetMarkerSize(2.5)
  gStyle.SetHistLineWidth(1)
  gStyle.SetStatFontSize(0.020)
  gStyle.SetTitleSize(0.06, "XYZ")
  gStyle.SetLabelSize(0.05, "XYZ")
  gStyle.SetLegendBorderSize(0)
  gStyle.SetPadTickX(1)
  gStyle.SetPadTickY(1)
  gStyle.SetEndErrorSize(5)
  
  for var in ["Jet-softdrop-mass-650","Jet-softdrop-mass-N2-650"]:
  
    canvas=TCanvas("efficiency-"+var, "efficiency-"+var, 0, 0, 300, 300)
    canvas.cd()
    
    hists=[]
    
    colors=[1,2,3,4,6,7,8,9,12,28,34,38,40,41,42,43,44,45,46,47,48,49]
    color=0

    l=TLegend(0.40,0.65,0.95,0.93,"650<p_{T}<725 GeV")
    l.SetTextSize(0.035)
    l.SetFillStyle(0)

    for sample,samplename in [("WJET_MadgraphPythia_12Sep2024","Madgraph+Pythia"),("WJET_MadgraphHerwig_12Sep2024","Madgraph+Herwig")]: #,("WJET_Pythia8_CP5_12Sep2024","Pythia")]:
        filename=sample+".yoda"
        histref=getHist(filename,var,var+sample)
        hist=getHist(filename,var+"-match",var+sample)
        hist.Divide(histref)
        hist.GetXaxis().SetTitle("Softdrop Mass (GeV)")
        hist.GetYaxis().SetTitle("Matching efficiency")
        hist.GetYaxis().SetRangeUser(0,1)
        hist.SetTitle("")
        hists+=[hist]

        #hist.SetLineWidth(1)
        hist.SetLineColor(colors[color])
        hist.SetLineStyle(color%5)
        hist.SetMarkerStyle(20+color)
        hist.SetMarkerColor(colors[color])
        hist.SetMarkerSize(1)

        if samplename=="Pythia8":
          hist.Draw("hist")
        else:
          hist.Draw("histplsame")
              
        l.AddEntry(hist,samplename,"l")
        color+=1

    l.Draw("same")
          
    canvas.SaveAs("matching_efficiency_"+var+".pdf")
