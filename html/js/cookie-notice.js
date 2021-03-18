function setCookie(name, value, options = {}) {

  options = {
    path: '/',
    // при необходимости добавьте другие значения по умолчанию
    ...options
  };

  if (options.expires instanceof Date) {
    options.expires = options.expires.toUTCString();
  }

  let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);

  for (let optionKey in options) {
    updatedCookie += "; " + optionKey;
    let optionValue = options[optionKey];
    if (optionValue !== true) {
      updatedCookie += "=" + optionValue;
    }
  }

  document.cookie = updatedCookie;
}

function сloseCookieNotice() {
//   document.cookie = "cookie_notice=off; expires=15/02/2011 00:00:00;path=/; samesite=lax";
  setCookie("cookie_notice", "off", {"samesite": "lax"})
  document.getElementById("cookie-notice").remove();
}

function getCookie(name) {
  var matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

var cookie_notice = getCookie("cookie_notice");
if(cookie_notice != 'off')
{
	document.write('<div id="cookie-notice" role="banner" class="cookie-revoke-hidden cn-position-bottom cn-effect-none cookie-notice-visible" aria-label="Cookie Notice" style="background-color: rgba(0,0,0,0.8);">	<div class="cookie-notice-container" style="color: #fff;"><span id="cn-notice-text" class="cn-text-container">Мы cохраняем файлы cookie: это помогает сайту работать лучше. Если Вы продолжите использовать сайт, мы будем считать, что Вас это устраивает.</span>	<button onclick="сloseCookieNotice();"; class="btn btn-primary" style="background-color: unset;border:1px solid orange;">ОК!</button>	</div></div>');
}

