// April 26, 2023: parse_clust2det_new

#include "solarsyst_dyn_geo01.h"
#include "cmath"


static void show_usage()
{
  cerr << "Usage: parse_clust2det_new -pairdet pairdet_file -insum input cluster summary file -clust2det input cluster-to-detection file -trackdiv tracklet_division_time -out output file\n";
}

int main(int argc, char *argv[])
{
  string sumfile,clust2detfile,outfile;
  vector <hlclust> inclustvec;
  vector  <longpair> inclust2det;
  vector <hldet> detvec;
  vector <hldet> cluster_detvec;
  vector <hldet> clustvec;
  vector <hldet> trackvec;
  double angvel,crosstrack,alongtrack,PA,poleRA,poleDec;
  angvel=crosstrack=alongtrack=PA=poleRA=poleDec=0.0;
  double arc,timespan;
  arc = timespan = 0;
  vector <double> angvelvec;
  vector <double> GCRvec;
  vector <double> PAvec;
  vector <double> arcvec;
  vector <double> timespanvec;
  vector <double> nightstepvec;
  vector <double> magvec;
  double min_nightstep,max_nightstep;
  long tracknum=0;
  double nightstep = 3.0l/24.0l;
  string pairdetfile,stest;
  ifstream instream1;
  ofstream outstream1;
  int status=0;
  long detnum=0;
  long detct=0;
  long clustct=0;
  long i=0;
  int verbose=0;
  long max_known_obj=0;
  double avg_det_qual=0.0l;
  double magrange,magmean,magrms;
  magrange = magmean = magrms = 0.0l;
  
  
  if(argc<9) {
    show_usage();
    return(1);
  }

  i=1;
  while(i<argc) {
    cout << "Checking out argv[" << i << "] = " << argv[i] << ".\n";
    if(string(argv[i]) == "-pairdets" || string(argv[i]) == "-pairdet" || string(argv[i]) == "-pd" || string(argv[i]) == "-pdet" || string(argv[i]) == "--pairdet" || string(argv[i]) == "--paireddetections" || string(argv[i]) == "--pairdetfile" || string(argv[i]) == "--pairdetections") {
      if(i+1 < argc) {
	//There is still something to read;
	pairdetfile=argv[++i];
	i++;
      }
      else {
	cerr << "Input pairdet file keyword supplied with no corresponding argument\n";
	show_usage();
	return(1);
      }
    } else if(string(argv[i]) == "-insum" || string(argv[i]) == "-inclust" || string(argv[i]) == "-clust" || string(argv[i]) == "-sum" || string(argv[i]) == "--input_summary" || string(argv[i]) == "--input_cluster" || string(argv[i]) == "--input_cluster_file" || string(argv[i]) == "--input_summary_file") {
      if(i+1 < argc) {
	//There is still something to read;
	sumfile=argv[++i];
	i++;
      }
      else {
	cerr << "Input cluster summary file keyword supplied with no corresponding argument\n";
	show_usage();
	return(1);
      }
    } else if(string(argv[i]) == "-clust2det" || string(argv[i]) == "-c2d" || string(argv[i]) == "-inc2d" || string(argv[i]) == "-input_c2d" || string(argv[i]) == "--input_clust2det" ) {
      if(i+1 < argc) {
	//There is still something to read;
	clust2detfile=argv[++i];
	i++;
      }
      else {
	cerr << "Input cluster list keyword supplied with no corresponding argument\n";
	show_usage();
	return(1);
      }
    } else if(string(argv[i]) == "-trackdiv" || string(argv[i]) == "-nightstep") {
      if(i+1 < argc) {
	//There is still something to read;
	nightstep = stod(argv[++i]);
	nightstep /= 24.0l;
	i++;
      }
      else {
	cerr << "Input cluster list keyword supplied with no corresponding argument\n";
	show_usage();
	return(1);
      }
    } else if(string(argv[i]) == "-out" || string(argv[i]) == "-outclust" || string(argv[i]) == "--outfile" || string(argv[i]) == "--outclust" || string(argv[i]) == "--output_cluster_file") {
      if(i+1 < argc) {
	//There is still something to read;
	outfile=argv[++i];
	i++;
      }
      else {
	cerr << "Output file keyword supplied with no corresponding argument\n";
	show_usage();
	return(1);
      }
    }  else if(string(argv[i]) == "-verbose" || string(argv[i]) == "-verb" || string(argv[i]) == "-VERBOSE" || string(argv[i]) == "-VERB" || string(argv[i]) == "--verbose" || string(argv[i]) == "--VERBOSE" || string(argv[i]) == "--VERB") {
      if(i+1 < argc) {
	//There is still something to read;
	verbose=stoi(argv[++i]);
	i++;
      }
      else {
	cerr << "Verbosity keyword supplied with no corresponding argument\n";
	show_usage();
	return(1);
      }
    } else {
      cerr << "Warning: unrecognized keyword or argument " << argv[i] << "\n";
      i++;
    }
  }

  // Catch required parameters if missing
  if(pairdetfile.size()<=0) {
    cout << "\nERROR: input paired detection file is required\n";
    show_usage();
    return(1);
  } else if(sumfile.size()<=0) {
    cout << "\nERROR: input cluster summary file is required\n";
    show_usage();
    return(1);
  } else if(clust2detfile.size()<=0) {
    cout << "\nERROR: input cluster-to-detection file is required\n";
    show_usage();
    return(1);
  } else if(outfile.size()<=0) {
    cout << "\nERROR: output filename is required\n";
    show_usage();
    return(1);
  }

  cout << "input paired detection file " << pairdetfile << "\n";
  cout << "input cluster summary file " << sumfile << "\n";
  cout << "input cluster-to-detection file " << clust2detfile << "\n";
  cout << "output file " << outfile << "\n";


  // Read paired detection file
  detvec={};
  status=read_pairdet_file(pairdetfile, detvec, verbose);
  if(status!=0) {
    cerr << "ERROR: could not successfully read paired detection file " << pairdetfile << "\n";
    cerr << "read_pairdet_file returned status = " << status << ".\n";
   return(1);
  }
  cout << "Read " << detvec.size() << " data lines from paired detection file " << pairdetfile << "\n";
  
  // Read cluster summary file
  inclustvec={};
  status=read_clustersum_file(sumfile, inclustvec, verbose);
  if(status!=0) {
    cerr << "ERROR: could not successfully read input cluster summary file " << sumfile << "\n";
    cerr << "read_clustersum_file returned status = " << status << ".\n";
    return(1);
  }
  cout << "Read " << inclustvec.size() << " data lines from cluster summary file " << sumfile << "\n";
  inclust2det={};
  // Read cluster-to-detection file
  status=read_longpair_file(clust2detfile, inclust2det, verbose);
  if(status!=0) {
    cerr << "ERROR: could not successfully read cluster-to-detection file " << clust2detfile << "\n";
    cerr << "read_longpair_file returned status = " << status << ".\n";
    return(1);
  }
  cout << "Read " << inclust2det.size() << " data lines from cluster-to-detection file " << clust2detfile << "\n";

  status = parse_clust2det(detvec, inclust2det, cluster_detvec);
  if(status!=0) {
    cerr << "ERROR: parse_clust2det failed with error status " << status << "\n";
    return(status);
  }
  detnum = cluster_detvec.size();
  cout << "Wrote cluster detection vector with " << detnum << "entries\n";
  
  outstream1.open(outfile);
  cout << "Writing " << inclustvec.size() << " clusters to output file " << outfile << "\n";
  detct=0;
  for(clustct=0 ; clustct<long(inclustvec.size()); clustct++) {
    // Load cluster-specific detection vector for this cluster
    clustvec={};
    if(detct<detnum) {
      if(cluster_detvec[detct].index!=clustct) {
	cerr << "ERROR: cluster counting mismatch, clustct = " << clustct << ", detct = " << detct << ", index = " << cluster_detvec[detct].index << "\n";
	return(2);
      }
      while(detct<detnum && cluster_detvec[detct].index==clustct) {
	clustvec.push_back(cluster_detvec[detct]);
	detct++;
      }
      cout << clustvec.size() << " points found for cluster " << clustct << "\n";
    }
    if(clustvec.size()>0) {
      // Time-sort clustvec, just to be sure
      sort(clustvec.begin(), clustvec.end(), early_hldet());
      // Run some analytics on this detection cluster
      avg_det_qual = 0.0l;
      max_known_obj=0;
      magvec={};
      for(i=0; i<long(clustvec.size()); i++) {
	avg_det_qual += double(clustvec[i].det_qual);
	if(clustvec[i].known_obj > max_known_obj) max_known_obj = clustvec[i].known_obj;
	if(clustvec[i].mag>0.0l) magvec.push_back(clustvec[i].mag);
      }
      avg_det_qual/=double(clustvec.size());
      // Loop over clustvec to extract individual tracklets
      trackvec={};
      nightstepvec={};
      trackvec.push_back(clustvec[0]);
      angvelvec = GCRvec = PAvec = timespanvec = arcvec = {};
      for(i=1; i<long(clustvec.size()); i++) {
	if((clustvec[i].MJD - clustvec[i-1].MJD) > nightstep) {
	  // We're looking at a gap between two successive tracklets.
	  // We're interested in the distribution of such gaps,
	  // so we add it to the nightstepvec.
	  nightstepvec.push_back(clustvec[i].MJD - clustvec[i-1].MJD);
	}
	if((clustvec[i].MJD - clustvec[i-1].MJD) < nightstep) {
	  // Add a new point to this tracklet
	  trackvec.push_back(clustvec[i]);
	} else {
	  // A tracklet is finished. Analyze it.
	  tracknum = trackvec.size();
	  if(tracknum>1) {
	    greatcircfit(trackvec, poleRA, poleDec, angvel, PA, crosstrack, alongtrack);
	    angvelvec.push_back(angvel);
	    GCRvec.push_back(sqrt(DSQUARE(crosstrack)+DSQUARE(alongtrack)));
	    PAvec.push_back(PA);
	    timespan = trackvec[trackvec.size()-1].MJD - trackvec[0].MJD;
	    arc = timespan*angvel;
	    arcvec.push_back(arc*3600.0l);
	    timespanvec.push_back(timespan*24.0l);
	    // Wipe trackvec, and load the next point of the next tracklet.
	    trackvec = {};
	    trackvec.push_back(clustvec[i]);
	  } else if(tracknum==1) {
	    // The 'tracklet' is a singleton. Set all tracket vectors to error codes or zero.
	    angvelvec.push_back(-1.0l);
	    GCRvec.push_back(-1.0l);
	    PAvec.push_back(-999.0l);
	    arcvec.push_back(0.0l);
	    timespanvec.push_back(0.0l);
	    // Wipe trackvec, and load the next point of the next tracklet.
	    trackvec = {};
	    trackvec.push_back(clustvec[i]);
	  }
	}
      }
      tracknum = trackvec.size();
      if(tracknum>1) {
	// Handle a final tracklet.
	greatcircfit(trackvec, poleRA, poleDec, angvel, PA, crosstrack, alongtrack);
	angvelvec.push_back(angvel);
	GCRvec.push_back(sqrt(DSQUARE(crosstrack)+DSQUARE(alongtrack)));
	PAvec.push_back(PA);
	timespan = trackvec[trackvec.size()-1].MJD - trackvec[0].MJD;
	arc = timespan*angvel;
	arcvec.push_back(arc*3600.0l);
	timespanvec.push_back(timespan*24.0l);
	// Wipe trackvec
	trackvec = {};
      } else if(tracknum==1) {
	// The final 'tracklet' is a singleton. Set all tracket vectors to error codes or zero.
	angvelvec.push_back(-1.0l);
	GCRvec.push_back(-1.0l);
	PAvec.push_back(-999.0l);
	arcvec.push_back(0.0l);
	timespanvec.push_back(0.0l);
	// Wipe trackvec.
	trackvec = {};
      }
      // Sort all of the tracklet statistics vectors
      tracknum = angvelvec.size();
      sort(angvelvec.begin(), angvelvec.end());
      sort(GCRvec.begin(), GCRvec.end());
      sort(PAvec.begin(), PAvec.end());
      sort(timespanvec.begin(), timespanvec.end());
      sort(arcvec.begin(), arcvec.end());

      // Sort nightstepvec
      sort(nightstepvec.begin(), nightstepvec.end());
      min_nightstep = max_nightstep = 0.0l;
      min_nightstep = nightstepvec[0];
      max_nightstep = nightstepvec[nightstepvec.size()-1];
      nightstepvec = {};

      // Analyze magnitude range.
      if(magvec.size()<=0) {
	magmean = 0.0;
	magrms = magrange = 99.9;
      } else if(magvec.size()==1) {
	magmean = magvec[0];
	magrms = magrange = 99.9;
      } else if(magvec.size()<=5) {
	// Sort magvec
	sort(magvec.begin(), magvec.end());
	dmeanrms01(magvec, &magmean, &magrms);
	// Magrange will be the full max-min
	magrange = magvec[magvec.size()-1] - magvec[0];
      } else {
	// Sort magvec
	sort(magvec.begin(), magvec.end());
	dmeanrms01(magvec, &magmean, &magrms);
	magrange = magvec[magvec.size()-2] - magvec[1];
	// Magrange will be the second-largest value minus
	// the second-smallest, offering some robustness
	// against outliers
      }
      magvec={};
      
      outstream1 << "\n#clusternum,posRMS,velRMS,totRMS,astromRMS,timespan,uniquepoints,obsnights,metric,orbit_a,orbit_e,orbit_MJD,orbitX,orbitY,orbitZ,orbitVX,orbitVY,orbitVZ,orbit_eval_count,avg_det_qual,max_known_obj,minvel,maxvel,minGCR,maxGCR,minpa,maxpa,mintimespan,maxtimespan,minarc,maxarc,stringID,min_nightstep,max_nightstep,magmean,magrms,magrange\n";
      outstream1 << fixed << setprecision(3) << inclustvec[clustct].clusternum << "," << inclustvec[clustct].posRMS << "," << inclustvec[clustct].velRMS << "," << inclustvec[clustct].totRMS << ",";
      outstream1 << fixed << setprecision(4) << inclustvec[clustct].astromRMS << ",";
      outstream1 << fixed << setprecision(6) << inclustvec[clustct].timespan << "," << inclustvec[clustct].uniquepoints << "," << inclustvec[clustct].obsnights << "," << inclustvec[clustct].metric << ",";
      outstream1 << fixed << setprecision(6) << inclustvec[clustct].orbit_a << "," << inclustvec[clustct].orbit_e << "," << inclustvec[clustct].orbit_MJD << ",";
      outstream1 << fixed << setprecision(1) << inclustvec[clustct].orbitX << "," << inclustvec[clustct].orbitY << "," << inclustvec[clustct].orbitZ << ",";
      outstream1 << fixed << setprecision(4) << inclustvec[clustct].orbitVX << "," << inclustvec[clustct].orbitVY << "," << inclustvec[clustct].orbitVZ << "," << inclustvec[clustct].orbit_eval_count << ",";
      outstream1 << fixed << setprecision(1) << avg_det_qual << "," << max_known_obj << ",";
      outstream1 << fixed << setprecision(6) << angvelvec[0] << "," << angvelvec[tracknum-1] << "," << GCRvec[0] << "," << GCRvec[tracknum-1] << "," << PAvec[0] << "," << PAvec[tracknum-1] << "," << timespanvec[0] << "," << timespanvec[tracknum-1] << "," << arcvec[0] << "," << arcvec[tracknum-1] << "," << clustvec[0].idstring << "," << min_nightstep << "," << max_nightstep << "," << magmean << "," << magrms << "," << magrange << "\n";
	
      // Write this data to the output file
      outstream1 << "#MJD,RA,Dec,mag,trail_len,trail_PA,sigmag,sig_across,sig_along,image,idstring,band,obscode,known_obj,det_qual,origindex\n";
      for(i=0; i<long(clustvec.size()); i++) {
	outstream1 << fixed << setprecision(7) << clustvec[i].MJD << "," << clustvec[i].RA << "," << clustvec[i].Dec << ",";
	outstream1 << fixed << setprecision(4) << clustvec[i].mag << ",";
	outstream1 << fixed << setprecision(2) << clustvec[i].trail_len << "," << clustvec[i].trail_PA << ",";
	outstream1 << fixed << setprecision(4) << clustvec[i].sigmag << ",";
	outstream1 << fixed << setprecision(3) << clustvec[i].sig_across << "," << clustvec[i].sig_along << ",";
	outstream1 << clustvec[i].image << "," << clustvec[i].idstring << "," << clustvec[i].band << ",";
	outstream1 << clustvec[i].obscode << "," << clustvec[i].known_obj << ",";
	outstream1 << clustvec[i].det_qual << "," << clustvec[i].index << "\n";
      }
    }
  }
  outstream1.close();
  
  return(0);
}
