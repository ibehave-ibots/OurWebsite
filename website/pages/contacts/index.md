---
title: About Us
contact_name: {{ data.people.nick.name }}
contact_email: {{ data.people.nick.email }}
booking_link: {{ data.people.nick.booking_url }}
mailing_list_link: {{ data.group.mailing_list_subscribe_url }}
people:
    current:
        {% for id, person in data.people.items() %}
        {% if person.role == "current" %}
        - id: {{ id }}
          name: {{ person.name }}
          email: {{ person.email or ''}}
          booking_url: {{ person.booking_url }}
          image: {{ person.image }}
        {% endif %}
        {% endfor %}
    past:
        {% for id, person in data.people.items() %}
        {% if person.role == "past" %}
        - id: {{ id }}
          name: {{ person.name }}
          email: {{ person.email or ''}}
          image: {{ person.image }}
        {% endif %}
        {% endfor %}
    other:
        {% for id, person in data.people.items() %}
        {% if person.role not in ["past", "current"] %}
        - id: {{ id }}
          name: {{ person.name }}
          email: {{ person.email or ''}}
          image: {{ person.image }}
        {% endif %}
        {% endfor %}

---