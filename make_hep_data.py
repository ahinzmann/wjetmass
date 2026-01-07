print("start hepdata_lib")
import hepdata_lib
print("hepdata_lib version", hepdata_lib.__version__)

from hepdata_lib import Submission
submission = Submission()

submission.read_abstract("abstract.txt")
submission.add_link("Webpage with all figures and tables", "https://cms-results.web.cern.ch/cms-results/public-results/publications/TODO/")
submission.add_link("arXiv", "http://arxiv.org/abs/arXiv:TODO")
submission.add_record_id(0, "inspire")

postfix="_UL17_NoModel" #"_NoSys" #"_UL16postVFP"

n=0
for pt in ["sum","pt1","pt2","pt3"]:
 for matching in ["","_NoMatching"]:
  for selection in ["","_N2Cut"]:
   n+=1
   from hepdata_lib import Table
   text=("W-match, " if matching=="_NoMatching" else "")+selection.replace("_N2Cut","N2<0.2, ")+pt.replace("sum","p$_T$>650 GeV").replace("pt1","650<p$_T$<800 GeV").replace("pt2","800<p$_T$<1200 GeV").replace("pt3","p$_T$>1200 GeV")
   table = Table("Figure "+str(n)+" ("+text+")")
   table.description = "Jet mass distribution, "+text
   table.location = "Data from Figure TODO, located on page TODO."
   table.keywords["observables"] = ["DSIG/DM"]
   table.keywords["reactions"] = ["P P --> W + JET"]
   #table.add_image("m_unfold_"+pt+"inclusive"+selection+matching+".pdf")

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
   mjet = Variable("$M_{SD}$", is_independent=True, is_binned=True, units="GeV")
   mjet.values = [[Data["x"][i]+Data["dx"][i][0],Data["x"][i]+Data["dx"][i][1]] for i in range(len(Data["x"]))]
   data = Variable("d$\sigma$/d$M_{SD}$", is_independent=False, is_binned=False, units="fb/GeV")
   data.values = Data["y"]
   # Multiply contents by bin-width
   #data.values = [data.values[i]*(mjet.values[i][1]-mjet.values[i][0]) for i in range(len(data.values))]
   unc_data = Uncertainty("total uncertainty", is_symmetric=False)
   unc_data.values = Data["dy"]
   data.add_uncertainty(unc_data)
   table.add_variable(mjet)
   table.add_variable(data)

   submission.add_table(table)

submission.create_files("output",remove_old=True)
