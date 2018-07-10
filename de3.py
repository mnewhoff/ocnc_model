from neuron import h, gui
 
h.load_file("nrngui.hoc")
h.nao0_na_ion = 115
h.cao0_ca_ion = 1.8
h.ko0_k_ion = 4


##------------------------------------------------------------------##
##----------------------Create passive sections---------------------##
soma = h.Section(name="soma")
soma.Ra = 300 
soma.L = 40 
soma.diam = 40 
soma.nseg = 1
soma.insert("pcell") 
#soma.insert('pas')

junction = h.Section(name="junction")
junction.Ra = 300
junction.L = 40
junction.diam = 10
junction.nseg = 3
junction.insert("pcell") 
#junction.insert('pas')

##------------------------------------------------------------------##
##---------------------Create active sections-----------------------##

axthick = h.Section(name="axthick")
axthick.L = 150
axthick.Ra = 300
axthick.diam = 6
axthick.nseg = 11
axthick.insert("pcell") 

axsiz = h.Section(name="axsiz") #spike initiation zone
axsiz.Ra = 300
axsiz.L = 10
axsiz.diam = 2
axsiz.nseg = 1
axsiz.insert("pcell") 

axthin = h.Section(name="axthin")
axthin.Ra = 300
axthin.L = 500
axthin.diam = 2
axthin.nseg = 30
axthin.insert("pcell") 

##------------------------------------------------------------------##
##--------------------------add dendrites---------------------------##

#add 6 med-length dendrites to soma-junction connection
sna = h.Section(name='sna')
snb = h.Section(name='snb')
snc = h.Section(name='snc')
snd = h.Section(name='snd')
sne = h.Section(name='sne')
snf = h.Section(name='snf')

soma_neurites = [sna,snb,snc,snd,sne,snf]
for n in soma_neurites:
  n.Ra = 300
  n.L = 80
  n.diam = 2
  n.nseg = 3
  n.insert("pcell")
  n.connect(soma(1))
  n.insert('pas')

#add 4 shorter neurites to junction
jna = h.Section(name='jna')
jnb = h.Section(name='jnb')
jnc = h.Section(name='jnc')
jnd = h.Section(name='jnd')

junction_neurites = [jna,jnb,jnc,jnd]
for n in junction_neurites:
  n.Ra = 300
  n.L = 50
  n.diam = 2
  n.nseg = 3
  n.insert("pcell")
  n.connect(junction(0.5))
  n.insert('pas')

#add 6 XL dendrites to axthick
axna = h.Section(name='axna')
axnb = h.Section(name='axnb')
axnc = h.Section(name='axnc')
axnd = h.Section(name='axnd')
axne = h.Section(name='axne')
axnf = h.Section(name='axnf')

axthick_neurites = [axna,axnb,axnc,axnd,axne,axnf]
for n in axthick_neurites:
  n.Ra = 300
  n.L = 150
  n.diam = 3
  n.nseg = 11
  n.insert("pcell")
  n.connect(axthick(0.5))
  n.insert('pas')

#added small branches to axna neurite
axba = h.Section(name='axba')
axbb = h.Section(name='axbb')
axbc = h.Section(name='axbc')
axbd = h.Section(name='axbd')
axbe = h.Section(name='axbe')
axbf = h.Section(name='axbf')
axna_branches = [axba,axbb,axbc,axbd,axbe,axbf]
for n in axna_branches:
  n.Ra = 300
  n.L = 10
  n.diam = 1
  n.nseg = 5
  n.insert("pcell")
  n.connect(axna(0.5))
  n.insert('pas')

##---------------------------------------------------------------##
##---------Introduce common channels to active segments----------##
act = [axthin,axsiz,axthick,junction]
for sec in act:
  sec.insert('na')
  sec.insert('napump')
  sec.insert('ca')
  sec.insert('cach')
  sec.insert('capump')

for sec in h.allsec():
  sec.ek = -71.5 #from Schlue and Deitmer, 1984
  sec.ena = 45 #from De Schutter et al., 1993

for sec in h.allsec():
  sec.localtemp_pcell = 22

##----------------------------------------------------------------##
##--------------Connections between sections----------------------##

junction.connect(soma)
axthick.connect(junction)
axsiz.connect(axthick)
axthin.connect(axsiz)

##-----------------------------------------------------------------##
##-----------------Insert a few synapses for fun-------------------##

asyn1 = h.AlphaSynapse(axna(0.5)) #onto first neurite off axthick
asyn1.onset = 20
asyn1.gmax = 1

asyn2 = h.AlphaSynapse(axne(0.5)) #onto fifth neurite off axthick
asyn2.onset = 100
asyn2.gmax = 1

asyn3 = h.AlphaSynapse(jnc(0.5)) #onto third neurite off junction
asyn3.onset = 500
asyn3.gmax = 1

##-----------------------------------------------------------------##
##------------Conductances to alter for spike amplitude------------##

# Model changes for spike height
soma.gnabar_pcell = 0 #zero sodium conductance at soma
junction.gnabar_pcell = 0 #zero in junction b.w soma and axon
axthick.gnabar_pcell = 0.15 #reduced by 50% in thick axon
axsiz.gnabar_pcell = .5 #increase gNa at spike initiation zone

for sec in h.allsec(): #increase K activation rate in whole cell
  sec.kactrate_pcell = 100.75 #0.75 from P cell, Schlue and Deitmer, 1984

##-----------------------------------------------------------------##
##----Add a bit of the Ornstein-Uhlenbeck noise (colored noise)----## 
for sec in h.allsec():
  sec.insert("OU")
  sec.tau_OU = 20
  sec.D_OU = 0.025 

##-----------------------------------------------------------------##
##------------------------Recording conditions---------------------##
soma.push() #record voltage at the soma

#h.celsius = 22 #typical lab temperature
h.tstop = 5000
h.xopen("de3_1.ses")

ic = h.IClamp(0.5, sec=axthick) #current injection to axthick w/ electrode if want
ic.delay = 100
ic.dur = 300
ic.amp = 0 #current amplitude

##-----------------------------------------------------------------##
##--------------------US-activated channel-------------------------##
soma.insert("uschan")
soma.onset_uschan = 5000 #US time on
soma.dur_uschan = 10000 #duration of US stimulus
soma.tact_uschan = 20000 # tau activation US-activated channel

##-----------------------------------------------------------------##
##--------------------------Graphs---------------------------------##
#vectors to plot
vsoma = h.Vector() #voltage in soma
vaxsiz = h.Vector() #voltage in SIZ
ina_axsiz = h.Vector() #Na current in SIZ 
ik_axsiz = h.Vector() #K current in SIZ

T = h.Vector() #time vector
vsoma.record(soma(0.5)._ref_v, 0.1) #record from midpoint of soma
vaxsiz.record(axsiz(0.5)._ref_v, 0.1) #record from midpoint of SIZ
ina_axsiz.record(axsiz(0.5)._ref_ina, 0.1) #record 
ik_axsiz.record(axsiz(0.5)._ref_ik, 0.1)
T.record(h._ref_t, 0.1)

h.init()
h.run()

import matplotlib.pyplot as plt
plt.figure()
plt.subplot(2,1,1)
plt.plot(T, vsoma)
plt.title('V soma')
plt.subplot(2,1,2)
plt.plot(T, vaxsiz)
plt.title('V axsiz')

plt.figure()
plt.subplot(2,1,1)
plt.plot(T, ina_axsiz) #plot Na current as a function of time
plt.title('INa')
plt.subplot(2,1,2)
plt.plot(T, ik_axsiz) #plot K current as a 
plt.title('IK')
