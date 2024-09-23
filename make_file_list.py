import os
for sample in [#"Pythia","MadgraphPythia","MadgraphHerwig",
      "Pythia84","Pythia82","Pythia81","Pythia80","Pythia79","Pythia78"]:
      #"Pythia84","Pythia83","Pythia82","Pythia81","Pythia80","Pythia79","Pythia78","Pythia77","Pythia76"]:
  jobs=os.listdir("/nfs/dust/cms/user/hinzmann/jetmass/gen"+sample)
  l=[]
  for job in jobs:
   if job.startswith("genjob"):
    d="/nfs/dust/cms/user/hinzmann/jetmass/gen"+sample+"/"+job
    if os.path.isdir(d):
      fl=os.listdir(d)
      f="WJET_"+sample.replace("76","").replace("77","").replace("78","").replace("79","").replace("80","").replace("81","").replace("82","").replace("83","").replace("84","")+"_inHepMC_5Sep2024.root"
      if f in fl:
       if os.path.getsize(d+"/"+f)>0:
        l+=["file:"+d+"/"+f]
  print(l)
  print("count:",len(l))
