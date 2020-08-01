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
