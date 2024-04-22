# Workshops

{% for name, workshop in pages.workshops.items() %}
  - [**{{ name }}**]({{ k }}.html): {{ workshop.hours }}
{% endfor %}