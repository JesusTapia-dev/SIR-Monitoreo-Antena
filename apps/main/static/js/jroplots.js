
var icon = {
    'width': 20,
    'path': 'M18.303,4.742l-1.454-1.455c-0.171-0.171-0.475-0.171-0.646,0l-3.061,3.064H2.019c-0.251,0-0.457,0.205-0.457,0.456v9.578c0,0.251,0.206,0.456,0.457,0.456h13.683c0.252,0,0.457-0.205,0.457-0.456V7.533l2.144-2.146C18.481,5.208,18.483,4.917,18.303,4.742 M15.258,15.929H2.476V7.263h9.754L9.695,9.792c-0.057,0.057-0.101,0.13-0.119,0.212L9.18,11.36h-3.98c-0.251,0-0.457,0.205-0.457,0.456c0,0.253,0.205,0.456,0.457,0.456h4.336c0.023,0,0.899,0.02,1.498-0.127c0.312-0.077,0.55-0.137,0.55-0.137c0.08-0.018,0.155-0.059,0.212-0.118l3.463-3.443V15.929z M11.241,11.156l-1.078,0.267l0.267-1.076l6.097-6.091l0.808,0.808L11.241,11.156z',
    'ascent': 20,
    'descent': 2,
};

function list2dict(values) {

    var o = {};
    $.each(values, function () {
        o[this.name] = this.value;
    });
    return o;
};
/* In this class is defined all the function to RTI plot */
class PcolorBuffer {
    constructor({ div, data }) {
        this.div = document.getElementById(div);
        this.n = 0;         
        this.divs = [];
        this.wait = false;
        this.lastRan = Date.now();
        this.lastFunc = null;
        this.zbuffer = [];
        this.xbuffer = [];
        this.empty = Array(data.metadata.yrange.length).fill(null);
        this.timespan = 12;
        this.metadata = data.metadata;
        this.setup(data);
    }
    /* This function is used to plot all the data that have the DB and just is used when is loaded or reloaded*/
    setup(data) {
        this.last = data.time.slice(-1);
        var diffArr = [];
        for(var i=0; i<data.time.length-1; i++){
            diffArr.push(data.time[i+1]-data.time[i]);
        }
        this.interval = Math.round(Math.min.apply(null, diffArr)*100 / 100);
        if (data.time.length == 1) {
            var values = { 'time': data.time, 'data': data['data'].map(function (x) { return [x] }) };
        } else {
            var values = this.fill_gaps(data.time, data['data'], this.interval, data['data'].length);
        }
        var t = values.time.map(function (x) {
            var a = new Date(x * 1000);
            // This condition is used to change from UTC to LT
            if (data.metadata.localtime == true){
                a.setTime( a.getTime() + a.getTimezoneOffset()*60*1000 );
            }
            return  a;
        });

        var label;
        if (data.metadata.localtime == true){
            label = "[LT]";

        }
        else{
            label = "[UTC]";
        }

        for (var i = 0; i < data['data'].length; i++) {
            var layout = {
                height: 350,
                xaxis: {
                    title: 'Time ' + label,
                    showgrid: false,
                    linewidth: 2,
                    size: 12,
                    mirror: true,
                },
                yaxis: {
                    title: data.metadata.ylabel || 'km',
                    showgrid: false,
                    linewidth: 2,
                    size: 12,
                    mirror: true,
                },
                titlefont: {
                    size: 16,
                },
                margin: {
                    t: 30,
                }
            };
            var iDiv = document.createElement('div');
            iDiv.id = 'plot-' + i;
            //iDiv.className += iDiv.className ? ' col-lg-6 col-md-6 col-sm-12' : 'col-lg-6 col-md-12 col-sm-12';
            this.zbuffer.push([]);
            this.n = this.n + 1;
            this.div.appendChild(iDiv);
            this.divs.push(iDiv.id);
            var trace = {
                z: values.data[i],
                x: t,
                y: data.metadata.yrange,
                colorscale: this.metadata.colormap || 'Jet',
                transpose: true,
                type: 'heatmap'
            };

            if (this.metadata.zmin) { trace.zmin = this.metadata.zmin }
            if (this.metadata.zmax) { trace.zmax = this.metadata.zmax }

            layout.title = 'Ch ' + i + ' - ' + t.slice(-1).toLocaleString();
            var conf = {
                modeBarButtonsToRemove: ['sendDataToCloud', 'autoScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian', 'lasso2d', 'select2d', 'zoomIn2d', 'zoomOut2d', 'toggleSpikelines'],
                modeBarButtonsToAdd: [{
                    name: 'Edit plot',
                    icon: icon,
                    click: function (gd) {
                        var div = gd.id;
                        $('input[id=id_plotdiv]').val(div);
                        $('#setup').modal('show');                        
                    }
                }],
                displaylogo: false,
                showTips: true
            };
            Plotly.newPlot('plot-' + i, [trace], layout, conf);
        }
    }

