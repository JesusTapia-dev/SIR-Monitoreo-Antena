
import ast
import json

from django import forms
from django.utils.safestring import mark_safe
     

class KmUnitWidget(forms.widgets.TextInput):
    
    def render(self, label, value, attrs=None):
        
        if isinstance(value, (int, float)):
            unit = int(value*attrs['km2unit'])
        elif isinstance(value, basestring):
            units = []
            values = [s for s in value.split(',') if s]
            for val in values:
                units.append('{0:.0f}'.format(float(val)*attrs['km2unit']))
        
            unit = ','.join(units)
        
        disabled = 'disabled' if attrs.get('disabled', False) else ''
        name = attrs.get('name', label)
        
        if 'line' in attrs:
            label += '_{0}'.format(attrs['line'].pk)
        
        html = '<div class="col-md-12 col-no-padding"><div class="col-md-5 col-no-padding"><input type="text" {0} class="form-control" id="id_{1}" name="{2}" value="{3}"></div><div class="col-md-1 col-no-padding">Km</div><div class="col-md-5 col-no-padding"><input type="text" {4} class="form-control" id="id_{5}_unit" value="{6}"></div><div class="col-md-1 col-no-padding">Units</div></div>'.format(disabled, label, name, value, disabled, label, unit)
        
        script = '''<script type="text/javascript">
        $(document).ready(function () {{
        
          km_fields.push("id_{label}"); 
          unit_fields.push("id_{label}_unit");                       
          
          $("#id_{label}").change(function() {{
            $("#id_{label}_unit").val(Math.round(str2unit($(this).val())));
            $("#id_{label}").val(str2km($("#id_{label}_unit").val()));
          }});
          $("#id_{label}_unit").change(function() {{
            $(this).val(Math.round(parseFloat($(this).val())));
            $("#id_{label}").val(str2km($(this).val()));
          }});
        }});  
        </script>'''.format(label=label)
        
        if disabled:
            return mark_safe(html)
        else:
            return mark_safe(html+script)


class UnitKmWidget(forms.widgets.TextInput):
    
    def render(self, label, value, attrs=None):
        
        if isinstance(value, (int, float)):
            km = value/attrs['km2unit']
        elif isinstance(value, basestring):
            kms = []
            values = [s for s in value.split(',') if s]
            for val in values:
                kms.append('{0:.0f}'.format(float(val)/attrs['km2unit']))
        
            km = ','.join(kms)
        
        disabled = 'disabled' if attrs.get('disabled', False) else ''
        name = attrs.get('name', label)
        
        if 'line' in attrs:
            label += '_{0}'.format(attrs['line'].pk)
        
        html = '''<div class="col-md-12 col-no-padding">
        <div class="col-md-5 col-no-padding"><input type="number" {0} class="form-control" id="id_{1}_unit" name="{2}" value="{3}"></div>
        <div class="col-md-1 col-no-padding">Units</div>
        <div class="col-md-5 col-no-padding"><input type="number" {4} class="form-control" id="id_{5}" value="{6}"></div>
        <div class="col-md-1 col-no-padding">Km</div></div>'''.format(disabled, label, name, value, disabled, label, km)
        
        script = '''<script type="text/javascript">
        $(document).ready(function () {{
        
          km_fields.push("id_{label}"); 
          unit_fields.push("id_{label}_unit");                       
          
          $("#id_{label}").change(function() {{
            $("#id_{label}_unit").val(str2unit($(this).val()));          
          }});
          $("#id_{label}_unit").change(function() {{
            $("#id_{label}").val(str2km($(this).val()));
          }});
        }});  
        </script>'''.format(label=label)
        
        if disabled:
            return mark_safe(html)
        else:
            return mark_safe(html+script)


class KmUnitHzWidget(forms.widgets.TextInput):
    
    def render(self, label, value, attrs=None):
        
        unit = float(value)*attrs['km2unit']
        if unit%10==0:
            unit = int(unit)
        hz = 150000*float(value)**-1
        
        disabled = 'disabled' if attrs.get('disabled', False) else ''
        name = attrs.get('name', label)
        
        if 'line' in attrs:
            label += '_{0}'.format(attrs['line'].pk)
        
        html = '''<div class="col-md-12 col-no-padding">
        <div class="col-md-3 col-no-padding"><input type="number" {0} class="form-control" id="id_{1}" name="{2}" value="{3}"></div>
        <div class="col-md-1 col-no-padding">Km</div>
        <div class="col-md-3 col-no-padding"><input type="number" {4} class="form-control" id="id_{1}_unit" value="{5}"></div>
        <div class="col-md-1 col-no-padding">Units</div>
        <div class="col-md-3 col-no-padding"><input type="number" {4} class="form-control" id="id_{1}_hz" value="{6}"></div>
        <div class="col-md-1 col-no-padding">Hz</div>
        </div>'''.format(disabled, label, name, value, disabled, unit, hz)
        
        script = '''<script type="text/javascript">
        $(document).ready(function () {{        
          km_fields.push("id_{label}"); 
          unit_fields.push("id_{label}_unit");          
          $("#id_{label}").change(function() {{
            $("#id_{label}_unit").val(str2unit($(this).val()));
            $("#id_{label}_hz").val(str2hz($(this).val()));
            updateDc();
          }});
          $("#id_{label}_unit").change(function() {{
            $(this).val(Math.round(parseFloat($(this).val())/10)*10);
            $("#id_{label}").val(str2km($(this).val()));
            $("#id_{label}_hz").val(str2hz($("#id_{label}").val()));
            updateDc();
          }});
          $("#id_{label}_hz").change(function() {{
            $("#id_{label}").val(str2hz($(this).val()));
            $("#id_{label}_unit").val(str2unit($("#id_{label}").val()));
            updateDc();
          }});
        }});  
        </script>'''.format(label=label)
        
        if disabled:
            return mark_safe(html)
        else:
            return mark_safe(html+script)
    

