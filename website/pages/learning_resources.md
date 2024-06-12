_template: learning_resources.html
title: Learning Resources
our_materials:
    {% for our_material in data.teaching_materials.our_materials %}
    - name: {{ our_material.name }}
      filepath: {{ our_material.notebook_filepath }}
      technologies:
        {% for technology in our_material.technologies %}
            - {{ technology }}
        {% endfor %}
    {% endfor %}
external_resources:
    {% for resource in data.teaching_materials.external_resources %}
        - {{ resource }}
    {% endfor %}
---

## Description

Vivamus ut ornare quam. In ullamcorper vehicula erat. Mauris magna diam, tempus sit amet elit eu, placerat euismod arcu. Quisque laoreet neque lectus. Aenean dui orci, aliquam eget eros eget, malesuada tincidunt lorem. Etiam mollis erat diam, vitae imperdiet erat elementum sit amet. Cras ultrices luctus nisi quis finibus. Sed in vehicula sapien, eget consectetur libero. Proin vulputate nulla eget elit pulvinar, et rutrum massa rhoncus. Fusce dictum justo ac augue tempus, vitae mattis purus malesuada. Phasellus id elementum ex.

Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Donec euismod lorem eros, aliquet tincidunt diam consequat hendrerit. Sed tristique vel ipsum eget lobortis. Pellentesque accumsan urna ipsum, sed pellentesque nibh tempus in. Sed et ornare erat. Donec non est nec metus ultrices consequat. Suspendisse nec vulputate arcu. Vestibulum ullamcorper eros et neque malesuada finibus. Maecenas eget metus sit amet orci tempor sollicitudin vel et enim. Duis vehicula luctus est, non congue ex ornare vel. Aenean convallis augue a eros dignissim, ac malesuada tortor cursus. Morbi ultricies iaculis nisl id rutrum. Nulla accumsan diam in odio auctor scelerisque.
