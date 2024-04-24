title: Intro to Python and Pandas for Neuroscientists
hours: 22
date: 2023-11-10
sessions:
  - date: 11.06.2023
    start_time: 09h00
    end_time: 12h30
    location: online
  - date: 11.07.2023
    start_time: 09h00
    end_time: 12h30
    location: online
  - date: 11.08.2023
    start_time: 09h00
    end_time: 12h30
    location: online
  - date: 11.09.2023
    start_time: 09h00
    end_time: 12h30
    location: online
  - date: 11.10.2023
    start_time: 09h00
    end_time: 12h30
    location: online
instructors:
  - name: {{ data.people.mohammad.name }}
    role: instructor
  - name: {{ data.people.ben_h.name }}
    role: assistant
  - name: {{ data.people.nick.name }}
    role: assistant
  - name: {{ data.people.sangeetha.name }}
    role: assistant
github_repo: https://github.com/ibehave-ibots/iBOTS-Tools/tree/main/workshops/intro-to-python-and-pandas
summary: |
  In this hands-on workshop, we will explore the Python and Pandas data analysis ecosystem in depth, applying them to data analysis of a real-world electrophysiology neuroscience experiment! Collaboration sessions see participants working in small teams, collaborating to learn new skills and share their perspectives in a diverse environment.  Libraries like Numpy, XArray, Seaborn, Pingouin, and Matplotlib will help span the data analysis path between processed neuroscience data and final results.
registration_link: https://us02web.zoom.us/j/86906426337?pwd=S2owMUowSGpSb1FiNzh3N3JGdUk0Zz09
format: online
class_size: 25
preparation_instructions: |
    Software installation instructions will be sent before the start of the course.
certificate_criteria: | 
    At the end of the course, participants who attend at least 80% of the course certificates of participation.
--- 

# Intro to Python and Pandas for Neuroscientists

In this hands-on workshop, we will explore the Python and Pandas data analysis ecosystem in depth, applying them to data analysis from the world of neuroscience!  Morning collaboration sessions see participants working in small teams, collaborating to learn new skills and share their perspectives in a diverse environment.  

At the end of each session, interactive Jupyter notebooks that explore the tools introduced the day will be available for independent learning and review, with teachers available to answer questions.  People of all skill levels, experiences, and backgrounds are welcome!

**Trainers**

{% for person in page.instructors %}
  - {{ person.name }}: {{ person.role }}
{% endfor %}

**Workshop Dates:**

{% for session in page.sessions %}
- {{ session.date }}, {{ session.start_time }}-{{ session.end_time}} ({{ session.location }})
{% endfor %}

**Assessment & Credits:**

- No exams
- {{ page.certificate_criteria }}
- {{ page.duration }} hours 