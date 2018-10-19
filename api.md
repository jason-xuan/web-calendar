# Web API

## register
```javascript
fetch('/api/users/register/', {
    method: "POST",
    body: JSON.stringify({email:'xuan@wustl', password:'1123'}),
    headers: {"Content-Type": "application/json; charset=utf-8",}
    })
  .then(res => res.json())
  .then(response => console.log('Success:', JSON.stringify(response)))
  .catch(error => console.error('Error:',error))
```



## login
```javascript
fetch('/api/users/login/', {
    method: "POST",
    body: JSON.stringify({email:'xuan@wustl', password:'1123'}),
    headers: {"Content-Type": "application/json; charset=utf-8"}
    })
  .then(res => res.json())
  .then(response => console.log('Success:', JSON.stringify(response)))
  .catch(error => console.error('Error:',error))
```

## logout
```javascript
fetch('/api/users/logout',{
    method: "GET"})
  .then(res => res.json())
  .then(response => console.log('Success:', JSON.stringify(response)))
  .catch(error => console.error('Error:',error))
```