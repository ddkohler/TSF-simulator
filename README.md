# TSF simulator

This TSF simulator is a user-friendly wrapper for simulating VVE-TRSF with the CMDS simulation package [NISE](https://github.com/wright-group/NISE).  The simulator considers a system with two vibrational modes (`I` and `i`), and their two-quantum modes (overtones and combination band).  There are two electronic states (`a` and `b`) that can be accessed from the two-quantum states.  The simulator includes functions to easily convert `NISE.lib.scan.Scan` objects into [WrightTools](http://wright.tools/en/master/)'s `Data` objects.  

## Setup

To setup, clone this repo to a `PYTHONPATH` folder.  You will also need [NISE](https://github.com/wright-group/NISE), [WrighTools](http://wright.tools/en/master/install.html), Numpy, and Scipy.

## Contents

* `lib.py` - library of functions useful for processing
* `run.py` - a template for running NISE simulations and converting into `WrightTools.Data` objects
* `H_TRSF.png` - image illustrating the states built in to this hamiltonian

## Running

The simulation is based on the `lib.run` command, which must be supplied with three dictionaries:  

1.  The `axes` dictionary:  controls the multidimensional space explored.  Keys define the properties of the laser that are changed (e.g., `'w2'`), and values are the points scanned (e.g. `numpy.linspace`)
2.  The `constants` dictionary: controls the parameters of the laser that are not scanned (e.g. `constants['d2'] = 0`)
3.  The `system` dictionary:  this controls the properties of the model system (dipoles, resonant frequencies, and dephasing rates).  The keys of this dictionary correspond to parameters of the Hamiltonian class `NISE.hamiltonians.H_TRSF` (all important keys can be found by inspecting `NISE.hamiltonians.H_TRSF.out_vars`).

Once these dictionaries are assembled, the simulation can be called:
```
# axes, constants and system are all dicts 
lib.run(axes, constants, system)
```
Upon completion, the simulation returns the output folder filepath.  The data can then be imported as a `Data` object using `l.load(fpath)`.  Again, `run.py` is an explicit template that performs all these actions.  

