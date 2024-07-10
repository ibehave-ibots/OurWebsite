---

title: Our Partners

partners: 
    {% for partner in data.orgs.partners %}
    - name: {{ partner.name }}
      website: {{ partner.url }}
      email: {{ partner.email }}
      description: {{ partner.description }}
      institute: 
        name: {{partner.institute.name }}
        url: {{ partner.institute.url }}
    {% endfor %}

---
