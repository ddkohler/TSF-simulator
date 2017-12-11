# TSF simulator

This TSF simulator is a user-friendly wrapper for simulating VVE-TRSF with the CMDS simulation package [NISE](https://github.com/wright-group/NISE).  The simulator considers a system with two vibrational modes (`I` and `i`), and their two-quantum modes (overtones and combination band).  There are two electronic states (`a` and `b`) that can be accessed from the two-quantum states.  The simulator includes functions to easily convert `NISE.lib.scan.Scan` objects into [WrightTools](http://wright.tools/en/master/)'s `Data` objects.  

## Setup

To setup, clone this repo to a `PYTHONPATH` folder.  You will also need [NISE](https://github.com/wright-group/NISE), [WrighTools](http://wright.tools/en/master/install.html), Numpy, and Scipy.

## Contents

* `lib.py` - library of functions useful for processing
* `run.py` - a template for running NISE simulations and converting into `WrightTools.Data` objects
* `H_TRSF.png` - image illustrating the states built in to this hamiltonian


