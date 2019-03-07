import array
import base64

import numpy as np

import xmltodict


class ECG():
    """ Class to reconstruct an ECG from an XML file """

    def __init__(self, xml_path):

        try:
            with open(xml_path, 'rb') as xml:
                self.__xml_file = xmltodict.parse(xml.read().decode('utf8'))
        except Exception as e:
            raise e

        self.__lead_data = self.__xml_file['RestingECG']['Waveform']['LeadData']
        self.num_samples = int(self.__lead_data[0]['LeadSampleCountTotal'])

        self.test = int(self.__lead_data[0]['LeadSampleCountTotal'])

        
        self.LeadI = np.zeros((1, self.num_samples))
        self.LeadII = np.zeros((1, self.num_samples))
        self.LeadIII = np.zeros((1, self.num_samples))
        self.LeadAVR = np.zeros((1, self.num_samples))
        self.LeadAVL = np.zeros((1, self.num_samples))
        self.LeadAVF = np.zeros((1, self.num_samples))
        self.LeadV1 = np.zeros((1, self.num_samples))
        self.LeadV2 = np.zeros((1, self.num_samples))
        self.LeadV3 = np.zeros((1, self.num_samples))
        self.LeadV4 = np.zeros((1, self.num_samples))
        self.LeadV5 = np.zeros((1, self.num_samples))
        self.LeadV6 = np.zeros((1, self.num_samples))

        self.__reconstruct_voltages()

    def getSample(self, i):

        sample = np.array((1,8))
        sample[0] = self.LeadV1[i]
        sample[1] = self.LeadV2[i]
        sample[2] = self.LeadV3[i]
        sample[3] = self.LeadV4[i]
        sample[4] = self.LeadV5[i]
        sample[5] = self.LeadV6[i]
        sample[6] = self.LeadI[i]
        sample[7] = self.LeadII[i]
        
        return sample

    def __reconstruct_voltages(self):

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

            print(lead_vals.shape)

        self.LeadIII = np.subtract(self.LeadII, self.LeadI)
        self.LeadAVR = np.add(self.LeadI, self.LeadII)*(-0.5)
        self.LeadAVL = np.subtract(self.LeadI, 0.5*self.LeadII)
        self.LeadAVF = np.subtract(self.LeadII, 0.5*self.LeadI)
