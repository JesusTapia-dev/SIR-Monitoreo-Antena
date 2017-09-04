
import ast
import json
from itertools import chain

from django import forms
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.utils.html import conditional_escape

try:
    basestring  # attempt to evaluate basestring
    def isstr(s):
        return isinstance(s, basestring)
except NameError:
    def isstr(s):
        return isinstance(s, str)

class KmUnitWidget(forms.widgets.TextInput):

    def render(self, label, value, attrs=None):

        if isinstance(value, (int, float)):
            unit = int(value*attrs['km2unit'])
        elif isstr(value):
            units = []
            values = [s for s in value.split(',') if s]
            for val in values:
                units.append('{0:.0f}'.format(float(val)*attrs['km2unit']))

            unit = ','.join(units)

        disabled = 'disabled' if attrs.get('disabled', False) else ''
        name = attrs.get('name', label)
        if attrs['id'] in ('id_delays',):
            input_type = 'text'
        else:
            input_type = 'number'

        if 'line' in attrs:
            label += '_{0}_{1}'.format(attrs['line'].pk, name.split('|')[0])

        html = '''<div class="col-md-12 col-no-padding">
        <div class="col-md-5 col-no-padding"><input type="{0}" step="any" {1} class="form-control" id="id_{2}" name="{3}" value="{4}"></div>
        <div class="col-md-1 col-no-padding">Km</div>
        <div class="col-md-5 col-no-padding"><input type="{0}" step="any" {1} class="form-control" id="id_{2}_unit" value="{5}"></div>
        <div class="col-md-1 col-no-padding">Units</div></div><br>'''.format(input_type, disabled, label, name, value, unit)

        script = '''<script type="text/javascript">
        $(document).ready(function () {{

          km_fields.push("id_{label}");
          unit_fields.push("id_{label}_unit");

          $("#id_{label}").change(function() {{
            $("#id_{label}_unit").val(str2unit($(this).val()));
            $("#id_{label}").val(str2km($("#id_{label}_unit").val()));
            updateWindows("#id_{label}");
          }});
          $("#id_{label}_unit").change(function() {{
            $(this).val(str2int($(this).val()));
            $("#id_{label}").val(str2km($(this).val()));
            updateWindows("#id_{label}");
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
            label += '_{0}_{1}'.format(attrs['line'].pk, name.split('|')[0])

        html = '''<div class="col-md-12 col-no-padding">
        <div class="col-md-5 col-no-padding"><input type="number" step="any" {0} class="form-control" id="id_{1}_unit" name="{2}" value="{3}"></div>
        <div class="col-md-1 col-no-padding">Units</div>
        <div class="col-md-5 col-no-padding"><input type="number" step="any" {4} class="form-control" id="id_{5}" value="{6}"></div>
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
        <div class="col-md-3 col-no-padding"><input type="number" step="any" {0} class="form-control" id="id_{1}" name="{2}" value="{3}"></div>
        <div class="col-md-1 col-no-padding">Km</div>
        <div class="col-md-3 col-no-padding"><input type="number" step="any" {4} class="form-control" id="id_{1}_unit" value="{5}"></div>
        <div class="col-md-1 col-no-padding">Units</div>
        <div class="col-md-3 col-no-padding"><input type="number" step="any" {4} class="form-control" id="id_{1}_hz" value="{6}"></div>
        <div class="col-md-1 col-no-padding">Hz</div>
        </div>'''.format(disabled, label, name, value, disabled, unit, hz)

        script = '''<script type="text/javascript">
        $(document).ready(function () {{
          km_fields.push("id_{label}");
          unit_fields.push("id_{label}_unit");
          $("#id_{label}").change(function() {{
            $("#id_{label}_unit").val(str2unit($(this).val()));
            $("#id_{label}").val(str2km($("#id_{label}_unit").val()));
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

        dc = float(json.loads(attrs['line'].params)['pulse_width'])*100/attrs['line'].rc_configuration.ipp

        html = '''<div class="col-md-12 col-no-padding">
        <div class="col-md-3 col-no-padding"><input type="number" step="any" {0} class="form-control" id="id_{1}" name="{2}" value="{3}"></div>
        <div class="col-md-1 col-no-padding">Km</div>
        <div class="col-md-3 col-no-padding"><input type="number" step="any" {4} class="form-control" id="id_{1}_unit" value="{5}"></div>
        <div class="col-md-1 col-no-padding">Units</div>
        <div class="col-md-3 col-no-padding"><input type="number" step="any" {4} class="form-control" id="id_{1}_dc" value="{6}"></div>
        <div class="col-md-1 col-no-padding">DC[%]</div>
        </div>'''.format(disabled, label, name, value, disabled, unit, dc)

        script = '''<script type="text/javascript">
        $(document).ready(function () {{
          km_fields.push("id_{label}");
          unit_fields.push("id_{label}_unit");
          dc_fields.push("id_{label}");
          $("#id_{label}").change(function() {{
            $("#id_{label}_unit").val(str2unit($(this).val()));
            $("#id_{label}").val(str2km($("#id_{label}_unit").val()));
            $("#id_{label}_dc").val(str2dc($("#id_{label}").val()));
          }});
          $("#id_{label}_unit").change(function() {{
            $("#id_{label}").val(str2km($(this).val()));
            $("#id_{label}_dc").val(str2dc($("#id_{label}").val()));
          }});

          $("#id_{label}_dc").change(function() {{
            $("#id_{label}").val(parseFloat($(this).val())*100/parseFloat($("#id_ipp").val()));
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
        itype = 'number' if label in ('number_of_samples', 'last_height') else 'text'
        name = attrs.get('name', label)
        if 'line' in attrs:
            label += '_{0}_{1}'.format(attrs['line'].pk, name.split('|')[0])

        if itype=='number':
            html = '<div class="col-md-12 col-no-padding"><div class="col-md-5 col-no-padding"><input {0} type="{1}" step="any" class="form-control" id="id_{2}" name="{3}" value="{4}"></div></div>'.format(disabled, itype, label, name, value)
        else:
            html = '<div class="col-md-12 col-no-padding"><div class="col-md-5 col-no-padding"><input {0} type="{1}" step="any" class="form-control" id="id_{2}" name="{3}" value="{4}"></div></div>'.format(disabled, itype, label, name, value)

        if 'last_height' in label or 'number_of_samples' in label:
            script = '''<script type="text/javascript">
        $(document).ready(function () {{

          $("#id_{label}").change(function() {{
            updateWindows("#id_{label}");
          }});

        }});
        </script>'''.format(label=label)
        else:
            script = ''

        if disabled:
            return mark_safe(html)
        else:
            return mark_safe(html+script)



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

class HCheckboxSelectMultiple(forms.CheckboxSelectMultiple):

    def render(self, name, value, attrs=None, choices=()):

        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<br><ul>']
        # Normalize to strings
        str_values = set([force_text(v) for v in value])
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = u' for="%s"' % final_attrs['id']
            else:
                label_for = ''

            cb = forms.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_text(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_text(option_label))
            output.append(u'<span><label%s>%s %s</label></span>' % (label_for, rendered_cb, option_label))
        output.append(u'</div><br>')
        return mark_safe(u'\n'.join(output))
