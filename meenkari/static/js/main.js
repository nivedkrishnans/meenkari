function generate_live_url(){
  var prefix = (window.location.protocol == 'https:') ? 'wss://' : 'ws://';
  var live_url = prefix + window.location.host + '/ws' + window.location.pathname;
  return live_url
}
