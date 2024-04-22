
title: Networking
clubs:
    title: Clubs
    schedule:
        {% for club in data.events.clubs %}
        - Club: {{ club.club }}
          Date: {{ club.date }}
          Start Time: {{ club.start_time }}
          End Time: {{ club.end_time }}
        {% endfor %}
---
