def round_value_to_decimals(cont, decimals=3):
    """
    round all values in a dictionary to some decimals in one go
    default round to 3 digits after period
    possible use case: correlations where typical values are within -1,1
    : param cont : dictionary as returned e.g. by RootFileReader::read_hist_1d()
    : type  cont : dictionary
    : param decimals: how many decimals for the rounding
    : type  decimals: integer
    """

    decimals = int(decimals)

    for i, val in enumerate(cont):
        if isinstance(val, tuple):
            cont[i] = (round(val[0], decimals), round(val[1], decimals))
        else:
            cont[i] = round(val, decimals)


print("start hepdata_lib")
import hepdata_lib
print("hepdata_lib version", hepdata_lib.__version__)

from hepdata_lib import Submission
submission = Submission()

submission.read_abstract("abstract.txt")
submission.add_link("Webpage with all figures and tables", "https://cms-results.web.cern.ch/cms-results/public-results/publications/SMP-24-012/")
#submission.add_link("arXiv", "http://arxiv.org/abs/arXiv:TODO")
submission.add_record_id(0, "inspire")

postfix="" #_UL17_NoModel #"_NoSys" #"_UL16postVFP"

n=0
sup=1
add_tables=[]
for matching in ["","_NoMatching"]:
  for selection,pt in [("_N2Cut","pt1"),("_N2Cut","pt2"),("_N2Cut","pt3"),("_N2Cut","sum"),("","sum"),("","pt1"),("","pt2"),("","pt3")]:
   n+=1
   from hepdata_lib import Table
   text=("W-match, " if matching=="_NoMatching" else "")+selection.replace("_N2Cut","N$_2$<0.2, ")+pt.replace("sum","p$_{T}$>650 GeV").replace("pt1","650<p$_{T}$<800 GeV").replace("pt2","800<p$_{T}$<1200 GeV").replace("pt3","p$_{T}$>1200 GeV")
   if n<4:
     figure="Figure 7"
   elif n==4 or n==5:
     figure="Figure 9"
   else:
     figure="Add. Fig. "+str(sup)
     sup+=1
   table = Table(figure+" - Jet mass ("+text.replace(" GeV","")+")")
   table.description = "Jet mass, "+text+". Unfolded and background subtracted jet mass distribution at the particle level."+(" The fiducial measurement region at the particle level includes the N$_2$<0.2 selection." if selection=="_N2Cut" else "")
   table.location = "Data from "+figure
   table.keywords["observables"] = ["DSIG/DM"]
   table.keywords["reactions"] = ["P P --> W + JET"]
   table.add_image("m_unfold_"+pt+"inclusive"+selection+matching+".pdf")

   from hepdata_lib import RootFileReader
   reader = RootFileReader("CombinedFit_results"+selection+matching+postfix+".root")
   Data = reader.read_graph("munfold_"+("no matching" if matching=="_NoMatching" else "matching")+"_"+pt.replace("pt","ipt"))

   if Data["x"][-1]<500:
     Data["x"][-1]=545.
     Data["dx"][-1]=(-455.,455.)
     #Data["y"][-1]*=900./160
     #Data["dy"][-1]=(Data["dy"][-1][0]*900./160,Data["dy"][-1][1]*900./160)
   #print(Data["x"])
   #print(Data["dx"])
   #print(Data["dy"])
   #print(Data["y"])

   from hepdata_lib import Variable, Uncertainty
   mjet = Variable("m$_{SD}$", is_independent=True, is_binned=True, units="GeV")
   mjet.values = [[Data["x"][i]+Data["dx"][i][0],Data["x"][i]+Data["dx"][i][1]] for i in range(len(Data["x"]))]
   data = Variable("d$\sigma$/dm$_{SD}$", is_independent=False, is_binned=False, units="fb/GeV")
   data.values = Data["y"]
   # Multiply contents by bin-width
   #data.values = [data.values[i]*(mjet.values[i][1]-mjet.values[i][0]) for i in range(len(data.values))]
   unc_data = Uncertainty("total uncertainty", is_symmetric=False)
   unc_data.values = Data["dy"]
   data.add_uncertainty(unc_data)
   table.add_variable(mjet)
   table.add_variable(data)

   if figure.startswith("Figure 7"):
     submission.add_table(table)
   else:
     add_tables+=[table]

import numpy as np
for selection in ["_N2Cut",""]:
   if selection=="_N2Cut":
     figure="Figure 8"
   else:
     figure="Add. Fig. "+str(sup)
     sup+=1
   table = Table(figure+" - Correlation matrix "+selection.replace("_N2Cut"," (N$_2$<0.2)"))
   table.description = "Correlation matrix"+selection.replace("_N2Cut",", N$_2$<0.2")+". Correlation matrix of the maximum likelihood estimators of the signal strength modifiers"+(" with inclusion of an N$_2$<0.2 selection in the particle-level definition" if selection=="_N2Cut" else "")+". The matrix is obtained after the fit to the data. The bin numbers correspond to 4 times the index (starting at 0) of the p$_{T}$ bin (650<p_$_{T}$<800, 800<p_$_{T}$<1200, p_$_{T}$>1200) plus the index (starting at 0) of the m$_{SD}$ bin (30<m$_{SD}$<80, 80<m$_{SD}$<90, 90<m$_{SD}$<100, m$_{SD}$>100)."
   table.location = "Data from "+"Additional Figure "+str(sup)
   table.keywords["reactions"] = ["P P --> W + JET"]

   if selection=="_N2Cut":
      corr_file="poi_correlation_matrix-withN2"+postfix+".npy"
   else:
      corr_file="poi_correlation_matrix-noN2"+postfix+".npy"
   result = np.load(corr_file, allow_pickle=True, encoding="latin1").item()
   corr = result["correlationMatrix"]
   #print(corr)
   from hepdata_lib import Variable
   x = Variable("Bin number 1 (4 p$_{T}$-bin + m$_{SD}$-bin)", is_independent=True, is_binned=False)
   x2 = Variable("Bin number 2 (4 p$_{T}$-bin + m$_{SD}$-bin)", is_independent=True, is_binned=False)
   y = Variable("Correlation coefficient", is_independent=False, is_binned=False)
   x.values = []
   x2.values = []
   y.values = []
   for b in range(0,len(corr)-4):
    for b1 in range(0,len(corr)-4):
     x.values.append(b)
     x2.values.append(b1)
     y.values.append(float(corr[b+4,b1+4]))
   round_value_to_decimals(y.values)
   #print(x.values,x2.values,y.values)
   table.add_variable(x)
   table.add_variable(x2)
   table.add_variable(y)
   if figure.startswith("Figure 8"):
     submission.add_table(table)
   else:
     add_tables+=[table]

for table in add_tables:
   submission.add_table(table)

submission.create_files("output",remove_old=True)
