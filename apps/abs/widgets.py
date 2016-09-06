import ast
import json
from itertools import chain

from django import forms
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape

style = """<style>

        .abs {
            border: 2px solid #00334d;
            vertical-align: top;
            display: inline-block;
            font-size: 85%;
        }

        .abs tr:nth-child(n) {
            border-bottom: 1px dashed #00334d;
        }
        .abs tr:nth-child(3) {
            border-bottom: 0px solid #00334d;
        }

        .abs td:nth-child(1){
            border-right: 1px dashed #00334d;
            text-align: center;
            padding: 1px;
        }
        .abs tr:nth-child(1) td:nth-child(1) {
            border-right: 0px solid #00334d;
        }
        .abs td{
            border-right: 0px solid #00334d;
            text-align: center;
            padding: 1px;
        }


        .north_quarter{
          border: 2px solid #00334d;
          vertical-align: center;
          font-weight: bold;
        }
        .north_quarter tr{
            border: 1px solid #ffffff;
            background-color: #ecf0f1;
        }
        .north_quarter td{
            border: 2px solid #e2e2e7;
            text-align: center;
        }

        .east_quarter{
          border: 2px solid #00334d;
          vertical-align: center;
          font-weight: bold;
        }
        .east_quarter tr{
            border: 1px solid #ffffff;
            background-color: #ecf0f1;
        }
        .east_quarter td{
            border: 2px solid #e2e2e7;
            text-align: center;
        }

        .west_quarter{
          border: 2px solid #00334d;
          vertical-align: center;
          font-weight: bold;
        }
        .west_quarter tr{
            border: 1px solid #ffffff;
            background-color: #ecf0f1;
        }
        .west_quarter td{
            border: 2px solid #e2e2e7;
            text-align: center;
        }

        .south_quarter{
          border: 2px solid #00334d;
          vertical-align: center;
          font-weight: bold;
        }
        .south_quarter tr{
            border: 1px solid #ffffff;
            background-color: #ecf0f1;
        }
        .south_quarter td{
            border: 2px solid #e2e2e7;
            text-align: center;
        }






        .abs_tx {
            border: 2px solid #00334d;
            vertical-align: top;
            display: inline-block;
            font-size: 85%;
            margin-left: 30px;
        }

        .abs_tx tr:nth-child(n) {
            border-bottom: 1px dashed #00334d;
        }
        .abs_tx tr:nth-child(3) {
            border-bottom: 0px solid #00334d;
        }

        .abs_tx td:nth-child(1){
            border-right: 1px dashed #00334d;
            text-align: center;
            padding: 1px;
        }
        .abs_tx tr:nth-child(1) td:nth-child(1) {
            border-right: 0px solid #00334d;
        }
        .abs_tx td{
            border-right: 0px solid #00334d;
            text-align: center;
            padding: 1px;
        }


        .tx_north_quarter{
          border: 2px solid #00334d;
          vertical-align: center;
          font-weight: bold;
        }
        .tx_north_quarter tr{
            border: 1px solid #ffffff;
            background-color: #ecf0f1;
        }
        .tx_north_quarter td{
            border: 2px solid #e2e2e7;
            text-align: center;
        }


        .tx_east_quarter{
          border: 2px solid #00334d;
          vertical-align: center;
          font-weight: bold;
        }
        .tx_east_quarter tr{
            border: 1px solid #ffffff;
            background-color: #ecf0f1;
        }
        .tx_east_quarter td{
            border: 2px solid #e2e2e7;
            text-align: center;
        }


        .tx_west_quarter{
          border: 2px solid #00334d;
          vertical-align: center;
          font-weight: bold;
        }
        .tx_west_quarter tr{
            border: 1px solid #ffffff;
            background-color: #ecf0f1;
        }
        .tx_west_quarter td{
            border: 2px solid #e2e2e7;
            text-align: center;
        }


        .tx_south_quarter{
          border: 2px solid #00334d;
          vertical-align: center;
          font-weight: bold;
        }
        .tx_south_quarter tr{
            border: 1px solid #ffffff;
            background-color: #ecf0f1;
        }
        .tx_south_quarter td{
            border: 2px solid #e2e2e7;
            text-align: center;
        }




        .abs_rx {
            border: 2px solid #00334d;
            vertical-align: top;
            display: inline-block;
            font-size: 85%;
            margin-left: 30px;
        }

        .abs_rx tr:nth-child(n) {
            border-bottom: 1px dashed #00334d;
        }
        .abs_rx tr:nth-child(3) {
            border-bottom: 0px solid #00334d;
        }

        .abs_rx td:nth-child(1){
            border-right: 1px dashed #00334d;
            text-align: center;
            padding: 1px;
        }
        .abs_rx tr:nth-child(1) td:nth-child(1) {
            border-right: 0px solid #00334d;
        }
        .abs_rx td{
            border-right: 0px solid #00334d;
            text-align: center;
            padding: 1px;
        }


        .rx_north_quarter{
          border: 2px solid #00334d;
          vertical-align: center;
          font-weight: bold;
        }
        .rx_north_quarter tr{
            border: 1px solid #ffffff;
            background-color: #ecf0f1;
        }
        .rx_north_quarter td{
            border: 2px solid #e2e2e7;
            text-align: center;
        }


        .rx_east_quarter{
          border: 2px solid #00334d;
          vertical-align: center;
          font-weight: bold;
        }
        .rx_east_quarter tr{
            border: 1px solid #ffffff;
            background-color: #ecf0f1;
        }
        .rx_east_quarter td{
            border: 2px solid #e2e2e7;
            text-align: center;
        }


        .rx_west_quarter{
          border: 2px solid #00334d;
          vertical-align: center;
          font-weight: bold;
        }
        .rx_west_quarter tr{
            border: 1px solid #ffffff;
            background-color: #ecf0f1;
        }
        .rx_west_quarter td{
            border: 2px solid #e2e2e7;
            text-align: center;
        }


        .rx_south_quarter{
          border: 2px solid #00334d;
          vertical-align: center;
          font-weight: bold;
        }
        .rx_south_quarter tr{
            border: 1px solid #ffffff;
            background-color: #ecf0f1;
        }
        .rx_south_quarter td{
            border: 2px solid #e2e2e7;
            text-align: center;
        }



        .tx {
          border: 2px solid #00334d;
          vertical-align: center;
          font-weight: bold;
        }
        .tx tr{
            border: 1px solid #ffffff;
            background-color: #ecf0f1;
        }
        .tx td{
            border: 2px solid #e2e2e7;
            text-align: center;
        }


        .rx {
          border: 2px solid #00334d;
          vertical-align: center;
          font-weight: bold;
        }
        .rx tr{
            border: 1px solid #ffffff;
            background-color: #ecf0f1;
        }
        .rx td{
            border: 2px solid #e2e2e7;
            text-align: center;
        }

        input[type="checkbox"] {
            margin-top: 0px;
            line-height: normal;
            margin-bottom: 0px;
            vertical-align: middle;
        }

        </style>"""


