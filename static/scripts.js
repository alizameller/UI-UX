// Add your JavaScript code here
// This file can be used to handle client-side interactions, such as form validation, AJAX requests, etc.

document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        timeZone: 'local',
        themeSystem: 'bootstrap5',
        aspectRatio: 2.5,
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay,listMonth'
        },
        customButtons: {
            homeButton: {
              text: 'Home',
              click: function() {
                window.location.href = "http://127.0.0.1:5000/dashboard";
              }
            }
        },
        footerToolbar: {
            center: 'homeButton'
        },
        /*views: {
            dayGridMonth: { // name of view
                titleFormat: { month: 'name', year: '4-digit' }
                // other view-specific options here
            }   
        },*/
        weekNumbers: true,
        dayMaxEvents: true, // allow "more" link when too many events
        // events: 'https://fullcalendar.io/api/demo-feeds/events.json',
        events: events,
        initialView: 'dayGridMonth',
        selectable: true,
        select: function(info) {
            let task = prompt("Add Task", "Task Name");
            let text;
            if (person == null || person == "") {
            text = "User cancelled the prompt.";
            } else {
            text = "Hello " + person + "! How are you today?";
            }
        }
    });

    calendar.render();
});
