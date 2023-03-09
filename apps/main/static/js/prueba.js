$(document).ready(function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on('connect', function(data) {
      console.log('Connecting... OK');
      makePlot("plot-temp",2,["T1","T2"],[14, 45])
      makePlot("plot-pot",2,["T1","T2"],[70,100])
      makePlot("plot-pot-t1",4,["P1","P2","P3","P4"],[0,26])
      makePlot("plot-pot-t2",4,["P1","P2","P3","P4"],[0,26])
      $("#temp-info-1").hide();
      $("#temp-info-2").hide();
    })

    socket.on('test', function(data) {
      let total = data.pow.reduce((a, b) => a + b, 0);
      var id = (data.num/4)>>0;
      streamPlot("plot-pot",data.time,total/1000.0,id,81);
      streamPlot("plot-temp",data.time,data.tmax[0],id,40);
      if(id == 0){
        streamPlot2("plot-pot-t1",data.time,data.pow);
        ligthStatus('status1','status-text1',data.status);
        PotenciaAmplificador(['#pot1-1','#pot1-2','#pot1-3','#pot1-4'],data.pow);
        $('#temp-1').text(data.tmax[0]);
        if(eval(data.tmax[0])>30){
          $("#temp-info-1").show();
          $("#temp-info-1").text("TX"+(id+1)+" - Amplificador " + data.tmax[1]);
        }
        else{$("#status-temp").hide();}
      }
      else if(id == 1){
        streamPlot2("plot-pot-t2",data.time,data.pow);
        ligthStatus('status2','status-text2',data.status);
        PotenciaAmplificador(['#pot2-1','#pot2-2','#pot2-3','#pot2-4'],data.pow);
        $('#temp-2').text(data.tmax[0]);
        if(eval(data.tmax[0])>30){
          $("#temp-info-2").show();
          $("#temp-info-2").text("TX"+(id+1)+" - Amplificador " + data.tmax[1]);
        }
        else{$("#status-temp").hide();}
      }
    })
    $('form#controlON').submit(function(event) {
      socket.emit('control_event', {data: 1});
      return false;
    });
    $('form#controlOFF').submit(function(event) {
      socket.emit('control_event', {data: 0});
      return false;
    });
    $('#plot1').on('show.bs.modal', function(){
      PotenciaAmplificador(['pot1-1','pot1-2','pot1-3','pot1-4']);
    });
    $('#plot1').on('show.bs.modal', function(){
      PotenciaAmplificador(['pot2-1','pot2-2','pot2-3','pot2-4']);
    });
  });

  function makePlot(div, n=1, names=["", ""],ranges){
    var plotDiv = document.getElementById(div);
    var traces = [];
    for (let i = 0; i < n; i++) {
      traces.push({x: [], y: [],mode: 'lines', name: names[i]});
    }
    traces.push({x: [], y: [],mode: 'lines',line: {color:'rgb(219, 64, 82)',dash: 'dot',width: 2},name:"nominal",showlegend: false});
    var yrange = ranges;
    var layout = {
      autosize: true,
      font: {size: 12},
      margin: { t: 10, b:50 },
      xaxis: {
        type: 'date'
      },
      yaxis: {
        range: yrange,
      },
    };

      Plotly.plot(plotDiv, traces, layout);
  };

  function streamPlot(div,x,y,ind,val){
    var plotDiv = document.getElementById(div);
    if (plotDiv.data[ind].x.length > 8){
      plotDiv.data[2].x = plotDiv.data[2].x.slice(-23)
      plotDiv.data[2].y = plotDiv.data[2].y.slice(-23)
      plotDiv.data[ind].x = plotDiv.data[ind].x.slice(-11)
      plotDiv.data[ind].y = plotDiv.data[ind].y.slice(-11)
    }
    var tm = [x];
    var values = [y];
    var data_update = {x: [tm,tm], y: [values,[val]]}
    Plotly.extendTraces(plotDiv, data_update,[ind,2])
  };
  function streamPlot2(div,x,y){
    var plotDiv = document.getElementById(div);
    if (plotDiv.data[0].x.length > 8){
      for(let i=0;i<4;i++){
        plotDiv.data[i].x = plotDiv.data[i].x.slice(-11)
        plotDiv.data[i].y = plotDiv.data[i].y.slice(-11)
      }
    }
    var tm = [x];
    var values = [];
    for(let i=0;i<4;i++){
      values[i]=[y[i]/1000.0];
    }    
    var data_update = {x: [tm,tm,tm,tm], y: values}
    Plotly.extendTraces(plotDiv, data_update,[0,1,2,3])
  };
  function ligthStatus(div1,div2,status){
    if(status==='0000'){
      document.getElementById(div1).style.backgroundColor = "red";
      document.getElementById(div2).innerHTML = "Desabilitado";
    }
    else if(status==='1111'){
      document.getElementById(div1).style.backgroundColor = "green";
      document.getElementById(div2).innerHTML = "Habilitado";
    }
    else{
      document.getElementById(div1).style.backgroundColor = "yellow";
      document.getElementById(div2).innerHTML = "Incompleto";
    }
  }
  function PotenciaAmplificador(div,data){
    for(let i=0; i<4; i++){
      $(div[i]).text(data[i]/1000.0);
    }
  }