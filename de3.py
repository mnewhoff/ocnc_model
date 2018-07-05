from neuron import h, gui
 
h.load_file("nrngui.hoc")
h.nao0_na_ion = 115
h.cao0_ca_ion = 1.8
h.ko0_k_ion = 4

soma = h.Section(name="soma")
soma.Ra = 200 
soma.L = 40 
soma.diam = 40 
soma.nseg = 1
soma.insert("pcell") 
soma.insert("na")
soma.insert("napump") 
#soma.insert("gkca")
soma.insert("ca")
soma.insert("cach") 
soma.insert("capump") 

junction = h.Section(name="soma")
junction.Ra = 200
junction.L = 40
junction.diam = 10
junction.nseg = 3
junction.insert("pcell") 
junction.insert("na")
junction.insert("napump") 
#junction.insert("gkca")
junction.insert("ca")
junction.insert("cach") 
junction.insert("capump") 

axthick = h.Section(name="axthick")
axthick.Ra = 200
axthick.L = 150
axthick.diam = 6
axthick.nseg = 11
axthick.insert("pcell") 
axthick.insert("na")
axthick.insert("napump") 
#axthick.insert("gkca")
axthick.insert("ca")
axthick.insert("cach") 
axthick.insert("capump") 

axsiz = h.Section(name="axsiz")
axsiz.Ra = 200
axsiz.L = 10
axsiz.diam = 2
axsiz.nseg = 1
axsiz.insert("pcell") 
axsiz.insert("na")
axsiz.insert("napump") 
#axsiz.insert("gkca")
axsiz.insert("ca")
axsiz.insert("cach") 
axsiz.insert("capump") 

axthin = h.Section(name="axthin")
axthin.Ra = 200
axthin.L = 500
axthin.diam = 2
axthin.nseg = 30
axthin.insert("pcell") 
axthin.insert("na")
axthin.insert("napump") 
#axthin.insert("gkca")
axthin.insert("ca")
axthin.insert("cach") 
axthin.insert("capump") 

for sec in h.allsec():
  sec.ek = -71.5 #from Schlue and Deitmer, 1984 

junction.connect(soma)
axthick.connect(junction)
axsiz.connect(axthick)
axthin.connect(axsiz)

# Model changes for spike height
soma.gnabar_pcell = 0 #zero sodium conductance at soma
junction.gnabar_pcell = 0 #zero in junction b.w soma and axon
axthick.gnabar_pcell = 0.15 #reduced by 50% in thick axon
axsiz.gnabar_pcell = .5 #increase gNa at spike initiation zone

for sec in h.allsec(): #increase K activation rate in whole cell
  sec.kactrate_pcell = 30.75 #0.75 from P cell, Schlue and Deitmer, 1984

soma.push() #record voltage at the soma

h.celsius = 22 #typical lab temperature
h.tstop = 300
h.xopen("de3_1.ses")

ic = h.IClamp(0.5, sec=axthick) #current injection to axthick
ic.delay = 100
ic.dur = 300
ic.amp = 0 #current amplitude

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
