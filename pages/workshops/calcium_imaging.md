title: Intro to Calcium Imaging Analysis with Python and CaImAn
duration: 15 hrs over 2.5 days

date: 2023-02-28
sessions:
    - date: 28.02.2024
      start_time: 14h00
      end_time: 17h00
      location: online
    - date: 29.02.2024
      start_time: 9h30
      end_time: 17h00
      location: online
    - date: 01.03.2024
      start_time: 9h30
      end_time: 17h00
      location: online
instructors:
    - name: {{ data.people.sangeetha.name }}
      role: instructor      
    - name: {{ data.people.oliver.name }}
      role: assistant
github_repo: https://github.com/ibehave-ibots/iBOTS-Tools/tree/main/workshops/intro_to_calcium_imaging
summary: CaImAn is a popular Python package for processing and extracting calcium imaging data. In this workshop, we’ll use Python and CaImAn to perform basic image operations, understand some techniques behind calcium imaging analysis, and run calcium imaging analyses.
registration_link: https://us02web.zoom.us/meeting/register/tZYuduiqqT0iHtcRAQa9i94dZnrVIfjw0OLc#/registration
format: Online on Zoom, Hands-On Course.
class_size: 25
preparation_instructions: |
    Software installation instructions will be sent before the start of the course.
certificate_criteria: | 
    At the end of the course, participants who attend at least 80% of the course certificates of participation.
prerequisites: Some Prior Experience with Matlab, Python, or R
---

## {{ page.title }}

Calcium imaging is a popular and powerful technique for probing the activity of individual neurons with unprecedented detail. To process and extract these neuronal signals, Python has a wide ecosystem of tools, including CaImAn, a popular workflow package for analyzing calcium imaging data. From image de-noising and artefact reduction to cell segmentation and neuronal signal source extraction, CaImAn will help in getting more control over the quality and efficiency of processing and analysis. 

In this workshop, we will first explore the concepts behind the pre-processing and processing stages involved in calcium imaging with popular Python packages like Numpy, OpenCV, and Matplotlib. With this background knowledge, we will then use CaImAn and its powerful customization capabilities that will enable us to quickly and efficiently get data ready for analysis. Further, we will dive into advanced topics that appear in real-world situations, including connecting to a GPU for high-performance processing and managing TIFF image data using the Tifffile Python package.

By the end of the workshop, we will be able use Python to perform basic image operations, gain a better understanding of some techniques that go behind calcium imaging analysis, and become more confident customizing the wide variety of options in CaImAn to suit our calcium imaging data.

**Trainers**

{% for person in page.instructors %}
  - {{ person.name }}: {{ person.role }}
{% endfor %}

**Prerequisites:** {{ page.prerequisites }} 

**Duration:** {{ page.duration }}

**Dates (Times):**

{% for session in page.sessions %}
- {{ session.date }}, {{ session.start_time }}-{{ session.end_time}} ({{ session.location }})
{% endfor %}


**Workshop Format:** {{ page.format }} {{ page.class_size }} Participants Max.

**Workshop Preparation:** {{ page.preparation_instructions }}

{{ page.certificate_criteria }}
