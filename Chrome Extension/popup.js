var cur_url = '';
var resp = '';
var urls = ["maila.com", "mailb.com", "mailc.com", "maild.com", "maile.com", "mailf.com"];
var svk_global = "";
var lang = "";


function sleep(delay) {
    var start = new Date().getTime();
    while (new Date().getTime() < start + delay);
}

function alert_wrong_url() {
  chrome.tabs.executeScript({
    file: 'alert_wrong_url.js'
  });
}

function alert_password() {
  chrome.tabs.executeScript({
    file: 'alert_password.js'
  });
}

function alert_user_not_found() {
  chrome.tabs.executeScript({
    file: 'alert_user_not_found.js'
  });
}


function validate_password(password) {
	var errors = [];
	var special_regex = /[ !@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/g;

	if (password.length < 8) {
  	errors.push("Your password must be at least 8 characters");
  }
  if (password.search(/[a-z]/) < 0) {
		errors.push("Your password must contain at least one lowercase.");
  }
	if (password.search(/[A-Z]/) < 0) {
		errors.push("Your password must contain at least one uppercase.");
  }
  if (password.search(/[0-9]/) < 0) {
		errors.push("Your password must contain at least one digit.");
  }
	if (password.search(special_regex) < 0) {
		errors.push("Your password must contain at least one special character");
	}

  return errors;
}


var fetch_current_url = chrome.tabs.query({
    active: true,
    currentWindow: true
  },
  function (tab) {
    cur_url = tab[0].url;
  });


function openInSameTab(url) {
  chrome.tabs.update({ url: url });
}


function url_with_userpath(link) {
	var str = link.substring(0, link.lastIndexOf("/"));
	return str.concat(lang);
}


function url_of(link) {
	var obj = new URL(link);
	var url = obj.hostname;
	if (obj.port) {
		return url.concat(":").concat(obj.port).concat(lang);
	}
	return url.concat(lang);
}

function pure_url_of(link) {
	var obj = new URL(link);
	var url = obj.hostname;
	if (obj.port) {
		return url.concat(":").concat(obj.port);
	}
	return url;
}

function construct_url(cur_url, path) {
	var pathname = pure_url_of(cur_url);
	return "http://".concat(pathname).concat(path);
}


function get_auth_result(url, username, resp) {
  console.log("saddasdasd");
	$.ajax({
    type:"POST",
    url: url,
    data:"username="+username+"&K="+resp ,
    success: function(data){
			if (data === "True") {
				var success_page = url_with_userpath(url).concat("/login_success")
				openInSameTab(success_page);
			}
			else {
				var fail_page = url_with_userpath(url).concat("/login_fail")
				openInSameTab(fail_page);
			}
    }
	});


	return "False";
}

function get_reg_result(url, username, svk) {
	$.ajax({
    type:"POST",
    url: url,
    data:"username="+username+"&K="+svk ,
    success: function(data){
			if (data === "True") {
				var success_page = url_with_userpath(url).concat("/register_success")
				openInSameTab(success_page);

			}
			else {
				var fail_page = url_with_userpath(url).concat("/register_fail")
				openInSameTab(fail_page);
			}
    }
	});


	return "False";
}

function typeOf(obj) {
  return {}.toString.call(obj).split(' ')[1].slice(0, -1).toLowerCase();
}

function get_chal(url, username) {
  var chal = "";
  $.ajax({
    type:"POST",
    async: false,
    url: url,
    data:"username=" + username,
    success: function(data){
      chal = data;
    }
  });
  return chal;
}

function get_bsk(id) {
  storage = localStorage.getItem(id);
  console.log("items: " + JSON.stringify(storage));

  items = JSON.parse(storage);
  if (!items) {
    alert_user_not_found();
    console.log("items bos geldi?????");
    return "";
  }
  var bsk = items["exported_bsk"];
  return import_key(bsk);
}

function get_ctext(id) {
  storage = localStorage.getItem(id);
  items = JSON.parse(storage);
  if (!items) {
    return "";
  }
  var ctext = items["ctext"];
  return ctext;
}

function base64encode(text) {
  return btoa(text);
}

function base64decode(text) {
  return atob(text);
}

function export_to_server(key) {
  var pem_formatted_key = KEYUTIL.getPEM(key);
  var trimmed_key = pem_formatted_key.replace(/(\r\n\t|\n|\r\t)/gm,"");
  parts = trimmed_key.trim().split("-----");
  part = parts[2];

  console.log(part);
  return export_public_key(key);

}

function export_public_key(key) {
  var pem_formatted_key = KEYUTIL.getPEM(key);
  var exportable_key = base64encode(pem_formatted_key);
  return exportable_key;
}

function export_private_key(key) {
  var pem_formatted_key = KEYUTIL.getPEM(key, "PKCS1PRV");
  var exportable_key = base64encode(pem_formatted_key);
  return exportable_key;
}

function import_key(exported_key) {
  var key = base64decode(exported_key);
  var ssk = KEYUTIL.getKey(key);
  return ssk;
}

function sha_256(text) {
  var digester = new KJUR.crypto.MessageDigest({alg: "sha256", prov: "cryptojs"});
  digester.updateString(text);
  return digester.digest()
}

function encrypt(key, plaintext) {
  var encrypted = CryptoJS.AES.encrypt(plaintext, key);
  console.log("Encrypted: " + encrypted);
  return encrypted.toString();
}

function decrypt(key, ctext, fail_page) {
  var decrypted = CryptoJS.AES.decrypt(ctext, key);
  console.log("Decrypted: " + decrypted);
  try {
    var result = decrypted.toString(CryptoJS.enc.Utf8);
  }
  catch {
    openInSameTab(fail_page);
  }
  return decrypted.toString(CryptoJS.enc.Utf8);
}

function sign(ssk, chal) {
  var sig = new KJUR.crypto.Signature({"alg": "SHA256withRSA"});
  sig.init(ssk);
  sig.updateString(chal);
  var hSigVal = sig.sign();
  return hSigVal;
}

function verify(svk, resp, chal) {
  var sig2 = new KJUR.crypto.Signature({"alg": "SHA256withRSA"});
  sig2.init(svk);
  sig2.updateString(chal);
  var isValid = sig2.verify(resp);
  return isValid;
}

function blind_sign(bsk, chal) {
  return sign(bsk, chal);
}

function generate_sign_keys() {
  var keys = KEYUTIL.generateKeypair("RSA", 1024);

  var prvKey = keys.prvKeyObj;
  var pubKey = keys.pubKeyObj;
  console.log(base64decode(export_private_key(prvKey)));
  console.log(base64decode(export_public_key(pubKey)));

  return [prvKey, pubKey, prvKey];
}


function add_new_creds(id, bsk, ctext) {
  var exported_bsk = export_private_key(bsk);
  var str = JSON.stringify({exported_bsk, ctext});
  localStorage[id] = str;
}


function auth(username, password, url) {
	var auth_url = url.concat("/auth");
  var chal_url = "http://" + pure_url_of(url).concat("/chal");

  var chal = get_chal(chal_url, username);
  console.log("chal: " + chal);

  var concat = username + url;
  var id = sha_256(concat);
  console.log("id: " + id);
  var bsk = get_bsk(id);
  console.log("bsk: " + bsk);
  var hashpwd = sha_256(password);
  console.log("passwd: " + password);
  console.log("hashpwd: " + hashpwd);
  var sig = blind_sign(bsk, hashpwd);
  console.log("sig: " + sig);

  var ctext = get_ctext(id);
  var fail_page = url_with_userpath(auth_url).concat("/login_fail")

  var decrypted = decrypt(sha_256(sig), ctext, fail_page);
  var ssk = import_key(decrypted);
  console.log("ssk: " + ssk);
  var resp = sign(ssk, chal);
  console.log("response: " + resp);
  var svk = svk_global;

	var response = get_auth_result(auth_url, username, resp);
}


function register(url, username, password) {
	var reg_url = url.concat("/register");

  var keys = generate_sign_keys();
  var ssk = keys[0]; // secret signature key
  var svk = keys[1]; // signature verification Key
  var bsk = keys[2]; // blind signature key

  var hashpwd = sha_256(password);
  console.log("password: " + password);
  console.log("hashpwd: "+ hashpwd);
  var sig = blind_sign(bsk, hashpwd);
  console.log("sig: " + sig);
  var exported_ssk = export_private_key(ssk);
  var ctext = encrypt(sha_256(sig), exported_ssk);
  console.log("ctext: " + ctext);
  var concat = username + url;
  console.log("concat: " +concat);
  var id = sha_256(concat);
  console.log("id: " + id);
  add_new_creds(id, bsk, ctext);
  console.log("local storage saved");

  svk_global = svk;

	var result = get_reg_result(reg_url, username, export_to_server(svk));

}

function get_lang(url) {
	if (url.indexOf("/tr") !== -1){
		lang = "/tr";
	}
	else {
		lang = ""
	}

}

function is_valid_url(url) {
	xxUrl = pure_url_of(url);

	return (urls.indexOf(xxUrl) > -1);
}

function signIn() {
	sleep(500); // sleep for cryptographic functions

	var username = document.getElementById('username').value;
	var password = document.getElementById('password').value;

	get_lang(cur_url);

	var url = url_of(cur_url);

	if (is_valid_url(cur_url) ) { //url is valid
    var start_time = performance.now();
    auth(username, password, url_with_userpath(cur_url));
    var end_time = performance.now();
    console.log("Authentication took " + (end_time - start_time) + " milliseconds.")
	}
	else {
		alert_wrong_url();
	}

}

function write_password_errors(password_errors) {
	for (var i = 0; i < password_errors.length; i++) {
		document.getElementById("errors" + (i+1).toString() ).innerHTML = password_errors[i];

	}
	for (var i = password_errors.length; i < 5; i++) {
		document.getElementById("errors" + (i+1).toString() ).innerHTML = ""

	}
}


function signUp() {
	sleep(500); // sleep for cryptographic functions

	var username = document.getElementById('username').value;
	var password = document.getElementById('password').value;

	get_lang(cur_url);


	var url = url_of(cur_url);

	password_errors = validate_password(password);
	write_password_errors(password_errors);

	if (password_errors.length > 0) {
		return;
	}

	if( is_valid_url(cur_url) ) { //url is valid
    var start_time = performance.now();
    register(url_with_userpath(cur_url), username, password);
    var end_time = performance.now();
    console.log("Registration took " + (end_time - start_time) + " milliseconds.")
	}
	else {
		alert_wrong_url();
	}

}

window.onload = function() {

  document.getElementById('login').onclick = signIn;
	document.getElementById('register').onclick = signUp;
};
