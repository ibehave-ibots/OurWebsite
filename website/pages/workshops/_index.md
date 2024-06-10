title: Workshops
contact_email: {{ data.group.email }}
mailing_list_link: {{ data.group.mailing_list_subscribe_url }}

upcoming_workshops:
{% for wshop_id, workshop in pages.workshops.items() %}
  {% if workshop.sessions[0].date >= today %}
  - id: {{ wshop_id }}
    title: {{ workshop.title }}
    start_date: {{ workshop.sessions[0].date }}
    instructor: {{ workshop.instructors[0].name }}
    duration: {{ workshop.hours }}
    registration_link: {{ workshop.registration_link }}
    summary: {{ workshop.summary }}
{% endif %}
{% endfor %}

past_workshops:
{% for wshop_id, workshop in pages.workshops.items() %}
  {% if workshop.sessions[0].date < today %}
  - id: {{ wshop_id }}
    title: {{ workshop.title }}
    start_date: {{ workshop.sessions[0].date }}
    instructor: {{ workshop.instructors[0].name }}
    duration: {{ workshop.hours }}
    registration_link: {{ workshop.registration_link }}
    summary: {{ workshop.summary }}
{% endif %}
{% endfor %}

statistics:
  - name: Number of Workshops
    value: {{ pages.workshops | length }}
    units: workshops
---

## Description

Morbi iaculis tincidunt convallis. Curabitur et diam convallis justo porttitor dapibus. Duis neque purus, tempus hendrerit dapibus a, vehicula non ante. Praesent semper tellus nec pulvinar maximus.

## Workshop Format

### Structure

Pellentesque lobortis luctus augue non bibendum. Vivamus non tortor id augue tempus blandit. Ut sit amet ipsum ac elit ultricies rhoncus. Aliquam ut ante id metus rhoncus euismod. Quisque urna nulla, sodales sed interdum sit amet, posuere tristique ipsum. Integer vel est venenatis, volutpat nisl at, tempus quam. Pellentesque maximus, ligula vitae congue convallis, lorem mi commodo mi, ac bibendum enim arcu id turpis. Aliquam ac euismod lectus. Donec commodo ut ex rhoncus luctus.

### Platforms

Pellentesque lobortis luctus augue non bibendum. Vivamus non tortor id augue tempus blandit. Ut sit amet ipsum ac elit ultricies rhoncus. Aliquam ut ante id metus rhoncus euismod. Quisque urna nulla, sodales sed interdum sit amet, posuere tristique ipsum. Integer vel est venenatis, volutpat nisl at, tempus quam. Pellentesque maximus, ligula vitae congue convallis, lorem mi commodo mi, ac bibendum enim arcu id turpis. Aliquam ac euismod lectus. Donec commodo ut ex rhoncus luctus.

## Open to All Neuroscience Researchers in the NRW

Morbi iaculis tincidunt convallis. Curabitur et diam convallis justo porttitor dapibus. Duis neque purus, tempus hendrerit dapibus a, vehicula non ante. Praesent semper tellus nec pulvinar maximus.

![Registration System](/static/images/early-registration-concept.png)



## Interested in Organizing or Teaching a Workshop? Contact Us!

Morbi iaculis tincidunt convallis. Curabitur et diam convallis justo porttitor dapibus. Duis neque purus, tempus hendrerit dapibus a, vehicula non ante. Praesent semper tellus nec pulvinar maximus.