    getSize() {
        var div = document.getElementById(this.divs[0]);
        var t = this.xbuffer.slice(-1)[0];
        var n = 0;
        var timespan = this.timespan * 1000 * 60 * 60;

        while ((t - div.data[0].x[n]) > timespan) {
            n += 1;
        }
        if(n>720){
            return 720;
        }else{
            return n;
        }
    }

    fill_gaps(xBuffer, zBuffer, interval, N) {

        var x = [xBuffer[0]];
        var z = [];
        var last;

        for (var j = 0; j < N; j++) {
            z.push([zBuffer[j][0]]);
        }

        for (var i = 1; i < xBuffer.length; i++) {
            var cnt = 0;
            last = x[x.length-1];
            while (Math.abs(parseFloat(xBuffer[i]) - last ) > 1.5 * parseFloat(interval)) {
                cnt += 1;
                last = last + interval;
                x.push(last);
                for (var j = 0; j < N; j++) {
                    z[j].push(this.empty);
                }
                // Avoid infinite loop
                if (cnt == 100) { break; }
            }
            x.push(xBuffer[i]);
            for (var j = 0; j < N; j++) {
                z[j].push(zBuffer[j][i]);
            }
        }
        return { 'time': x, 'data': z };
    }

    plot() {
        // add new data to plots and empty buffers
        var N = this.getSize();
        console.log('Plotting...');
        for (var i = 0; i < this.n; i++) {
            var div = document.getElementById(this.divs[i]);
            if (N > 0) {
                div.data[0].z = div.data[0].z.slice(N, )
                div.data[0].x = div.data[0].x.slice(N, )
            }
            Plotly.extendTraces(div, {
                z: [this.zbuffer[i]],
                x: [this.xbuffer]
            }, [0]);
            this.zbuffer[i] = [];
        }
        this.xbuffer = [];
    }
    //This function just add the last data and is used if previously was used setup()
    update(obj) {

        // fill data gaps
        var cnt = 0;

        while (Math.abs(parseFloat(obj.time[0]) - this.last) > 1.5 * parseFloat(this.interval)) {
            cnt += 1;
            this.last += this.interval;
            var newt = new Date((this.last) * 1000);
            // This condition is used to change from UTC to LT
            if (obj.metadata.localtime == true){
                newt.setTime( newt.getTime() + newt.getTimezoneOffset()*60*1000 );
            }
            this.xbuffer.push(newt);
            for (var i = 0; i < obj['data'].length; i++) {
                this.zbuffer[i].push(this.empty);
            }
            // Avoid infinite loop
            if (cnt == 100) { break; }
        }

        // update buffers
        this.last = parseFloat(obj.time[0]);
        var t = new Date(obj.time[0] * 1000);
        // This condition is used to change from UTC to LT
        if (obj.metadata.localtime == true){
            t.setTime( t.getTime() + t.getTimezoneOffset()*60*1000 );
        }
        this.xbuffer.push(t);
        for (var i = 0; i < obj['data'].length; i++) {
            this.zbuffer[i].push(obj['data'][i]);
            var div = document.getElementById(this.divs[i]);
            Plotly.relayout(div, {
                title: 'Ch ' + i + ' - ' + t.toLocaleString(),
            });
        }

        if (!this.wait) {
            this.plot();
            this.wait = true;
        } else {
            clearTimeout(this.lastFunc)
            this.lastFunc = setTimeout(function (scope) {
                if ((Date.now() - scope.lastRan) >= 30000) {
                    scope.plot()
                    scope.lastRan = Date.now()
                }
            }, 30000 - (Date.now() - this.lastRan), this)
        }
    }
    // With this function You can change parameters in your plot
    restyle(values) {

        var values = list2dict(values);
        var div = document.getElementById(values.plotdiv);

        Plotly.relayout(div, {
            yaxis: {
                range: [values.ymin, values.ymax],
                title: this.metadata.ylabel || 'km',
                linewidth: 2,
                size: 12,
                mirror: true,
            }

        });

        Plotly.restyle(div, {
            zmin: values.zmin,
            zmax: values.zmax,
            colorscale: values.colormap
        });
    }
}
/* In this class is defined all the function to SPC plot */
class Pcolor {
    constructor({ div, data }) {
        this.div = document.getElementById(div);
        this.n = 0;
        this.divs = [];
        this.metadata = data.metadata;
        this.setup(data);
    }
    /* This function is used to plot all the data that have the DB and just is used when is loaded or reloaded*/
    setup(data) {
        for (var i = 0; i < data['data'].length; i++) {
            var layout = {
                margin: {
                    t:30,
                },
                height: 320,
                xaxis: {
                    title: data.metadata.xlabel || 'Velocity',
                    showgrid: false,
                    zeroline: false,
                    linewidth: 2,
                    mirror: true,
                    size: 12,
                },
                yaxis: {
                    title: data.metadata.ylabel || 'km',
                    showgrid: false,
                    linewidth: 2,
                    mirror: 'all',
                    size: 12,
                },
                titlefont: {
                    size: 14
                },
            };
            var iDiv = document.createElement('div');
            iDiv.id = 'plot-' + i;
            iDiv.className += iDiv.className ? ' col-md-5' : 'col-md-5';
            this.n = this.n + 1;
            this.div.appendChild(iDiv);
            this.divs.push(iDiv.id);
            var iDiv = document.createElement('div');
            iDiv.className = 'col-md-1';
            this.div.appendChild(iDiv);
            var trace1 = {
                z: data['data'][i],
                y: data.metadata.yrange,
                x: data.metadata.xrange,
                colorscale: this.metadata.colormap || 'Jet',
                transpose: true,
                type: 'heatmap'
            };
            
            if (this.metadata.zmin) {
                trace1.zmin = this.metadata.zmin
            }
            if (this.metadata.zmax) {
                trace1.zmax = this.metadata.zmax;
            }

            var t = new Date(data.time * 1000);
            if (data.metadata.localtime == true){
                t.setTime( t.getTime() + t.getTimezoneOffset()*60*1000 );
            }
            if ('titles' in data.metadata){
                layout.title = data.metadata.titles[i] + ' ' + t.toLocaleString();
            }else{
                layout.title = 'Ch ' + i + ': ' + t.toLocaleString();
            }
            var conf = {
                modeBarButtonsToRemove: ['sendDataToCloud', 'autoScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian', 'lasso2d', 'select2d', 'zoomIn2d', 'zoomOut2d', 'toggleSpikelines'],
                modeBarButtonsToAdd: [{
                    name: 'Edit plot',
                    icon: icon,
                    click: function (gd) {
                        var div = gd.id;
                        $('input[id=id_plotdiv]').val(div);
                        $('#setup').modal('show');                        
                    }
                }],
                displaylogo: false,
                showTips: true
            };
            
            var traces = [trace1]
            
            Plotly.newPlot('plot-' + i, traces, layout, conf);
        }
    }

