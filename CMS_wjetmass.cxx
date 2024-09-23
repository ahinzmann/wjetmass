/*
  Copyright 2021, D. Britzger, Max-Planck-Institute for Physics, Munich, Germany

  Permission is hereby granted, free of charge, to any person obtaining
  a copy of this software and associated documentation files (the
  "Software"), to deal in the Software without restriction, including
  without limitation the rights to use, copy, modify, merge, publish,
  distribute, sublicense, and/or sell copies of the Software, and to
  permit persons to whom the Software is furnished to do so, subject to
  the following conditions: 
 
  The above copyright notice and this permission notice shall be
  included in all copies or substantial portions of the Software. 

  The Software is provided "as is", without warranty of any kind,
  express or implied, including but not limited to the warranties of
  merchantability, fitness for a particular purpose and
  noninfringement. In no event shall the authors or copyright holders be
  liable for any claim, damages or other liability, whether in an action
  of contract, tort or otherwise, arising from, out of or in connection
  with the Software or the use or other dealings in the Software. 
*/

/*
Adapted for CMS_wjetmass analysis.
*/

// -------------------------------------------------------------------- //


#include <iostream>
#include <fstream>

#include "LTF/LTF.h"
#include "LTF/LTF_Tools.h"

#if defined __WITH_ROOT__ || defined __CLING__
#include "LTF/LTF_ROOTTools.h"
#endif


// -------------------------------------------------------------------- //
//!
//! example_CMSinclusivejets_NN30_BRSSWpaper()
//!
//! Example application of the Linear Template Fit
//!
//! determine the value of the strong coupling constant from 
//! CMS inclusive jet data arXiv:1212.6660 using NLO QCD predictions,
//! similar to Eur.Phys.J.C 79 (2019) 68 [arXiv:1712.00480]
//!
//! Data published in Phys.Rev.D 87 (2013) 112002, PRD 87 (2013) 119902 (erratum) [arXiv:1212.6660]
//! 
// -------------------------------------------------------------------- //
int CMS_wjetmass(std::string arg1) {
   using namespace std;
#ifdef __CLING__
   gSystem->Load("libLTF.so");
   //gSystem->Load("LTF_cxx.so");
   TH1D::AddDirectory(false);
#endif

   // --- for 'common'-type and 'H1'-type fits, using log-normal chi2 [see EPJ C 79 (2019) 68 [arXiv:1712.00480]]
   map < string, vector<double> > templates   = LTF_Tools::read_input_table(arg1+"_templates.txt",4+1*(arg1.find(std::string("-0"))!=std::string::npos));

   // --- data
   map < string, vector<double> > input_table = LTF_Tools::read_input_table(arg1+"_data.txt",4);
   vector<vector<double > > corr              = LTF_Tools::read_correlations(arg1+"_correlations.txt",2);
   vector<double> data                        = input_table["Sigma"];

   // --- linear template fit
   LTF ltf_CMS; // instantiate Linear Template Fit LTF
   ltf_CMS.SetData( data ); // set data

   // some settings for LTF
   ltf_CMS.SetGamma(vector<double>{1});
   ltf_CMS.UseNuisanceParameters(false);
   ltf_CMS.UseLogNormalUncertainties(false);

   
   // ---- set templates
   if (templates.count("78"))
     ltf_CMS.AddTemplate( 78 , templates["78"] );
   if (templates.count("79"))
     ltf_CMS.AddTemplate( 79 , templates["79"] );
   if (templates.count("80"))
     ltf_CMS.AddTemplate( 80 , templates["80"] );
   if (templates.count("80.4"))
     ltf_CMS.AddTemplate( 80.4 , templates["80.4"] );
   if (templates.count("81"))
     ltf_CMS.AddTemplate( 81 , templates["81"] );
   if (templates.count("82"))
     ltf_CMS.AddTemplate( 82 , templates["82"] );
   if (templates.count("84"))
     ltf_CMS.AddTemplate( 84 , templates["84"] );

   // ---- set uncertainties
   auto cov  = LTF_Tools::corr_to_cov(corr, input_table["total"], data);
   ltf_CMS.AddError( "total",  cov  );

   // ---- do the Linear Template Fit !
   LTF::LiTeFit fit = ltf_CMS.DoLiTeFit();
   fit.PrintFull();


   // ---- do an alternative fit with a non-linear model representation
   fit.DoIterativeFitNewton() ;
   fit.PrintFull();

   // --- plot the Linear Template Fit
#if defined __WITH_ROOT__ || defined __CLING__
   vector<double> bins;
   for ( int i = 0; i<data.size()+1; i++ ) bins.push_back(i); // dummy binning for the plotting function
   LTF_ROOTTools::plotLiTeFit(fit,bins,"d#sigma/dm_{SD} [pb/GeV]","W mass [GeV]","Bin");//, const vector<double> bins)
#endif
   return 0;
}



// -------------------------------------------------------------------- //
//!  main-function if you want to compile this as an executable
int main(int argc, char *argv[]) {
   return CMS_wjetmass(argv[1]);
}
