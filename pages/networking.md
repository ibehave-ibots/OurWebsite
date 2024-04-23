
title: Networking
clubs:
  {% for club in data.events.clubs %}
  - name: {{ club.club }}
    date: {{ club.date }}
    start: {{ club.start_time }}
    end: {{ club.end_time }}
    location:
      inperson: {{ club.location.inperson }}
      remote: {{ club.location.remote }}
    host_org:
      name: {{ club.host_org.name }}
      url: {{ club.host_org.url }}
  {% endfor %}

---
