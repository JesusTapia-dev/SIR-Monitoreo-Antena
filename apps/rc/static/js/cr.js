var km_fields = [];
var unit_fields = [];
var dc_fields = [];


function str2hz(s){
  
  return 150000*Math.pow(parseFloat(s), -1);
}


function str2unit(s){
  var km2unit = (20/3)*(parseFloat($('#id_clock_in').val())/parseFloat($('#id_clock_divider').val()));
  var ret = "";
  values = s.split(",");
  for (i=0; i<values.length; i++) {
    ret += parseFloat(values[i])*km2unit;
    ret += ","; 
  }
  return ret.substring(0, ret.length-1);
}


function str2km(s){
  var km2unit = (20/3)*(parseFloat($('#id_clock_in').val())/parseFloat($('#id_clock_divider').val()));
  var ret = "";
  values = s.split(",");
  for (i=0; i<values.length; i++) {
    ret += parseFloat(values[i])/km2unit;
    ret += ","; 
  }
  return ret.substring(0, ret.length-1);
}

function str2dc(s){
  
  return  parseFloat(s)*100/parseFloat($('#id_ipp').val())
}


function updateUnits() {
  
  for (j=0; j<km_fields.length; j++){
    label_unit = "#"+km_fields[j]+"_unit";
    label = "#"+km_fields[j];
    $(label_unit).val(str2unit($(label).val()));
  }
}


function updateDc() {
  
  for (j=0; j<dc_fields.length; j++){
    label_dc = "#"+dc_fields[j]+"_dc";
    label = "#"+dc_fields[j];
    $(label_dc).val(str2dc($(label).val()));
  }
}


  
  $("#id_clock_in").change(function() {
    $("#id_clock").val(parseFloat($('#id_clock_in').val())/parseFloat($('#id_clock_divider').val()));
    updateUnits();
  });

  $("#id_clock_divider").change(function() {
    $("#id_clock").val(parseFloat($('#id_clock_in').val())/parseFloat($('#id_clock_divider').val()));
    updateUnits();
  });

