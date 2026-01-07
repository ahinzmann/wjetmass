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
                ys+=[(float(s[2]),sqrt(float(s[3])))]
        binning.append(lastx)
        hist=TH1F(histname,histname,len(binning)-1,binning)
        i=1
        for y,ye in ys:
          hist.SetBinContent(i,y)
          hist.SetBinError(i,ye)
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
  
  model_uncertainty_map={}

  pt=0
  histmap={}
  for var in ["d03-x01-y01","d05-x01-y01","d07-x01-y01","d09-x01-y01",
              "d03-x01-y02","d05-x01-y02","d07-x01-y02","d09-x01-y02",
              "d03-x01-y03","d05-x01-y03","d07-x01-y03","d09-x01-y03",
              ]:
    matchstr="_matched" if "y02" in var else "_unmatched" if "y03" in var else ""
    if "d03" in var: pt=0
  
    canvas=TCanvas("model_uncertainty-"+var, "model_uncertainty-"+var, 0, 0, 300, 300)
    canvas.cd()
    
    hists=[]
    
    colors=[1,2,3,4,6,7,8,9,12,28,34,38,40,41,42,43,44,45,46,47,48,49]
    color=0

    l=TLegend(0.40,0.65,0.95,0.93,str(pt)+matchstr)
    l.SetTextSize(0.035)
    l.SetFillStyle(0)
    
    first=True
    for sample,samplename in [("WJET_MadgraphPythia_12Sep2024","Madgraph+Pythia"),("WJET_MadgraphHerwig_12Sep2024","Madgraph+Herwig"),("WJET_Pythia8_CP5_12Sep2024","Pythia")]:
        filename=sample+".yoda"
        hist=getHist(filename,var,var+sample)
        for b in range(hist.GetNbinsX()):
          hist.SetBinContent(b+1,hist.GetBinContent(b+1)/hist.GetBinWidth(b+1))

        hist.GetXaxis().SetTitle("Softdrop Mass (GeV)")
        hist.GetYaxis().SetTitle("Cross section")
        hist.GetYaxis().SetRangeUser(0,hist.GetMaximum()*2.)
        hist.SetTitle("")
        hists+=[hist]

        #hist.SetLineWidth(1)
        hist.SetLineColor(colors[color])
        hist.SetLineStyle(color%5)
        hist.SetMarkerStyle(20+color)
        hist.SetMarkerColor(colors[color])
        hist.SetMarkerSize(1)

        if first:
          first=False
          hist.Draw("hist")
        else:
          hist.Draw("histplsame")
              
        l.AddEntry(hist,samplename,"l")
        color+=1

        if not samplename+matchstr in model_uncertainty_map.keys():        
          model_uncertainty_map[samplename+matchstr]=[]
        model_uncertainty_map[samplename+matchstr]+=[[]]
        histmap[samplename+str(pt)+matchstr]=hist
        for b in range(hist.GetNbinsX()):
          model_uncertainty_map[samplename+matchstr][pt]+=[hist.GetBinContent(b+1)]

    l.Draw("same")
          
    canvas.SaveAs("model_uncertainty_"+var+".pdf")
    
    pt+=1

  canvas=TCanvas("model_uncertainty_ratio", "model_uncertainty_ratio", 0, 0, 300, 300)
  canvas.SetLogx()

  color=0

  l=TLegend(0.40,0.65,0.95,0.93,"")
  l.SetTextSize(0.035)
  l.SetFillStyle(0)

  for matchstr in ("_matched","_unmatched",""):
   for pt in range(0,4):
    histref=histmap["Madgraph+Pythia"+str(pt)+matchstr]
    hist=histmap["Madgraph+Herwig"+str(pt)+matchstr]
    hist.Divide(histref)
    hist.GetXaxis().SetTitle("Softdrop Mass (GeV)")
    hist.GetYaxis().SetTitle("MG+Herwig / MG+Pythia")
    hist.GetXaxis().SetRangeUser(1,1000)
    hist.GetYaxis().SetRangeUser(0,2)
    hist.GetXaxis().SetMoreLogLabels()
    #f=TF1("fit","[0]+[1]*log(x)+[2]*log(x)*log(x)",10,1000)
    #f=TF1("fit","[0]+[1]*tanh((1+[2])*(x/80-1))",0,1000)
    #f.SetParLimits(2,-0.5,2)
    f1=TF1("fit","min([0]+[1]/x,"+str(hist.GetBinContent(1))+")",0,1000)
    hist.Fit(f1,"nqb")
    f=TF1("fit","max(min([0]+[1]/x,"+str(hist.GetBinContent(1))+"),"+str(hist.GetBinContent(4))+")",0,1000)
    f.SetParameters(0,f1.GetParameter(0))
    f.SetParameters(1,f1.GetParameter(1))
    f.SetParLimits(0,0,1)
    f.SetParLimits(1,0,50)
    if matchstr=="_unmatched":
      f.SetParLimits(1,0,50)
    elif matchstr=="_matched":
      f.SetParLimits(1,0,500)
    hist.Fit(f,"nqb")
    print(f.GetExpFormula("P"))
    model_uncertainty_map["Madgraph+Herwig"+matchstr][pt]=[]
    for b in range(hist.GetNbinsX()):
      #hist.SetBinContent(b+1,f.Eval(hist.GetXaxis().GetBinCenter(b+1)))
      model_uncertainty_map["Madgraph+Herwig"+matchstr][pt]+=[histref.GetBinContent(b+1)*f.Eval(hist.GetXaxis().GetBinCenter(b+1))]
    hist.SetTitle("")
    hists+=[hist]

    #hist.SetLineWidth(1)
    hist.SetLineColor(colors[color])
    hist.SetLineStyle(color%5)
    hist.SetMarkerStyle(20+color)
    hist.SetMarkerColor(colors[color])
    hist.SetMarkerSize(1)

    if color==0:
      hist.Draw("histpe")
    else:
      hist.Draw("histpesame")
    f.SetLineColor(colors[color])
    f.SetLineStyle(color%5)
    f.Draw("same")
          
    l.AddEntry(hist,"pt"+str(pt)+matchstr,"l")
    color+=1

   l.Draw("same")
          
   canvas.SaveAs("model_uncertainty_ratio.pdf")




  canvas=TCanvas("model_uncertainty_ratio2", "model_uncertainty_ratio2", 0, 0, 300, 300)

  color=0

  l=TLegend(0.40,0.65,0.95,0.93,"")
  l.SetTextSize(0.035)
  l.SetFillStyle(0)

  for matchstr in ("_matched","_unmatched",""):
   histdiv=[histmap["Madgraph+Herwig"+str(pt)+matchstr] for pt in range(0,4)]
   for msd in range(0,4):
    hist=TH1F("msd"+matchstr,"msd"+matchstr,4,0,4)
    for pt in range(0,4):
      hist.SetBinContent(pt+1,histdiv[pt].GetBinContent(msd+1))
      hist.SetBinError(pt+1,histdiv[pt].GetBinError(msd+1))
    hist.GetXaxis().SetTitle("pT bin")
    hist.GetYaxis().SetTitle("MG+Herwig / MG+Pythia")
    hist.GetXaxis().SetRangeUser(0,4)
    hist.GetYaxis().SetRangeUser(0,2)
    f=TF1("fit","[0]+[1]*x",0,4)
    hist.Fit(f,"nqb")
    print(f.GetExpFormula("P"))
    hist.SetTitle("")
    hists+=[hist]

    #hist.SetLineWidth(1)
    hist.SetLineColor(colors[color])
    hist.SetLineStyle(color%5)
    hist.SetMarkerStyle(20+color)
    hist.SetMarkerColor(colors[color])
    hist.SetMarkerSize(1)

    if color==0:
      hist.Draw("histpe")
    else:
      hist.Draw("histpesame")
    f.SetLineColor(colors[color])
    f.SetLineStyle(color%5)
    f.Draw("same")
          
    l.AddEntry(hist,"msd"+str(msd)+matchstr,"lp")
    color+=1

   l.Draw("same")
          
   canvas.SaveAs("model_uncertainty_ratio2.pdf")

  print(model_uncertainty_map)
