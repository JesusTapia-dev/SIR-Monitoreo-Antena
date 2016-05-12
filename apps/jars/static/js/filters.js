$("#id_fch").change(function() {
	 updateParameters()
});

$("#id_clock").change(function() {
	 updateParameters()
});

$("#id_mult").change(function() {
	 updateParameters()
});

function updateParameters(){
	var fclock = $("#id_clock").val();  					// clock frequency (MHz)
	var fch    = $("#id_fch").val();    					// RF frequency (MHz)
	var m_dds  = $("#id_mult").val();   					// DDS multiplier
	
	if (fch < fclock/2){ 			    					// Si se cumple nyquist
	    var nco   = Math.pow(2,32)*((fch/fclock)%1);
		var nco_i = Math.round(nco/m_dds)*m_dds;
	}
	else {             
	    nco = Math.pow(2,32)*(fclock-fch)/(fclock);
	    nco_i = Math.round(nco/m_dds)*m_dds;
	}
	fch_decimal = $("#id_fch_decimal")
	$(fch_decimal).val(nco_i)
}