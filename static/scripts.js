// Add your JavaScript code here
// This file can be used to handle client-side interactions, such as form validation, AJAX requests, etc.
document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        timeZone: 'local',
        themeSystem: 'bootstrap5',
        aspectRatio: 2.2,
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
        events: [
            {
                title  : 'Task 1',
                start  : '2024-03-31',
            },
            {
                title  : 'Task 2',
                start  : '2024-03-05',
                end    : '2024-03-07',
                color: 'purple'
            },
            {
                title  : 'Task 3',
                start  : '2024-04-01T10:30:00',
                color: 'green'
            }, 
            {
                title: 'Meeting',
                start: '2024-04-01T11:30:00',
                end: '2024-04-01T13:30:00'
            },
            {
                title: 'Lunch',
                start: '2024-04-01T12:00:00', 
                color: 'purple'
            },
            {
                title: 'Meeting',
                start: '2024-04-01T14:30:00'
            },
        ],
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
