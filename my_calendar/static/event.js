function getEvent(day) {
    let day = new Date(day);
    let eventCell = document.createElement("div");
    eventCell.appendChild(document.createTextNode("time"));
    eventCell.appendChild(document.createTextNode("Meet Jenny hahaha"));
    eventCell.setAttribute("class", "events");
    eventCell.setAttribute("id", "event1");
    document.getElementById("2018-10-20").appendChild(eventCell);
}
getEvent();

function createEvent(day) {
    let day = new Date(day);
    let title = document.getElementById("title").value;
    let date = document.getElementById("date").value;
    let time = document.getElementById("time").value;
    let notes = document.getElementById("description").value;
}