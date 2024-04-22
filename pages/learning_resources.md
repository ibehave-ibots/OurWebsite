title: Learning Resources

---

## Description
Vivamus ut ornare quam. In ullamcorper vehicula erat. Mauris magna diam, tempus sit amet elit eu, placerat euismod arcu. Quisque laoreet neque lectus. Aenean dui orci, aliquam eget eros eget, malesuada tincidunt lorem. Etiam mollis erat diam, vitae imperdiet erat elementum sit amet. Cras ultrices luctus nisi quis finibus. Sed in vehicula sapien, eget consectetur libero. Proin vulputate nulla eget elit pulvinar, et rutrum massa rhoncus. Fusce dictum justo ac augue tempus, vitae mattis purus malesuada. Phasellus id elementum ex.

Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Donec euismod lorem eros, aliquet tincidunt diam consequat hendrerit. Sed tristique vel ipsum eget lobortis. Pellentesque accumsan urna ipsum, sed pellentesque nibh tempus in. Sed et ornare erat. Donec non est nec metus ultrices consequat. Suspendisse nec vulputate arcu. Vestibulum ullamcorper eros et neque malesuada finibus. Maecenas eget metus sit amet orci tempor sollicitudin vel et enim. Duis vehicula luctus est, non congue ex ornare vel. Aenean convallis augue a eros dignissim, ac malesuada tortor cursus. Morbi ultricies iaculis nisl id rutrum. Nulla accumsan diam in odio auctor scelerisque.

## Our Materials
{% for our_material in data.teaching_materials.our_materials %}
<h4> {{ our_material.name }} </h4>
<a href="{{ our_material.notebook_filepath }}">{{ our_material.notebook_filepath }}</a>
<ul>
{% for technology in our_material.technologies %}
    <li>{{ technology }}</li>
{% endfor %}

</ul>

{% endfor %}

## External Resources
<ul>
{% for resource in data.teaching_materials.external_resources %}
    <li> <a href="{{ resource }}">{{ resource }}</a> </li>
{% endfor %}
</ul>