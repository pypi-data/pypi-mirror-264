// November 30, 2023: link_purify:
// Based on link_refine_Herget_univar, this code takes the paradigm-shifting step
// of actually altering the linkages with which it is supplied, rather than
// simply selecting the best ones. Linkages with low enough astrometric RMS, and
// no time duplicates, are passed without alteration. If a linkage has a large
// astrometric RMS, the worst astrometric outliers are rejected, one at a time,
// until either the linkage becomes invalid and is discarded, or the astrometric
// RMS drops into the acceptable range. I expect that culling astrometric outliers
// will eliminate most time-duplicates as well. In cases where this expectation
// is not realized -- that is, time duplicates remain even though the astrometric
// RMS is low -- that point in each duplicate that has the larger astrometric RMS
// we be deleted, until no time-duplicates remain. If the cluster is still valid
// and low-RMS, it will be passed.

#include "solarsyst_dyn_geo01.h"
#include "cmath"

#define MAXCLUSTRMS 1.0e5
#define DEBUG 1
#define ESCAPE_SCALE 0.99L // If the input velocity is above escape velocity, we
                           // scale it down by this amount.
// New quantities in LinkPurifyConfig that are not in LinkRefineConfig:
//  double config.rejfrac = 0.5;         Maximum fraction of points that can be rejected.
//  double config.max_astrom_rms = 1.0;  Maximum RMS astrometric residual, in arcsec.
//  int config.minobsnights = 3;         Minimum number of distinct observing nights for a valid linkage
//  int config.minpointnum = 6;          Minimum number of individual detections for a valid linkage

static void show_usage()
{
  cerr << "Usage: link_planarity -imgs imfile -pairdet pairdet_file -lflist link_file_list -mjd mjdref -simptype simplex_type -rejfrac max fraction of points that can be rejected -max_astrom_rms max astrometric RMS (arcsec) -oop RMS out of plane deviation -minobsnights min number of distinct nights -minpointnum min number of individual detections -ptpow point_num_exponent -nightpow night_num_exponent -timepow timespan_exponent -rmspow astrom_rms_exponent -maxrms maxrms -outsum summary_file -clust2det clust2detfile -heliovane 1 -verbose verbosity\n\nOR, at minimum:\nlink_planarity -imgs imfile -pairdet pairdet_file -lflist link_file_list -mjd mjdref\n";
}

