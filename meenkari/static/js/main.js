function generate_live_url(){
    //this function generates the url for websockets defined in routers.py
  var prefix = (window.location.protocol == 'https:') ? 'wss://' : 'ws://';
  var live_url = prefix + window.location.host + '/ws' + window.location.pathname;
  return live_url
}

function lobby_finalized(){
        //this function informs the non-host players in the lobby that the players have been chosen and reloads the page
    var countdown = 10;
    document.getElementById("host_response").innerHTML="The host has chosen the players. Reload the page to know if you are a part of the team. Page will reload automatically in: ";
    setInterval(function(){
        document.getElementById("host_response_countdown").innerHTML= countdown.toString() + " sec";
        countdown--;
    },1000);
    setTimeout(function(){location.reload();},10000);
}

function time_sec(seconds){
    // takes the number of seconds and display in MM:SS format
    seconds = Math.round(seconds);
    var sec = seconds%60;
    var min = Math.floor(seconds/60);
    //console.log(seconds,sec,min);
    var str = (Math.floor(min/10)).toString() + (min%10).toString() + ":" + (Math.floor(sec/10)).toString() + (sec%10).toString();
    return str;
}