
#include <string>
#include <fstream>
#include <iostream>
#include <sstream>
#include <math.h>
#include <algorithm>

#include "lhco_Analysis.h"
//#include "ran1.h"

#define PI 3.1415926536

using namespace std;

int main(int argc, char *argv[]){ //func:14

int programStep;
stringstream sin;

  if(argc != 3) // accept only one command line argument.
     cout<<"usage: "<<argv[0]<<"  filename  "<<"  CrossSection\n\n";
        else {
           fileNamePart = argv[1];
           sin<<argv[2];
           sin>>crSec;
           cout<<"crSec = "<<crSec<<endl;
           
           ReadEventsAndAnalyze();
           programStep++;
  }

return programStep;

}//endFunc:14


bool ReadEventsAndAnalyze(){//func:38
    
    

int setLuminosity = 1;// luminosity = 1 fb^-1
int numEventsMax = crSec*setLuminosity;
cout<<"setLuminosity = "<<setLuminosity<<endl;
cout<<"numEventsMax = "<<numEventsMax<<endl;

        float tempFloat;
        int nStart = -1;

totalEvents = 0;
for(int i=0; i<50; i++){
  nCuts[i] = 0.;
}

string fileName;
string eventPart;
stringstream eventLine;

//set the output file name
outData.open ("data/lhco_Analysis_mva.dat", std::ofstream::out | std::ofstream::app);
//hCuts       = new Histogram("hCuts");


for(fileNumber=1; fileNumber<=900000; fileNumber++){//for:40
    
    


//input your file name here
fileName.clear();
fileName.assign("");
fileName.append(fileNamePart);
fileName.append("-");

stringstream ssFileNumber;
ssFileNumber.clear();
ssFileNumber<<fileNumber;
fileName.append(ssFileNumber.str());

fileName.append(".lhco"); 
cout<<fileName<<"\n\n";
ifstream inFile(fileName.data(), ifstream::in);

    nStart = -1;
    if(inFile.good()) {// if:260

   eventNumber = 0;
   numLhcoObj = 0;
   for(int i=0; i<45; i++){
     lhcoObj[i].clear();
   }
   


            //skipe the head part
            eventPart.clear();
            while(!inFile.eof() && eventPart.compare("dum2") != 0){
                eventPart.clear();
                inFile>>eventPart;
            }
//                   cout<<"#"<<eventNumber<<" L272: eventPart = "<<eventPart<<endl;

             inFile>>nStart;
             while(!inFile.eof()) {// while:263

                     // Read eventNumber and print 100th event
                     if(nStart==0){// if:313 begin event

                     // Clear event variables:
        numLhcoObj = 0;
        for(int i=0; i<45; i++){
          lhcoObj[i].clear();
        }

        numElectrons = 0;
        numMuons = 0;
        numTaus = 0;
        numJets = 0;
        myMet.clear();
        myNeutrino.clear();
        for(int i=0; i<45; i++){
          myElectrons[i].clear();
          myMuons[i].clear();
          myTaus[i].clear();
          myJets[i].clear();
        }

                         // Read eventNumber and print 1000th event
                         inFile>>eventNumber>>tempFloat;
                         if(eventNumber % 10000 == 0)
                            cout<<eventNumber<<endl;
                         inFile>>nStart;

                          while(!inFile.eof() && nStart!=0){

     inFile>>lhcoObj[numLhcoObj].type>>lhcoObj[numLhcoObj].eta>>lhcoObj[numLhcoObj].phi
           >>lhcoObj[numLhcoObj].pt>>lhcoObj[numLhcoObj].mass>>lhcoObj[numLhcoObj].chargeNtrk
           >>lhcoObj[numLhcoObj].bTag>>lhcoObj[numLhcoObj].Ehad2Em>>lhcoObj[numLhcoObj].pID
           >>lhcoObj[numLhcoObj].dum2;

                             numLhcoObj++;
                             inFile>>nStart;
                          }


                      }// endif:313 
                      else{
                        cout<<"\n\n ERROR: begin wrong event!!!";
                        cout<<"\n\n     nStart = "<<nStart;
                        cout<<"\n\n\n";
                        return false;
                      }// endif:313 


//====================================
                              for(int i=0; i<45; i++) {
                                  myTaus[i].clear();
                               }

          //loop over lhco reconstructed objects
          //convert them into myElectrons, myMuons, myTaus, myJets, myMet
          for(int i=0; i<numLhcoObj; i++){//for:157
            //cout<<lhcoObj[i].type<<"  "<<lhcoObj[i].eta<<"  "<<lhcoObj[i].phi<<"  "<<lhcoObj[i].pt<<"  "
            //<<lhcoObj[i].mass<<"  "<<lhcoObj[i].chargeNtrk<<"  "<<lhcoObj[i].bTag<<"  "
            //<<lhcoObj[i].Ehad2Em<<"  "<<lhcoObj[i].pID<<"  "<<lhcoObj[i].dum2<<endl;

            if(lhcoObj[i].type==1){
               myElectrons[numElectrons].eta = lhcoObj[i].eta;
               myElectrons[numElectrons].phi = lhcoObj[i].phi;
               myElectrons[numElectrons].pt  = lhcoObj[i].pt;
               myElectrons[numElectrons].mass = lhcoObj[i].mass;
               myElectrons[numElectrons].charge = lhcoObj[i].chargeNtrk;

               myElectrons[numElectrons].fourVector();

               numElectrons++;
            }

            else if(lhcoObj[i].type==2){
               myMuons[numMuons].eta = lhcoObj[i].eta;
               myMuons[numMuons].phi = lhcoObj[i].phi;
               myMuons[numMuons].pt  = lhcoObj[i].pt;
               myMuons[numMuons].mass = lhcoObj[i].mass;
               myMuons[numMuons].charge = lhcoObj[i].chargeNtrk;

               myMuons[numMuons].fourVector();

               numMuons++;
            }

            else if(lhcoObj[i].type==3){
               myTaus[numTaus].eta = lhcoObj[i].eta;
               myTaus[numTaus].phi = lhcoObj[i].phi;
               myTaus[numTaus].pt  = lhcoObj[i].pt;
               myTaus[numTaus].mass = lhcoObj[i].mass;
               myTaus[numTaus].charge = lhcoObj[i].chargeNtrk;

               myTaus[numTaus].fourVector();

               numTaus++;
            }

            else if(lhcoObj[i].type==4){
               myJets[numJets].eta = lhcoObj[i].eta;
               myJets[numJets].phi = lhcoObj[i].phi;
               myJets[numJets].pt  = lhcoObj[i].pt;
               myJets[numJets].mass = lhcoObj[i].mass;
               myJets[numJets].bTag = lhcoObj[i].bTag;
               myJets[numJets].pID  = lhcoObj[i].pID;

               myJets[numJets].fourVector();

               numJets++;
            }

            else if(lhcoObj[i].type==6){
               myMet.phi = lhcoObj[i].phi;
               myMet.pt  = lhcoObj[i].pt;

               myMet.px = myMet.pt * cos(myMet.phi);
               myMet.py = myMet.pt * sin(myMet.phi);

            }

          }//endfor:157

          //Sort by pt
          sortRecobjs(numElectrons, myElectrons);
          sortRecobjs(numMuons, myMuons);
          sortRecobjs(numTaus, myTaus);
          sortRecobjs(numJets, myJets);

//Begin to analyze
// ==================================
          
                 

          AnalyzeEvents();
          
                

          totalEvents++;

        //cout the infomation
        if(totalEvents % 10000 == 0) cout<<"totalEvents = "<<totalEvents<<endl;
        if(totalEvents % 100 == 0) cout<<"totalEvents = "<<totalEvents<<endl;
        if(totalEvents>= numEventsMax) return true;

      }  // endwhile:263 next Event
    }// endif:260
    else { // The file was bad or does not exist!!
      // Write an error message and die.
      cout<<"\n\n ERROR: Does that file really exist??";
      cout<<"\n\n     FileName = "<<fileName;
      cout<<"\n\n\n";
      return false;
    }
    
    inFile.close();

    cout<<"========================================"<<endl;
    cout<<"totalEvents = "<<totalEvents<<endl;
    for(int i=0; i<50; i++){
          cout<<nCuts[i]<<endl;
    }

  }//endFor:40 File has ended.  Next File.

  outData.close();
  // All files have ended.
  return true;

}//endFunc:38