class EditUpDataWidget(forms.widgets.TextInput):

    def render(self, label, value, attrs=None):

        try:
            beam     = attrs.get('beam', value)
        except:
            return

        checked_tx = {}
        for i in range(1,65):
            checked_tx['']=''

        checked_onlyrx = ''
        if beam.get_up_onlyrx == True:
            checked_onlyrx = 'checked="True"'


        html = '''

         <div class="container">
             <div style="display:inline-block">
               Name:
               <label style="display:inline-block"><input value="{beam.name}" style="display:inline-block" name="beam_name" class="form-control" id="id_name" type="text"></label>
             </div>
         </div>

        <br>
        <div class="panel-group">
          <div style="display: inline-block" id="UP" class="panel panel-default">

            <div class="panel-heading">UP</div>


            <div class="panel-body">

              <table class="abs">
                <tr>
                  <td colspan="2"> <b>Antenna</b> </td>
                </tr>
                <tr>
                  <td> <b>North Quarter</b>
                    <table class="north_quarter">
                      <tr>
                        <td><select id="abs_value1" name="abs_up1"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select id="abs_value2" name="abs_up2"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select id="abs_value3" name="abs_up3"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select id="abs_value4" name="abs_up4"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                      </tr>
                      <tr>
                        <td><select id="abs_value9" name="abs_up9"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select id="abs_value10" name="abs_up10"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select id="abs_value11" name="abs_up11"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select id="abs_value12" name="abs_up12"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                      </tr>
                      <tr>
                        <td><select id="abs_value17" name="abs_up17"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select id="abs_value18" name="abs_up18"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select id="abs_value19" name="abs_up19"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select id="abs_value20" name="abs_up20"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                      </tr>
                      <tr>
                        <td><select id="abs_value25" name="abs_up25"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select id="abs_value26" name="abs_up26"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select id="abs_value27" name="abs_up27"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select id="abs_value28" name="abs_up28"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                      </tr>
                      </table>
                    </td>
                    <td> <b>East Quarter</b>
                      <table class="east_quarter">
                        <tr>
                          <td><select id="abs_value5" name="abs_up5"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value6" name="abs_up6"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value7" name="abs_up7"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value8" name="abs_up8"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select id="abs_value13" name="abs_up13"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value14" name="abs_up14"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value15" name="abs_up15"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value16" name="abs_up16"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select id="abs_value21" name="abs_up21"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value22" name="abs_up22"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value23" name="abs_up23"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value24" name="abs_up24"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select id="abs_value29" name="abs_up29"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value30" name="abs_up30"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value31" name="abs_up31"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value32" name="abs_up32"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                  <tr>
                    <td> <b>West Quarter</b>
                      <table class="west_quarter">
                        <tr>
                          <td><select id="abs_value33" name="abs_up33"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value34" name="abs_up34"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value35" name="abs_up35"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value36" name="abs_up36"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select id="abs_value41" name="abs_up41"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value42" name="abs_up42"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value43" name="abs_up43"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value44" name="abs_up44"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select id="abs_value49" name="abs_up49"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value50" name="abs_up50"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value51" name="abs_up51"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value52" name="abs_up52"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select id="abs_value57" name="abs_up57"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value58" name="abs_up58"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value59" name="abs_up59"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value60" name="abs_up60"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                      </table>
                    </td>
                    <td> <b>South Quarter</b>
                      <table class="south_quarter">
                        <tr>
                          <td><select id="abs_value37" name="abs_up37"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value38" name="abs_up38"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value39" name="abs_up39"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value40" name="abs_up40"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select id="abs_value45" name="abs_up45"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value46" name="abs_up46"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value47" name="abs_up47"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value48" name="abs_up48"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select id="abs_value53" name="abs_up53"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value54" name="abs_up54"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value55" name="abs_up55"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value56" name="abs_up56"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select id="abs_value61" name="abs_up61"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value62" name="abs_up62"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value63" name="abs_up63"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_value64" name="abs_up64"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>



                <table class="abs_tx">
                  <tr>
                    <td colspan="2"> <b>TX</b> </td>
                  </tr>
                  <tr>
                    <td> <b>North Quarter</b>
                      <table align="center" class="tx_north_quarter">
                         <tr>
                           <td> <input id="uptx1" name="uptx_checks" type="checkbox" value=1> </td>
                           <td> <input id="uptx2" name="uptx_checks" type="checkbox" value=2> </td>
                           <td> <input id="uptx3" name="uptx_checks" type="checkbox" value=3> </td>
                           <td> <input id="uptx4" name="uptx_checks" type="checkbox" value=4> </td>
                         </tr>
                         <tr>
                           <td> <input id="uptx9" name="uptx_checks" type="checkbox" value=9> </td>
                           <td> <input id="uptx10" name="uptx_checks" type="checkbox" value=10> </td>
                           <td> <input id="uptx11" name="uptx_checks" type="checkbox" value=11> </td>
                           <td> <input id="uptx12" name="uptx_checks" type="checkbox" value=12> </td>
                         </tr>
                         <tr>
                           <td> <input id="uptx17" name="uptx_checks" type="checkbox" value=17> </td>
                           <td> <input id="uptx18" name="uptx_checks" type="checkbox" value=18> </td>
                           <td> <input id="uptx19" name="uptx_checks" type="checkbox" value=19> </td>
                           <td> <input id="uptx20" name="uptx_checks" type="checkbox" value=20> </td>
                         </tr>
                         <tr>
                           <td> <input id="uptx25" name="uptx_checks" type="checkbox" value=25> </td>
                           <td> <input id="uptx26" name="uptx_checks" type="checkbox" value=26> </td>
                           <td> <input id="uptx27" name="uptx_checks" type="checkbox" value=27> </td>
                           <td> <input id="uptx28" name="uptx_checks" type="checkbox" value=28> </td>
                         </tr>
                      </table>
                    </td>
                    <td> <b>East Quarter</b>
                      <table align="center" class="tx_east_quarter">
                        <tr>
                          <td> <input id="uptx5" name="uptx_checks" type="checkbox" value=5> </td>
                          <td> <input id="uptx6" name="uptx_checks" type="checkbox" value=6> </td>
                          <td> <input id="uptx7" name="uptx_checks" type="checkbox" value=7> </td>
                          <td> <input id="uptx8" name="uptx_checks" type="checkbox" value=8> </td>
                        </tr>
                        <tr>
                          <td> <input id="uptx13" name="uptx_checks" type="checkbox" value=13> </td>
                          <td> <input id="uptx14" name="uptx_checks" type="checkbox" value=14> </td>
                          <td> <input id="uptx15" name="uptx_checks" type="checkbox" value=15> </td>
                          <td> <input id="uptx16" name="uptx_checks" type="checkbox" value=16></td>
                        </tr>
                        <tr>
                          <td> <input id="uptx21" name="uptx_checks" type="checkbox" value=21> </td>
                          <td> <input id="uptx22" name="uptx_checks" type="checkbox" value=22> </td>
                          <td> <input id="uptx23" name="uptx_checks" type="checkbox" value=23> </td>
                          <td> <input id="uptx24" name="uptx_checks" type="checkbox" value=24> </td>
                        </tr>
                        <tr>
                          <td> <input id="uptx29" name="uptx_checks" type="checkbox" value=29> </td>
                          <td> <input id="uptx30" name="uptx_checks" type="checkbox" value=30> </td>
                          <td> <input id="uptx31" name="uptx_checks" type="checkbox" value=31> </td>
                          <td> <input id="uptx32" name="uptx_checks" type="checkbox" value=32> </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                  <tr>
                    <td> <b>West Quarter</b>
                      <table align="center" class="tx_west_quarter">
                        <tr>
                          <td> <input id="uptx33" name="uptx_checks" type="checkbox" value=33> </td> <!--class="checkbox-inline"--->
                          <td> <input id="uptx34" name="uptx_checks" type="checkbox" value=34> </td>
                          <td> <input id="uptx35" name="uptx_checks" type="checkbox" value=35> </td>
                          <td> <input id="uptx36" name="uptx_checks" type="checkbox" value=36> </td>
                        </tr>
                        <tr>
                          <td> <input id="uptx41" name="uptx_checks" type="checkbox" value=41> </td>
                          <td> <input id="uptx42" name="uptx_checks" type="checkbox" value=42> </td>
                          <td> <input id="uptx43" name="uptx_checks" type="checkbox" value=43> </td>
                          <td> <input id="uptx44" name="uptx_checks" type="checkbox" value=44> </td>
                        </tr>
                        <tr>
                          <td> <input id="uptx49" name="uptx_checks" type="checkbox" value=49> </td>
                          <td> <input id="uptx50" name="uptx_checks" type="checkbox" value=50> </td>
                          <td> <input id="uptx51" name="uptx_checks" type="checkbox" value=51> </td>
                          <td> <input id="uptx52" name="uptx_checks" type="checkbox" value=52> </td>
                        </tr>
                        <tr>
                          <td> <input id="uptx57" name="uptx_checks" type="checkbox" value=57> </td>
                          <td> <input id="uptx58" name="uptx_checks" type="checkbox" value=58> </td>
                          <td> <input id="uptx59" name="uptx_checks" type="checkbox" value=59> </td>
                          <td> <input id="uptx60" name="uptx_checks" type="checkbox" value=60> </td>
                        </tr>
                      </table>
                    </td>
                    <td> <b>South Quarter</b>
                      <table align="center" class="tx_south_quarter">
                        <tr>
                          <td> <input id="uptx37" name="uptx_checks" type="checkbox" value=37> </td>
                          <td> <input id="uptx38" name="uptx_checks" type="checkbox" value=38> </td>
                          <td> <input id="uptx39" name="uptx_checks" type="checkbox" value=39> </td>
                          <td> <input id="uptx40" name="uptx_checks" type="checkbox" value=40> </td>
                        </tr>
                        <tr>
                          <td> <input id="uptx45" name="uptx_checks" type="checkbox" value=45> </td>
                          <td> <input id="uptx46" name="uptx_checks" type="checkbox" value=46> </td>
                          <td> <input id="uptx47" name="uptx_checks" type="checkbox" value=47> </td>
                          <td> <input id="uptx48" name="uptx_checks" type="checkbox" value=48> </td>
                        </tr>
                        <tr>
                          <td> <input id="uptx53" name="uptx_checks" type="checkbox" value=53> </td>
                          <td> <input id="uptx54" name="uptx_checks" type="checkbox" value=54> </td>
                          <td> <input id="uptx55" name="uptx_checks" type="checkbox" value=55> </td>
                          <td> <input id="uptx56" name="uptx_checks" type="checkbox" value=56> </td>
                        </tr>
                        <tr>
                          <td> <input id="uptx61" name="uptx_checks" type="checkbox" value=61> </td>
                          <td> <input id="uptx62" name="uptx_checks" type="checkbox" value=62> </td>
                          <td> <input id="uptx63" name="uptx_checks" type="checkbox" value=63> </td>
                          <td> <input id="uptx64" name="uptx_checks" type="checkbox" value=64> </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>

                <table class="abs_rx">
                  <tr>
                    <td colspan="2"> <b>RX</b> </td>
                  </tr>
                  <tr>
                    <td> <b>North Quarter</b>
                      <table align="center" class="rx_north_quarter">
                         <tr>
                           <td> <input id="uprx1" name="uprx_checks" type="checkbox" value=1> </td>
                           <td> <input id="uprx2" name="uprx_checks" type="checkbox" value=2> </td>
                           <td> <input id="uprx3" name="uprx_checks" type="checkbox" value=3> </td>
                           <td> <input id="uprx4" name="uprx_checks" type="checkbox" value=4> </td>
                         </tr>
                         <tr>
                           <td> <input id="uprx9" name="uprx_checks" type="checkbox" value=9> </td>
                           <td> <input id="uprx10" name="uprx_checks" type="checkbox" value=10> </td>
                           <td> <input id="uprx11" name="uprx_checks" type="checkbox" value=11> </td>
                           <td> <input id="uprx12" name="uprx_checks" type="checkbox" value=12> </td>
                         </tr>
                         <tr>
                           <td> <input id="uprx17" name="uprx_checks" type="checkbox" value=17> </td>
                           <td> <input id="uprx18" name="uprx_checks" type="checkbox" value=18> </td>
                           <td> <input id="uprx19" name="uprx_checks" type="checkbox" value=19> </td>
                           <td> <input id="uprx20" name="uprx_checks" type="checkbox" value=20> </td>
                         </tr>
                         <tr>
                           <td> <input id="uprx25" name="uprx_checks" type="checkbox" value=25> </td>
                           <td> <input id="uprx26" name="uprx_checks" type="checkbox" value=26> </td>
                           <td> <input id="uprx27" name="uprx_checks" type="checkbox" value=27> </td>
                           <td> <input id="uprx28" name="uprx_checks" type="checkbox" value=28> </td>
                         </tr>
                      </table>
                    </td>
                    <td> <b>East Quarter</b>
                      <table align="center" class="rx_east_quarter">
                        <tr>
                          <td> <input id="uprx5" name="uprx_checks" type="checkbox" value=5> </td>
                          <td> <input id="uprx6" name="uprx_checks" type="checkbox" value=6> </td>
                          <td> <input id="uprx7" name="uprx_checks" type="checkbox" value=7> </td>
                          <td> <input id="uprx8" name="uprx_checks" type="checkbox" value=8> </td>
                        </tr>
                        <tr>
                          <td> <input id="uprx13" name="uprx_checks" type="checkbox" value=13> </td>
                          <td> <input id="uprx14" name="uprx_checks" type="checkbox" value=14> </td>
                          <td> <input id="uprx15" name="uprx_checks" type="checkbox" value=15> </td>
                          <td> <input id="uprx16" name="uprx_checks" type="checkbox" value=16></td>
                        </tr>
                        <tr>
                          <td> <input id="uprx21" name="uprx_checks" type="checkbox" value=21> </td>
                          <td> <input id="uprx22" name="uprx_checks" type="checkbox" value=22> </td>
                          <td> <input id="uprx23" name="uprx_checks" type="checkbox" value=23> </td>
                          <td> <input id="uprx24" name="uprx_checks" type="checkbox" value=24> </td>
                        </tr>
                        <tr>
                          <td> <input id="uprx29" name="uprx_checks" type="checkbox" value=29> </td>
                          <td> <input id="uprx30" name="uprx_checks" type="checkbox" value=30> </td>
                          <td> <input id="uprx31" name="uprx_checks" type="checkbox" value=31> </td>
                          <td> <input id="uprx32" name="uprx_checks" type="checkbox" value=32> </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                  <tr>
                    <td> <b>West Quarter</b>
                      <table align="center" class="rx_west_quarter">
                        <tr>
                          <td> <input id="uprx33" name="uprx_checks" type="checkbox" value=33> </td> <!--class="checkbox-inline"--->
                          <td> <input id="uprx34" name="uprx_checks" type="checkbox" value=34> </td>
                          <td> <input id="uprx35" name="uprx_checks" type="checkbox" value=35> </td>
                          <td> <input id="uprx36" name="uprx_checks" type="checkbox" value=36> </td>
                        </tr>
                        <tr>
                          <td> <input id="uprx41" name="uprx_checks" type="checkbox" value=41> </td>
                          <td> <input id="uprx42" name="uprx_checks" type="checkbox" value=42> </td>
                          <td> <input id="uprx43" name="uprx_checks" type="checkbox" value=43> </td>
                          <td> <input id="uprx44" name="uprx_checks" type="checkbox" value=44> </td>
                        </tr>
                        <tr>
                          <td> <input id="uprx49" name="uprx_checks" type="checkbox" value=49> </td>
                          <td> <input id="uprx50" name="uprx_checks" type="checkbox" value=50> </td>
                          <td> <input id="uprx51" name="uprx_checks" type="checkbox" value=51> </td>
                          <td> <input id="uprx52" name="uprx_checks" type="checkbox" value=52> </td>
                        </tr>
                        <tr>
                          <td> <input id="uprx57" name="uprx_checks" type="checkbox" value=57> </td>
                          <td> <input id="uprx58" name="uprx_checks" type="checkbox" value=58> </td>
                          <td> <input id="uprx59" name="uprx_checks" type="checkbox" value=59> </td>
                          <td> <input id="uprx60" name="uprx_checks" type="checkbox" value=60> </td>
                        </tr>
                      </table>
                    </td>
                    <td> <b>South Quarter</b>
                      <table align="center" class="rx_south_quarter">
                        <tr>
                          <td> <input id="uprx37" name="uprx_checks" type="checkbox" value=37> </td>
                          <td> <input id="uprx38" name="uprx_checks" type="checkbox" value=38> </td>
                          <td> <input id="uprx39" name="uprx_checks" type="checkbox" value=39> </td>
                          <td> <input id="uprx40" name="uprx_checks" type="checkbox" value=40> </td>
                        </tr>
                        <tr>
                          <td> <input id="uprx45" name="uprx_checks" type="checkbox" value=45> </td>
                          <td> <input id="uprx46" name="uprx_checks" type="checkbox" value=46> </td>
                          <td> <input id="uprx47" name="uprx_checks" type="checkbox" value=47> </td>
                          <td> <input id="uprx48" name="uprx_checks" type="checkbox" value=48> </td>
                        </tr>
                        <tr>
                          <td> <input id="uprx53" name="uprx_checks" type="checkbox" value=53> </td>
                          <td> <input id="uprx54" name="uprx_checks" type="checkbox" value=54> </td>
                          <td> <input id="uprx55" name="uprx_checks" type="checkbox" value=55> </td>
                          <td> <input id="uprx56" name="uprx_checks" type="checkbox" value=56> </td>
                        </tr>
                        <tr>
                          <td> <input id="uprx61" name="uprx_checks" type="checkbox" value=61> </td>
                          <td> <input id="uprx62" name="uprx_checks" type="checkbox" value=62> </td>
                          <td> <input id="uprx63" name="uprx_checks" type="checkbox" value=63> </td>
                          <td> <input id="uprx64" name="uprx_checks" type="checkbox" value=64> </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>


                <div id="id_ues_up" class="container">
                  <h5>Ues</h5>
                    <div class="col-xs-2">
                      <input name="ues_up1" value="{beam.get_up_ues[0]}" class="form-control" id="input1" type="number" step="any">
                    </div>
                    <div class="col-xs-2">
                      <input name="ues_up2" value="{beam.get_up_ues[1]}" class="form-control" id="input2" type="number" step="any">
                    </div>
                    <div class="col-xs-2">
                      <input name="ues_up3" value="{beam.get_up_ues[2]}" class="form-control" id="input3" type="number" step="any">
                    </div>
                    <div class="col-xs-2">
                      <input name="ues_up4" value="{beam.get_up_ues[3]}" class="form-control" id="input4" type="number" step="any">
                    </div>
                    <div style="vertical-align:center; margin-top:20px;">
                      <label class="checkbox-inline"><input name="onlyrx" {checked_onlyrx} style="vertical-align:bottom" id="onlyrx_up"  type="checkbox" value=1>Only RX</label>
                    </div>
                </div>


            </div>



          </div>
        </div>
        '''.format(beam=beam, checked_onlyrx=checked_onlyrx)

        script = '''

        <script type="text/javascript">
        $(document).ready(function () {{

          var antenna_upvalues     = {beam.get_upvalues};
          var tx_upvalues          = {beam.get_uptx};
          var rx_upvalues          = {beam.get_uprx};

          for (var i = 1, len = 65; i < len; i++) {{
            var abs_select = "abs_value"+i.toString()
            document.getElementById(abs_select).value = antenna_upvalues[i-1];

            var abs_uptx = "uptx"+i.toString()
            if (tx_upvalues[i-1]==1){{
              document.getElementById(abs_uptx).checked = true;
            }}

            var abs_uprx = "uprx"+i.toString()
            if (rx_upvalues[i-1]==1){{
              document.getElementById(abs_uprx).checked = true;
            }}
          }}


          for (var i = 1, len = 65; i < len; i++) {{

          }}



        }});
        </script>

        '''.format(beam=beam)

        return mark_safe(style+html+script)


