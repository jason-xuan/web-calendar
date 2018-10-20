# Web API
## description
there are three types of module:
 1.  user, which can make user registration and login
 2.  event, shown in calendar
 3.  tag, tag on event
 
 ### what api we need
 * basic control: register, login, logout
 * events: create, read, modify, delete events
    1. create event of the current user
    2. get events of current user from given year and month
    3. modify or delete event with given event_id
 * tags: create, read, modify, delete tags
    1. create a tag with a given event_id and it's name
    2. get tags with given event_id
    3. modify or delete event with given tag_id

## actual api
### register
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

### login
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

### logout
```javascript
fetch('/api/users/logout',{
    method: "GET"})
  .then(res => res.json())
  .then(response => console.log('Success:', JSON.stringify(response)))
  .catch(error => console.error('Error:',error))
```
