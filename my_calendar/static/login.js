function login() {
	let email = $("#login_email").val();

	let password = $("#login_password").val();

	fetch('/api/users/login', {
		method: "POST",
		body: JSON.stringify({ email: email, password: password, csrf_token: csrf_token }),
		headers: { "Content-Type": "application/json; charset=utf-8" }
	})
		.then(res => res.json())
		.then(function (response) {
			//alert(response);
			console.log(response)
			if (response["code"] == 200) {
				//alert("hi");
				//already sign in
				loggedIn = true;
				update(loggedIn);
				$("#loginuser").hide();
				$("#adduser").hide();	
				$("#logout_btn").show();
				$("#save_changes_btn").hide();
			} else {
				if(response["error"] != null) {
					alert(response["error"]);
				}
			}
			//console.log('Success:', JSON.stringify(response));
		})
		.catch(error => console.error('Error:', error))
}
$("#login_btn").click(login);

function register() {
	let email = $("#register_email").val();
	let password = $("#register_password").val();
	fetch('/api/users/register', {
		method: "POST",
		body: JSON.stringify({ email: email, password: password, csrf_token: csrf_token}),
		headers: { "Content-Type": "application/json; charset=utf-8", }
	})
		.then(res => res.json())
		.then(function(res){
			console.log(res);
			if(res["code"] == 201) {
				loggedIn = true;
				update(loggedIn);
				$("#loginuser").hide();
				$("#adduser").hide();	
				$("#logout_btn").show();
				$("#save_changes_btn").hide();
			} else {
				alert(res["error"]);
			}
		}) 
		.catch(error => console.error('Error:', error))
}
$("#register_btn").click(register);
function logOut() {
	fetch('/api/users/logout', {
		method: "GET"
	})
		.then(res => res.json())
		.then(function(res){
			console.log(res);
			if(res["code"] == 200) {
				loggedIn = false;
				$("#mydialog").hide();
				$("#logout_btn").hide();
				$("#loginuser").show();
				$("#adduser").show();
				//location.reload();
				document.getElementById("register_email").value = "";
				document.getElementById("register_password").value = "";
				update(loggedIn);
			}
		}) 
		.catch(error => console.error('Error:', error))
}
$("#logout_btn").click(logOut);