    plot(obj) {
        this.data = obj;
        // add new data to plots and empty buffers
        console.log('Plotting...');
        var t = new Date(obj.time[0] * 1000);
        // This condition is used to change from UTC to LT
        if (obj.metadata.localtime == true){
            t.setTime( t.getTime() + t.getTimezoneOffset()*60*1000 );
        }
        for (var i = 0; i < this.n; i++) {
            var div = document.getElementById(this.divs[i]);
            
            if ('titles' in obj.metadata){
                var title = obj.metadata.titles[i] + ' ' + t.toLocaleString();
            }else{
                var title = 'Ch ' + i + ': ' + t.toLocaleString();
            }

            Plotly.relayout(div, {
                title: title,
            });

            Plotly.restyle(div, {
                z: [obj['data'][i]],
                x: [obj.xrange]
            }, [0]);
        }
    }
    
    update(data) {
        this.plot(data);
    }
    
    restyle(values) {
        
        var values = list2dict(values);
        var div = document.getElementById(values.plotdiv);

        Plotly.relayout(div, {
            yaxis: {
                title: this.metadata.ylabel || 'km',
                linewidth: 2,
                range: [values.ymin, values.ymax]
            },
            xaxis: {
                title: this.metadata.xlabel || 'Velocity',
                linewidth: 2,
                mirror: true,
                range: [values.xmin, values.xmax]
            }
        });
        
        Plotly.restyle(div, {
            zmin: values.zmin,
            zmax: values.zmax,
            colorscale: values.colormap
        });
    }
}

