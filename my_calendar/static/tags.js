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
        body: JSON.stringify({event_id : event_id, tag_name: tag_value, csrf_token: csrf_token}),
        headers: { "Content-Type": "application/json; charset=utf-8" }
    })
        .then(res => res.json())
        .then(function(res) {
            console.log(res);
            if(res["code"] == 201) {
                alert("tag created");
                document.getElementById("tag").value = "";
                update(loggedIn);
            } else {
                alert(res["error"]);
            }
        })
}
document.getElementById("save_tags_btn").addEventListener("click", createTag);
function getTag(event_id) {
    fetch('/api/tags/event', {
        method: "POST",
        body: JSON.stringify({event_id : event_id, csrf_token: csrf_token}),
        headers: { "Content-Type": "application/json; charset=utf-8" }
    })
        .then(res => res.json())
        .then(function(res) {
            console.log(res);
            let event = document.getElementById(event_id);
            for(let i = 0; i < res.tags.length; i++) {
                //if(tags[i].activated == true)
                //console.log(res.tags[i].activated);
                let activated = res.tags[i].activated;
                let tag_name = res.tags[i].tag_name;
                let tag = document.createElement("a");
                tag.setAttribute("class", "tag");
                tag.setAttribute("type", "button");
                if(activated) {
                    tag.appendChild(document.createTextNode(res.tags[i].tag_name + "!!!"));
                } else {
                    tag.appendChild(document.createTextNode(res.tags[i].tag_name));
                }
                tag.addEventListener("click", function() {
                    activated = !activated;
                    updateTag(event_id, tag_name, activated);
                })
                event.appendChild(tag);
            }
        })
}
function updateTag(event_id, tag_name, activated) {
    fetch('/api/tags/update', {
        method: "POST",
        body: JSON.stringify({event_id: event_id, tag_name: tag_name, activated: activated, csrf_token: csrf_token}),
        headers: { "Content-Type": "application/json; charset=utf-8" }        
    })
    .then(res => res.json())
    .then(function(res) {
        console.log(res);
        update(loggedIn);
    }) 
    $("#mydialog").hide();
   /*  $("#tag").show();
    $("#edit_tag_btn").show()
    $("#title").hide();
    $("#title_lb").hide();
    $("#save_changes_btn").hide();
    $("#save_tags_btn").hide();
    $("#time").hide();
    $("#time_lb").hide(); */
    //document.getElementById("id").value = event_id;
    //document.getElementById("tag").value = tag_name;
}
document.getElementById("edit_tags_btn").addEventListener("click", updateTag);
function deleteTag(event_id, tag_name) {
    //delete the tag related to a event
    fetch('api/tags/delete', {
        method: "POST",
        body: JSON.stringify({event_id: event_id, tag_name: tag_name, csrf_token: csrf_token}),
        headers: { "Content-Type": "application/json; charset=utf-8" }
    })
    .then(res => res.json())
    .then(function(res) {
        console.log(res);
        if(res["code"] == 200) {
            update("logedIn");
            $("#mydialog").hide();
        }
    })
}