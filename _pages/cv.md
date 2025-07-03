---
# layout: archive  # determine the page layout, which is in _layouts folder
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

Education
------
* MSc Computer Science, Uppsala University, Sweden (2024-2026)
* BSc Information and Communication Engineering, Chulalongkorn University, Thailand (2020-2024)

Work experience
------
* Research Engineer Intern
  * KASIKORN Business-Technology Group (KBTG)
  * Jun 2023 - Jul 2023

As a part of an image processing team, my main responsibility was to conduct an experiment on a scalable machine learning model. Normally, the model would not be able to classify the image that was not available on the training data; however, I changed a problem and created a model pipeline that could tell the similarity value of the new classes to the classes available in the training set. 

The objective was that we can still use the same model even if there was new data. For example, if we get a new passport from a new country that is not presented in the original training set, my model pipeline can still predict that this is the passport because the new passport looks similar enough to the passports in the training set. This experiment tried to decrease the need of retraining the model, which may incur a significant amount of cost.

* DevOps Engineer Intern
  * PRIMO World
  * Jan 2023 - Apr 2023

I focused on enhancing efficiency and optimizing cloud resources. I implemented automated workflows using scripting and cloud tools, replacing manual processes and improving accuracy. For example, I implement an automating VPN setup on AWS EC2 instances with a Terraform-based solution complemented by shell scripting, which achieved network isolation. I also developed a Terraform codebase for automated provisioning and management of AWS EC2 instances, reducing manual intervention and error rates. 

To address cost-efficiency, I implemented a cost-saving strategy using AWS Lambda to automatically shut down and restart EC2 instances during non-peak hours, optimizing resource usage. Additionally, I set up a dashboard using Grafana Synthetic Monitoring to monitor API statuses, ensuring continuous oversight of critical systems.

* Software Engineer Intern
  * CentrovisioN
  * Jun 2022 - Jul 2022

This company works in a building inspection field. There was an attempt to use a machine learning model to detect construction defects from images gathered by using drones. At that time, MaskRCNN was applied to create a proof-of-concept model. My responsibility was to create an API to take an image, send it to the model, and return the image with the defect annotations. Authentication system was also implemented so that only authorized users can use it. FastAPI was chosen to implement the API, and AWS services, such as AWS ECS and Fargate, are chosen to deploy the API.

Apart from implementing the API, I designed a data storage system for the company. Before doing this, data were stored haphazardly. Therefore, I organized the data storage. Unstructured data was stored in AWS S3 with a proper structure, and structured data was stored in AWS RDS PostgreSQL. Although seeming trivially, data can be retrieved more efficiently, which can increase the organization performance.
  
Skills
-------
* <b>Programming Language</b>: C++, Python, JavaScript
* <b>Databases</b>: MySQL, PostgreSQL, MongoDB, Schema Design, Indexing and Query Optimization
* <b>Cloud Platforms & Tools</b>: AWS (EC2, Lambda, S3, EventBridge, Glue, RDS), DigitalOcean
* <b>Infrastructure as Code (IaC)</b>: Terraform
* <b>DevOps & CI/CD</b>: Docker, Git, GitHub Actions
* <b>Machine Learning & MLOps</b>: Scikit-learn, TensorFlow, PyTorch, MLFlow (model versioning, experiment
tracking, and model registry)
* <b>Data Engineering & ETL</b>: Mage.ai, data pipeline design, data ingestion and transformation, data warehousing

Language
-------
* Thai (Native)
* English (Fluent - IELTS Academic 7.5 out of 9)
* Swedish (Elementary - Equivalent to CEFR A2)

Certificates and Achievements
-------
* [Microsoft Certified: Azure Fundamentals](https://www.credly.com/badges/090130c5-e4bf-43a3-b851-dae2ed10c2cd/public_url)
* [Microsoft Certified: Azure AI Fundamentals](https://www.credly.com/badges/6f4702c8-0f0e-4272-9daf-37704febb753/public_url)
* [Microsoft Certified: Azure Data Fundamentals](https://www.credly.com/badges/3cd9194a-34c6-4483-b1f5-82aea9a7596b/public_url)
* [Deep Learning Specialization: Coursera](https://coursera.org/share/6f53bce50d55ed6625df050195dc72bf)
* Participant: Thailand Olympiad in Informatics 15 (TOI 15)

Activities
----------
* <b>Thinc Club. Chula (2021-2024)</b>: Participated as a developer in a team to create a website for freshman activity registration. Actively involved in organizing club events and served as a speaker for a "JavaScript" session.
* <b>Academic Club, Chula Engineering (2021-2022)</b>: Contributed as a member of the academic team, focusing on providing review sessions for freshmen during midterm and final examinations.

<!-- Publications
======
  <ul>{% for post in site.publications reversed %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>
  
Talks
======
  <ul>{% for post in site.talks reversed %}
    {% include archive-single-talk-cv.html  %}
  {% endfor %}</ul>
  
Teaching
======
  <ul>{% for post in site.teaching reversed %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>
  
Service and leadership
======
* Currently signed in to 43 different slack teams -->
