
    function freq2Binary(mclock, frequency) {
    	
    	var freq_bin = parseInt(frequency * (Math.pow(2,48)/mclock));
    	return freq_bin;
    	
    }
   
    function binary2Freq(mclock, binary) {
    	
    	var frequency = (1.0*binary) / (Math.pow(2,48)/mclock);
    	return frequency;
    }