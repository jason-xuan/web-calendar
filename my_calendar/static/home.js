// these are labels for the days of the week
cal_days_labels = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

// these are human-readable month name labels, in order
cal_months_labels = ['January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August', 'September',
    'October', 'November', 'December'];

// these are the days of the week for each month, in order
cal_days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
cal_current_date = new Date();
function Calendar(month, year) {
    this.month = (isNaN(month) || month == null) ? cal_current_date.getMonth() : month;
    this.year  = (isNaN(year) || year == null) ? cal_current_date.getFullYear() : year;
}
cal = new Calendar();
let loggedIn = false;
function update () {
    clearCalendar();
    document.getElementById('display_month').innerHTML = cal_months_labels[cal.month] + " " + cal.year;
    // get first day of month
    let firstDay = new Date(cal.year, cal.month, 1);
    let startingDay = firstDay.getDay();

    // find number of days in month
    let monthLength = cal_days_in_month[cal.month];

    // compensate for leap year
    if (cal.month == 1) { // February only!
        if((cal.year % 4 == 0 && cal.year % 100 != 0) || cal.year % 400 == 0){
            monthLength = 29;
        }
    }
    //html += '</tr><tr>';

    // fill in the days
    let day = 1;
    // this loop is for is weeks (rows)
    for (let i = 0; i < 9; i++) {
        // this loop is for weekdays (cells)
        let weekRow = document.createElement("tr");
        for (let j = 0; j <= 6; j++) {
            let dateCell = document.createElement("td");
            //html += '<td class="calendar-day">';
            if (day <= monthLength && (i > 0 || j >= startingDay)) {
                //html += day;
                dateCell.appendChild(document.createTextNode(day.toString()));
                dateCell.setAttribute("id",cal.year.toString() + "-" + (cal.month + 1).toString() + "-" + day.toString());
                dateCell.setAttribute("class", "editable");
                weekRow.appendChild(dateCell);
                day++;
            } else {
                dateCell.appendChild(document.createTextNode(""));
                weekRow.appendChild(dateCell);
            }
            //html += '</td>';
        }
        document.getElementById("calendar_main").appendChild(weekRow);
        // stop making rows if we've run out of days
        if (day > monthLength) {
            break;
        }
    }
}
function clearCalendar() {
    let main = document.getElementById("calendar_main");
    while (main.childNodes.length > 2) {
        main.removeChild(main.lastChild);
    }
}
//when you click the datecell, it can show the edit ui.
$(document).on("click", ".editable", function() {
      //alert("hi");
        
    });

document.getElementById("next_month").addEventListener("click", function(){
    if(cal.month == 11) {
        cal.month = 0;
        cal.year = cal.year + 1;
    } else {
        cal.month = cal.month + 1;
    }
    update();

}, false);
// Change motn when the prev button is pressed
document.getElementById("prev_month").addEventListener("click", function(){
    if(cal.month == 0) {
        cal.month = 11;
        cal.year = cal.year - 1;
    } else {
        cal.month = cal.month - 1;
    }
    update();

}, false);
update();