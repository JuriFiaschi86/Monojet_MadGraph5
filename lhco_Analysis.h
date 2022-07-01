
#include <string>
#include <fstream>
#include <math.h>

//#include "Histogram.h"
//#include "Histogram.cpp"

using namespace std;


//lhco data from Jue, which can be read by Mathematica
class clLhcoMathObj
{
public:

    float index;
    float type;
    float eta;
    float phi;
    float pt;
    float mass;
    float chargeNtrk;
    float bTag;
    float Ehad2Em;
    float pID;
    float dum2;
    
    void clear()
    {
        index = 0.;
        type = -999.;
        eta = 99999.;
        phi = -99.;
        pt = 0.;
        mass = 0.;
        chargeNtrk = 0.;
        bTag = 0.;
        Ehad2Em = 0.;
        pID = 0.;
        dum2 = 0.;
    }

};


class clRecobj
{
public:

    float eta;
    float phi;
    float pt;
    float mass;
    float charge;
    float bTag;
    float pID;

    float px;
    float py;
    float pz;
    float p0;
    string mother;

    void fourVector()
    {
      px = pt * cos(phi);
      py = pt * sin(phi);
      pz = pt * sinh(eta);
      p0 = sqrt(px*px+py*py+pz*pz+mass*mass);
    }
    
    void clear()
    {
      eta = 99999.;
      phi = -99.;
      pt = 0.;
      mass = 0.;
      charge = 0.;
      bTag = 0.;
      pID = 0.;

      px = 0.;
      py = 0.;
      pz = 0.;
      p0 = 0.;

      mother = "none";
    }
};


class mgLheobj
{
public:
        int id;
        int iStatus;
        int iMoth1;
        int iMoth2;
        int iColfl1;
        int iColfl2;

        float px;
        float py;
        float pz;
        float p0;
        float mass;
        float helicity;
	
	void clear()
	{
             id = 1199222;
             iStatus = 1199222;
             iMoth1 = 1199222;
             iMoth2 = 1199222;
             iColfl1 = 1199222;
             iColfl2 = 1199222;

             px = 0.;
             py = 0.;
             pz = 0.;
             p0 = 0.;
             mass = 0.;
             helicity = 1199222.;
	}
};


class clLheobj
{
public:

    int id;

    float p0;
    float px;
    float py;
    float pz;
    float pt;
    float phi;
    float eta;
    float mass;
    float charge;
    
    void clear()
    {
        id =0;

        p0 = 0.;
        px = 0.;
        py = 0.;
        pz = 0.;
        pt = 0.;
        phi = -99.;
        eta = 99999.;
        mass = 0.;
        charge = 0.;
    }

};


class visTau
{
public:
	int index;
        int indPGS;
        int indMC;
        int imatch;
        float charge;
	float px;
	float py;
	float pz;
	float p0;
	float pt;
        float eta;
	float pxvis;
	float pyvis;
	float pzvis;
	float p0vis;
	float ptvis;
	float ptiso;
        int   tightUnique;
        int   looseUnique;

	void clear()
	{
                index = 0;
                indPGS = -1;
                indMC = -1;
                imatch = -1;
		charge = 0.;
		px = 0.;
		py = 0.;
		pz = 0.;
		p0 = 0.;
		pt = 0.;
                           eta = 99999.;
		pxvis = 0.;
		pyvis = 0.;
		pzvis = 0.;
		p0vis = 0.;
		ptvis = 0.;
		ptiso = 0.;
                tightUnique = -1;
                looseUnique = -1;
	}
};

        bool ReadEventsAndAnalyze();
        bool AnalyzeEvents();
        void FindCorrectPair(float &mN, float &mW);
        int solveEqn(float *slns, float a, float b, float c);
        float determinePT(float p_x, float p_y);
        float determinePhi(float p_x, float p_y);
        float determineEta(float p_x, float p_y, float p_z);
        float determineDeltaPhi(float phi1, float phi2);
        float determineDeltaR(float p1_x, float p1_y, float p1_z, float p2_x, float p2_y, float p2_z);
        void sortLheobjs(const int nObjs, clLheobj *theObjs);
        void sortRecobjs(const int nObjs, clRecobj *theObjs);
        void sortTaus(const int nTaus, visTau *theTaus);
        float determineMass(float p0, float px, float py, float pz);
        float determineMT(float p1_m, float p1_x, float p1_y, float p2_m, float p2_x, float p2_y);
        float determineMrecoil(float sqrtS, float p0, float px, float py, float pz);
        void LorentzTrans(float *pLT, float *pRef);

        float dPhiMetEl[45];
        float mtMetEl[45];

        float dPhiMetMu[45];
        float mtMetMu[45];

        float mMuEl[45];
        float dPhiMuEl[45];
        float phiMuEl[45];
        float dPhiMetMuEl[45];
        float mtMetMuEl[45];

        float mElMu[45];
        float dPhiElMu[45];
        float phiElMu[45];
        float dPhiMetElMu[45];
        float mtMetElMu[45];

        clLhcoMathObj lhcoObj[45];
        int numLhcoObj;

        clRecobj myElectrons[45];
        int numElectrons;

        clRecobj myMuons[45];
        int numMuons;

        clRecobj myTaus[45];
        int numTaus;

        clRecobj myJets[45];
        int numJets;

        clRecobj myMet;
        clRecobj myNeutrino;

        float crSec;
        int totalEvents;
        //int numTotalEvtsNoSln;
        int eventNumber;
        int fileNumber;
        float nCuts[50];

        // --- For IO.
        string fileNamePart;

        // --- Histograms.
        //Histogram* hCuts;

        ofstream outData;








