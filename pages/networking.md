
title: Networking
---

## Clubs
{% for club in data.events.clubs %}
<h3>{{ club.club }}</h3>
<ul>
  <li>On: {{ club.date }} at {{ club.start_time }}</li>
  <li>Where: {{ club.location_inperson if club.location_inperson is not none else club.location_remote }} </li>
</ul>
{% endfor %}
## Conferences

## Seminars