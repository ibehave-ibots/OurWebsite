upcoming_workshops:
  - name: aa
    date: 2223
  - name: bb
    date: 3344

---

# Workshops

## Subscribe for Announcements

To get announcements of upcoming workshops and be the first to register for them, [Join Our Mailing List]({{ data.group.mailing_list_subscribe_url }})

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

{% for workshop in page.upcoming_workshops %}
  - {{ workshop.name }}: {{ workshop.date }}
{% endfor %}



## Past Workshops

{% for name, workshop in pages.workshops.items() %}
  - [**{{ name }}**]({{ name }}.html): {{ workshop.date }}
{% endfor %}


## Statistics

  - Num Workshops: {{ pages.workshops | length }}


## Interested in Organizing or Teaching a Workshop? Contact Us!

Morbi iaculis tincidunt convallis. Curabitur et diam convallis justo porttitor dapibus. Duis neque purus, tempus hendrerit dapibus a, vehicula non ante. Praesent semper tellus nec pulvinar maximus.

{{ data.group.email }}