class EditDownDataWidget(forms.widgets.TextInput):

    def render(self, label, value, attrs=None):

        try:
            beam     = attrs.get('beam', value)
        except:
            return

        checked_onlyrx = ''
        if beam.get_down_onlyrx == True:
            checked_onlyrx = 'checked="True"'

        html = '''
        <br>
        <div class="panel-group">
          <div style="display: inline-block" id="DOWN" class="panel panel-default">

            <div class="panel-heading">Down</div>


            <div class="panel-body">

              <table class="abs">
                <tr>
                  <td colspan="2"> <b>Antenna</b> </td>
                </tr>
                <tr>
                  <td> <b>North Quarter</b>
                    <table class="north_quarter">
                      <tr>
                        <td><select id="abs_dvalue1" name="abs_down1"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select id="abs_dvalue2" name="abs_down2"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select id="abs_dvalue3" name="abs_down3"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select id="abs_dvalue4" name="abs_down4"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                      </tr>
                      <tr>
                        <td><select id="abs_dvalue9" name="abs_down9"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select id="abs_dvalue10" name="abs_down10"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select id="abs_dvalue11" name="abs_down11"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select id="abs_dvalue12" name="abs_down12"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                      </tr>
                      <tr>
                        <td><select id="abs_dvalue17" name="abs_down17"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select id="abs_dvalue18" name="abs_down18"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select id="abs_dvalue19" name="abs_down19"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select id="abs_dvalue20" name="abs_down20"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                      </tr>
                      <tr>
                        <td><select id="abs_dvalue25" name="abs_down25"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select id="abs_dvalue26" name="abs_down26"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select id="abs_dvalue27" name="abs_down27"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select id="abs_dvalue28" name="abs_down28"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                      </tr>
                      </table>
                    </td>
                    <td> <b>East Quarter</b>
                      <table class="east_quarter">
                        <tr>
                          <td><select id="abs_dvalue5" name="abs_down5"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue6" name="abs_down6"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue7" name="abs_down7"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue8" name="abs_down8"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select id="abs_dvalue13" name="abs_down13"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue14" name="abs_down14"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue15" name="abs_down15"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue16" name="abs_down16"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select id="abs_dvalue21" name="abs_down21"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue22" name="abs_down22"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue23" name="abs_down23"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue24" name="abs_down24"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select id="abs_dvalue29" name="abs_down29"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue30" name="abs_down30"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue31" name="abs_down31"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue32" name="abs_down32"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                  <tr>
                    <td> <b>West Quarter</b>
                      <table class="west_quarter">
                        <tr>
                          <td><select id="abs_dvalue33" name="abs_down33"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue34" name="abs_down34"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue35" name="abs_down35"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue36" name="abs_down36"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select id="abs_dvalue41" name="abs_down41"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue42" name="abs_down42"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue43" name="abs_down43"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue44" name="abs_down44"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select id="abs_dvalue49" name="abs_down49"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue50" name="abs_down50"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue51" name="abs_down51"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue52" name="abs_down52"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select id="abs_dvalue57" name="abs_down57"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue58" name="abs_down58"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue59" name="abs_down59"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue60" name="abs_down60"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                      </table>
                    </td>
                    <td> <b>South Quarter</b>
                      <table class="south_quarter">
                        <tr>
                          <td><select id="abs_dvalue37" name="abs_down37"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue38" name="abs_down38"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue39" name="abs_down39"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue40" name="abs_down40"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select id="abs_dvalue45" name="abs_down45"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue46" name="abs_down46"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue47" name="abs_down47"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue48" name="abs_down48"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select id="abs_dvalue53" name="abs_down53"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue54" name="abs_down54"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue55" name="abs_down55"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue56" name="abs_down56"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select id="abs_dvalue61" name="abs_down61"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue62" name="abs_down62"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue63" name="abs_down63"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select id="abs_dvalue64" name="abs_down64"> <option value=0>0.0</option> <option value=0.5>0.5</option> <option value=1>1.0</option> <option value=1.5>1.5</option> <option value=2>2.0</option> <option value=2.5>2.5</option> <option value=3>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>



                <table class="abs_tx">
                  <tr>
                    <td colspan="2"> <b>TX</b> </td>
                  </tr>
                  <tr>
                    <td> <b>North Quarter</b>
                      <table align="center" class="tx_north_quarter">
                         <tr>
                           <td> <input id="downtx1" name="downtx_checks" type="checkbox" value=1> </td>
                           <td> <input id="downtx2" name="downtx_checks" type="checkbox" value=2> </td>
                           <td> <input id="downtx3" name="downtx_checks" type="checkbox" value=3> </td>
                           <td> <input id="downtx4" name="downtx_checks" type="checkbox" value=4> </td>
                         </tr>
                         <tr>
                           <td> <input id="downtx9" name="downtx_checks" type="checkbox" value=9> </td>
                           <td> <input id="downtx10" name="downtx_checks" type="checkbox" value=10> </td>
                           <td> <input id="downtx11" name="downtx_checks" type="checkbox" value=11> </td>
                           <td> <input id="downtx12" name="downtx_checks" type="checkbox" value=12> </td>
                         </tr>
                         <tr>
                           <td> <input id="downtx17" name="downtx_checks" type="checkbox" value=17> </td>
                           <td> <input id="downtx18" name="downtx_checks" type="checkbox" value=18> </td>
                           <td> <input id="downtx19" name="downtx_checks" type="checkbox" value=19> </td>
                           <td> <input id="downtx20" name="downtx_checks" type="checkbox" value=20> </td>
                         </tr>
                         <tr>
                           <td> <input id="downtx25" name="downtx_checks" type="checkbox" value=25> </td>
                           <td> <input id="downtx26" name="downtx_checks" type="checkbox" value=26> </td>
                           <td> <input id="downtx27" name="downtx_checks" type="checkbox" value=27> </td>
                           <td> <input id="downtx28" name="downtx_checks" type="checkbox" value=28> </td>
                         </tr>
                      </table>
                    </td>
                    <td> <b>East Quarter</b>
                      <table align="center" class="tx_east_quarter">
                        <tr>
                          <td> <input id="downtx5" name="downtx_checks" type="checkbox" value=5> </td>
                          <td> <input id="downtx6" name="downtx_checks" type="checkbox" value=6> </td>
                          <td> <input id="downtx7" name="downtx_checks" type="checkbox" value=7> </td>
                          <td> <input id="downtx8" name="downtx_checks" type="checkbox" value=8> </td>
                        </tr>
                        <tr>
                          <td> <input id="downtx13" name="downtx_checks" type="checkbox" value=13> </td>
                          <td> <input id="downtx14" name="downtx_checks" type="checkbox" value=14> </td>
                          <td> <input id="downtx15" name="downtx_checks" type="checkbox" value=15> </td>
                          <td> <input id="downtx16" name="downtx_checks" type="checkbox" value=16> </td>
                        </tr>
                        <tr>
                          <td> <input id="downtx21" name="downtx_checks" type="checkbox" value=21> </td>
                          <td> <input id="downtx22" name="downtx_checks" type="checkbox" value=22> </td>
                          <td> <input id="downtx23" name="downtx_checks" type="checkbox" value=23> </td>
                          <td> <input id="downtx24" name="downtx_checks" type="checkbox" value=24> </td>
                        </tr>
                        <tr>
                          <td> <input id="downtx29" name="downtx_checks" type="checkbox" value=29> </td>
                          <td> <input id="downtx30" name="downtx_checks" type="checkbox" value=30> </td>
                          <td> <input id="downtx31" name="downtx_checks" type="checkbox" value=31> </td>
                          <td> <input id="downtx32" name="downtx_checks" type="checkbox" value=32> </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                  <tr>
                    <td> <b>West Quarter</b>
                      <table align="center" class="tx_west_quarter">
                        <tr>
                          <td> <input id="downtx33" name="downtx_checks" type="checkbox" value=33> </td> <!--class="checkbox-inline"--->
                          <td> <input id="downtx34" name="downtx_checks" type="checkbox" value=34> </td>
                          <td> <input id="downtx35" name="downtx_checks" type="checkbox" value=35> </td>
                          <td> <input id="downtx36" name="downtx_checks" type="checkbox" value=36> </td>
                        </tr>
                        <tr>
                          <td> <input id="downtx41" name="downtx_checks" type="checkbox" value=41> </td>
                          <td> <input id="downtx42" name="downtx_checks" type="checkbox" value=42> </td>
                          <td> <input id="downtx43" name="downtx_checks" type="checkbox" value=43> </td>
                          <td> <input id="downtx44"name="downtx_checks" type="checkbox" value=44> </td>
                        </tr>
                        <tr>
                          <td> <input id="downtx49" name="downtx_checks" type="checkbox" value=49> </td>
                          <td> <input id="downtx50" name="downtx_checks" type="checkbox" value=50> </td>
                          <td> <input id="downtx51" name="downtx_checks" type="checkbox" value=51> </td>
                          <td> <input id="downtx52" name="downtx_checks" type="checkbox" value=52> </td>
                        </tr>
                        <tr>
                          <td> <input id="downtx57" name="downtx_checks" type="checkbox" value=57> </td>
                          <td> <input id="downtx58" name="downtx_checks" type="checkbox" value=58> </td>
                          <td> <input id="downtx59" name="downtx_checks" type="checkbox" value=59> </td>
                          <td> <input id="downtx60" name="downtx_checks" type="checkbox" value=60> </td>
                        </tr>
                      </table>
                    </td>
                    <td> <b>South Quarter</b>
                      <table align="center" class="tx_south_quarter">
                        <tr>
                          <td> <input id="downtx37" name="downtx_checks" type="checkbox" value=37> </td> <!--class="checkbox-inline"--->
                          <td> <input id="downtx38" name="downtx_checks" type="checkbox" value=38> </td>
                          <td> <input id="downtx39" name="downtx_checks" type="checkbox" value=39> </td>
                          <td> <input id="downtx40" name="downtx_checks" type="checkbox" value=40> </td>
                        </tr>
                        <tr>
                          <td> <input id="downtx45" name="downtx_checks" type="checkbox" value=45> </td>
                          <td> <input id="downtx46" name="downtx_checks" type="checkbox" value=46> </td>
                          <td> <input id="downtx47" name="downtx_checks" type="checkbox" value=47> </td>
                          <td> <input id="downtx48" name="downtx_checks" type="checkbox" value=48> </td>
                        </tr>
                        <tr>
                          <td> <input id="downtx53" name="downtx_checks" type="checkbox" value=53> </td>
                          <td> <input id="downtx54" name="downtx_checks" type="checkbox" value=54> </td>
                          <td> <input id="downtx55" name="downtx_checks" type="checkbox" value=55> </td>
                          <td> <input id="downtx56" name="downtx_checks" type="checkbox" value=56> </td>
                        </tr>
                        <tr>
                          <td> <input id="downtx61" name="downtx_checks" type="checkbox" value=61> </td>
                          <td> <input id="downtx62" name="downtx_checks" type="checkbox" value=62> </td>
                          <td> <input id="downtx63" name="downtx_checks" type="checkbox" value=63> </td>
                          <td> <input id="downtx64" name="downtx_checks" type="checkbox" value=64> </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>

                <table class="abs_rx">
                  <tr>
                    <td colspan="2"> <b>RX</b> </td>
                  </tr>
                  <tr>
                    <td> <b>North Quarter</b>
                      <table align="center" class="rx_north_quarter">
                         <tr>
                           <td> <input id="downrx1" name="downrx_checks" type="checkbox" value=1> </td>
                           <td> <input id="downrx2" name="downrx_checks" type="checkbox" value=2> </td>
                           <td> <input id="downrx3" name="downrx_checks" type="checkbox" value=3> </td>
                           <td> <input id="downrx4" name="downrx_checks" type="checkbox" value=4> </td>
                         </tr>
                         <tr>
                           <td> <input id="downrx9" name="downrx_checks" type="checkbox" value=9> </td>
                           <td> <input id="downrx10" name="downrx_checks" type="checkbox" value=10> </td>
                           <td> <input id="downrx11" name="downrx_checks" type="checkbox" value=11> </td>
                           <td> <input id="downrx12" name="downrx_checks" type="checkbox" value=12> </td>
                         </tr>
                         <tr>
                           <td> <input id="downrx17" name="downrx_checks" type="checkbox" value=17> </td>
                           <td> <input id="downrx18" name="downrx_checks" type="checkbox" value=18> </td>
                           <td> <input id="downrx19" name="downrx_checks" type="checkbox" value=19> </td>
                           <td> <input id="downrx20" name="downrx_checks" type="checkbox" value=20> </td>
                         </tr>
                         <tr>
                           <td> <input id="downrx25" name="downrx_checks" type="checkbox" value=25> </td>
                           <td> <input id="downrx26" name="downrx_checks" type="checkbox" value=26> </td>
                           <td> <input id="downrx27" name="downrx_checks" type="checkbox" value=27> </td>
                           <td> <input id="downrx28" name="downrx_checks" type="checkbox" value=28> </td>
                         </tr>
                      </table>
                    </td>
                    <td> <b>East Quarter</b>
                      <table align="center" class="rx_east_quarter">
                        <tr>
                          <td> <input id="downrx5" name="downrx_checks" type="checkbox" value=5> </td>
                          <td> <input id="downrx6" name="downrx_checks" type="checkbox" value=6> </td>
                          <td> <input id="downrx7" name="downrx_checks" type="checkbox" value=7> </td>
                          <td> <input id="downrx8" name="downrx_checks" type="checkbox" value=8> </td>
                        </tr>
                        <tr>
                          <td> <input id="downrx13" name="downrx_checks" type="checkbox" value=13> </td>
                          <td> <input id="downrx14" name="downrx_checks" type="checkbox" value=14> </td>
                          <td> <input id="downrx15" name="downrx_checks" type="checkbox" value=15> </td>
                          <td> <input id="downrx16" name="downrx_checks" type="checkbox" value=16> </td>
                        </tr>
                        <tr>
                          <td> <input id="downrx21" name="downrx_checks" type="checkbox" value=21> </td>
                          <td> <input id="downrx22" name="downrx_checks" type="checkbox" value=22> </td>
                          <td> <input id="downrx23" name="downrx_checks" type="checkbox" value=23> </td>
                          <td> <input id="downrx24" name="downrx_checks" type="checkbox" value=24> </td>
                        </tr>
                        <tr>
                          <td> <input id="downrx29" name="downrx_checks" type="checkbox" value=29> </td>
                          <td> <input id="downrx30" name="downrx_checks" type="checkbox" value=30> </td>
                          <td> <input id="downrx31" name="downrx_checks" type="checkbox" value=31> </td>
                          <td> <input id="downrx32" name="downrx_checks" type="checkbox" value=32> </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                  <tr>
                    <td> <b>West Quarter</b>
                      <table align="center" class="rx_west_quarter">
                        <tr>
                          <td> <input id="downrx33" name="downrx_checks" type="checkbox" value=33> </td>
                          <td> <input id="downrx34" name="downrx_checks" type="checkbox" value=34> </td>
                          <td> <input id="downrx35" name="downrx_checks" type="checkbox" value=35> </td>
                          <td> <input id="downrx36" name="downrx_checks" type="checkbox" value=36> </td>
                        </tr>
                        <tr>
                          <td> <input id="downrx41" name="downrx_checks" type="checkbox" value=41> </td>
                          <td> <input id="downrx42" name="downrx_checks" type="checkbox" value=42> </td>
                          <td> <input id="downrx43" name="downrx_checks" type="checkbox" value=43> </td>
                          <td> <input id="downrx44" name="downrx_checks" type="checkbox" value=44> </td>
                        </tr>
                        <tr>
                          <td> <input id="downrx49" name="downrx_checks" type="checkbox" value=49> </td>
                          <td> <input id="downrx50" name="downrx_checks" type="checkbox" value=50> </td>
                          <td> <input id="downrx51" name="downrx_checks" type="checkbox" value=51> </td>
                          <td> <input id="downrx52" name="downrx_checks" type="checkbox" value=52> </td>
                        </tr>
                        <tr>
                          <td> <input id="downrx57" name="downrx_checks" type="checkbox" value=57> </td>
                          <td> <input id="downrx58" name="downrx_checks" type="checkbox" value=58> </td>
                          <td> <input id="downrx59" name="downrx_checks" type="checkbox" value=59> </td>
                          <td> <input id="downrx60" name="downrx_checks" type="checkbox" value=60> </td>
                        </tr>
                      </table>
                    </td>
                    <td> <b>South Quarter</b>
                      <table align="center" class="rx_south_quarter">
                        <tr>
                          <td> <input id="downrx37" name="downrx_checks" type="checkbox" value=37> </td>
                          <td> <input id="downrx38" name="downrx_checks" type="checkbox" value=38> </td>
                          <td> <input id="downrx39" name="downrx_checks" type="checkbox" value=39> </td>
                          <td> <input id="downrx40" name="downrx_checks" type="checkbox" value=40> </td>
                        </tr>
                        <tr>
                          <td> <input id="downrx45" name="downrx_checks" type="checkbox" value=45> </td>
                          <td> <input id="downrx46" name="downrx_checks" type="checkbox" value=46> </td>
                          <td> <input id="downrx47" name="downrx_checks" type="checkbox" value=47> </td>
                          <td> <input id="downrx48" name="downrx_checks" type="checkbox" value=48> </td>
                        </tr>
                        <tr>
                          <td> <input id="downrx53" name="downrx_checks" type="checkbox" value=53> </td>
                          <td> <input id="downrx54" name="downrx_checks" type="checkbox" value=54> </td>
                          <td> <input id="downrx55" name="downrx_checks" type="checkbox" value=55> </td>
                          <td> <input id="downrx56" name="downrx_checks" type="checkbox" value=56> </td>
                        </tr>
                        <tr>
                          <td> <input id="downrx61" name="downrx_checks" type="checkbox" value=61> </td>
                          <td> <input id="downrx62" name="downrx_checks" type="checkbox" value=62> </td>
                          <td> <input id="downrx63" name="downrx_checks" type="checkbox" value=63> </td>
                          <td> <input id="downrx64" name="downrx_checks" type="checkbox" value=64> </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>


                <div id="id_ues_down" class="container">
                  <h5>Ues</h5>
                    <div class="col-xs-2">
                      <input name="ues_down1" value="{beam.get_down_ues[0]}" class="form-control" id="input1_down" type="number" step="any">
                    </div>
                    <div class="col-xs-2">
                      <input name="ues_down2" value="{beam.get_down_ues[1]}" class="form-control" id="input2_down" type="number" step="any">
                    </div>
                    <div class="col-xs-2">
                      <input name="ues_down3" value="{beam.get_down_ues[2]}" class="form-control" id="input3_down" type="number" step="any">
                    </div>
                    <div class="col-xs-2">
                      <input name="ues_down4" value="{beam.get_down_ues[3]}" class="form-control" id="input4_down" type="number" step="any">
                    </div>
                    <div style="vertical-align:center; margin-top:20px;">
                      <label class="checkbox-inline"><input style="vertical-align:bottom" {checked_onlyrx} name="onlyrx" id="onlyrx_down"  type="checkbox" value=2>Only RX</label>
                    </div>
                </div>


            </div>


          </div>
        </div>
        '''.format(beam=beam, checked_onlyrx=checked_onlyrx)

        script = '''

        <script type="text/javascript">
        $(document).ready(function () {{
          var antenna_downvalues     = {beam.get_downvalues};
          var tx_downvalues          = {beam.get_downtx};
          var rx_downvalues          = {beam.get_downrx};

          for (var i = 1, len = 65; i < len; i++) {{
            var abs_dselect = "abs_dvalue"+i.toString()
            document.getElementById(abs_dselect).value = antenna_downvalues[i-1];

            var abs_downtx = "downtx"+i.toString()
            if (tx_downvalues[i-1]==1){{
              document.getElementById(abs_downtx).checked = true;
            }}

            var abs_downrx = "downrx"+i.toString()
            if (rx_downvalues[i-1]==1){{
              document.getElementById(abs_downrx).checked = true;
            }}
          }}

        }});
        </script>

        '''.format(beam=beam)



        return mark_safe(style+html+script)



