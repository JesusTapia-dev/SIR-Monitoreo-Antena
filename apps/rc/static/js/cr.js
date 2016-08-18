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
    ret += Math.round(parseFloat(values[i])*km2unit);
    ret += ","; 
  }
  return ret.substring(0, ret.length-1);
}


function str2int(s){
  var ret = "";
  values = s.split(",");
  for (i=0; i<values.length; i++) {
    ret += Math.round(parseFloat(values[i]));
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


function updateWindows(label) {

  if (label.indexOf("first_height")>0){
    llabel = label.replace("first_height", "last_height");
    rlabel = label.replace("first_height", "resolution");
    nlabel = label.replace("first_height", "number_of_samples");
    value = parseFloat($(label).val())+parseFloat($(rlabel).val())*(parseInt($(nlabel).val())-1);
    $(llabel).val(value);
  }
  
  if (label.indexOf("resolution")>0){
    llabel = label.replace("resolution", "last_height");
    flabel = label.replace("resolution", "first_height");
    nlabel = label.replace("resolution", "number_of_samples");
    value = parseFloat($(flabel).val())+parseFloat($(label).val())*(parseInt($(nlabel).val())-1);
    $(llabel).val(value);
  }
  
  if (label.indexOf("number_of_samples")>0){
    llabel = label.replace("number_of_samples", "last_height");
    rlabel = label.replace("number_of_samples", "resolution");
    flabel = label.replace("number_of_samples", "first_height");
    value = parseFloat($(flabel).val())+parseFloat($(rlabel).val())*(parseInt($(label).val())-1);
    $(llabel).val(value);
  }
  
  if (label.indexOf("last_height")>0){
    flabel = label.replace("last_height", "first_height");
    rlabel = label.replace("last_height", "resolution");
    nlabel = label.replace("last_height", "number_of_samples");
    
    nvalue = Math.round((parseFloat($(label).val())-parseFloat($(flabel).val()))/parseFloat($(rlabel).val()))+1;
    $(nlabel).val(nvalue);
    value = parseFloat($(flabel).val())+parseFloat($(rlabel).val())*(nvalue-1);
    $(label).val(value);
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