class ScatterBuffer {
    constructor({ div, data }) {
        this.div = document.getElementById(div);
        this.n = 0;
        this.wait = false;
        this.lastRan = Date.now();
        this.lastFunc = null;
        this.ybuffer = [];
        this.xbuffer = [];
        this.timespan = 12;
        this.metadata = data.metadata;
        this.setup(data);
    }
    /* This function is used to plot all the data that have the DB and just is used when is loaded or reloaded*/
    setup(data) {

        var traces = [];
        this.last = data.time.slice(-1);
        var diffArr = [];
        for(var i=0; i<data.time.length-1; i++){
            diffArr.push(data.time[i+1]-data.time[i]);
        }
        this.interval = Math.round(Math.min.apply(null, diffArr)*100 / 100);
        
        if (data.time.length == 1) {
            var values = { 'time': data.time, 'data': data['data'] };
        } else {
            var values = this.fill_gaps(data.time, data['data'], this.interval, data['data'].length);
        }

        var t = values.time.map(function (x) {
            var a = new Date(x * 1000);
            // This condition is used to change from UTC to LT
            if (data.metadata.localtime == true){
                a.setTime( a.getTime() + a.getTimezoneOffset()*60*1000 );
            }
            return  a;
        });

        for (var i = 0; i < data['data'].length; i++) {

            this.n = this.n + 1;
            this.ybuffer.push([]);
            var trace = {
                x: t,
                y: values.data[i],
                mode: 'lines',
                type: 'scatter',
                name: 'Channel ' + i,
                connectgaps: false,
            };

            traces.push(trace);
        }

        var label;
        if (data.metadata.localtime == true){
            label = "[LT]";

        }
        else{
            label = "[UTC]";
        }

        var layout = {
            height: 300,
            title: t.slice(-1).toLocaleString(),
            font: {
                size: 12,
              },
            xaxis: {
                title: 'Time ' + label,
                size: 12,
                linewidth: 2,
                mirror: true,
            },
            yaxis: {
                title: data.metadata.ylabel || 'dB',
                linewidth: 2,
                mirror: true,
            },
            titlefont: {
                size: 16,
            },
            margin: {
                t: 30,
            }
        };

        if (data.metadata.ymin) { layout.yaxis.range = [data.metadata.ymin, data.metadata.ymax] }

        var conf = {
            modeBarButtonsToRemove: ['sendDataToCloud', 'autoScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian', 'lasso2d', 'select2d', 'zoomIn2d', 'zoomOut2d', 'toggleSpikelines'],
            modeBarButtonsToAdd: [{
                name: 'Edit plot',
                icon: icon,
                click: function (gd) {
                    $('#setup').modal('show');
                }
            }],
            displaylogo: false,
            showTips: true
        };
        Plotly.newPlot('plot', traces, layout, conf);
    }