class UpDataWidget(forms.widgets.TextInput):

    def render(self, label, value, attrs=None):


        html = '''

         <div class="container">
             <div style="display:inline-block">
               Name:
               <label style="display:inline-block"><input value="Beam" style="display:inline-block" name="beam_name" class="form-control" id="id_name" type="text"></label>
             </div>
         </div>

        <br>
        <div class="panel-group">
          <div style="display: inline-block" id="UP" class="panel panel-default">

            <div class="panel-heading">UP</div>


            <div class="panel-body">

              <table class="abs">
                <tr>
                  <td colspan="2"> <b>Antenna</b> </td>
                </tr>
                <tr>
                  <td> <b>North Quarter</b>
                    <table class="north_quarter">
                      <tr>
                        <td><select name="abs_up1"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select name="abs_up2"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select name="abs_up3"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select name="abs_up4"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                      </tr>
                      <tr>
                        <td><select name="abs_up9"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select name="abs_up10"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select name="abs_up11"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select name="abs_up12"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                      </tr>
                      <tr>
                        <td><select name="abs_up17"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select name="abs_up18"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select name="abs_up19"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select name="abs_up20"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                      </tr>
                      <tr>
                        <td><select name="abs_up25"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select name="abs_up26"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select name="abs_up27"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select name="abs_up28"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                      </tr>
                      </table>
                    </td>
                    <td> <b>East Quarter</b>
                      <table class="east_quarter">
                        <tr>
                          <td><select name="abs_up5"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up6"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up7"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up8"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select name="abs_up13"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up14"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up15"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up16"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select name="abs_up21"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up22"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up23"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up24"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select name="abs_up29"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up30"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up31"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up32"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                  <tr>
                    <td> <b>West Quarter</b>
                      <table class="west_quarter">
                        <tr>
                          <td><select name="abs_up33"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up34"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up35"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up36"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select name="abs_up41"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up42"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up43"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up44"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select name="abs_up49"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up50"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up51"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up52"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select name="abs_up57"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up58"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up59"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up60"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                      </table>
                    </td>
                    <td> <b>South Quarter</b>
                      <table class="south_quarter">
                        <tr>
                          <td><select name="abs_up37"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up38"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up39"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up40"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select name="abs_up45"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up46"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up47"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up48"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select name="abs_up53"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up54"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up55"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up56"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select name="abs_up61"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up62"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up63"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_up64"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>



                <table class="abs_tx">
                  <tr>
                    <td colspan="2"> <b>TX</b> </td>
                  </tr>
                  <tr>
                    <td> <b>North Quarter</b>
                      <table align="center" class="tx_north_quarter">
                         <tr>
                           <td> <input name="uptx_checks" type="checkbox" value=1> </td>
                           <td> <input name="uptx_checks" type="checkbox" value=2> </td>
                           <td> <input name="uptx_checks" type="checkbox" value=3> </td>
                           <td> <input name="uptx_checks" type="checkbox" value=4> </td>
                         </tr>
                         <tr>
                           <td> <input name="uptx_checks" type="checkbox" value=9> </td>
                           <td> <input name="uptx_checks" type="checkbox" value=10> </td>
                           <td> <input name="uptx_checks" type="checkbox" value=11> </td>
                           <td> <input name="uptx_checks" type="checkbox" value=12> </td>
                         </tr>
                         <tr>
                           <td> <input name="uptx_checks" type="checkbox" value=17> </td>
                           <td> <input name="uptx_checks" type="checkbox" value=18> </td>
                           <td> <input name="uptx_checks" type="checkbox" value=19> </td>
                           <td> <input name="uptx_checks" type="checkbox" value=20> </td>
                         </tr>
                         <tr>
                           <td> <input name="uptx_checks" type="checkbox" value=25> </td>
                           <td> <input name="uptx_checks" type="checkbox" value=26> </td>
                           <td> <input name="uptx_checks" type="checkbox" value=27> </td>
                           <td> <input name="uptx_checks" type="checkbox" value=28> </td>
                         </tr>
                      </table>
                    </td>
                    <td> <b>East Quarter</b>
                      <table align="center" class="tx_east_quarter">
                        <tr>
                          <td> <input name="uptx_checks" type="checkbox" value=5> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=6> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=7> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=8> </td>
                        </tr>
                        <tr>
                          <td> <input name="uptx_checks" type="checkbox" value=13> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=14> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=15> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=16></td>
                        </tr>
                        <tr>
                          <td> <input name="uptx_checks" type="checkbox" value=21> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=22> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=23> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=24> </td>
                        </tr>
                        <tr>
                          <td> <input name="uptx_checks" type="checkbox" value=29> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=30> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=31> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=32> </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                  <tr>
                    <td> <b>West Quarter</b>
                      <table align="center" class="tx_west_quarter">
                        <tr>
                          <td> <input name="uptx_checks" type="checkbox" value=33> </td> <!--class="checkbox-inline"--->
                          <td> <input name="uptx_checks" type="checkbox" value=34> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=35> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=36> </td>
                        </tr>
                        <tr>
                          <td> <input name="uptx_checks" type="checkbox" value=41> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=42> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=43> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=44> </td>
                        </tr>
                        <tr>
                          <td> <input name="uptx_checks" type="checkbox" value=49> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=50> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=51> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=52> </td>
                        </tr>
                        <tr>
                          <td> <input name="uptx_checks" type="checkbox" value=57> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=58> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=59> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=60> </td>
                        </tr>
                      </table>
                    </td>
                    <td> <b>South Quarter</b>
                      <table align="center" class="tx_south_quarter">
                        <tr>
                          <td> <input name="uptx_checks" type="checkbox" value=37> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=38> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=39> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=40> </td>
                        </tr>
                        <tr>
                          <td> <input name="uptx_checks" type="checkbox" value=45> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=46> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=47> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=48> </td>
                        </tr>
                        <tr>
                          <td> <input name="uptx_checks" type="checkbox" value=53> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=54> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=55> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=56> </td>
                        </tr>
                        <tr>
                          <td> <input name="uptx_checks" type="checkbox" value=61> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=62> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=63> </td>
                          <td> <input name="uptx_checks" type="checkbox" value=64> </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>

                <table class="abs_rx">
                  <tr>
                    <td colspan="2"> <b>RX</b> </td>
                  </tr>
                  <tr>
                    <td> <b>North Quarter</b>
                      <table align="center" class="rx_north_quarter">
                         <tr>
                           <td> <input name="uprx_checks" type="checkbox" value=1> </td>
                           <td> <input name="uprx_checks" type="checkbox" value=2> </td>
                           <td> <input name="uprx_checks" type="checkbox" value=3> </td>
                           <td> <input name="uprx_checks" type="checkbox" value=4> </td>
                         </tr>
                         <tr>
                           <td> <input name="uprx_checks" type="checkbox" value=9> </td>
                           <td> <input name="uprx_checks" type="checkbox" value=10> </td>
                           <td> <input name="uprx_checks" type="checkbox" value=11> </td>
                           <td> <input name="uprx_checks" type="checkbox" value=12> </td>
                         </tr>
                         <tr>
                           <td> <input name="uprx_checks" type="checkbox" value=17> </td>
                           <td> <input name="uprx_checks" type="checkbox" value=18> </td>
                           <td> <input name="uprx_checks" type="checkbox" value=19> </td>
                           <td> <input name="uprx_checks" type="checkbox" value=20> </td>
                         </tr>
                         <tr>
                           <td> <input name="uprx_checks" type="checkbox" value=25> </td>
                           <td> <input name="uprx_checks" type="checkbox" value=26> </td>
                           <td> <input name="uprx_checks" type="checkbox" value=27> </td>
                           <td> <input name="uprx_checks" type="checkbox" value=28> </td>
                         </tr>
                      </table>
                    </td>
                    <td> <b>East Quarter</b>
                      <table align="center" class="rx_east_quarter">
                        <tr>
                          <td> <input name="uprx_checks" type="checkbox" value=5> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=6> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=7> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=8> </td>
                        </tr>
                        <tr>
                          <td> <input name="uprx_checks" type="checkbox" value=13> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=14> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=15> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=16></td>
                        </tr>
                        <tr>
                          <td> <input name="uprx_checks" type="checkbox" value=21> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=22> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=23> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=24> </td>
                        </tr>
                        <tr>
                          <td> <input name="uprx_checks" type="checkbox" value=29> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=30> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=31> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=32> </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                  <tr>
                    <td> <b>West Quarter</b>
                      <table align="center" class="rx_west_quarter">
                        <tr>
                          <td> <input name="uprx_checks" type="checkbox" value=33> </td> <!--class="checkbox-inline"--->
                          <td> <input name="uprx_checks" type="checkbox" value=34> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=35> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=36> </td>
                        </tr>
                        <tr>
                          <td> <input name="uprx_checks" type="checkbox" value=41> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=42> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=43> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=44> </td>
                        </tr>
                        <tr>
                          <td> <input name="uprx_checks" type="checkbox" value=49> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=50> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=51> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=52> </td>
                        </tr>
                        <tr>
                          <td> <input name="uprx_checks" type="checkbox" value=57> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=58> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=59> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=60> </td>
                        </tr>
                      </table>
                    </td>
                    <td> <b>South Quarter</b>
                      <table align="center" class="rx_south_quarter">
                        <tr>
                          <td> <input name="uprx_checks" type="checkbox" value=37> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=38> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=39> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=40> </td>
                        </tr>
                        <tr>
                          <td> <input name="uprx_checks" type="checkbox" value=45> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=46> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=47> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=48> </td>
                        </tr>
                        <tr>
                          <td> <input name="uprx_checks" type="checkbox" value=53> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=54> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=55> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=56> </td>
                        </tr>
                        <tr>
                          <td> <input name="uprx_checks" type="checkbox" value=61> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=62> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=63> </td>
                          <td> <input name="uprx_checks" type="checkbox" value=64> </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>


                <div id="id_ues_up" class="container">
                  <h5>Ues</h5>
                    <div class="col-xs-2">
                      <input name="ues_up1" value="0" class="form-control" id="input1" type="number" step="any">
                    </div>
                    <div class="col-xs-2">
                      <input name="ues_up2" value="0" class="form-control" id="input2" type="number" step="any">
                    </div>
                    <div class="col-xs-2">
                      <input name="ues_up3" value="0" class="form-control" id="input3" type="number" step="any">
                    </div>
                    <div class="col-xs-2">
                      <input name="ues_up4" value="0" class="form-control" id="input4" type="number" step="any">
                    </div>
                    <div style="vertical-align:center; margin-top:20px;">
                      <label class="checkbox-inline"><input name="onlyrx" style="vertical-align:bottom" id="onlyrx_up"  type="checkbox" value=1>Only RX</label>
                    </div>
                </div>


            </div>


          </div>
        </div>
        '''

        script = '''

        '''

        return mark_safe(style+html+script)


