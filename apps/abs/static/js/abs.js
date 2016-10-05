$(document).ready(function() {
	updateOperationMode()
});

$("#id_operation_mode").on('change', function() {
  updateOperationMode()
});

function updateOperationMode(){
	var operation_mode = $("#id_operation_mode").val();
	if (operation_mode==0){
		document.getElementById("id_operation_value").disabled=true;
		$("#id_operation_value").hide();
	}
	else {
		document.getElementById("id_operation_value").disabled=false;
		$("#id_operation_value").show();
	}
}
