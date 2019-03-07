import numpy as np

from ECG import ECG

class FranksVCG():

    franks_matrix = np.matrix('-0.172 -0.074 0.122 0.231 0.239 0.194 0.156 -0.010;\
                                0.057 -0.019 -0.106 -0.022 0.041 0.048 -0.227 0.887;\
                               -0.229 -0.310 -0.246 -0.063 0.055 0.108 0.022 0.102')

    def __init__(self, ecg):

        self.FranksX = np.zeros((ecg.num_samples,1)) 
        self.FranksY = np.zeros((ecg.num_samples,1))
        self.FranksZ = np.zeros((ecg.num_samples,1))

        self.__constructFranks(ecg)

    def __constructFranks(self, ecg):

        for i in range(0, ecg.num_samples):
            sample = ecg.getSample(i)

            print(sample)
        