class DownDataWidget(forms.widgets.TextInput):

    def render(self, label, value, attrs=None):

        html = '''
        <br>
        <div class="panel-group">
          <div style="display: inline-block" id="DOWN" class="panel panel-default">

            <div class="panel-heading">Down</div>


            <div class="panel-body">

              <table class="abs">
                <tr>
                  <td colspan="2"> <b>Antenna</b> </td>
                </tr>
                <tr>
                  <td> <b>North Quarter</b>
                    <table class="north_quarter">
                      <tr>
                        <td><select name="abs_down1"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select name="abs_down2"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select name="abs_down3"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select name="abs_down4"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                      </tr>
                      <tr>
                        <td><select name="abs_down9"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select name="abs_down10"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select name="abs_down11"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select name="abs_down12"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                      </tr>
                      <tr>
                        <td><select name="abs_down17"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select name="abs_down18"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select name="abs_down19"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select name="abs_down20"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                      </tr>
                      <tr>
                        <td><select name="abs_down25"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select name="abs_down26"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select name="abs_down27"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        <td><select name="abs_down28"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                      </tr>
                      </table>
                    </td>
                    <td> <b>East Quarter</b>
                      <table class="east_quarter">
                        <tr>
                          <td><select name="abs_down5"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down6"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down7"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down8"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select name="abs_down13"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down14"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down15"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down16"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select name="abs_down21"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down22"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down23"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down24"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select name="abs_down29"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down30"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down31"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down32"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                  <tr>
                    <td> <b>West Quarter</b>
                      <table class="west_quarter">
                        <tr>
                          <td><select name="abs_down33"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down34"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down35"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down36"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select name="abs_down41"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down42"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down43"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down44"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select name="abs_down49"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down50"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down51"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down52"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select name="abs_down57"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down58"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down59"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down60"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                      </table>
                    </td>
                    <td> <b>South Quarter</b>
                      <table class="south_quarter">
                        <tr>
                          <td><select name="abs_down37"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down38"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down39"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down40"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select name="abs_down45"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down46"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down47"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down48"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select name="abs_down53"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down54"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down55"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down56"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                        <tr>
                          <td><select name="abs_down61"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down62"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down63"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                          <td><select name="abs_down64"> <option value=0.0>0.0</option> <option value=0.5>0.5</option> <option value=1.0>1.0</option> <option value=1.5>1.5</option> <option value=2.0>2.0</option> <option value=2.5>2.5</option> <option value=3.0>3.0</option> <option value=3.5>3.5</option> </select></td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>



                <table class="abs_tx">
                  <tr>
                    <td colspan="2"> <b>TX</b> </td>
                  </tr>
                  <tr>
                    <td> <b>North Quarter</b>
                      <table align="center" class="tx_north_quarter">
                         <tr>
                           <td> <input name="downtx_checks" type="checkbox" value=1> </td>
                           <td> <input name="downtx_checks" type="checkbox" value=2> </td>
                           <td> <input name="downtx_checks" type="checkbox" value=3> </td>
                           <td> <input name="downtx_checks" type="checkbox" value=4> </td>
                         </tr>
                         <tr>
                           <td> <input name="downtx_checks" type="checkbox" value=9> </td>
                           <td> <input name="downtx_checks" type="checkbox" value=10> </td>
                           <td> <input name="downtx_checks" type="checkbox" value=11> </td>
                           <td> <input name="downtx_checks" type="checkbox" value=12> </td>
                         </tr>
                         <tr>
                           <td> <input name="downtx_checks" type="checkbox" value=17> </td>
                           <td> <input name="downtx_checks" type="checkbox" value=18> </td>
                           <td> <input name="downtx_checks" type="checkbox" value=19> </td>
                           <td> <input name="downtx_checks" type="checkbox" value=20> </td>
                         </tr>
                         <tr>
                           <td> <input name="downtx_checks" type="checkbox" value=25> </td>
                           <td> <input name="downtx_checks" type="checkbox" value=26> </td>
                           <td> <input name="downtx_checks" type="checkbox" value=27> </td>
                           <td> <input name="downtx_checks" type="checkbox" value=28> </td>
                         </tr>
                      </table>
                    </td>
                    <td> <b>East Quarter</b>
                      <table align="center" class="tx_east_quarter">
                        <tr>
                          <td> <input name="downtx_checks" type="checkbox" value=4> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=6> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=7> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=8> </td>
                        </tr>
                        <tr>
                          <td> <input name="downtx_checks" type="checkbox" value=13> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=14> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=15> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=16> </td>
                        </tr>
                        <tr>
                          <td> <input name="downtx_checks" type="checkbox" value=21> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=22> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=23> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=24> </td>
                        </tr>
                        <tr>
                          <td> <input name="downtx_checks" type="checkbox" value=29> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=30> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=31> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=32> </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                  <tr>
                    <td> <b>West Quarter</b>
                      <table align="center" class="tx_west_quarter">
                        <tr>
                          <td> <input name="downtx_checks" type="checkbox" value=33> </td> <!--class="checkbox-inline"--->
                          <td> <input name="downtx_checks" type="checkbox" value=34> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=35> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=36> </td>
                        </tr>
                        <tr>
                          <td> <input name="downtx_checks" type="checkbox" value=41> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=42> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=43> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=44> </td>
                        </tr>
                        <tr>
                          <td> <input name="downtx_checks" type="checkbox" value=49> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=50> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=51> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=52> </td>
                        </tr>
                        <tr>
                          <td> <input name="downtx_checks" type="checkbox" value=57> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=58> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=59> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=60> </td>
                        </tr>
                      </table>
                    </td>
                    <td> <b>South Quarter</b>
                      <table align="center" class="tx_south_quarter">
                        <tr>
                          <td> <input name="downtx_checks" type="checkbox" value=37> </td> <!--class="checkbox-inline"--->
                          <td> <input name="downtx_checks" type="checkbox" value=38> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=39> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=40> </td>
                        </tr>
                        <tr>
                          <td> <input name="downtx_checks" type="checkbox" value=45> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=46> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=47> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=48> </td>
                        </tr>
                        <tr>
                          <td> <input name="downtx_checks" type="checkbox" value=53> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=54> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=55> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=56> </td>
                        </tr>
                        <tr>
                          <td> <input name="downtx_checks" type="checkbox" value=61> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=62> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=63> </td>
                          <td> <input name="downtx_checks" type="checkbox" value=64> </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>

                <table class="abs_rx">
                  <tr>
                    <td colspan="2"> <b>RX</b> </td>
                  </tr>
                  <tr>
                    <td> <b>North Quarter</b>
                      <table align="center" class="rx_north_quarter">
                         <tr>
                           <td> <input name="downrx_checks" type="checkbox" value=1> </td>
                           <td> <input name="downrx_checks" type="checkbox" value=2> </td>
                           <td> <input name="downrx_checks" type="checkbox" value=3> </td>
                           <td> <input name="downrx_checks" type="checkbox" value=4> </td>
                         </tr>
                         <tr>
                           <td> <input name="downrx_checks" type="checkbox" value=9> </td>
                           <td> <input name="downrx_checks" type="checkbox" value=10> </td>
                           <td> <input name="downrx_checks" type="checkbox" value=11> </td>
                           <td> <input name="downrx_checks" type="checkbox" value=12> </td>
                         </tr>
                         <tr>
                           <td> <input name="downrx_checks" type="checkbox" value=17> </td>
                           <td> <input name="downrx_checks" type="checkbox" value=18> </td>
                           <td> <input name="downrx_checks" type="checkbox" value=19> </td>
                           <td> <input name="downrx_checks" type="checkbox" value=20> </td>
                         </tr>
                         <tr>
                           <td> <input name="downrx_checks" type="checkbox" value=25> </td>
                           <td> <input name="downrx_checks" type="checkbox" value=26> </td>
                           <td> <input name="downrx_checks" type="checkbox" value=27> </td>
                           <td> <input name="downrx_checks" type="checkbox" value=28> </td>
                         </tr>
                      </table>
                    </td>
                    <td> <b>East Quarter</b>
                      <table align="center" class="rx_east_quarter">
                        <tr>
                          <td> <input name="downrx_checks" type="checkbox" value=5> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=6> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=7> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=8> </td>
                        </tr>
                        <tr>
                          <td> <input name="downrx_checks" type="checkbox" value=13> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=14> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=15> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=16> </td>
                        </tr>
                        <tr>
                          <td> <input name="downrx_checks" type="checkbox" value=21> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=22> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=23> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=24> </td>
                        </tr>
                        <tr>
                          <td> <input name="downrx_checks" type="checkbox" value=29> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=30> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=31> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=32> </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                  <tr>
                    <td> <b>West Quarter</b>
                      <table align="center" class="rx_west_quarter">
                        <tr>
                          <td> <input name="downrx_checks" type="checkbox" value=33> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=34> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=35> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=36> </td>
                        </tr>
                        <tr>
                          <td> <input name="downrx_checks" type="checkbox" value=41> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=42> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=43> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=44> </td>
                        </tr>
                        <tr>
                          <td> <input name="downrx_checks" type="checkbox" value=49> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=50> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=51> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=52> </td>
                        </tr>
                        <tr>
                          <td> <input name="downrx_checks" type="checkbox" value=57> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=58> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=59> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=60> </td>
                        </tr>
                      </table>
                    </td>
                    <td> <b>South Quarter</b>
                      <table align="center" class="rx_south_quarter">
                        <tr>
                          <td> <input name="downrx_checks" type="checkbox" value=37> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=38> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=39> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=40> </td>
                        </tr>
                        <tr>
                          <td> <input name="downrx_checks" type="checkbox" value=45> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=46> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=47> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=48> </td>
                        </tr>
                        <tr>
                          <td> <input name="downrx_checks" type="checkbox" value=53> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=54> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=55> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=56> </td>
                        </tr>
                        <tr>
                          <td> <input name="downrx_checks" type="checkbox" value=61> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=62> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=63> </td>
                          <td> <input name="downrx_checks" type="checkbox" value=64> </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>


                <div id="id_ues_down" class="container">
                  <h5>Ues</h5>
                    <div class="col-xs-2">
                      <input name="ues_down1" value="0" class="form-control" id="input1_down" type="number" step="any">
                    </div>
                    <div class="col-xs-2">
                      <input name="ues_down2" value="0" class="form-control" id="input2_down" type="number" step="any">
                    </div>
                    <div class="col-xs-2">
                      <input name="ues_down3" value="0" class="form-control" id="input3_down" type="number" step="any">
                    </div>
                    <div class="col-xs-2">
                      <input name="ues_down4" value="0" class="form-control" id="input4_down" type="number" step="any">
                    </div>
                    <div style="vertical-align:center; margin-top:20px;">
                      <label class="checkbox-inline"><input style="vertical-align:bottom" name="onlyrx" id="onlyrx_down"  type="checkbox" value=2>Only RX</label>
                    </div>
                </div>


            </div>


          </div>
        </div>
        '''

        script = '''


        '''



        return mark_safe(style+html+script)