    getSize() {
        var t = this.xbuffer.slice(-1)[0];
        var n = 0;
        var timespan = this.timespan * 1000 * 60 * 60;

        while ((t - this.div.data[0].x[n]) > timespan) {
            n += 1;
        }
        if(n>720){
            return 720;
        }else{
            return n;
        }
    }

    fill_gaps(xBuffer, yBuffer, interval, N) {

        var x = [xBuffer[0]];
        var y = [];

        for (var j = 0; j < N; j++) {
            y.push([yBuffer[j][0]]);
        }

        var last;

        for (var i = 1; i < xBuffer.length; i++) {
            var cnt = 0;
            last = x.slice(-1)[0];
            while (Math.abs(parseFloat(xBuffer[i]) - last) > 1.5 * parseFloat(interval)) {
                cnt += 1;
                last = last + interval;
                x.push(last);
                for (var j = 0; j < N; j++) {
                    y[j].push(null);
                }
                // Avoid infinite loop
                if (cnt == 50) { break; }
            }
            x.push(xBuffer[i]);

            for (var j = 0; j < N; j++) {
                y[j].push(yBuffer[j][i]);
            }
        }
        return { 'time': x, 'data': y };
    }

    plot() {
        // add new data to plots and empty buffers
        var xvalues = [];
        var yvalues = [];
        var traces = [];
        var N = this.getSize();
        console.log('Plotting...');
        for (var i = 0; i < this.n; i++) {
            if (N > 0) {
                this.div.data[i].y = this.div.data[i].y.slice(N, )
                this.div.data[i].x = this.div.data[i].x.slice(N, )
            }
            yvalues.push(this.ybuffer[i]);
            xvalues.push(this.xbuffer);
            traces.push(i);
            this.ybuffer[i] = [];
        }
        Plotly.extendTraces(this.div, {
            y: yvalues,
            x: xvalues
        }, traces);
        this.xbuffer = [];
    }
    //This function just add the last data and is used if previously was used setup()
    update(obj) {
        // fill data gaps
        var cnt = 0;
        while (Math.abs(parseFloat(obj.time[0]) - this.last ) > 1.5 * parseFloat(this.interval)) {
            cnt += 1;
            this.last += this.interval;
            var newt = new Date((this.last) * 1000);
            // This condition is used to change from UTC to LT
            if (obj.metadata.localtime == true){
                newt.setTime( newt.getTime() + newt.getTimezoneOffset()*60*1000 );
            }
            this.xbuffer.push(newt);
            for (var i = 0; i < this.n; i++) {
                this.ybuffer[i].push(null);
            }
            // Avoid infinite loop
            if (cnt == 100) { break; }
        }

        // update buffers
        this.last = parseFloat(obj.time[0]);
        var t = new Date(obj.time[0] * 1000);
        // This condition is used to change from UTC to LT
        if (obj.metadata.localtime == true){
            t.setTime( t.getTime() + t.getTimezoneOffset()*60*1000 );
        }
        this.xbuffer.push(t);
        for (var i = 0; i < this.n; i++) {
            this.ybuffer[i].push(obj['data'][i][0]);
        }
        
        Plotly.relayout(this.div, {
            title: t.toLocaleString(),
        });

        if (!this.wait) {
            this.plot();
            this.wait = true;
        } else {
            clearTimeout(this.lastFunc)
            this.lastFunc = setTimeout(function (scope) {
                if ((Date.now() - scope.lastRan) >= 30000) {
                    scope.plot()
                    scope.lastRan = Date.now()
                }
            }, 30000 - (Date.now() - this.lastRan), this)
        }
    }

    restyle(values) {

        var values = list2dict(values);
        Plotly.relayout(this.div, {
            yaxis: {
                range: [values.ymin, values.ymax],
                title: this.metadata.ylabel || 'dB'
            }

        });
    }
}
