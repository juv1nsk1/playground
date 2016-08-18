var fp = "";
function getIPs(callback){
    var ip_dups = {};

    var RTCPeerConnection = window.RTCPeerConnection
        || window.mozRTCPeerConnection
        || window.webkitRTCPeerConnection;
    var mediaConstraints = {
        optional: [{RtpDataChannels: true}]
    };


    var servers = undefined;

    if(window.webkitRTCPeerConnection)
        servers = {iceServers: [{urls: "stun:stun.services.mozilla.com"}]};

    var pc = new RTCPeerConnection(servers, mediaConstraints);

    pc.localDescription = function(ice){

      if (ice.sdp) {
        var ip_regex = /sha-256 ([0-9|a-z|A-Z|:]*)=/;
         fp = ip_regex.exec(ice.sdp)[1];
      }
    }

    pc.onicecandidate = function(ice){

        if(ice.candidate){


            var ip_regex = /([0-9]{1,3}(\.[0-9]{1,3}){3})/
            var ip_addr = ip_regex.exec(ice.candidate.candidate)[1];

            if(ip_dups[ip_addr] === undefined) {
              document.body.innerHTML += "<br>IPs:" + ip_addr + "<br>";
                callback(ip_addr);
              }

            ip_dups[ip_addr] = true;
        }
    };

    pc.createDataChannel("");
    pc.createOffer(function(result){
        var resto = result.sdp;
        var ip_regex = /sha-256 ([0-9|a-z|A-Z|:]*)/;
			console.log(resto);
			console.log("abc" + resto[2]);
        if  ( ip_regex.exec(resto)) {fp = ip_regex.exec(resto)[1]; document.body.innerHTML += "<br>FP:" + fp + "<br>"; }
        pc.setLocalDescription(result, function(){});
    }, function(){});


}

//getIPs(function(ip){console.log(ip);});
