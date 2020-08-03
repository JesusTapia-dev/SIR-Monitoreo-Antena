$(document).ready(function() {
	RawDataOrPData()
	DecodeDataOrNone()
});

$("#id_exp_type").change(function() {
	RawDataOrPData()
});

$("#id_decode_data").change(function() {
	 DecodeDataOrNone()
});

function RawDataOrPData(){
	var type = $("#id_exp_type").val();
	incohe_integr = $("#id_incohe_integr")
	spectral        = $("#id_spectral")
	fftpoints       = $("#id_fftpoints")
	save_ch_dc      = $("#id_save_ch_dc")
	add_spec_button = $("#add_spectral_button")
	del_spec_button = $("#delete_spectral_button")
	sel_spec_button = $("#self_spectral_button")
	cro_spec_button = $("#cross_spectral_button")
	all_spec_button = $("#all_spectral_button")

	if (type == 0) {
		$(incohe_integr).attr('readonly', true);
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
		$(incohe_integr).attr('readonly', false);
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
}


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

$("#id_cohe_integr").on('change', function() {
	updateAcquiredProfiles();
});

$("#id_profiles_block").on('change', function() {
	updateAcquiredProfiles();
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


function DecodeDataOrNone() {
	var decode_data = $("#id_decode_data").val();
	post_coh_int        = $("#id_post_coh_int")
	if (decode_data != 0) {
		$(post_coh_int).attr('readonly', false);
		$(post_coh_int).attr('disabled', false);
	}
	else {
		$(post_coh_int).attr('readonly', true);
		$(post_coh_int).attr('disabled', true);
	}
}

function updateAcquiredProfiles() {
	var profiles_block  = $("#id_profiles_block").val();
	var cohe_integr = $("#id_cohe_integr").val();
	var acq_prof = profiles_block * cohe_integr;
	$("#id_acq_profiles").val(acq_prof)
}
