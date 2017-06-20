function onClick() {
  var char1 = document.getElementById('Character1');
  var char2 = document.getElementById('Character2');
  var char3 = document.getElementById('Character3');

  url = api_base_url + char1.value + char2.value + char3.value

  xmlHttpRequest = new XMLHttpRequest();
  xmlHttpRequest.open('get', url);
}