int main(int argc, char *argv[])
{
  string clusterlist;
  string sumfile,clust2detfile;
  vector <hlclust> inclustvec;
  vector <hlclust> clustvecmain;
  vector <hlclust> outclust;
  vector  <longpair> inclust2det;
  vector  <longpair> clust2detmain;
  vector  <longpair> outclust2det;
  vector <hlimage> image_log;
  vector <hldet> detvec;
  LinkPurifyConfig config;
  string imfile, pairdetfile,stest;
  string outsumfile = "LRHsumfile_test.csv";
  string outclust2detfile = "LRHclust2detfile_test.csv";
  ifstream instream1;
  ofstream outstream1;
  long i=0;
  long clustnum=0;
  int status=0;
  long clustct=0;
  int default_simptype, default_ptpow, default_nightpow, default_timepow;
  default_simptype = default_ptpow = default_nightpow = default_timepow = 1;
  int default_rmspow, default_maxrms, default_max_oop, default_sumfile, default_clust2det;
  default_rmspow = default_maxrms = default_max_oop = default_sumfile = default_clust2det = 1;
  //  vector <long> pointind;
  //  vector <long> deletelist;
  //  vector <vector <long>> pointind_mat;
  //  vector <long_index> lindvec;
  //  double_index dindex = double_index(0l,0l);
  //  vector <double_index> dindvec;
  // vector <int> keepvec;

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
    } else if(string(argv[i]) == "-i" || string(argv[i]) == "-imgs" || string(argv[i]) == "-inimgs" || string(argv[i]) == "-img" || string(argv[i]) == "--inimgs" || string(argv[i]) == "--img" || string(argv[i]) == "--image" || string(argv[i]) == "--images") {
      if(i+1 < argc) {
	//There is still something to read;
	imfile=argv[++i];
	i++;
      }
      else {
	cerr << "Image file keyword supplied with no corresponding argument\n";
	show_usage();
	return(1);
      }
    } else if(string(argv[i]) == "-lflist" || string(argv[i]) == "-clist" || string(argv[i]) == "-cl" || string(argv[i]) == "-clustlist" || string(argv[i]) == "--clusterlist" || string(argv[i]) == "--clist" || string(argv[i]) == "--clusterl" || string(argv[i]) == "--clustlist") {
      if(i+1 < argc) {
	//There is still something to read;
	clusterlist=argv[++i];
	i++;
      }
      else {
	cerr << "Input cluster list keyword supplied with no corresponding argument\n";
	show_usage();
	return(1);
      }
    }  else if(string(argv[i]) == "-m" || string(argv[i]) == "-mjd" || string(argv[i]) == "-mjdref" || string(argv[i]) == "-MJD" || string(argv[i]) == "--mjd" || string(argv[i]) == "--MJD" || string(argv[i]) == "--modifiedjulianday" || string(argv[i]) == "--ModifiedJulianDay") {
      if(i+1 < argc) {
	//There is still something to read;
	config.MJDref=stold(argv[++i]);
	i++;
      }
      else {
	cerr << "Reference MJD keyword supplied with no corresponding argument";
	show_usage();
	return(1);
      }
    } else if(string(argv[i]) == "-simptype" || string(argv[i]) == "-stype" || string(argv[i]) == "-simpt" || string(argv[i]) == "-simplextype" || string(argv[i]) == "-simplex_type" || string(argv[i]) == "--simptype" || string(argv[i]) == "--simplex_type") {
      if(i+1 < argc) {
	//There is still something to read;
	config.simptype=stoi(argv[++i]);
	default_simptype=0;
	i++;
      }
      else {
	cerr << "Simplex type keyword supplied with no corresponding argument";
	show_usage();
	return(1);
      }
    } else if(string(argv[i]) == "-rejfrac" || string(argv[i]) == "-maxrej" || string(argv[i]) == "-maxrejfrac" || string(argv[i]) == "-rlev" || string(argv[i]) == "-rlev" || string(argv[i]) == "-max_rej_frac" || string(argv[i]) == "--rejfrac" ) {
      if(i+1 < argc) {
	//There is still something to read;
	config.rejfrac=stol(argv[++i]);
	default_simptype=0;
	i++;
      }
      else {
	cerr << "Rejection fraction keyword supplied with no corresponding argument";
	show_usage();
	return(1);
      }
    } else if(string(argv[i]) == "-max_astrom_rms" || string(argv[i]) == "-maxastromrms" || string(argv[i]) == "-astrom_rms" || string(argv[i]) == "-arms" || string(argv[i]) == "-marms" || string(argv[i]) == "-max_astrometric_rms" || string(argv[i]) == "--max_arms" ) {
      if(i+1 < argc) {
	//There is still something to read;
	config.max_astrom_rms=stod(argv[++i]);
	default_simptype=0;
	i++;
      }
      else {
	cerr << "Max astrometric RMS keyword supplied with no corresponding argument\n";
	show_usage();
	return(1);
      }
    } else if(string(argv[i]) == "-oop" || string(argv[i]) == "-max_oop" || string(argv[i]) == "-plane_rms" || string(argv[i]) == "-oop_rms" || string(argv[i]) == "-maxoop" || string(argv[i]) == "-max_plane_rms" || string(argv[i]) == "--oop" ) {
      if(i+1 < argc) {
	//There is still something to read;
	config.max_oop=stod(argv[++i]);
	default_max_oop=0;
	i++;
      }
      else {
	cerr << "Max astrometric RMS keyword supplied with no corresponding argument\n";
	show_usage();
	return(1);
      }
    } else if(string(argv[i]) == "-minobsnights" || string(argv[i]) == "-min_nights" || string(argv[i]) == "-nightmin" || string(argv[i]) == "-min_obs_nights" || string(argv[i]) == "-min_nights" || string(argv[i]) == "--min_obs_nights" || string(argv[i]) == "--minobsnights" ) {
      if(i+1 < argc) {
	//There is still something to read;
	config.minobsnights=stoi(argv[++i]);
	default_ptpow=0;
	i++;
      }
      else {
	cerr << "Keyword for min number of distinct nights supplied with no corresponding argument\n";
	show_usage();
	return(1);
      }
    } else if(string(argv[i]) == "-minpointnum" || string(argv[i]) == "-min_pts" || string(argv[i]) == "-minpoints" || string(argv[i]) == "-min_point_num" || string(argv[i]) == "-min_points" || string(argv[i]) == "--min_point_num" || string(argv[i]) == "--minpointnum" ) {
      if(i+1 < argc) {
	//There is still something to read;
	config.minpointnum=stoi(argv[++i]);
	default_ptpow=0;
	i++;
      }
      else {
	cerr << "Keyword for min number of individual detections supplied with no corresponding argument\n";
	show_usage();
	return(1);
      }
    } else if(string(argv[i]) == "-ptpow" || string(argv[i]) == "-ptexp" || string(argv[i]) == "-pointpow" || string(argv[i]) == "-pointnumpow" || string(argv[i]) == "-pointnum_exp" || string(argv[i]) == "--ptpow" || string(argv[i]) == "--pointnum_power") {
      if(i+1 < argc) {
	//There is still something to read;
	config.ptpow=stoi(argv[++i]);
	default_ptpow=0;
	i++;
      }
      else {
	cerr << "keyword for ptpow, the power to which the number of unique points\nis raised when calcuating the quality metric\nsupplied with no corresponding argument";
	show_usage();
	return(1);
      }
    } else if(string(argv[i]) == "-nightpow" || string(argv[i]) == "-nightexp" || string(argv[i]) == "-npow" || string(argv[i]) == "-nightnumpow" || string(argv[i]) == "-nightnum_exp" || string(argv[i]) == "--nightpow" || string(argv[i]) == "--nightnum_power") {
      if(i+1 < argc) {
	//There is still something to read;
	config.nightpow=stoi(argv[++i]);
	default_nightpow=0;
	i++;
      }
      else {
	cerr << "keyword for nightpow, the power to which the number of unique\n observing nights is raised when calcuating the quality metric\nsupplied with no corresponding argument";
	show_usage();
	return(1);
      }
    } else if(string(argv[i]) == "-timepow" || string(argv[i]) == "-timeexp" || string(argv[i]) == "-timexp" || string(argv[i]) == "-tpow" || string(argv[i]) == "-timespan_pow" || string(argv[i]) == "--timepow" || string(argv[i]) == "--timespan_power") {
      if(i+1 < argc) {
	//There is still something to read;
	config.timepow=stoi(argv[++i]);
	default_timepow=0;
	i++;
      }
      else {
	cerr << "keyword for timepow, the power to which the total timespan is raised when calcuating\nthe quality metric supplied with no corresponding argument";
	show_usage();
	return(1);
      }
    } else if(string(argv[i]) == "-rmspow" || string(argv[i]) == "-rmsexp" || string(argv[i]) == "-rmspower" || string(argv[i]) == "-rpow" || string(argv[i]) == "-astromrms_pow" || string(argv[i]) == "--rmspow" || string(argv[i]) == "--astrom_rms_power") {
      if(i+1 < argc) {
	//There is still something to read;
	config.rmspow=stoi(argv[++i]);
	default_rmspow=0;
	i++;
      }
      else {
	cerr << "keyword for rmspow, the power to which the astrometric\nRMS residual is raised when calcuatingthe quality metric\nsupplied with no corresponding argument";
	show_usage();
	return(1);
      }
    } else if(string(argv[i]) == "-maxrms" || string(argv[i]) == "-mr" || string(argv[i]) == "-mrms" || string(argv[i]) == "-rms" || string(argv[i]) == "-maxr" || string(argv[i]) == "--maxrms" || string(argv[i]) == "--maximumrms") {
      if(i+1 < argc) {
	//There is still something to read;
	config.maxrms=stod(argv[++i]);
	default_maxrms=0;
	i++;
      }
      else {
	cerr << "Maximum RMS keyword supplied with no corresponding argument";
	show_usage();
	return(1);
      }
    }  else if(string(argv[i]) == "-outsum" || string(argv[i]) == "-sum" || string(argv[i]) == "-rms" || string(argv[i]) == "-outrms" || string(argv[i]) == "-or" || string(argv[i]) == "--outsummaryfile" || string(argv[i]) == "--outsum" || string(argv[i]) == "--sum") {
      if(i+1 < argc) {
	//There is still something to read;
	outsumfile=argv[++i];
	default_sumfile=0;
	i++;
      }
      else {
	cerr << "Output summary file keyword supplied with no corresponding argument\n";
	show_usage();
	return(1);
      }
    } else if(string(argv[i]) == "-clust2det" || string(argv[i]) == "-c2d" || string(argv[i]) == "-clust2detfile" || string(argv[i]) == "--clust2detfile" || string(argv[i]) == "--clust2det" || string(argv[i]) == "--cluster_to_detection") {
      if(i+1 < argc) {
	//There is still something to read;
	outclust2detfile=argv[++i];
	default_clust2det=0;
	i++;
      }
      else {
	cerr << "Output cluster-to-detection file keyword supplied with no corresponding argument\n";
	show_usage();
	return(1);
      }
    } else if(string(argv[i]) == "-heliovane" || string(argv[i]) == "-use_heliovane" || string(argv[i]) == "-vane" || string(argv[i]) == "--uhv" || string(argv[i]) == "-usevane" || string(argv[i]) == "--use_heliovane") {
      if(i+1 < argc) {
	//There is still something to read;
	config.use_heliovane=stoi(argv[++i]);
	i++;
      }
      else {
	cerr << "Output cluster-to-detection file keyword supplied with no corresponding argument\n";
	show_usage();
	return(1);
      }
    } else if(string(argv[i]) == "-verbose" || string(argv[i]) == "-verb" || string(argv[i]) == "-VERBOSE" || string(argv[i]) == "-VERB" || string(argv[i]) == "--VERB" || string(argv[i]) == "--VERBOSE" || string(argv[i]) == "--verbose") {
      if(i+1 < argc) {
	//There is still something to read;
	config.verbose=stoi(argv[++i]);
	i++;
      }
      else {
	cerr << "keyword for verbosity supplied with no corresponding argument";
	show_usage();
	return(1);
      }
    } else {
      cerr << "Warning: unrecognized keyword or argument " << argv[i] << "\n";
      i++;
    }
  }

  // Catch required parameters if missing
  if(imfile.size()<=0) {
    cout << "\nERROR: input image catalog file is required\n";
    show_usage();
    return(1);
  } else if(pairdetfile.size()<=0) {
    cout << "\nERROR: input detection file is required\n";
    show_usage();
    return(1);
  } else if(clusterlist.size()<=0) {
    cout << "\nERROR: input cluster list file is required\n";
    show_usage();
    return(1);
  } else if(config.MJDref<=0.0l) {
    cout << "\nERROR: input reference MJD is required. Note that\n";
    cout << "it should match the reference MJD used in the heliolinc run\n";
    cout << "that produced the input files.\n";
    show_usage();
    return(1);
  }

  cout << "input paired detection file " << pairdetfile << "\n";
  cout << "input cluster list file " << clusterlist << "\n";
  cout << "Reference MJD: " << config.MJDref << "\n";
  cout << "Maximum RMS in km: " << config.maxrms << "\n";
  cout << "Maximum out-of-plane RMS in km: " << config.max_oop << "\n";
  cout << "Maximum astrometric RMS: " << config.max_astrom_rms << "\n";
  cout << "Maximum fraction of points to be rejected: " << config.rejfrac << "\n";
  cout << "Minimum number of observing nights: " << config.minobsnights << "\n";
  cout << "Minimum number of unique detections: " << config.minpointnum << "\n";
  cout << "output cluster file " << outclust2detfile << "\n";
  cout << "output rms file " << outsumfile << "\n";

  if(default_simptype==1) cout << "Defaulting to simplex type = " << config.simptype << "\n";
  else cout << "user-specified simplex type " << config.simptype << "\n\n";
  
  cout << "In calculating the cluster quality metric, the number of\n";
  cout << "unique points will be raised to the power of " << config.ptpow << ",\n";
  if(default_ptpow==1) cout << "which is the default.\n";
  else cout << "as specified by the user.\n";
  cout << "The number of unique nights will be raised to the power of " << config.nightpow << ",\n";
  if(default_nightpow==1) cout << "which is the default.\n";
  else cout << "as specified by the user.\n";
  cout << "The total timespan will be raised to the power of " << config.timepow << ",\n";
  if(default_timepow==1) cout << "which is the default.\n";
  else cout << "as specified by the user.\n";
  cout << "Finally, the astrometric RMS will be raised to the power of (negative) " << config.rmspow << ",\n";
  if(default_rmspow==1) cout << "which is the default.\n";
  else cout << "as specified by the user.\n\n";
  
  if(default_maxrms==1) cout << "Defaulting to maximum cluster RMS = " << config.maxrms << " km\n";
  else cout << "User-specified maximum cluster RMS is " << config.maxrms << " km\n";
  if(default_max_oop==1) cout << "Defaulting to maximum out-of-plane RMS = " << config.max_oop << " km\n";
  else cout << "User-specified maximum out-of-plane RMS is " << config.max_oop << " km\n";
  if(default_sumfile==1) cout << "WARNING: using default name " << outsumfile << " for summary output file\n";
  else cout << "summary output file " << outsumfile << "\n";
  if(default_clust2det==1) cout << "WARNING: using default name " << outclust2detfile << " for output clust2det file\n";
  else cout << "output clust2det file " << outclust2detfile << "\n";

  if(config.use_heliovane==1) cout << "Expecting input from heliovane rather than heliolinc\n";
  
  image_log={};
  status=read_image_file2(imfile, image_log);
  if(status!=0) {
    cerr << "ERROR: could not successfully read image file " << imfile << "\n";
    cerr << "read_image_file2 returned status = " << status << ".\n";
   return(1);
  }
  cout << "Read " << image_log.size() << " data lines from image file " << imfile << "\n";

  // Read paired detection file
  detvec={};
  status=read_pairdet_file(pairdetfile, detvec, config.verbose);
  if(status!=0) {
    cerr << "ERROR: could not successfully read paired detection file " << pairdetfile << "\n";
    cerr << "read_pairdet_file returned status = " << status << ".\n";
   return(1);
  }
  cout << "Read " << detvec.size() << " data lines from paired detection file " << pairdetfile << "\n";
  
  // Read cluster list, reading and concatenating the data from each
  // pair of files in the list.
  clustvecmain={};
  clust2detmain={};
  instream1.open(clusterlist,ios_base::in);
  if(!instream1) {
    cerr << "can't open input file " << clusterlist << "\n";
    return(1);
  }
  while(instream1 >> sumfile >> clust2detfile) {
    if(sumfile.size()>0 && clust2detfile.size()>0) {
      // Read cluster summary file
      inclustvec={};
      status=read_clustersum_file(sumfile, inclustvec, config.verbose);
      if(status!=0) {
	cerr << "ERROR: could not successfully read input cluster summary file " << sumfile << "\n";
	cerr << "read_clustersum_file returned status = " << status << ".\n";
	return(1);
      }
      cout << "Read " << inclustvec.size() << " data lines from cluster summary file " << sumfile << "\n";
      inclust2det={};
      // Read cluster-to-detection file
      status=read_longpair_file(clust2detfile, inclust2det, config.verbose);
      if(status!=0) {
	cerr << "ERROR: could not successfully read cluster-to-detection file " << clust2detfile << "\n";
	cerr << "read_longpair_file returned status = " << status << ".\n";
	return(1);
      }
      cout << "Read " << inclust2det.size() << " data lines from cluster-to-detection file " << clust2detfile << "\n";
      // Append data from the new summary file to the master list
      clustnum = clustvecmain.size();
      for(i=0;i<long(inclustvec.size());i++) {
	inclustvec[i].clusternum += clustnum;
	clustvecmain.push_back(inclustvec[i]);
      }
      for(i=0;i<long(inclust2det.size());i++) {
	inclust2det[i].i1 += clustnum;
	clust2detmain.push_back(inclust2det[i]);
      }
    } else {
      cerr << "WARNING: unable to read valid file names from cluster list file " << clusterlist << "\n";
    }
  }
  instream1.close();
  cout << "Finished creating master cluster summary vector with length " << clustvecmain.size() << ",\n";
  cout << "and master cluster-to-detection vector with length " << clust2detmain.size() << "\n";

  status = link_planarity(image_log, detvec, clustvecmain, clust2detmain, config, outclust, outclust2det);
  if(status!=0) {
    cerr << "ERROR: link_purify failed with status " << status << "\n";
    return(status);
  } 
  
  outstream1.open(outsumfile);
  cout << "Writing " << outclust.size() << " lines to output cluster-summary file " << outsumfile << "\n";
  outstream1 << "#clusternum,posRMS,velRMS,totRMS,astromRMS,pairnum,timespan,uniquepoints,obsnights,metric,rating,heliohyp0,heliohyp1,heliohyp2,posX,posY,posZ,velX,velY,velZ,orbit_a,orbit_e,orbit_MJD,orbitX,orbitY,orbitZ,orbitVX,orbitVY,orbitVZ,orbit_eval_count\n";
  for(clustct=0 ; clustct<long(outclust.size()); clustct++) {
    outstream1 << fixed << setprecision(3) << outclust[clustct].clusternum << "," << outclust[clustct].posRMS << "," << outclust[clustct].velRMS << "," << outclust[clustct].totRMS << ",";
    outstream1 << fixed << setprecision(4) << outclust[clustct].astromRMS << ",";
    outstream1 << fixed << setprecision(6) << outclust[clustct].pairnum << "," << outclust[clustct].timespan << "," << outclust[clustct].uniquepoints << "," << outclust[clustct].obsnights << "," << outclust[clustct].metric << "," << outclust[clustct].rating << ",";
    outstream1 << fixed << setprecision(6) << outclust[clustct].heliohyp0 << "," << outclust[clustct].heliohyp1 << "," << outclust[clustct].heliohyp2 << ",";
    outstream1 << fixed << setprecision(1) << outclust[clustct].posX << "," << outclust[clustct].posY << "," << outclust[clustct].posZ << ",";
    outstream1 << fixed << setprecision(4) << outclust[clustct].velX << "," << outclust[clustct].velY << "," << outclust[clustct].velZ << ",";
    outstream1 << fixed << setprecision(6) << outclust[clustct].orbit_a << "," << outclust[clustct].orbit_e << "," << outclust[clustct].orbit_MJD << ",";
    outstream1 << fixed << setprecision(1) << outclust[clustct].orbitX << "," << outclust[clustct].orbitY << "," << outclust[clustct].orbitZ << ",";
    outstream1 << fixed << setprecision(4) << outclust[clustct].orbitVX << "," << outclust[clustct].orbitVY << "," << outclust[clustct].orbitVZ << "," << outclust[clustct].orbit_eval_count << "\n";
  }
  outstream1.close();
  
  outstream1.open(outclust2detfile);
  cout << "Writing " << outclust2det.size() << " lines to output clust2det file " << outclust2detfile << "\n";
  outstream1 << "#clusternum,detnum\n";
  for(clustct=0 ; clustct<long(outclust2det.size()); clustct++) {
    outstream1 << outclust2det[clustct].i1 << "," << outclust2det[clustct].i2 << "\n";
  }
  outstream1.close();
  
  return(0);
}
