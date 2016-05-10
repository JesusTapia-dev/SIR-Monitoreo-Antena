
import ast
import json
from itertools import chain

from django import forms
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
     

class SpectralWidget(forms.widgets.TextInput):
    
    def render(self, label, value, attrs=None):
        
        disabled = 'disabled' if attrs.get('disabled', False) else ''
        name = attrs.get('name', label)
        if '[' in value:
            value = ast.literal_eval(value)
        
        codes = value
        if not isinstance(value, list):
            if len(value) > 1:
                text=''
                for val in value:
                    text = text+str(val)+','
            codes=text
        else:
            codes=value+","
                
        html = '''<textarea rows="5" {0} class="form-control" id="id_{1}" name="{2}" style="white-space:nowrap; overflow:scroll;">{3}</textarea>
                  <input type="text" class="col-md-1 col-no-padding" id="num1" value=0>
                  <input type="text" class="col-md-1 col-no-padding" id="num2" value=0>
                  <button type="button" class="button" id="add_spectral_button"> Add </button>
                  <button type="button" class="button" id="all_spectral_button"> All </button>
                  <button type="button" class="button" id="self_spectral_button"> Self </button>
                  <button type="button" class="button" id="cross_spectral_button"> Cross </button>
                  <button type="button" class="button" id="delete_spectral_button"> Delete </button>
                  '''.format(disabled, label, name, codes)
        
        script = '''
                <script type="text/javascript"> 
                $(document).ready(function () {{
                
                    var spectral_number1 = $("#num1").val();
                    var spectral_number2 = $("#num2").val();
                    
                    
                    $("#all_spectral_button").click(function(){{
                        alert(spectral_comb)
                    }});
                    
                    $("#add_spectral_button").click(function(){{
                        var spectral_comb = $("#id_spectral").val();
                        var spectral_number1 = $("#num1").val();
                        var spectral_number2 = $("#num2").val();
                        var str = spectral_number1+", "+spectral_number2;
                        //not to duplicate
                        var n = spectral_comb.search(str);
                        if (n==-1){
                            $("#id_spectral").val(spectral_comb+"["+$("#num1").val()+", "+$("#num2").val()+"],")   
                        }                     
                    }});
                    
                    $("#delete_spectral_button").click(function(){{
                        var spectral_comb = $("#id_spectral").val();
                        var spectral_number1 = $("#num1").val();
                        var spectral_number2 = $("#num2").val();
                        var str = spectral_number1+", "+spectral_number2;
                        var n = spectral_comb.search(str);
                        if (n==-1){
                            
                        }
                        else {
                            n= spectral_comb.length;
                            if (n<8){
                                var tuple = "["+$("#num1").val()+", "+$("#num2").val()+"],"
                                var txt = spectral_comb.replace(tuple,'');
                            }
                            else {
                                var tuple = ",["+$("#num1").val()+", "+$("#num2").val()+"]"
                                var txt = spectral_comb.replace(tuple,'');
                            }
                            $("#id_spectral").val(txt)
                            
                            var tuple = "["+$("#num1").val()+", "+$("#num2").val()+"],"
                            var txt = spectral_comb.replace(tuple,'');
                            $("#id_spectral").val(txt)
                        }                     
                    }});
                    
                }});
                </script>
                '''
        
        return mark_safe(html+script)