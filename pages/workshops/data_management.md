title: Intro to File- and Database-oriented Neuroscience Data Management With Python, SQL, and HDF5
summary: |
    What is all this hype about databases, and how can I use them to make my analysis work simpler?  In this workshop, you’ll build databases and query them in Python and SQL using DuckDB, store complex data in HDF5, and host it with Git and GitHub.
hours: 15
sessions:
- date: 2024-02-22
  start_time: 9h30
  end_time: 17h00
  location: online
- date: 2024-02-23
  start_time: 9h30
  end_time: 17h00
  location: online
instructors:
  - name: {{ data.people.nick.name }}
    role: instructor
github_repo: |
    https://github.com/ibehave-ibots/iBOTS-Tools/tree/main/workshops/data-management
registration_link: |
    https://us02web.zoom.us/meeting/register/tZctcuCoqTwtE927LBOm_u8zlNJIQbxZeONv#/registration
format: Online, Hands-On Course. 
class_size: 25
preparation_instructions: |
    Software installation instructions will be sent before the start of the course.
certificate_criteria: | 
    At the end of the course, participants who attend at least 80% of the course certificates of participation.
---

## {{ page.title }}

Neuroscience is evolving rapidly, with experimental data becoming increasingly complex. How can you seamlessly integrate vast and diverse datasets for insightful analysis and easy sharing? And how would your process improve if, instead of having to write long scripts, you could analyze data with just a few lines of code?

In this workshop, discover the power of database management systems, a game-changer in neuroscience research. We will dive into the world of SQL and learn about DuckDB SQL engine, which makes it easy to apply industry-standard data organization methods to research data as a relational database – no server management needed! You'll also gain hands-on experience with HDF5 and JSON for key-value data storage and learn how to  combine various management techniques for optimal convenience and performance by building hybrid database systems. 

By the course's end, you'll be adept at writing Python scripts to create and extract data from databases, query large databases in SQL, store complex data in HDF5, manage your work with Git, and publish your projects on GitHub.

**Trainers**

{% for person in page.instructors %}
  - {{ person.name }}: {{ person.role }}
{% endfor %}

**Prerequisites:** This workshop is ideal for Neuroscience Researchers at any level (Masters, PhD Candidate, Postdoc, PI) with some background in data analysis using Matlab, Python, or R.

**Duration:** {{ page.duration }}

**Dates (Times):**

{% for session in page.sessions %}
- {{ session.date }}, {{ session.start_time }}-{{ session.end_time}} ({{ session.location }})
{% endfor %}

**Workshop Format:** {{ page.format }}

**Workshop Preparation:** {{ page.preparation_instructions }}

{{ page.certificate_criteria }}