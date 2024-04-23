title: About Us
current:
    {% for person in data.people_consolidated.current %}
    - name: {{ person.name }}
      email: {{ person.email }}
      booking_url: {{ person.booking_url }}
    {% endfor %}
past:
    {% for person in data.people_consolidated.past %}
    - name: {{ person.name }}
      email: {{ person.email }}
    {% endfor %}
other:
    {% for person in data.people_consolidated.other %}
    - name: {{ person.name }}
      email: {{ person.email }}
    {% endfor %}

---
## What is an RSE?
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur facilisis velit sem, non hendrerit magna tincidunt sed. Etiam et ex rhoncus, semper mauris vitae, elementum erat. Cras faucibus ex vitae lacus iaculis scelerisque. Pellentesque ante risus, convallis et metus at, sodales blandit odio. Nunc elementum nisi tempus, pulvinar augue id, tempor leo. Ut risus libero, ornare eget metus vitae, aliquet sagittis enim. Phasellus dictum sollicitudin enim eget vehicula.

## What is a RSC/Teaching RSE?
Morbi id mattis orci. Maecenas elit sapien, viverra in urna eu, ornare finibus eros. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut non tristique lacus, nec dapibus dui. Sed volutpat tempor nunc, et ullamcorper arcu ullamcorper in. Nulla facilisis in sapien ut porttitor. Mauris commodo sollicitudin nibh a cursus. Proin porttitor dictum libero vel rhoncus. Vestibulum enim enim, iaculis in massa eu, vulputate laoreet nulla.

## What We Do?
Nunc est ante, ornare at tortor luctus, dapibus euismod est. Vivamus elementum facilisis varius. Cras in ipsum tempus tellus aliquam blandit. Morbi vitae metus non felis accumsan pretium. Integer enim lacus, dapibus at tincidunt nec, porta eget ex. Proin ultricies commodo nibh, in pellentesque magna sodales ac. Cras feugiat purus vel augue tincidunt, ut dignissim odio efficitur. Aliquam iaculis, quam non lobortis posuere, metus dolor pharetra metus, non suscipit eros nunc ut quam. Donec id suscipit sapien. Praesent vel elementum nisi, vulputate blandit arcu. Donec purus ex, eleifend in tellus in, dictum pretium erat. Ut non purus id metus hendrerit faucibus in id risus. Aliquam erat volutpat. Curabitur suscipit risus nec justo volutpat, posuere auctor turpis vulputate. Aenean ornare faucibus arcu, sed scelerisque diam fermentum sit amet.

