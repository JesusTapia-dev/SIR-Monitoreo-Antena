
import ast
import json
from itertools import chain

from django import forms
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape


class SpectralWidget(forms.widgets.TextInput):

    def render(self, label, value, attrs=None):

        readonly = 'readonly' if attrs.get('readonly', False) else ''
        name = attrs.get('name', label)
        if value == None:
            value = '[0, 0],'
        if '[' in value:
            if value[len(value)-1] == ",":
                value = ast.literal_eval(value)
            else:
                value = value + ","
                value = ast.literal_eval(value)

        codes = value
        if not isinstance(value, list):
            text=''
            #lista = []
            #if len(value) > 1:
            for val in value:
                text = text+str(val)+','
                #lista.append(val)
            codes=text
        else:
            codes=''

        html = '''<textarea rows="5" {0} class="form-control" id="id_{1}" name="{2}" style="white-space:nowrap; overflow:scroll;">{3}</textarea>
                  <input type="text" class="col-md-1 col-no-padding" id="num1" value=0>
                  <input type="text" class="col-md-1 col-no-padding" id="num2" value=0>
                  <button type="button" class="button" id="add_spectral_button"> Add </button>
                  <button type="button" class="button" id="delete_spectral_button"> Delete </button>
                  <button type="button" class="button pull-right" id="cross_spectral_button"> Cross </button>
                  <button type="button" class="button pull-right" id="self_spectral_button"> Self </button>
                  <button type="button" class="button pull-right" id="all_spectral_button"> All </button>
                  '''.format(readonly, label, name, codes)

        script = '''
                <script type="text/javascript">
                $(document).ready(function () {{

                    var spectral_number1 = $("#num1").val();
                    var spectral_number2 = $("#num2").val();


                    $("#all_spectral_button").click(function(){{
                        var sequence1 = selfSpectral()
                        var sequence2 = crossSpectral()
                        $("#id_spectral").val(sequence1+sequence2)
                        updateSpectralNumber()
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
                        updateSpectralNumber()
                    }});


                    $("#self_spectral_button").click(function(){{
                        var sequence = selfSpectral()
                        $("#id_spectral").val(sequence)

                        updateSpectralNumber()
                    }});

                    $("#cross_spectral_button").click(function(){{
                        var sequence = crossSpectral()
                        $("#id_spectral").val(sequence)

                        updateSpectralNumber()
                    }});


                    function selfSpectral() {
                        var channels = $("#id_channels").val();
                        var n = (channels.length)-1;
                        var num = parseInt(channels[n]);
                        sequence = ""
                        for (i = 0; i < num; i++) {
                            sequence = sequence + "[" + i.toString() + ", " + i.toString() + "],"
                        }
                        return sequence
                    }


                    function crossSpectral() {
                        var channels = $("#id_channels").val();
                        var n = (channels.length)-1;
                        var num = parseInt(channels[n]);
                        sequence = ""
                        for (i = 0; i < num; i++) {
                            for (j = i+1; j < num; j++) {
                            sequence = sequence + "[" + i.toString() + ", " + j.toString() + "],"
                            }
                        }
                        return sequence
                    }


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
                        updateSpectralNumber()
                    }});


                }});
                </script>
                '''

        return mark_safe(html+script)
