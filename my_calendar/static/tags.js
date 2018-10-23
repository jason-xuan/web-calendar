function createTag() {
   /*  response = self.client.post('/api/tags/create', json={
        'event_id': self.event_id,
        'tag_name': 'important',
        'csrf_token': self.csrf_token
    }) */
    let event_id = document.getElementById("id").value;
    let tag_value = document.getElementById("tag").value;
    fetch('/api/tags/create', {
        method: "POST",
        body: JSON.stringify({event_id : event_id, tag_name: tag_value}),
        headers: { "Content-Type": "application/json; charset=utf-8" }
    })
        .then(res => res.json())
        .then(function(res) {
            console.log(res);
            if(res["code"] == 201) {
                alert("tag created");
                document.getElementById("tag").value = "";
                update(loggedIn);
            }
        })
}
//document.getElementById("save_tags_btn").addEventListener("click", createTag);
function getTag(event_id) {
    fetch('/api/tags/event', {
        method: "POST",
        body: JSON.stringify({event_id : event_id}),
        headers: { "Content-Type": "application/json; charset=utf-8" }
    })
        .then(res => res.json())
        .then(function(res) {
            console.log(res);
            let event = document.getElementById(event_id);
            for(let i = 0; i < res.tags.length; i++) {
                //if(tags[i].activated == true)
                let tag = document.createElement("strong");
                tag.appendChild(document.createTextNode(res.tags[i].tag_name));
                event.appendChild(tag);
            }
        })
}