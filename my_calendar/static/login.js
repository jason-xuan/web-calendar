function login() {
    let email = document.getElementById("login_email").value;
    let password = document.getElementById("login_password").value;
    fetch('/api/users/login/', {
        method: "POST",
        body: JSON.stringify({email: email, password: password}),
        headers: {"Content-Type": "application/json; charset=utf-8"}
        })
      .then(res => res.json())
      .then(response => console.log('Success:', JSON.stringify(response)))
      .then(
        //document.getElementById("login_email").style.visibility="hidden",
        //document.getElementById("logout_btn").style.visibility="visible",
        //document.getElementById("login_password").style.visibility="hidden"
      )
      .catch(error => console.error('Error:',error))
      
}
document.getElementById("login_btn").addEventListener("click", login(), false);