title: Organizations
partners: 
    {% for partner in data.partners %}
    - name: {{ partner.name }}
      website: {{ partner.url }}
      email: {{ partner.email }}
      description: {{ partner.description }}
    {% endfor %}

sponsors: 
    {% for sponsor in data.sponsors %}
    - name: {{ sponsor.name }}
      website: {{ sponsor.url }}
      email: {{ sponsor.email }}
      description: {{ sponsor.description }}
    {% endfor %}


---

# Description

Nullam interdum orci tellus, quis mollis leo pellentesque non. Aenean aliquam odio quis ipsum cursus blandit. Fusce ultrices eu dolor et vestibulum. Donec efficitur luctus justo. Quisque maximus sollicitudin tellus a maximus. Curabitur rhoncus augue est, eget congue augue placerat vitae. Nam laoreet dignissim ligula, ac dictum eros maximus at.


