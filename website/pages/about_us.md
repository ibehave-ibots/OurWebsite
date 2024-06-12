_template: about_us.html
title: About Us
contact_name: {{ data.people.nick.name }}
contact_email: {{ data.people.nick.email }}
booking_link: {{ data.people.nick.booking_url }}
mailing_list_link: {{ data.group.mailing_list_subscribe_url }}
sections:
    - title: What is an RSE?
      image: https://placehold.co/600x600
      paragraphs:
        - Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur facilisis velit sem, non hendrerit magna tincidunt sed. Etiam et ex rhoncus, semper mauris vitae, elementum erat.
        - Cras faucibus ex vitae lacus iaculis scelerisque. Pellentesque ante risus, convallis et metus at, sodales blandit odio. Nunc elementum nisi tempus, pulvinar augue id, tempor leo. Ut risus libero, ornare eget metus vitae, aliquet sagittis enim. Phasellus dictum sollicitudin enim eget vehicula.
      features:
        - title: Share Your Code
          sentence: aaa
          icon: icon.svg
        - title: Release Your Software
          sentence: aaa
          icon: icon.svg
        - title: Test Your Software
          sentence: aaa
          icon: icon.svg
        - title: Standardize Your Software
          sentence: aaa
          icon: icon.svg
          
      
    - title: What is a RSC/Teaching RSE?
      image: https://placehold.co/600x600
      paragraphs: 
        - Morbi id mattis orci. Maecenas elit sapien, viverra in urna eu, ornare finibus eros. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut non tristique lacus, nec dapibus dui.
        - Sed volutpat tempor nunc, et ullamcorper arcu ullamcorper in. Nulla facilisis in sapien ut porttitor. Mauris commodo sollicitudin nibh a cursus. Proin porttitor dictum libero vel rhoncus. Vestibulum enim enim, iaculis in massa eu, vulputate laoreet nulla.
      features: 
        - title: Share Your Code
          sentence: aaa
          icon: icon.svg
        - title: Release Your Software
          sentence: aaa
          icon: icon.svg

    - title: What Do We Do?
      image: https://placehold.co/600x600
      paragraphs: 
        - Morbi id mattis orci. Maecenas elit sapien, viverra in urna eu, ornare finibus eros. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut non tristique lacus, nec dapibus dui.
        - Sed volutpat tempor nunc, et ullamcorper arcu ullamcorper in. Nulla facilisis in sapien ut porttitor. Mauris commodo sollicitudin nibh a cursus. Proin porttitor dictum libero vel rhoncus. Vestibulum enim enim, iaculis in massa eu, vulputate laoreet nulla.
      features:
        - title:  Develop a Workshop with Us
          sentence:  aa
          icon: icon.svg
        - title:  Organize a Coding Retreat with Us
          sentence:  aa
          icon: icon.svg
        - title:  Co-Develop Data Standards for Your Lab
          sentence: bb
          icon: icon.svg
        - title: Teach One of Our Workshops
          sentence:
          icon: icon.svg
people:
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

sponsors: 
    {% for sponsor in data.orgs.sponsors %}
    - name: {{ sponsor.name }}
      website: {{ sponsor.url }}
      email: {{ sponsor.email }}
      description: {{ sponsor.description }}
      logo: {{ sponsor.logo }}
    {% endfor %}

---


