$(document).ready(function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on('connect', function(data) {
        console.log('Connecting OK');
        makePlot("plot-temp",2,["Tx1","Tx2"],[14, 45])
        makePlot("plot-pot",2,["Tx1","Tx2"],[70,100])
        makePlot("plot-pot-t1",4,["P1","P2","P3","P4"],[0,25])
        makePlot("plot-pot-t2",4,["P1","P2","P3","P4"],[0,25])
    })

    socket.on('test', function(data) {
        UpdateData(data.num,data);
    })
    $('#ONBtn1').click(function() {
      console.log("holaa")
      socket.emit('atrad_control_event', '11');
    });
    $('#ONBtn2').click(function(){
      console.log("holaa2")
      socket.emit('atrad_control_event', '21');
    });
    $('#OFFBtn1').click(function() {
      socket.emit('atrad_control_event','10');
    });
    $('#OFFBtn2').click(function(){
      socket.emit('atrad_control_event', '20');
    });
});

function UpdateData(id,data){
    let total = data.pow.reduce((a, b) => a + b, 0)/1000.0;
    streamPlot("plot-pot",data.time,total,id,81);
    streamPlot("plot-temp",data.time,data.tmax[0],id,40);
    streamPlot2("plot-pot-t"+(id+1),data.time,data.pow);
    ligthStatus(id,data.status);
    PotenciaAmplificador(id,data.pow,total,data.time);
    $('#temp'+(id+1)).text(data.tmax[0]);
    if(eval(data.tmax[0])>20){
        $('#alerttemp-time'+(id+1)).text(data.time.slice(-8,));
        $('#alerttemp-'+(id+1)).text(data.tmax[0]);
        $('#alerttemp-loc'+(id+1)).text('Tx'+(id+1)+' '+data.tmax[1]);
    }
}

function makePlot(div, n=1, names=["", ""],ranges){
    var plotDiv = document.getElementById(div);
    var traces = [];
    for (let i = 0; i < n; i++) {
        traces.push({x: [], y: [],mode: 'lines', name: names[i]});
    }
    traces.push({x: [], y: [],mode: 'lines',line: {color:'rgb(219, 64, 82)',dash: 'dot',width: 2},name:"nominal",showlegend: false});
    var yrange = ranges;
    var layout = {
        width: 700,
        height: 350,
        font: {size: 12},
        margin: { t: 10, b:40,},
        xaxis: {
        type: 'date'
        },
        yaxis: {
        range: yrange,
        },
    };
    var config = {responsive: true}
    Plotly.newPlot(plotDiv, traces, layout,config);
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

function ligthStatus(id,status){
    let div1 = 'status'+(id+1);
    let div2 = 'status-text'+(id+1);

    if(status==='0000'){
        document.getElementById(div1).style.backgroundColor = "red";
        document.getElementById(div2).innerHTML = "Disable";
    }
    else if(status==='1111'){
        document.getElementById(div1).style.backgroundColor = "green";
        document.getElementById(div2).innerHTML = "Fully enable";
    }
    else{
        document.getElementById(div1).style.backgroundColor = "yellow";
        document.getElementById(div2).innerHTML = "Not fully enable";
    }
};

function PotenciaAmplificador(id,data1,data2,time){
    id_tx = (id+1)
    let div = '#pot'+id_tx;
    for(let i=1; i<5; i++){
        var pot = (data1[i-1]/1000.0).toFixed(1)
        $(div+'-'+i).text(pot);
        if (data1[i-1]<23000){
            $("#alertpot-time"+id_tx).text(time.slice(-8,));
            $("#alertpot-"+id_tx).text(pot);
            $("#alertpot-loc"+id_tx).text('Tx'+ id_tx+ ' Amp '+i);
        }
    }
    $(div).text(data2.toFixed(1));
}
$(".clickable-row").click(function() {
    window.open($(this).data("href"),);
});