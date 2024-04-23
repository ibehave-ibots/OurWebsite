
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
    summary: {{ club.summary }} 
    target_audience: {{ club.target_audience }}
    people: 
    {% for person in club.people %}
      - name: {{ person.name }}
        role: {{ person.role }}
        url: {{ person.url }}
    {% endfor %}
    registration_url: {{ club.registration_url }}
  {% endfor %}

conferences:
  {% for conference in data.events.conferences %}
  - name: {{ conference.conference }}
    date: {{ conference.date }}
    start: {{ conference.start_time }}
    end: {{ conference.end_time }}
    location:
      inperson: {{ conference.location.inperson }}
      remote: {{ conference.location.remote }}
    host_org:
      name: {{ conference.host_org.name }}
      url: {{ conference.host_org.url }}
    summary: {{ conference.summary }} 
    target_audience: {{ conference.target_audience }}
    people: 
    {% for person in conference.people %}
      - name: {{ person.name }}
        role: {{ person.role }}
        url: {{ person.url }}
    {% endfor %}
    registration_url: {{ conference.registration_url }}
  {% endfor %}

---
