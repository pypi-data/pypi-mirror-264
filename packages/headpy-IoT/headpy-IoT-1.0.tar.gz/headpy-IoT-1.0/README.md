# ```HEADpy``` Library
A frequency-based anomaly detection library for homomorphically encrypted IoT data.

The ```HEADpy``` library offers support build equi-width histograms and to detect anomalies within HE IoT sensor data, based on the distribution of the data, using ```Concrete``` circuits.  


## Structure of the repository
The repository is structured as follows:
- "src/data_preprocessing": includes data preprocessing functionalities and the configuration which allows setting the data source
- "src/histo_building": includes the onfiguration for building the histogram and the histogram building module (```builder```) which is responsible for building both clear and cryptographic equi-width histograms
- "src/anomaly_detection": implements the anomaly detection functionalities within the ```detector``` module and allows setting the anomaly detection configuration parameters
- "src/concrete_aux": includes function-agnostic ```Concrete``` circuits compilation, tesing and checking the results against the results of the corresponding clear function on the same data sample
- "src/examples": includes some code examples of calling the functions within the library on specific data samples
- "doc": includes the library documentation
- "LICENSE"
- "README.md": this file


## References
Hangan, A., Lazea, D., & Cioara, T. (2024). Privacy Preserving Anomaly Detection on Homomorphic Encrypted Data from IoT Sensors. arXiv preprint arXiv:2403.09322. 