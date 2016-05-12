$(document).ready(function() {
	var type = $("#id_exp_type").val();
	spectral_number = $("#id_spectral_number")
	spectral        = $("#id_spectral")
	fftpoints       = $("#id_fftpoints")
	save_ch_dc      = $("#id_save_ch_dc")
	add_spec_button = $("#add_spectral_button")
	del_spec_button = $("#delete_spectral_button")
	sel_spec_button = $("#self_spectral_button")
	cro_spec_button = $("#cross_spectral_button")
	all_spec_button = $("#all_spectral_button")
	
	if (type == 0) {
		$(spectral_number).attr('readonly', true);	
		$(spectral).attr('readonly', true);
		$(fftpoints).attr('readonly', true);
		$(save_ch_dc).attr('disabled', true);
		$(save_ch_dc).attr('readonly', true);
		$(add_spec_button).attr('disabled', true);
		$(del_spec_button).attr('disabled', true);
		$(sel_spec_button).attr('disabled', true);
		$(cro_spec_button).attr('disabled', true);
		$(all_spec_button).attr('disabled', true);
	}
	else {
		$(spectral_number).attr('readonly', false);
		$(spectral).attr('readonly', false);
		$(fftpoints).attr('readonly', false);
		$(save_ch_dc).attr('disabled', false);
		$(save_ch_dc).attr('readonly', false);
		$(add_spec_button).attr('disabled', false);
		$(del_spec_button).attr('disabled', false);
		$(sel_spec_button).attr('disabled', false);
		$(cro_spec_button).attr('disabled', false);
		$(all_spec_button).attr('disabled', false);
	}	
});

$("#id_exp_type").change(function() {
	var type = $("#id_exp_type").val();
	spectral_number = $("#id_spectral_number")
	spectral        = $("#id_spectral")
	fftpoints       = $("#id_fftpoints")
	save_ch_dc      = $("#id_save_ch_dc")
	add_spec_button = $("#add_spectral_button")
	del_spec_button = $("#delete_spectral_button")
	sel_spec_button = $("#self_spectral_button")
	cro_spec_button = $("#cross_spectral_button")
	all_spec_button = $("#all_spectral_button")
	
	if (type == 0) {
		$(spectral_number).attr('readonly', true);	
		$(spectral).attr('readonly', true);
		$(fftpoints).attr('readonly', true);
		$(save_ch_dc).attr('disabled', true);
		$(save_ch_dc).attr('readonly', true);
		$(add_spec_button).attr('disabled', true);
		$(del_spec_button).attr('disabled', true);
		$(sel_spec_button).attr('disabled', true);
		$(cro_spec_button).attr('disabled', true);
		$(all_spec_button).attr('disabled', true);
	}
	else {
		$(spectral_number).attr('readonly', false);
		$(spectral).attr('readonly', false);
		$(fftpoints).attr('readonly', false);
		$(save_ch_dc).attr('disabled', false);
		$(save_ch_dc).attr('readonly', false);
		$(add_spec_button).attr('disabled', false);
		$(del_spec_button).attr('disabled', false);
		$(sel_spec_button).attr('disabled', false);
		$(cro_spec_button).attr('disabled', false);
		$(all_spec_button).attr('disabled', false);
	}
});


$("#id_cards_number").on('change', function() {
	var cards_number = $("#id_cards_number").val();
	channels_number = $("#id_channels_number")
	$(channels_number).val(cards_number*2)	
	updateChannelsNumber();
});


$("#id_channels_number").on('change', function() {
	updateChannelsNumber();
});


$("#id_spectral").on('change', function() {
	updateSpectralNumber();
});


function updateSpectralNumber(){
    var spectral_comb = $("#id_spectral").val();
    var num = spectral_comb.length;
    var cont = 0
    for (i = 0; i < num; i++) {
        if (spectral_comb[i] == "]"){
            cont = cont + 1
        }
    }
    $("#id_spectral_number").val(cont)
}


function updateChannelsNumber() {
	
	var channels_number = $("#id_channels_number").val();
	channels = $("#id_channels")
	sequence = ""
	
	for (i = 1; i <= channels_number; i++) {
		if (i==1){
			sequence = i.toString()
		}
		else{
			sequence = sequence + "," + i.toString()
		}    	
	}
	$(channels).val(sequence)
}