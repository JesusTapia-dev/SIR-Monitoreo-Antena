$("#id_frequency").change(function() {
	 updateParameters()
});

$("#id_clock").change(function() {
	 updateParameters()
});

$("#id_multiplier").change(function() {
	 updateParameters()
});

function updateParameters(){
	var clock = $("#id_clock").val();  					// clock frequency (MHz)
	var fch    = $("#id_frequency").val();    			// RF frequency (MHz)
	var m_dds  = $("#id_multiplier").val();   			// DDS multiplier

	if (Math.abs(fch) < clock/2){ 			    		// Si se cumple nyquist
	    var nco   = Math.pow(2,32)*((fch/clock)%1);
		//var nco_i = Math.round(nco/m_dds)*m_dds;
		var nco_i = Math.round(nco)
	}
	else {
	    nco = Math.pow(2,32)*(clock-fch)/(clock);
	    //nco_i = Math.round(nco/m_dds)*m_dds;
		var nco_i = Math.round(nco)
	}
	$("#id_f_decimal").val(nco_i)
}
