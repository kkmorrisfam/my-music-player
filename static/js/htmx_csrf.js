// set global CSRF token for button requests
// only for same-origin requests during htmx:configRequest
(function () {
  function getCookie(name) {
    const m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return m ? m.pop() : '';
  }

  // gets request after parameters are collected and before it's sent (in-between)
  document.body.addEventListener('htmx:configRequest', function (e) {
    // Only send CSRF to my domain
    // where is the request going?
    const url = new URL(e.detail.path, window.location.href);
    // if url is from us/same site
    if (url.origin === window.location.origin) {
      //get cookie with csrf token to add to header
      e.detail.headers['X-CSRFToken'] = getCookie('csrftoken');
    }
  });
})();

