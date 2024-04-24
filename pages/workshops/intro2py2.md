title: Intro to Data Analysis with Python and Pandas
hours: 15
date: 2023-11-17
sessions:
    - date: 11.13.2023
      start_time: 9h00
      end_time: 12h30
      location: online
    - date: 11.14.2023
      start_time: 9h00
      end_time: 12h30
      location: online
    - date: 11.15.2023
      start_time: 9h00
      end_time: 12h30
      location: online
    - date: 11.16.2023
      start_time: 9h00
      end_time: 12h30
      location: online
    - date: 11.17.2023
      start_time: 9h00
      end_time: 12h30
      location: online
main_instructor: Sangeetha Nandakumar
assistants:
    - Ben Hastings
    - Mohammad Bashiri
    - Nicholas Del Grosso
github_repo: https://github.com/ibehave-ibots/iBOTS-Tools/tree/main/workshops/intro-to-python-and-pandas2
summary:  | 
    In this hands-on workshop, we will explore the Python and Pandas data analysis ecosystem in depth, applying them to data analysis of a real-world electrophysiology neuroscience experiment! Collaboration sessions see participants working in small teams, collaborating to learn new skills and share their perspectives in a diverse environment.  Libraries like Numpy, XArray, Seaborn, Pingouin, and Matplotlib will help span the data analysis path between processed neuroscience data and final results.
registration_link: https://us02web.zoom.us/j/86906426337?pwd=S2owMUowSGpSb1FiNzh3N3JGdUk0Zz09
format: online
class_size: 25
preparation_instructions: |
    Software installation instructions will be sent before the start of the course.
certificate_criteria: | 
    At the end of the course, participants who attend at least 80% of the course certificates of participation.
--- 

##  Intro to Data Analysis with Python and Pandas

In this hands-on workshop, we will explore the Python and Pandas data analysis ecosystem in depth, applying them to data analysis from the world of neuroscience! Morning collaboration sessions see participants working in small teams, collaborating to learn new skills and share their perspectives in a diverse environment.

At the end of each session, interactive Jupyter notebooks that explore the tools introduced the day will be available for independent learning and review, with teachers available to answer questions. People of all skill levels, experiences, and backgrounds are welcome!


**Workshop Dates:**

{% for session in page.sessions %}
- {{ session.date }}, {{ session.start_time }}-{{ session.end_time}} ({{ session.location }})
{% endfor %}

**Assessment & Credits:**

- No exams
- {{ page.certificate_criteria }}
- {{ page.duration }} hours
