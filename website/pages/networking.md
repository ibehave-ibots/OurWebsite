
title: Networking
clubs:
  {% for club in data.networking_events.clubs %}
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
  {% for conference in data.networking_events.conferences %}
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

seminars:
  {% for seminar in data.networking_events.seminars %}
  - name: {{ seminar.seminar }}
    date: {{ seminar.date }}
    start: {{ seminar.start_time }}
    end: {{ seminar.end_time }}
    location:
      inperson: {{ seminar.location.inperson }}
      remote: {{ seminar.location.remote }}
    host_org:
      name: {{ seminar.host_org.name }}
      url: {{ seminar.host_org.url }}
    summary: {{ seminar.summary }} 
    target_audience: {{ seminar.target_audience }}
    people: 
    {% for person in seminar.people %}
      - name: {{ person.name }}
        role: {{ person.role }}
        url: {{ person.url }}
    {% endfor %}
    registration_url: {{ seminar.registration_url }}
  {% endfor %}

partners: 
    {% for partner in data.orgs.partners %}
    - name: {{ partner.name }}
      website: {{ partner.url }}
      email: {{ partner.email }}
      description: {{ partner.description }}
    {% endfor %}
---
