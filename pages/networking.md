
title: Networking

---

## Clubs
{% for club in data.events.clubs %}

###{{ club.club }}###
<ul>
  <li>On: {{ club.date }} at {{ club.start_time }}</li>
  <li>Location: {{ club.location.inperson if club.location.inperson is not none else club.location.remote }} </li>
</ul>
{% endfor %}
## Conferences

## Seminars