bool AnalyzeEvents(){

// Analyze the current event......        
    
          
        for(int i=0; i<45; i++){
              dPhiMetEl[i] = -99.;
                mtMetEl[i] = 0.;

              dPhiMetMu[i] = -99.;
                mtMetMu[i] = 0.;
        }

        float mjj = 0.;
        float mjjEl = 0.;
        float mjjMu = 0.;
        float mElMu = 0.;
        float mjjElMu = 0.;
        float ht = 0.;//sum of all jets pt

        float p0Allj = 0.;
        float pxAllj = 0.;
        float pyAllj = 0.;
        float pzAllj = 0.;
        float mAllj = 0.;
        float mAlljEl = 0.;
        float mAlljElMu = 0.;

        int numBjets = 0;

        float  ptjjEl = 0.;
        float  ptjjMu = 0.;
        float phijjEl = -99.;
        float etajjEl = -999.;
        float phijjMu = -99.;
        float etajjMu = -999.;

        float phijj    = -99.;
        float dPhijjEl = -99.;
        float dPhij1El = -99.;
        float dPhij2El = -99.;
        float dPhijjMu = -99.;
        float dPhij1Mu = -99.;
        float dPhij2Mu = -99.;

        float etajj    = -999.;
        float dEtajjEl = -999.;
        float dEtaj1El = -999.;
        float dEtaj2El = -999.;
        float dEtajjMu = -999.;
        float dEtaj1Mu = -999.;
        float dEtaj2Mu = -999.;

        float dRjjEl = -9999.;
        float dRj1El = -9999.;
        float dRj2El = -9999.;
        float dRjjMu = -9999.;
        float dRj1Mu = -9999.;
        float dRj2Mu = -9999.;
        
        
        float maxjetpT = 0.;

        //------------------
        //Basic cuts
        nCuts[0]++;

        // >= 1 mu-
//         if(numMuons < 1)  return false;
//         nCuts[1]++;

//         if(myMuons[0].charge != -1)  return false;
//         nCuts[2]++;

        // >= 1 e+
//         if(numElectrons < 1)  return false;
//         nCuts[3]++;

//         if(myElectrons[0].charge != 1)  return false;
//         nCuts[4]++;

        // >= 2 j
//         if(numJets < 2)  return false;
//         nCuts[5]++;

        //------------------
        for(int i=0; i<numJets; i++){
          if(myJets[i].bTag > 0 )  {
              numBjets++;
          }
          ht = ht + myJets[i].pt;

          p0Allj = p0Allj + myJets[i].p0;
          pxAllj = pxAllj + myJets[i].px;
          pyAllj = pyAllj + myJets[i].py;
          pzAllj = pzAllj + myJets[i].pz;
        }
        
    
        for(int i=0; i<numJets; i++){
            if (myJets[i].pt > maxjetpT) {
                maxjetpT = myJets[i].pt;
            }
        }
        
        
        if (maxjetpT < 150.) {
            return true;
        }
        
        if (ht < 200.) {
            return true;
        }
        

        mAllj = determineMass(p0Allj, pxAllj, pyAllj, pzAllj );

        mAlljEl = determineMass(p0Allj + myElectrons[0].p0, 
                                pxAllj + myElectrons[0].px, 
                                pyAllj + myElectrons[0].py, 
                                pzAllj + myElectrons[0].pz );

        mAlljElMu = determineMass(p0Allj + myElectrons[0].p0 + myMuons[0].p0, 
                                  pxAllj + myElectrons[0].px + myMuons[0].px, 
                                  pyAllj + myElectrons[0].py + myMuons[0].py, 
                                  pzAllj + myElectrons[0].pz + myMuons[0].pz );

        mjj = determineMass(myJets[0].p0 + myJets[1].p0, 
                            myJets[0].px + myJets[1].px, 
                            myJets[0].py + myJets[1].py, 
                            myJets[0].pz + myJets[1].pz );

        mElMu = determineMass(myElectrons[0].p0 + myMuons[0].p0, 
                              myElectrons[0].px + myMuons[0].px, 
                              myElectrons[0].py + myMuons[0].py, 
                              myElectrons[0].pz + myMuons[0].pz );

        mjjElMu = determineMass(myJets[0].p0 + myJets[1].p0 + myElectrons[0].p0 + myMuons[0].p0, 
                                myJets[0].px + myJets[1].px + myElectrons[0].px + myMuons[0].px, 
                                myJets[0].py + myJets[1].py + myElectrons[0].py + myMuons[0].py, 
                                myJets[0].pz + myJets[1].pz + myElectrons[0].pz + myMuons[0].pz );


        ptjjEl = determinePT(myJets[0].px + myJets[1].px + myElectrons[0].px, 
                             myJets[0].py + myJets[1].py + myElectrons[0].py );
        phijjEl = determinePhi(myJets[0].px + myJets[1].px + myElectrons[0].px, 
                               myJets[0].py + myJets[1].py + myElectrons[0].py );
        etajjEl = determineEta(myJets[0].px + myJets[1].px + myElectrons[0].px, 
                               myJets[0].py + myJets[1].py + myElectrons[0].py, 
                               myJets[0].pz + myJets[1].pz + myElectrons[0].pz);
        mjjEl = determineMass(myJets[0].p0 + myJets[1].p0 + myElectrons[0].p0, 
                              myJets[0].px + myJets[1].px + myElectrons[0].px, 
                              myJets[0].py + myJets[1].py + myElectrons[0].py, 
                              myJets[0].pz + myJets[1].pz + myElectrons[0].pz );
        ptjjMu  = determinePT(myJets[0].px + myJets[1].px + myMuons[0].px, 
                              myJets[0].py + myJets[1].py + myMuons[0].py );
        phijjMu = determinePhi(myJets[0].px + myJets[1].px + myMuons[0].px, 
                               myJets[0].py + myJets[1].py + myMuons[0].py );
        etajjMu = determineEta(myJets[0].px + myJets[1].px + myMuons[0].px, 
                               myJets[0].py + myJets[1].py + myMuons[0].py, 
                               myJets[0].pz + myJets[1].pz + myMuons[0].pz );
        mjjMu = determineMass(myJets[0].p0 + myJets[1].p0 + myMuons[0].p0, 
                              myJets[0].px + myJets[1].px + myMuons[0].px, 
                              myJets[0].py + myJets[1].py + myMuons[0].py, 
                              myJets[0].pz + myJets[1].pz + myMuons[0].pz );

        phijj = determinePhi(myJets[0].px + myJets[1].px, 
                             myJets[0].py + myJets[1].py );
        dPhijjEl = determineDeltaPhi(phijj, myElectrons[0].phi );
        dPhij1El = determineDeltaPhi(myJets[0].phi, myElectrons[0].phi );
        dPhij2El = determineDeltaPhi(myJets[1].phi, myElectrons[0].phi );
        dPhijjMu = determineDeltaPhi(phijj, myMuons[0].phi );
        dPhij1Mu = determineDeltaPhi(myJets[0].phi, myMuons[0].phi );
        dPhij2Mu = determineDeltaPhi(myJets[1].phi, myMuons[0].phi );

        etajj = determineEta(myJets[0].px + myJets[1].px, 
                             myJets[0].py + myJets[1].py, 
                             myJets[0].pz + myJets[1].pz );
        dEtajjEl = fabs(        etajj - myElectrons[0].eta );
        dEtaj1El = fabs(myJets[0].eta - myElectrons[0].eta );
        dEtaj2El = fabs(myJets[1].eta - myElectrons[0].eta );
        dEtajjMu = fabs(        etajj - myMuons[0].eta );
        dEtaj1Mu = fabs(myJets[0].eta - myMuons[0].eta );
        dEtaj2Mu = fabs(myJets[1].eta - myMuons[0].eta );

        dRjjEl = determineDeltaR( myJets[0].px + myJets[1].px, 
                                  myJets[0].py + myJets[1].py, 
                                  myJets[0].pz + myJets[1].pz,
                                  myElectrons[0].px, myElectrons[0].py, myElectrons[0].pz );
        dRj1El = determineDeltaR( myJets[0].px, myJets[0].py, myJets[0].pz,
                                  myElectrons[0].px, myElectrons[0].py, myElectrons[0].pz );
        dRj2El = determineDeltaR( myJets[1].px, myJets[1].py, myJets[1].pz,
                                  myElectrons[0].px, myElectrons[0].py, myElectrons[0].pz );
        dRjjMu = determineDeltaR( myJets[0].px + myJets[1].px, 
                                  myJets[0].py + myJets[1].py, 
                                  myJets[0].pz + myJets[1].pz,
                                  myMuons[0].px, myMuons[0].py, myMuons[0].pz );
        dRj1Mu = determineDeltaR(  myJets[0].px,  myJets[0].py,  myJets[0].pz,
                                  myMuons[0].px, myMuons[0].py, myMuons[0].pz );
        dRj2Mu = determineDeltaR(  myJets[1].px,  myJets[1].py,  myJets[1].pz,
                                  myMuons[0].px, myMuons[0].py, myMuons[0].pz );

        //-------------------------------
        // only output possible useful obervables
        
        
//         outData << " " << totalEvents+1 << "  " << numMuons << "  " << numElectrons << "  " << numJets << "  " << numTaus << "  " << ht << endl;
        
        outData << " " << totalEvents+1 << "  " << numJets << "  " << "  " << ht << " " << maxjetpT << endl;

        //------------------

        return true;
}


