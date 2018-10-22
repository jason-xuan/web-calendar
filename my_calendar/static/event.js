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
                //if(i < 2) {
                let event_div = document.createElement("div");
                event_div.appendChild(document.createTextNode(res.events[i].event_time));
                event_div.appendChild(document.createTextNode(res.events[i].event_name));
                event_div.setAttribute("class", "event");
                event_div.setAttribute("id", res.events[i].event_id);
                let res_day = res.events[i].event_time.substring(0, 10);
                document.getElementById(res_day).appendChild(event_div);
                // }
                /* else {
                  let res_day = res.events[i].event_time.substring(0,10);
                  event_other.appendChild(document.createTextNode((res.events.length - 2).toString() + "other events"));
                  event_other.setAttribute("id", res_day + "other");
                  document.getElementById(res_day).appendChild(event_other);
                } */
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
            if (res["msg"] == title + " create successfully") {
                
				//alert("hi");
				//already sign in
				loggedIn = true;
				update(loggedIn);
			}
        })
        .catch(error => console.error('Error:', error));
}
document.getElementById("save_btn").addEventListener("click", createEvent);
function deleteEvent(day) {

}