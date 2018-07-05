COMMENT
Since this is an electrode current, positive values of i depolarize the cell
and in the presence of the extracellular mechanism there will be a change
in vext since i is not a transmembrane current but a current injected
directly to the inside of the cell.
ENDCOMMENT

NEURON {
	SUFFIX uschan
	RANGE onset, dur, n, gkbar
	USEION k READ ek WRITE ik
}

UNITS {
	(nA) = (nanoamp)
}

PARAMETER {
	onset (ms)
	dur (ms)	<0,1e9>

	v (mV)
	celsius = 20 (degC)
	gkbar = .01 (mho/cm2)
	ek = -68 (mV)
}

STATE {
    n
}

ASSIGNED {
    ik (mA/cm2)
}

INITIAL {
	n = 0
}

BREAKPOINT {
	at_time(onset)
	at_time(onset+dur)

	if (t < onset + dur && t >= onset) {
		n = 1
	}else{
		n = 0
	}
	
	ik = gkbar*n*(v - ek)
}