// ============================================================================
void sortRecobjs(const int nObjs, clRecobj *theObjs)
{
  clRecobj dummyObj;
  
  if (nObjs == 0) return;
  
  for (int i = 0; i < nObjs - 1; i++)
    for (int j = i + 1; j < nObjs; j++)
      if ( (theObjs+j)->pt > (theObjs+i)->pt ) {
        dummyObj = *(theObjs+j);
        *(theObjs+j) = *(theObjs+i);
        *(theObjs+i) = dummyObj;
  }
}


void sortLheobjs(const int nObjs, clLheobj *theObjs)
{
	clLheobj dummyObj;
	
	if (nObjs == 0) return;
	
	for (int i = 0; i < nObjs - 1; i++)
		for (int j = i + 1; j < nObjs; j++)
			if ( (theObjs+j)->pt > (theObjs+i)->pt ) {
				dummyObj = *(theObjs+j);
				*(theObjs+j) = *(theObjs+i);
				*(theObjs+i) = dummyObj;
	}
}


void sortTaus(const int nTaus, visTau *theTaus)
{
	visTau dummyTau;
	
	if (nTaus == 0) return;
	
	for (int i = 0; i < nTaus - 1; i++)
		for (int j = i+1; j < nTaus; j++)
      	if ( (theTaus+j)->ptvis > (theTaus+i)->ptvis) {
				dummyTau = *(theTaus+j);
				*(theTaus+j) = *(theTaus+i);
				*(theTaus+i) = dummyTau;
	}
}


