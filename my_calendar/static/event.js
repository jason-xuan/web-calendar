function getEvent(month, year) {
    fetch('/api/events/user', {
        method: "POST",
        body: JSON.stringify({ year: year, month: month + 1 }),
        headers: { "Content-Type": "application/json; charset=utf-8" }
    })
        .then(res => res.json())
        .then(function (res) {
            console.log(res.events.length)
            let event_other = document.createElement("p");
            for (let i = 0; i < res.events.length; i++) {
                let event_div = document.createElement("div");
                event_div.appendChild(document.createTextNode(res.events[i].event_time));
                event_div.appendChild(document.createTextNode(res.events[i].event_name));
                event_div.setAttribute("class", "event");
                event_div.setAttribute("id", res.events[i].event_id);
                //render a event by using this edit button
                let event_edit = document.createElement("a");
                event_edit.appendChild(document.createTextNode("edit"));
                event_edit.setAttribute("type", "button");
                event_edit.addEventListener("click", function() {
                    renderEvent(res.events[i].event_id, res.events[i].event_time, res.events[i].event_name);

                    //console.log("event" + res.events[i].json);
                    alert("edit!!!");
                })
                //event_edit.addEventListener("click", renderEvent(res.events[i].event_id, res.events[i].event_time, res.events[i].event_name))

                event_div.appendChild(event_edit);
                let res_day = res.events[i].event_time.substring(0, 10);
                document.getElementById(res_day).appendChild(event_div);
            }

        })
        .catch(error => console.error('Error:', error))
}

function createEvent() {
    let title = document.getElementById("title").value;
    let date = document.getElementById("date").value.split("-");
    let year = Number(date[0]);
    let month = Number(date[1]) - 1;
    let day = Number(date[2]);
    let time = document.getElementById("time").value.split(":");
    let hour = Number(time[0]);
    let minute = Number(time[1]);
    let notes = document.getElementById("description").value;
    fetch('/api/events/create', {
        method: "POST",
        body: JSON.stringify({ event_name: title, event_time: new Date(year, month, day, hour - 5, minute, 0) }),
        headers: { "Content-Type": "application/json; charset=utf-8" }
    })
        .then(res => res.json())
        
        .then(function(res) {
            console.log(res["msg"]);
            if (res["code"] == 201) {
                
				//alert("hi");
				//already sign in
				loggedIn = true;
				update(loggedIn);
			}
        })
        .catch(error => console.error('Error:', error));
}
document.getElementById("save_btn").addEventListener("click", createEvent);

function renderEvent(event_id, time, event) {
    /* console.log("time:" + time);
    console.log("event:" + event);
    console.log("id:" + event_id); */
    document.getElementById("edit_add_title").innerText = "Update Event"
    if(event != null) {
        document.getElementById("title").value = event;
    } 
    if(time != null) {
        document.getElementById("time").value = time.substring(11,16);
    }
    if(event_id != null) {
        document.getElementById("id").value = event_id;
    } 
    $("#date").hide();
}

function updateEvent(event_id, time, event) {
    let title = document.getElementById("title").value;
    let event_id = document.getElementById("id").value;
    let notes = document.getElementById("description").value;
    fetch('/api/events/update', {
        method: "POST",
        body: JSON.stringify({
            event_id: id,
            update_fields: {
                event_name: title
            }
        }),
        headers: {"Content-Type": "application/json; charset=utf-8"}
        })
      .then(res => res.json())
      .then(response => console.log('Success:', JSON.stringify(response)))
      .catch(error => console.error('Error:',error))
}
document.getElementById("save_changes_btn").addEventListener("click", updateEvent);

function deleteEvent(day) {

}