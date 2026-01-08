from ROOT import *
import ROOT
import array, math, sys
import os
import numpy as np
import array
import scipy.stats as stats
import cmsstyle as CMS
CMS.SetExtraText("Preliminary")

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
              print("found data")
            if start:
              if "END" in line: break
              s=line.split("	")
              if len(s)==7 and is_float_try(s[0]):
                print(l)
                binning.append(float(s[0]))
                lastx=float(s[1])
                ys+=[(float(s[2]),float(s[3]))]
              if len(s)==6 and is_float_try(s[0]):
                print(l)
                binning.append(float(s[0])-float(s[1]))
                lastx=float(s[0])+float(s[2])
                ys+=[(float(s[3]),float(s[4]))]
        #binning.append(lastx)
        binning.append(250) # move last border from 1000 to 250
        hist=TH1F(histname,histname,len(binning)-1,binning)
        i=1
        for y,yerror in ys:
          hist.SetBinContent(i,y)
          hist.SetBinError(i,yerror)
          i+=1
        hist.GetXaxis().ChangeLabel(len(ys)+1,-1,-1,-1,-1,-1,"1000")
        return hist
        
if __name__=="__main__":
 print("start ROOT")
 #gROOT.Reset()
 gROOT.SetStyle("Plain")
 gROOT.SetBatch(True)

 postfix="-Jan2026" #"-UL18-Asimov"

 CMS.SetLumi("138" if postfix=="" else postfix.strip("-"))
 CMS.SetEnergy("13")
 CMS.ResetAdditionalInfo()
 CMS.setCMSStyle()

 gStyle.SetOptStat(0)
 gStyle.SetOptFit(0)
 gStyle.SetTitleOffset(1.2,"X")
 gStyle.SetTitleOffset(1.4,"Y")
 gStyle.SetPadLeftMargin(0.18)
 gStyle.SetPadBottomMargin(0.15)
 gStyle.SetPadTopMargin(0.08)
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
 
 all_masses=[79,80,80.4,81,82]
 
 #for var in ["d01-x01-y01","d02-x01-y01" # befoore Jan2026
 for var in ["d05-x01-y01","d04-x01-y01" # since Jan2026
              ]:
  measured=[]
  measured_up=[]
  measured_down=[]
  datasets=["0Data","0DataNoSys","0MP","0MH","0CP1","0CP2","0CP5","0CP5highstat"]
  for skip in [*datasets,*all_masses]:

    data=[]
    correlations=[]
    templates=[]

    if "d01" in var or "d05" in var:
      corr_file="poi_correlation_matrix-noN2"+postfix+("-NoSys" if "NoSys" in str(skip) else "")+".npy"
    else:
      corr_file="poi_correlation_matrix-withN2"+postfix+("-NoSys" if "NoSys" in str(skip) else "")+".npy"
    result = np.load(corr_file, allow_pickle=True, encoding="latin1").item()
    pois = result["pois"]
    corr = result["correlationMatrix"]
    cov = result["covarianceMatrix"]
    #print(pois)
    #print(cov)

    masses=all_masses.copy()
    if skip in masses:
      masses.pop(masses.index(skip))

    canvas=TCanvas("w_mass-"+var+"-"+str(skip), "w_mass-"+var+"-"+str(skip), 0, 0, 300, 300)
    canvas.cd()
    
    hists=[]
    
    colors=[1,2,3,4,6,7,8,9,12,28,34,38,40,41,42,43,44,45,46,47,48,49]
    color=0

    l=TLegend(0.45,0.60,0.95,0.90,"")#"no N2 cut" if "d01" in var else "N2<0.2")
    l.SetTextSize(0.04)
    l.SetFillStyle(0)
    
    xs=[]
    chi2s=[]
    min_b=1
    max_b=3
    
    first=True
    firsthist=None
    for mass in ["Data",*masses]:
        if mass=="Data":
          if skip=="0Data":
            samplename="HEPData"+postfix+"-yoda1"
          elif skip=="0DataNoSys":
            samplename="HEPData-yoda1-NoSys"
          elif skip=="0MP":
            samplename="WJET_MadgraphPythia_12Sep2024"
          elif skip=="0MH":
            samplename="WJET_MadgraphHerwig_17Sep2024"
          elif skip=="0CP1":
            samplename="WJET_Pythia8_CP1_10Sep2025"
          elif skip=="0CP2":
            samplename="WJET_Pythia8_CP2_10Sep2025"
          elif skip=="0CP5":
            samplename="WJET_Pythia8_CP5_12Sep2024"
          elif skip=="0CP5highstat":
            samplename="WJET_Pythia8_CP5_12Jun2025"
          else:
            samplename="WJET_Pythia8_CP5"+("_m"+str(skip)).replace("_m80.4","")+"_12Jun2025" # high stat used for CP2 check, and post CWR
            #samplename="WJET_Pythia8_CP5"+("_m"+str(skip)).replace("_m80.4","")+"_12Sep2024" # low stat used for consistency with approval result
        else:
            samplename="WJET_Pythia8_CP5"+("_m"+str(mass)).replace("_m80.4","")+"_12Jun2025" # high stat sued for CP2 check, and post CWR
            #samplename="WJET_Pythia8_CP5"+("_m"+str(mass)).replace("_m80.4","")+"_12Sep2024" # low stat used for consistency with approval result
        filename=samplename+".yoda"
        hist=getHist(filename,var,var+samplename)
        hist.GetXaxis().SetTitle("m_{SD,ptcl} [GeV]")
        hist.GetYaxis().SetTitle("1/#sigma d#sigma/dm_{SD,ptcl} [1/GeV]")
        hist.SetTitle("")
        hists+=[hist]
        if "Data" in samplename:
          for b in range(hist.GetNbinsX()):
            hist.SetBinContent(b+1,hist.GetBinContent(b+1)*hist.GetXaxis().GetBinWidth(b+1))
            hist.SetBinError(b+1,hist.GetBinError(b+1)*hist.GetXaxis().GetBinWidth(b+1))
        hist.Scale(1.0/hist.Integral(min_b+1,max_b))
        if "Data" in samplename:
          histdata=hist.Clone("data"+var)
        #hist.Scale(histdata.Integral(min_b+1,max_b)/hist.Integral(min_b+1,max_b))
        if mass=="Data":
          for b in range(hist.GetNbinsX()):
            hist.SetBinError(b+1,histdata.GetBinError(b+1))
          histref=hist.Clone("ref"+var+"-"+str(skip))
        else:
          for b in range(hist.GetNbinsX()):
            hist.SetBinError(b+1,0)

        datay=[]
        mcy=[]
        covyy=[]
        for b in range(hist.GetNbinsX())[min_b:max_b]:
          datay+=[histref.GetBinContent(b+1)]
          mcy+=[hist.GetBinContent(b+1)]
          covyy+=[[]]
          for b2 in range(hist.GetNbinsX())[min_b:max_b]:
            covyy[-1]+=[histref.GetBinContent(b+1)*histref.GetBinContent(b2+1)*corr[b+4][b2+4]]
        datay=np.array(datay)
        mcy=np.array(mcy)
        covyy=np.array(covyy)
        print(datay)
        print(mcy)
        print(covyy)
        print((datay-mcy).transpose(),np.linalg.inv(covyy),(datay-mcy))
        chi2=np.matmul(np.matmul((datay-mcy).transpose(),np.linalg.inv(covyy)),(datay-mcy))
        chi2=1-stats.chi2.cdf(chi2,df=2)
        print(chi2)
        if mass!="Data":
          xs+=[mass]
          chi2s+=[chi2]
          
        for b in range(hist.GetNbinsX()):
            hist.SetBinContent(b+1,hist.GetBinContent(b+1)/hist.GetXaxis().GetBinWidth(b+1))
            hist.SetBinError(b+1,hist.GetBinError(b+1)/hist.GetXaxis().GetBinWidth(b+1))

        if mass=="Data":
          for b in range(hist.GetNbinsX())[min_b:max_b]:
            data+=[[hist.GetXaxis().GetBinLowEdge(b+1),hist.GetXaxis().GetBinUpEdge(b+1),hist.GetBinContent(b+1),100*hist.GetBinError(b+1)/hist.GetBinContent(b+1)]]
            correlations+=[[]]
            for b2 in range(hist.GetNbinsX())[min_b:max_b]:
              correlations[-1]+=[corr[b+4][b2+4]]
        else:
          templates+=[[]]
          for b in range(hist.GetNbinsX())[min_b:max_b]:
            templates[-1]+=[hist.GetBinContent(b+1)]

        #hist.Scale(hists[0].Integral()/hist.Integral())
        #hist.GetYaxis().SetRangeUser(0,1.2)
        if "Data" in samplename:
          data_max=hist.GetMaximum()
          data_min=hist.GetMinimum()
          hist.GetYaxis().SetRangeUser(0,data_max*1.5)

        #hist.SetLineWidth(1)
        hist.SetLineColor(colors[color])
        hist.SetLineStyle(color%5)
        hist.SetMarkerStyle(20+color)
        hist.SetMarkerColor(colors[color])
        hist.SetMarkerSize(1)
        #canvas.SetLogy()
        
        if first:
          first=False
          hist.SetMarkerSize(0)
          hist.SetLineWidth(2)
          hist.Draw("e")
          firsthist=hist
        else:
          hist.Draw("hpsame")
              
        l.AddEntry(hist,("" if mass=="Data" else "W+Jets m_{W} = ")+str("Pythia "+str(skip).strip("0") if "CP" in str(skip) and mass=="Data" else ("Madgraph+Pythia" if skip=="0MP" and mass=="Data" else ("Madgraph+Herwig" if skip=="0MH" and mass=="Data" else mass)))+(" GeV" if not mass=="Data" else ""),"le" if mass=="Data" else "lp")
        color+=1

    firsthist.Draw("esame")
    l.Draw("same")
          
    CMS.CMS_lumi(canvas, 0)
    canvas.Modified()
    canvas.Update()
    canvas.RedrawAxis()
    canvas.GetFrame().Draw()
    canvas.SaveAs("w_mass_"+var+"-"+str(skip)+postfix+".pdf")
   
    canvas=TCanvas("chi2-"+var+"-"+str(skip), "chi2-"+var+"-"+str(skip), 0, 0, 300, 300)
    canvas.cd()
    
    l=TLegend(0.45,0.65,0.95,0.93,"")#"no N2 cut" if "d01" in var else "N2<0.2")
    l.SetTextSize(0.04)
    l.SetFillStyle(0)
    
    hist=TGraph(len(chi2s),array.array("d",xs),array.array("d",chi2s))
    hist.GetXaxis().SetTitle("W Mass [GeV]")
    hist.GetYaxis().SetTitle("#chi^{2} probabilty")
    hist.SetTitle("")
    hists+=[hist]
    hist.GetYaxis().SetRangeUser(0,1)
    #hist.GetYaxis().SetRangeUser(0,max(chi2s[0],chi2s[-1])*1.5)

    #hist.SetLineWidth(1)
    hist.SetLineColor(colors[color])
    hist.SetLineStyle(color%5)
    hist.SetMarkerStyle(20+color)
    hist.SetMarkerColor(colors[color])
    hist.SetMarkerSize(1)

    hist.Draw("ap")
    
    #f=TF1("fit"+var+"-"+str(skip),"pol2",xs[0],xs[-1])
    #hist.Fit(f,"")
    f=TSpline3("spline"+var+"-"+str(skip),hist)
    f.Draw("lsame")
    #f=hist
    
    ls=TLine(xs[0]-1,0.68,xs[-1]+1,0.68)
    ls.Draw()
          
    l.Draw("same")
    
    min_m=-1e10
    max_m=1e10
    best_chi2=-1e10
    best_m=-1e10
    for m in range(int(masses[0]*100),int(masses[-1]*100)):
       chi2=f.Eval(m/100)
       if chi2>0.68:
         if min_m<0: min_m=m
         max_m=m
       elif min_m>0: break
       if chi2>best_chi2:
         best_chi2=chi2
         best_m=m
  
    #measured+=[best_m/100]
    #if max_m<1e5:
    #  measured_up+=[(max_m-best_m)/100]
    #else:
    #  measured_up+=[10]
    #if min_m>0:
    #  measured_down+=[(best_m-min_m)/100]
    #else:
    #  measured_down+=[10]
  
    CMS.CMS_lumi(canvas, 0)
    canvas.Modified()
    canvas.Update()
    canvas.RedrawAxis()
    canvas.GetFrame().Draw()
    canvas.SaveAs("chi2_"+var+"-"+str(skip)+postfix+".pdf")

    ### Carry our LinearTemplateFit
    with open("CMS_wjetmass_"+var+"-"+str(skip)+"_data.txt","w") as f:
      f.write("mlow mhigh Sigma total"+"\n")
      for d in data:
        s=""
        for e in d:
          s+=str(e)+" "
        f.write(s+"\n")
    with open("CMS_wjetmass_"+var+"-"+str(skip)+"_correlations.txt","w") as f:
      for c1 in correlations:
        s=""
        for c2 in c1:
          s+=str(c2)+" "
        f.write(s+"\n")
    with open("CMS_wjetmass_"+var+"-"+str(skip)+"_templates.txt","w") as f:
      s=""
      for m in masses:
        s+=str(m)+" "
      f.write(s+"\n")
      for t in range(len(templates[0])):
        s=""
        for m in range(len(masses)):
          s+=str(templates[m][t])+" "
        f.write(s+"\n") 
    command="cd /afs/desy.de/user/h/hinzmann/wjetmass/LinearTemplateFit/LTF_Eigen;/afs/desy.de/user/h/hinzmann/wjetmass/LinearTemplateFit/LTF_Eigen/build/bin/CMS_wjetmass /afs/desy.de/user/h/hinzmann/wjetmass/CMS_wjetmass_"+var+"-"+str(skip)+" > /afs/desy.de/user/h/hinzmann/wjetmass/CMS_wjetmass_"+var+"-"+str(skip)+"_fit.txt"
    print(command)
    os.system(command)
    with open("/afs/desy.de/user/h/hinzmann/wjetmass/CMS_wjetmass_"+var+"-"+str(skip)+"_fit.txt") as f:
      count=0
      for l in f.readlines():
        if "Error" in l:
          print("found error in fit",l)
          raise
        if "Fit done. Result:" in l:
         count+=1
         if count>1: # second method
          result=l.split(":")[-1].strip(" ").split(" ")
          #print(result)
          measured+=[float(result[0])]
          measured_up+=[float(result[3])]
          measured_down+=[float(result[3])]
          break
           
  print(datasets+all_masses)
  print(measured)
  print(measured_up)
  print(measured_down)

  canvas=TCanvas("measured-"+var, "measured-"+var, 0, 0, 300, 300)
  canvas.cd()
  
  l=TLegend(0.40,0.65,0.95,0.93,"")#"no N2 cut" if "d01" in var else "N2<0.2")
  l.SetTextSize(0.035)
  l.SetFillStyle(0)
  
  hist=TGraphAsymmErrors(len(all_masses[1:-1]),array.array("d",all_masses[1:-1]),array.array("d",measured[1+len(datasets):-1]),array.array("d",[0]*len(all_masses[1:-1])),array.array("d",[0]*len(all_masses[1:-1])),array.array("d",measured_down[1+len(datasets):-1]),array.array("d",measured_up[1+len(datasets):-1]))
  hist.GetXaxis().SetTitle("W Mass generated [GeV]")
  hist.GetYaxis().SetTitle("W Mass measured [GeV]")
  hist.SetTitle("")
  hists+=[hist]
  #hist.GetYaxis().SetRangeUser(0,3)

  #hist.SetLineWidth(1)
  hist.SetLineColor(colors[color])
  hist.SetLineStyle(color%5)
  hist.SetMarkerStyle(20+color)
  hist.SetMarkerColor(colors[color])
  hist.SetMarkerSize(1)

  hist.Draw("ap")
  
  f=TF1("fit","pol1",all_masses[0],all_masses[-1])
  f.SetParameter(0,0)
  f.SetParameter(1,1)
  #hist.Fit(f,"")
  f.Draw("lsame")
  
  l.Draw("same")

  hist.GetXaxis().SetLimits(all_masses[0],all_masses[-1])
  hist.SetMinimum(all_masses[0])
  hist.SetMaximum(all_masses[-1])
  
  CMS.CMS_lumi(canvas, 0)
  canvas.Modified()
  canvas.Update()
  canvas.RedrawAxis()
  canvas.GetFrame().Draw()
  canvas.SaveAs("measured_"+var+postfix+".pdf")
