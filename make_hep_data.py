import hepdata_lib
print("hepdata_lib version", hepdata_lib.__version__)

from hepdata_lib import Submission
submission = Submission()

submission.read_abstract("abstract.txt")
submission.add_link("Webpage with all figures and tables", "https://cms-results.web.cern.ch/cms-results/public-results/publications/TODO/")
submission.add_link("arXiv", "http://arxiv.org/abs/arXiv:TODO")
submission.add_record_id(0, "inspire")

for selection in ["","_N2Cut"]:
  from hepdata_lib import Table
  table = Table("Figure 1"+selection)
  table.description = "Jet mass distribution"+selection
  table.location = "Data from Figure TODO, located on page TODO."
  table.keywords["observables"] = ["DSIG/DM"]
  table.keywords["reactions"] = ["P P --> W + JET"]
  table.add_image("m_unfold_suminclusive"+selection+".pdf")

  from hepdata_lib import RootFileReader
  reader = RootFileReader("CombinedFit_results"+selection+".root")
  Data = reader.read_graph("munfold_matching_sum")

  from hepdata_lib import Variable, Uncertainty
  mjet = Variable("$M_{SD}$", is_independent=True, is_binned=True, units="GeV")
  mjet.values = [[Data["x"][i]+Data["dx"][i][0],Data["x"][i]+Data["dx"][i][1]] for i in range(len(Data["x"]))]
  data = Variable("d$\sigma$/d$M_{SD}$", is_independent=False, is_binned=False, units="fb/GeV")
  data.values = Data["y"]
  unc_data = Uncertainty("total uncertainty", is_symmetric=False)
  unc_data.values = Data["dy"]
  data.add_uncertainty(unc_data)
  table.add_variable(mjet)
  table.add_variable(data)

  submission.add_table(table)

submission.create_files("output",remove_old=True)
