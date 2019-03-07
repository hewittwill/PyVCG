from PyVCG import ECG, VCG

# Create an ECG object from an XML file
ecg = ECG('ecg.xml')

# Create a VCG object from the ECG
vcg = VCG(ecg)

# Compute and print mean spatial QRST angle (i.e. mean angle between the QRS and T loops)
print( vcg.mean_spatial_qrs_t() )

# Compute and print peak spatial QRST angle (i.e. angle between the QRS and T loops at the R wave)
print( vcg.peak_spatial_qrs_t() )