class KmUnitDcWidget(forms.widgets.TextInput):
    
    def render(self, label, value, attrs=None):
        
        unit = int(float(value)*attrs['km2unit'])
        
        disabled = 'disabled' if attrs.get('disabled', False) else ''
        name = attrs.get('name', label)
        
        label += '_{0}'.format(attrs['line'].pk)
        
        dc = float(json.loads(attrs['line'].params)['pulse_width'])*attrs['line'].rc_configuration.ipp/100
        
        html = '''<div class="col-md-12 col-no-padding">
        <div class="col-md-3 col-no-padding"><input type="number" {0} class="form-control" id="id_{1}" name="{2}" value="{3}"></div>
        <div class="col-md-1 col-no-padding">Km</div>
        <div class="col-md-3 col-no-padding"><input type="number" {4} class="form-control" id="id_{1}_unit" value="{5}"></div>
        <div class="col-md-1 col-no-padding">Units</div>
        <div class="col-md-3 col-no-padding"><input type="number" {4} class="form-control" id="id_{1}_dc" value="{6}"></div>
        <div class="col-md-1 col-no-padding">DC[%]</div>
        </div>'''.format(disabled, label, name, value, disabled, unit, dc)
        
        script = '''<script type="text/javascript">
        $(document).ready(function () {{        
          km_fields.push("id_{label}"); 
          unit_fields.push("id_{label}_unit");
          dc_fields.push("id_{label}");      
          $("#id_{label}").change(function() {{
            $("#id_{label}_unit").val(str2unit($(this).val()));
            $("#id_{label}_dc").val(str2dc($("#id_{label}").val()));
          }});
          $("#id_{label}_unit").change(function() {{
            $("#id_{label}").val(str2km($(this).val()));
            $("#id_{label}_dc").val(str2dc($("#id_{label}").val()));
          }});
          
          $("#id_{label}_dc").change(function() {{
            $("#id_{label}").val(parseFloat($(this).val())*parseFloat($("#id_ipp").val())/100);
            $("#id_{label}_unit").val(str2unit($("#id_{label}").val()));
          }});          
        }});  
        </script>'''.format(label=label)
        
        if disabled:
            return mark_safe(html)
        else:
            return mark_safe(html+script)


class DefaultWidget(forms.widgets.TextInput):
    
    def render(self, label, value, attrs=None):
        
        disabled = 'disabled' if attrs.get('disabled', False) else ''
        name = attrs.get('name', label)
        
        html = '<div class="col-md-12 col-no-padding"><div class="col-md-5 col-no-padding"><input {0} type="text" class="form-control" id="id_{1}" name="{2}" value="{3}"></div></div>'.format(disabled, label, name, value)
        
        return mark_safe(html)    


class HiddenWidget(forms.widgets.HiddenInput):
    
    def render(self, label, value, attrs=None):
        
        disabled = 'disabled' if attrs.get('disabled', False) else ''
        name = self.attrs.get('name', label)
        
        html = '<input {0} type="hidden" class="form-control" id="id_{1}" name="{2}" value="{3}">'.format(disabled, label, name, value)
        
        return mark_safe(html)
    

class CodesWidget(forms.widgets.Textarea):
    
    def render(self, label, value, attrs=None):
        
        disabled = 'disabled' if attrs.get('disabled', False) else ''
        name = attrs.get('name', label)
        
        if '[' in value:
            value = ast.literal_eval(value)
        
        if isinstance(value, list):
            codes = '\r\n'.join(value)
        else:
            codes = value
                
        html = '<textarea rows="5" {0} class="form-control" id="id_{1}" name="{2}" style="white-space:nowrap; overflow:scroll;">{3}</textarea>'.format(disabled, label, name, codes)
        
        return mark_safe(html)
    