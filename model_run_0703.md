# Notebook for model run July 3.

| Begin | End |
|-------| ----|
| July 3, 2018| someday |

## Goals

* Review compiling/running the model
* Check the transfer resistance
* Make the spike height measured at the soma comparable to the data
    1. reduce Na conductance at soma and others,
    2. speed up opening of delayed rectifier K channels
* Make the model fire spontaneously


## Steps for compiling and running the model
**Setting up a git repo**: First, set up a git repo (`git init`), add `.gitignore`, a file that lists files to be ignored by git, add all the files `git add *`, and make the first commit `git commit -m "<COMMIT MESSAGE>"`.

2. Compile .mod files: `nrnivmodl` in the command line,
3. Current our main model file: `de3.py`. Use `ipython -i de3.py`,

## Spike height issue
### Trial 1: Na conductance change

1. To view the params of the soma, `h.psection(soma)`:
```
soma { nseg=2  L=40  Ra=200
	/*location 0 attached to cell 0*/
	/* First segment only */
	insert capacitance { cm=1}
	insert pcell { gnabar_pcell=0.35 gkbar_pcell=0.006 gl_pcell=0.0005 el_pcell=-49}
	insert na {}
	insert napump { vmax_napump=0.003 khalf_napump=12 ksteep_napump=1}
	insert na_ion {}
	insert gkca { gkcabar_gkca=0.0008 ikca_gkca=0.000348034}
	insert k_ion { ek=-68}
	insert ca {}
	insert morphology { diam=50}
	insert cach { gcabar_cach=2e-06}
	insert capump {}
	insert ca_ion {}
}
```
2. To change the conductance, `soma.gnabar_pcell = <VALUE>`.
    1. Try completely turning it off, `soma.gnabar_pcell=0`: Mesured spike hight reduced to ~15 mV.
    2. Further eliminate/reduce Na conductance in junction and axthick


## Steps to make the DE-3 model more motoneuron-like and less sensory neuron-like
1. Remove Ca-activated K conductance and replace with IA K conductance as seen in AP cells
* From Stewart et al., 1989
    * Inactivation time constant 26 ±
  2 ms
    * Activation time constant similar to Retz, 
2. Sodium activation adjustment --> spontaneous firing
* alpha = .06 * vtrap(-(v+28),15) (was 0.03) 
3. Na activation system
* alpha = .065 * exp(-(v+58)/18) (was 0.035)
4. Speed up K activation to truncate spike waveform
* kactrate from 0.75 --> 30.75 in .py file
5. Speed up K inactivation rate to prevent huge AHP
* k beta = 0.75*exp(-(v+48)/35) (was 0.3)
6. Attempt to further truncate waveform by speeding up Na inactivation rate in pcell.mod
* alpha = .180 * exp(-(v+58)/18) (was 0.095)

## Changes 7/5/18
1. Added Ornstein-Uhlenbeck noise to better mimic biological system
* OU term incorporated (ou.mod)
2. Added "mechanosensitive channel" USchan

## Changes 7/6-7/18
1. Incorporate neurites to better mimic DE-3 morphology



2. Incorporate synaptic inputs to get (small) PSPs


3. Continue to attempt to lower spike amplitude
* again increase Na inactivation rate
* 

4. Reduce baseline firing rate (lower Na activation rate?)
* reduced Na alpha = .035 * vtrap(-(v+28),15) (was 0.06)
	* now down to ~1Hz firing rate = target
* increased gl = .0008 (mho/cm2) (was 0.0005)

5. Increased .Ra from 200 to 300 in all sections

## Goals for 7/8/18
1. Play with temperature
2. Try to find Q10s for conductance parameters
* Q10 for Na, K


## When things go boring...
![Cat Karate](cat_karate.jpeg)

![In case of fire...](In_case_of_fire_git_push_first.jpg)






