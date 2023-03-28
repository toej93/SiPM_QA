#ifndef ROOT_TO_PHYS_H
#define ROOT_TO_PHYS_H

#include "Rtypes.h"

using namespace std;

class DataFile {
    public:
        string fileName; // TODO: not currently using abs paths
        FILE* file;
        int oldTimeTag = 0;
        int timeTagRollover;

        DataFile(string fileName);
        bool getNextTrigger(Int_t& event_ID, Long64_t& trg_time, vector<Double_t>& waveform);


    private:
        int headerLength = 32; // In bits
        int eventSize;
        int boardId;
};


class RawTrigger {
    public:
        int pattern;
        int channel;
        int eventCounter;
        //int triggerTimeTag;
        uint32_t triggerTimeTag;
        int triggerTime;
        vector<Double_t> trace;

        RawTrigger(int eventSize);
        vector<Double_t>& getTrace() {return trace;}
};

Bool_t check_saturation(vector<Double_t>);

Double_t calc_baseline(vector<Double_t>, Int_t, Int_t);

Double_t calc_integral(vector<Double_t>, Int_t, Int_t);

Int_t calc_CFD_sample(vector<Double_t>, Double_t);

#endif
