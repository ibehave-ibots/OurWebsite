title: Intro to (M)EEG Analysis with MNE-Python
summary: |
    Would you like to learn more about (M)EEG analysis and programming in Python? By the course's end, you’ll have an understanding of how to install and setup a Python environment with MNE and be able use it to analyze your (M)EEG data.
duration: 15
sessions:
    - date: 2024-07-02
      start_time: 14h00
      end_time: 17h00
      location: online
    - date: 2024-08-02
      start_time: 9h30
      end_time: 17h00
      location: online
    - date: 2024-09-02
      start_time: 9h30
      end_time: 17h00
      location: online
instructors:
  - name: {{ data.people.thomas.name }}
    role: instructor
  - name: {{ data.people.sangeetha.name }}
    role: assistant
  - name: {{ data.people.nick.name }}
    role: assistant
github_repo:  |
    https://github.com/ibehave-ibots/iBOTS-Tools/tree/main/workshops/mne_course
registration_link: |
    https://us02web.zoom.us/meeting/register/tZ0uf-utqj0vGdI5V0ouc_qthEQJyvejqqRU
format: Online, Hands-On Course
class_size: 25
perequisites: |
    People of all skill levels, experiences, and backgrounds are welcome!
preparation_instructions: |
    Software installation instructions will be sent before the start of the course.
certificate_criteria: | 
    At the end of the course, participants who attend at least 80% of the course certificates of participation.
--- 

## {{ page.title }}

Do you have EEG or MEG data, and would like to use Python to analyze it?  Would you like to learn more about (M)EEG analysis, plus a little Python programming?  With over 150 researchers contributing to its open project, the rapidly-growing MNE-Python library is just the package to learn!  

In this hands-on workshop, led by a contributor to the MNE source code and an author of MNE-Connectivity (https://github.com/mne-tools/mne-connectivity) Thomas Binns, and offered in collaboration with the Charité, we’ll walk through the basics of EEG analysis with the MNE package.  From understanding how to load data into MNE’s data structures to doing spectral filtering, artifact rejection, and ERP analysis, the workshop is designed to help you get started in doing your analysis in Python.  We’ll even look at some impressive features of MNE, including inverse modeling to brain sources and connectivity analysis.

By the course's end, you’ll have an understanding of how to install and setup a Python environment with MNE and be able to write analysis notebooks on standard (M)EEG data.  And, who knows? Some requested features and discoveries during the course may appear in future versions of MNE and MNE-Connectivity!  

Intended Participants: {{ page.audience }}

**Duration:** {{ page.duration }} hrs

**Dates (Times):**

{% for session in page.sessions %}
- {{ session.date }}, {{ session.start_time }}-{{ session.end_time}} ({{ session.location }})
{% endfor %}

**Workshop Format:** {{ page.format }}

**Workshop Preparation:** {{ page.preparation_instructions }}

{{ page.certification_criteria }}