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
junction.diam = 7
junction.nseg = 5
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
axsiz.diam = 10
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

#add 9 med-length dendrites to soma-junction connection
sna = h.Section(name='sna')
snb = h.Section(name='snb')
snc = h.Section(name='snc')
snd = h.Section(name='snd')
sne = h.Section(name='sne')
snf = h.Section(name='snf')
sng = h.Section(name='sng')
snh = h.Section(name='snh')
sni = h.Section(name='sni')

soma_neurites = [sna,snb,snc,snd,sne,snf,sng,snh,sni]
for n in soma_neurites:
  n.Ra = 300
  n.L = 80
  n.diam = 2
  n.nseg = 3
  n.insert("pcell")
  n.connect(soma(1))
  #n.insert('pas')

#add 8 shorter neurites to junction
jna = h.Section(name='jna')
jnb = h.Section(name='jnb')
jnc = h.Section(name='jnc')
jnd = h.Section(name='jnd')
jne = h.Section(name='jne')
jnf = h.Section(name='jnf')
jng = h.Section(name='jng')
jnh = h.Section(name='jnh')

junction_neurites = [jna,jnb,jnc,jnd,jne,jnf,jng,jnh]
for n in junction_neurites:
  n.Ra = 300
  n.L = 50
  n.diam = 2
  n.nseg = 3
  n.insert("pcell")
  n.connect(junction(0.5))
  #n.insert('pas')

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
  #n.insert('pas')

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
  #n.insert('pas')

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

for sec in h.allsec(): #can now set different temperatures in different sections
  sec.localtemp_pcell = 22

##----------------------------------------------------------------##
##--------------Connections between sections----------------------##

junction.connect(soma)
axthick.connect(junction)
axsiz.connect(axthick)
axthin.connect(axsiz)

##-----------------------------------------------------------------##
##------Insert a randomish synaptic input to up firing rate--------##

syn1=h.NetStim(axna(0))
nc=h.NetCon(None,syn1)
syn1.start = 0
syn1.interval = 500
syn1.noise = 0.5
nc.weight[0] = 100

##-----------------------------------------------------------------##
##------------Conductances to alter for spike amplitude------------##

# Model changes for spike height
soma.gnabar_pcell = 0 #zero sodium conductance at soma
junction.gnabar_pcell = 0 #zero in junction b.w soma and axon
axthick.gnabar_pcell = 0.15 #reduced by 50% in thick axon
axsiz.gnabar_pcell = 1.8 #increase gNa at spike initiation zone
nainactrate_pcell = 0.58

for sec in h.allsec(): #increase K activation rate in whole cell
  sec.kactrate_pcell = 100.75 #0.75 from P cell, Schlue and Deitmer, 1984

##-----------------------------------------------------------------##
##----Add a bit of the Ornstein-Uhlenbeck noise (colored noise)----## 
for sec in h.allsec():
  sec.insert("OU")
  sec.tau_OU = 20 #seems to reduce noise if increase
  sec.D_OU = 0.025 

##-----------------------------------------------------------------##
##------------------------Recording conditions---------------------##
soma.push() #record voltage at the soma

#h.celsius = 22 #typical lab temperature
h.tstop = 5000
h.xopen("de3_1.ses")

ic = h.IClamp(0.5, sec=axthick) #current injection to axthick w/ electrode if want
ic.delay = 100
ic.dur = 25000
ic.amp = 0.5 #current amplitude

##-----------------------------------------------------------------##
##--------------------US-activated channel-------------------------##
soma.insert("uschan")
soma.onset_uschan = 5000 #US time on
soma.dur_uschan = 10000 #duration of US stimulus
soma.tact_uschan = 20000 # tau activation US-activated channel
##--------------------------------------------------------------##

##----Local temperature fluctuation ----##
def make_vector_linear_increase(length, init=22.0, target=24.5):
  vtemp = h.Vector(length)
  slope = (target-init)/(length-1)
  for i in range(length):
    vtemp.x[i] = i*slope + init
  return vtemp

dt = 1
L = 1000 #int(h.tstop/dt)
vtemp = make_vector_linear_increase(L, init=22.0, target=24.5)

# vtemp.play(soma(0.5)._ref_localtemp_pcell, dt)
for seg in soma.allseg():
  vtemp.play(seg._ref_localtemp_pcell, dt)        

vtemp.play(axthin(0.1)._ref_localtemp_pcell, dt)


##--------------------------Graphs------------------------------##
#vectors to plot
vsoma = h.Vector() #voltage in soma
vaxsiz = h.Vector() #voltage in SIZ
ina_axsiz = h.Vector() #Na current in SIZ 
ik_axsiz = h.Vector() #K current in SIZ
#somatemp = h.Vector()

T = h.Vector() #time vector
vsoma.record(soma(0.5)._ref_v, 0.1) #record from midpoint of soma
vaxsiz.record(axsiz(0.5)._ref_v, 0.1) #record from midpoint of SIZ
ina_axsiz.record(axsiz(0.5)._ref_ina, 0.1) #record 
ik_axsiz.record(axsiz(0.5)._ref_ik, 0.1)
T.record(h._ref_t, 0.1)
#somatemp.record(&soma.localtemp_pcell,0.1)

##------------------------------------------------------------------##
##-------------------Change temperature as event--------------------##
def heat_change():
  soma.localtemp_pcell = 100

#fih = h.FInitializeHandler(2,heat_change)

#
# fih = f.FInitializeHandler(500,heat_change)
# h.finitialize(-45)
#
# fih = f.FInitializeHandler(500,heat_change)
# h.CVode().event(500,heat_change)
#h.continuerun(15000)

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
#plt.plot(T,localtemp_soma)
#plt.title('Temperature at Soma')


plt.figure()
plt.subplot(2,1,1)
plt.plot(T, ina_axsiz) #plot Na current as a function of time
plt.title('INa')
plt.subplot(2,1,2)
plt.plot(T, ik_axsiz) #plot K current as a function of time
plt.title('IK')
