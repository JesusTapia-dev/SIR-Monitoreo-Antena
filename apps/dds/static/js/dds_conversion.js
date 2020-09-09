function freq2Binary(mclock, frequency) {
    	
    var freq_bin = parseInt(frequency * (Math.pow(2,48)/mclock));
    return freq_bin;
    
}

function binary2Freq(mclock, binary) {
    
    var frequency = (1.0*binary) / (Math.pow(2,48)/mclock);
    return frequency;
}


function binary2FreqDelta(mclock, binary) {
    
    var frequency = (1.0*binary) / (Math.pow(2,48)/mclock);
    return frequency;
}    

function freqDelta2Binary(mclock, frequency) {
    
    var freq_bin = parseInt(frequency * (Math.pow(2,48)/mclock));
    return freq_bin;
}    

function binary2Ramp(mclock, binary) {
    
    var frequency = (1.0*mclock) / (binary+1);
    return frequency;
}    

function freqRamp2Binary(mclock, frequency) {
    
    var freq_bin = parseInt(mclock/frequency-1);
    return freq_bin;
}    

function us2Ramp(step_us) {
    //periodo_delpaso = sysclockperiod x (N+1)
    // freqsys/(N+1)=freq_ddelpaso=1/step
    var freq = (1.0/(step_us));
    return freq;
}       