float determineEta(float p_x, float p_y, float p_z)
{
  float theta, eta, p_t;
  
  p_t = sqrt(p_x*p_x + p_y*p_y);

  theta = atan(fabs(p_t / p_z));
  if(p_z < 0.)
    theta = PI - theta;
  eta = -log(tan(theta / 2));
  
  return eta;
}


float determinePhi(float p_x, float p_y)
{
  float phi;
  
  phi = atan(fabs(p_y / p_x));
  if(p_x < 0. && p_y > 0.)
    phi = PI - phi;
  if(p_x < 0. && p_y < 0.)
    phi = PI + phi;
  if(p_x > 0. && p_y < 0.)
    phi = 2*PI - phi;
    
  return phi;
}


float determineDeltaPhi(float phi1, float phi2)
{
  float deltaphi;
  
  deltaphi = fabs(phi1 - phi2);
  if(deltaphi > PI)
    deltaphi = 2.*PI - deltaphi;
  
  return deltaphi;
}


float determinePT(float p_x, float p_y)
{
	float pt;
	pt = sqrt(p_x*p_x + p_y*p_y);
	return pt;
}


float determineDeltaR(float p1_x, float p1_y, float p1_z, float p2_x, float p2_y, float p2_z)
{
  float delR, eta1, eta2, phi1, phi2, delphi;
  
  eta1 = determineEta(p1_x, p1_y, p1_z);
  eta2 = determineEta(p2_x, p2_y, p2_z);
  
  phi1 = determinePhi(p1_x, p1_y);
  phi2 = determinePhi(p2_x, p2_y);
  
  delphi = fabs(phi1 - phi2);
  if(delphi > PI)
    delphi = 2.*PI - delphi;
  
  delR = sqrt((eta1 - eta2)*(eta1 - eta2) + delphi*delphi);
  
  return delR;
}


float determineMass(float p0, float px, float py, float pz)
{
   float mass;

   mass = p0*p0 - px*px - py*py - pz*pz;
   if(mass < 0.)  mass = -sqrt(-mass);
   else mass = sqrt(mass);

   return mass;
}


float determineMT(float p1_m, float p1_x, float p1_y, float p2_m, float p2_x, float p2_y)
{
   float et1, et2, mt;

   et1 = sqrt(p1_m*p1_m + p1_x*p1_x + p1_y*p1_y);
   et2 = sqrt(p2_m*p2_m + p2_x*p2_x + p2_y*p2_y);

   mt = p1_m*p1_m + p2_m*p2_m + 2.*(et1*et2 - p1_x*p2_x - p1_y*p2_y);
   if(mt < 0.)  mt = -sqrt(-mt); //in case nan
   else mt = sqrt(mt);

   return mt;
}

