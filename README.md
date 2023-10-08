# ./postprocessing

You should only be running this after all the data has been preprocessed in the ../preprocessing/X/ folder, where X is the dataset type (one of cat or monkey, currently)

.py files are labelled sn_X.py for single neuron analysis, clustering.py for the intermediate clustering step, and decoding_X.py for the logistic regression decoding.
Running main.py should be straightforward and do everything automatically.

## TODO : migrate the CSD and logistic regression parameter scan to this repo

## run_introduction.py ; utils_introduction.py
Makes the introduction figures (a natural images + HOG) and generates MotionClouds for illustrative purposes

## run_sn_tuning_curves.py ; utils_single_neuron.py
Makes tuning curves for the example neurons and computes statistics.
* If clustering has been performed, makes a figure showing that last btheta at which a neuron is tuned

## run_sn_psth.py ; utils_single_neuron.py
Makes PSTH figures, pretty straightforward and light

## run_sn_dynamics ; utils_single_neuron.py
Computes the dynamical properties of the tuning curves and the firing rates, and also computes a very important array that serves for clustering and some NKR properties later on
* If clustering has been performed, makes two figures of optimal delay ratio and early/late spiking ratio

## run_sn_NKR ; utils_single_neuron.py
Makes the Naka-Rushton plots for single neuron and population, requires run_sn_dynamics to have been run.
* If clustering has been performed, makes a plot of circular variance at Btheta = 0 and Btheta = 36 deg.
