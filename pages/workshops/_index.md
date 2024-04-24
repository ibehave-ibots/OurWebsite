contact_email: {{ data.group.email }}
mailing_list_link: {{ data.group.mailing_list_subscribe_url }}
---

# Workshops

## Subscribe for Announcements

To get announcements of upcoming workshops and be the first to register for them, [Join Our Mailing List]({{ page.mailing_list_link }})

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

## Upcoming Workshops

{% for name, workshop in pages.workshops.items() %}
  {% if workshop.sessions[0].date >= today %}
### [**{{ workshop.title }}**]({{ name }}.html)
  - Start Date: {{ workshop.sessions[0].date }}
  - Instructor: {{ workshop.main_instructor }}
  - Duration: {{ workshop.hours }} Hours
  - Registration Link: [{{ workshop.registration_link }}]({{ workshop.registration_link }})
{% if workshop.assistants %}
  - Teaching assistants: {{ workshop.assistants | join(', ')}}
{% endif %}
  

{{ workshop.summary }}

  {% endif %}
{% endfor %}



## Past Workshops


{% for name, workshop in pages.workshops.items() %}
  {% if workshop.sessions[0].date < today %}
### [**{{ workshop.title }}**]({{ name }}.html)
  - Start Date: {{ workshop.sessions[0].date }}
  - Instructor: {{ workshop.main_instructor }}
  - Duration: {{ workshop.hours }} Hours
{% if workshop.assistants %}
  - Teaching assistants: {{ workshop.assistants | join(', ')}}
{% endif %}
  

{{ workshop.summary }}

  {% endif %}
{% endfor %}


## Statistics

  - Num Workshops: {{ pages.workshops | length }}


## Interested in Organizing or Teaching a Workshop? Contact Us!

Morbi iaculis tincidunt convallis. Curabitur et diam convallis justo porttitor dapibus. Duis neque purus, tempus hendrerit dapibus a, vehicula non ante. Praesent semper tellus nec pulvinar maximus.

{{ page.contact_email }}