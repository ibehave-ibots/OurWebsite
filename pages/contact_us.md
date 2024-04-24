title: Contact Us
contact_name: {{ data.people.nick.name }}
contact_email: {{ data.people.nick.email }}
booking_link: {{ data.people.nick.booking_url }}
mailing_list_link: {{ data.group.mailing_list_subscribe_url }}

current:
    {% for person in data.people.values() %}
    {% if person.role == "current" %}
    - name: {{ person.name }}
      email: {{ person.email }}
      booking_url: {{ person.booking_url }}
    {% endif %}
    {% endfor %}
past:
    {% for person in data.people.values() %}
    {% if person.role == "past" %}
    - name: {{ person.name }}
      email: {{ person.email }}
    {% endif %}
    {% endfor %}
other:
    {% for person in data.people.values() %}
    {% if person.role not in ["past", "current"] %}
    - name: {{ person.name }}
      email: {{ person.email }}
    {% endif %}
    {% endfor %}
---


