function logoutAndRedirect(url, logoutUrl) {
  var xhr = new XMLHttpRequest();
  xhr.open('POST', logoutUrl);
  xhr.setRequestHeader(
    'X-CSRFToken',
    document.getElementsByName('csrfmiddlewaretoken')[0].value
  );
  xhr.onload = function () {
    window.location.href = url;
  };
  xhr.send();
}
