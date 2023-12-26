$(document).ready(function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on('connect', function(data) {
        console.log('Connecting OK');
        makePlot("plot-pot",2,["Tx1","Tx2"],[100,6000])
        makePlot("plot-pot-t1",1,["P1"],[100,1000])
        makePlot("plot-pot-t2",1,["P2"],[100,1000])
        makePlot("plot-pot-t3",1,["P3"], [100,1000])
        makePlot("plot-pot-t4",1,["P4"],[100,1000])
        makePlot("plot-pot-t5",1,["P5"],[100,1000])
        makePlot("plot-pot-t6",1,["P6"],[100,1000])
        makePlot("plot-pot-t7",1,["P7"],[100,1000])
        makePlot("plot-pot-t8",1,["P8"],[100,1000])
    })

    socket.on('test', function(data) {
        UpdateData(data);
    })
    $('#ONBtn1').click(function() {
      socket.emit('atrad_control_event', '11');
    });
    $('#ONBtn2').click(function(){
      socket.emit('atrad_control_event', '21');
    });
    $('#OFFBtn1').click(function() {
      socket.emit('atrad_control_event','10');
    });
    $('#OFFBtn2').click(function(){
      socket.emit('atrad_control_event', '20');
    });
});

function UpdateData(data){
    let total = data.pow.reduce((a, b) => a + b, 0);
    streamPlot("plot-pot",data.time,total);
    streamPlot2("plot-pot-t",data.time,data.pow);
    ligthStatus(data.status);
    console.log("actualizar");
    PotenciaAmplificador(data.pow,total,data.potenciaNominal,data.time);
    console.log("actualizado");
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
        height: 300,
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

function streamPlot(div,x,y){
    var plotDiv = document.getElementById(div);
    var tm = [x];
    var values = [y];
    var time=new Date();
    var data_update = {x: [[time]], y: [[y]]}
    Plotly.extendTraces(plotDiv, data_update,[0])
};
function streamPlot2(div,x,y){
    for(var i=1;i<9;i++){
        var division=div+i
        var plotDiv = document.getElementById(division);
        var time = new Date();
        var values = y[i-1];
        var data_update = {x: [[time]], y: [[values]]};
        Plotly.extendTraces(plotDiv, data_update,[0])
    }
};

function ligthStatus(status){
    for(var i=0;i<8;i++){
        if(status[i]==1){
            let div1 = 'status'+(i+1);
            let div2 = 'status-text'+(i+1);
            document.getElementById(div1).style.backgroundColor = "green";
            document.getElementById(div2).innerHTML = "Fully enable";
        }
        else {
            let div1 = 'status'+(i+1);
            let div2 = 'status-text'+(i+1);
            document.getElementById(div1).style.backgroundColor = "red";
            document.getElementById(div2).innerHTML = "Disable";
        }
    }
};

function PotenciaAmplificador(data1,data2,dataNominal,time){
    let div = '#pot1';
    console.log("potNominal");
    for(let i=1; i<9; i++){
        var pot = (data1[i-1]).toFixed(1);
        var potNominal=(dataNominal[i-1]).toFixed(1);
        var maxPot=potNominal+150,minPot=potNominal-150;
        if(pot>maxPot || pot<minPot){
            $(div+'-'+i).text(pot);
            $("#alertpot-time"+i).text(time.slice(-8,));
            $("#alertpot-"+i).text(pot+" kW");   
            console.log("potNominal");
        }
        else{
            $("#alertpot-time"+i).text(time.slice(-8,));
            $("#alertpot-"+i).text("Valor dentro de rango");   
            console.log("else");
        }
    }
    $(div).text(data2.toFixed(1));
}
$(".clickable-row").click(function() {
    window.open($(this).data("href"),);
});