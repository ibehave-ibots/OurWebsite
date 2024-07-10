---
title: Home
milestones:
    {% for milestone in data.group.milestones %}
    - date: {{ milestone.date }}
      name: {{ milestone.name }}
      summary: {{ milestone.summary }}
      icon: {{ milestone.icon }}
    {% endfor %}
consulting: 
    n_sessions: {{ data.group.consulting_stats.num_consulting_sessions}}
    n_clients: {{ data.group.consulting_stats.num_of_clients}}
    n_labs: {{ data.group.consulting_stats.which_labs_have_used_ibots }}
    total_hours: {{ data.group.consulting_stats.total_hours_consulting }}
workshop:
    n_workshops: {{ data.group.workshop_stats.num_workshops }}
    n_students: {{ data.group.workshop_stats.num_of_students }}
    total_hours: {{ data.group.workshop_stats.total_teaching_hours }}

---

## Our Mission
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum maximus porta ex, ac ultricies eros pellentesque ac. In hac habitasse platea dictumst. In velit magna, porta at luctus sit amet, consectetur a nisi. Proin sed risus quis libero finibus lobortis. Ut tristique nisi varius magna mattis pellentesque. Vivamus ullamcorper eros suscipit blandit volutpat. Aliquam eget sapien tincidunt, vulputate odio vitae, mattis dui. In hac habitasse platea dictumst.

Cras lectus leo, volutpat eget lorem eu, rutrum finibus est. Maecenas in nulla malesuada, mattis augue quis, molestie mauris. Vestibulum ullamcorper a massa in faucibus. Pellentesque ultricies mauris et facilisis luctus. Aenean gravida consectetur arcu. Sed mattis massa sit amet felis mollis, nec auctor augue finibus. Integer lacinia vulputate dignissim. Aenean ac lacus mi. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Fusce lacinia est sed feugiat sollicitudin. Vivamus convallis ultricies sodales.

## The iBOTS Way
Donec tincidunt quis ex quis ultrices. Nam eget nibh condimentum, ornare orci in, tincidunt risus. Vivamus mattis libero id sapien semper condimentum. Praesent lacinia tortor elit, at fermentum justo imperdiet vel. Vestibulum iaculis nunc nec purus pretium euismod. Phasellus nibh tellus, interdum ac odio a, lobortis cursus mi. Aliquam nec quam turpis. Aliquam erat volutpat. Donec velit nisi, pellentesque a ex nec, semper sagittis nibh. Etiam eget porttitor lectus, sit amet tincidunt orci. Integer nec lectus et magna volutpat luctus sed eget lacus. Quisque et imperdiet orci, eget vestibulum ante. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur imperdiet ligula in nibh vehicula, a varius neque hendrerit.

Morbi pellentesque est dapibus mauris laoreet suscipit. Maecenas egestas nulla risus. Mauris bibendum faucibus gravida. Cras rutrum viverra ex, id gravida purus semper a. Curabitur sit amet lacinia eros. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Duis mattis ac felis quis dignissim. Proin scelerisque metus sed dolor commodo porta.

Donec tincidunt gravida nulla, in condimentum ante scelerisque ut. Nulla et venenatis eros, in viverra ex. Duis feugiat aliquam metus vitae aliquet. Aenean sit amet dictum arcu, ac pharetra enim. Etiam semper sem eget interdum egestas. Mauris at nibh orci. Sed ac felis a dui lobortis iaculis vitae vitae diam.

## About iBehave

Curabitur elementum enim sed purus dignissim consectetur. Nulla vestibulum odio id dolor ultricies hendrerit. Ut dignissim feugiat lacinia. Donec ultrices tellus vel augue blandit accumsan. Mauris placerat eget nisi nec aliquet. Vestibulum vitae ipsum non sem rhoncus tempus nec in ante. Nullam sed felis in enim finibus imperdiet.

In vel risus suscipit, eleifend odio nec, venenatis nunc. Vestibulum et porttitor sem, eu scelerisque nunc. Aliquam vitae orci eros. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean molestie luctus magna, faucibus laoreet nisl vestibulum vel. Suspendisse eget euismod ipsum. Morbi sodales nunc id ligula tincidunt gravida.

Pellentesque condimentum sapien eget ex rhoncus elementum. Proin ac augue auctor, dignissim eros vitae, volutpat eros. Aenean sed imperdiet lectus. Proin faucibus elit at lorem imperdiet malesuada a a ante. Nunc non efficitur diam. Aliquam erat volutpat. Integer a lacus justo. Curabitur ultricies est a massa maximus bibendum. Sed feugiat nibh porttitor leo facilisis hendrerit. Nulla ac lectus non neque pharetra dignissim. Cras ut bibendum purus. Suspendisse pellentesque libero eu cursus accumsan.