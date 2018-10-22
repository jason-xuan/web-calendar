function login() {
	let email = $("#login_email").val();

	let password = $("#login_password").val();

	fetch('/api/users/login/', {
		method: "POST",
		body: JSON.stringify({ email: email, password: password }),
		headers: { "Content-Type": "application/json; charset=utf-8" }
	})
		.then(res => res.json())
		.then(function (response) {
			alert(JSON.stringify(response));
			if (response["msg"] == "successfully login") {
				//alert("hi");
				//already sign in
				loggedIn = true;
				update(loggedIn);
			}
			//console.log('Success:', JSON.stringify(response));
		})
		.catch(error => console.error('Error:', error))
}
$("#login_btn").click(login);

function register() {
	let email = $("#register_email").val();
	let password = $("#register_password").val();
	fetch('/api/users/register/', {
		method: "POST",
		body: JSON.stringify({ email: email, password: password }),
		headers: { "Content-Type": "application/json; charset=utf-8", }
	})
		.then(res => res.json())
		.then(response => console.log('Success:', JSON.stringify(response)))
		.catch(error => console.error('Error:', error))
}
$("#register_btn").click(register);
function logOut() {
	fetch('/api/users/logout', {
		method: "GET"
	})
		.then(res => res.json())
		.then(response => console.log('Success:', JSON.stringify(response)))
		.catch(error => console.error('Error:', error))
}
$("#logout_btn").click(logOut);