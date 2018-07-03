*****to compile mod files: go to directory where mod files are stored
should say successfully created special file


nrnivmodl




This is an implementation of Stephen Baccus's original model from the paper
Baccus SA. Synaptic facilitation by reflected action potentials: 
enhancement of transmission when nerve impulses reverse direction 
at axon branch points. Proc Natl Acad Sci U S A. 1998 Jul 7;95(14):8345-50
with minor changes by Michael Hines and Tom Morse.

Stephen Baccus's email:
baccus@fas.harvard.edu

How to use:

First install the neuron simulator if you have not already:
http://www.neuron.yale.edu

To start the simulation:

On Macintosh computers:

   Download the zip file.
   Drag it onto the mos2nrn application icon.

On PC's or UNIX:

   Auto-launch the program from the model description page in modelDB.
   (or download, extract the zip file; compile with mknrndll;  Clicking on
   the mosinit.hoc file on the pc or typing nrngui mosinit.hoc under
   unix will start the simulation)

----------------------------------

Once the default simulation is started you can
1)click on the Voltage Space Plot and then
2)click on the Fig 6 button.

Action potentials are shown propagating down the stimulated
axon and then occasionally reflecting back down this stimulated
axon and also propagating into the thick axon and the thin posterior
axon.  See paper for details. Note that the AP's travel faster in 
thicker axons than thiner axons.

If you wish to slow down the simulation 
3) click on high resolution (after stopping the model from the
   run control page if it is not already stopped)
4) click on the Fig 6 button to start again.

20110411 changed solve method to cnexp in caacum.mod and naacum.mod as
per "Integration methods for SOLVE statements" topic in the NEURON
forum http://www.neuron.yale.edu/phpBB/viewtopic.php?f=28&t=592
20110412 corrected above change to derivimplicit from cnexp
-ModelDB Administrator
