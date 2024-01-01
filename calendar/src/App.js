import React from "react";
import "./styles.css";
import FullCalendar from "@fullcalendar/react";
import timeGridPlugin from "@fullcalendar/timegrid";
import iCalendarPlugin from "@fullcalendar/icalendar";
import rrule from "@fullcalendar/rrule";

export default function App() {
  let events1 = [
    {
      title: "event1",
      start: "2021-01-06T12:30:00",
      end: "2021-01-06T14:30:00"
    }
  ];
  let events2 = [
    {
      title: "event1",
      start: "2021-01-06T16:30:00",
      end: "2021-01-06T18:30:00"
    }
  ];

  let icalEvents = {
    url:
      "https://cors-anywhere.herokuapp.com/https://calendar.google.com/calendar/ical/ssg14ioomu1khvrp6kkc5r2as8%40group.calendar.google.com/private-ef1d570f85d6de56666bc03ba2a0a239/basic.ics",
    format: "ics"
  };

  return (
    <FullCalendar
      plugins={[timeGridPlugin, iCalendarPlugin]}
      initialView="timeGridDay"
      initialDate="2021-01-06"
      events={icalEvents}
      // eventSources={[events1, icalEvents]}
    />
  );
}
