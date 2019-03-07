import array
import base64

import numpy as np

import xmltodict

__author__ = "Will Hewitt"
__credits__ = ["Will Hewitt"]
__version__ = "1.0.0"
__maintainer__ = "Will Hewitt"
__email__ = "william.hewitt@auckland.ac.nz"
__status__ = "Development"

class VCG:
    """ Class to compute VCG loops and calculate metrics """
    
    # matrix to reconstruct Franks XYZ from 8L 
    franks_x = np.matrix('-0.172; -0.074;  0.122;  0.231;  0.239;  0.194;  0.156; -0.010')
    franks_y = np.matrix('0.057; -0.019; -0.106; -0.022;  0.041;  0.048; -0.227;  0.887')
    franks_z = np.matrix('-0.229; -0.310; -0.246; -0.063;  0.055;  0.108;  0.022;  0.102')

    def __init__(self, ecg):

        self.ecg = ecg

        self.FranksX = np.zeros((ecg.lead_sample_count, 1))
        self.FranksY = np.zeros((ecg.lead_sample_count, 1))
        self.FranksZ = np.zeros((ecg.lead_sample_count, 1))

        self.__construct_franks()
    
    def mean_spatial_qrs_t(self):
        raise NotImplementedError
    
    def peak_spatial_qrs_t(self):
        raise NotImplementedError
    
    def __construct_franks(self):

        for i in range(0, self.ecg.lead_sample_count):

            sample = self.ecg.get_8L_sample(i)

            self.FranksX[i] = -1*(sample*self.franks_x)
            self.FranksY[i] = sample*self.franks_y
            self.FranksZ[i] = -1*(sample*self.franks_z)
            
        self.FranksX = np.squeeze(self.FranksX)
        self.FranksY = np.squeeze(self.FranksY)
        self.FranksZ = np.squeeze(self.FranksZ)


class ECG:
    """ Class that processes an XML file into an ECG object """ 

    def __init__(self, path):

        try:
            with open(path, 'rb') as xml:
                self.__file = xmltodict.parse(xml.read().decode('utf8'))
        except Exception as e:
            raise e

        self.__lead_data = self.__file['RestingECG']['Waveform']['LeadData']
        self.lead_sample_count = int(self.__lead_data[0]['LeadSampleCountTotal'])

        self.LeadI = np.zeros((self.lead_sample_count, 1))
        self.LeadII = np.zeros((self.lead_sample_count, 1))
        self.LeadIII = np.zeros((self.lead_sample_count, 1))
        self.LeadAVR = np.zeros((self.lead_sample_count, 1))
        self.LeadAVL = np.zeros((self.lead_sample_count, 1))
        self.LeadAVF = np.zeros((self.lead_sample_count, 1))
        self.LeadV1 = np.zeros((self.lead_sample_count, 1))
        self.LeadV2 = np.zeros((self.lead_sample_count, 1))
        self.LeadV3 = np.zeros((self.lead_sample_count, 1))
        self.LeadV4 = np.zeros((self.lead_sample_count, 1))
        self.LeadV5 = np.zeros((self.lead_sample_count, 1))
        self.LeadV6 = np.zeros((self.lead_sample_count, 1))

        self.__unpack()

    def get_8L_sample(self, i):

        return np.array([ self.LeadV1[i], self.LeadV2[i], self.LeadV3[i], self.LeadV4[i], self.LeadV5[i], self.LeadV6[i], self.LeadI[i], self.LeadII[i] ])

    def __unpack(self):

        for lead in self.__lead_data:

            lead_id = lead['LeadID']
            lead_data = lead['WaveFormData']
            lead_b64 = base64.b64decode(lead_data)
            lead_vals = np.array(array.array('h', lead_b64))

            if lead_id == 'I':
                self.LeadI = lead_vals
            elif lead_id == 'II':
                self.LeadII = lead_vals
            elif lead_id == 'V1':
                self.LeadV2 = lead_vals
            elif lead_id == 'V2':
                self.LeadV2 = lead_vals
            elif lead_id == 'V3':
                self.LeadV3 = lead_vals
            elif lead_id == 'V4':
                self.LeadV4 = lead_vals
            elif lead_id == 'V5':
                self.LeadV5 = lead_vals
            elif lead_id == 'V6':
                self.LeadV6 = lead_vals

        self.LeadIII = np.subtract(self.LeadII, self.LeadI)
        self.LeadAVR = np.add(self.LeadI, self.LeadII)*(-0.5)
        self.LeadAVL = np.subtract(self.LeadI, 0.5*self.LeadII)
        self.LeadAVF = np.subtract(self.LeadII, 0.5*self.LeadI)
