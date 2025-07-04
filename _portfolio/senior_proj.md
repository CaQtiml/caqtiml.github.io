---
title: "Machine Learning for Financial Market"
excerpt: "My bachelor thesis for BEng Information and Communication Engineering"
collection: portfolio
---

{% include toc %}

## About this Project
This is a one-year compulsory final project for obtaining BEng Information and Communication Engineering from a Faculty of Engineering, Chulalongkorn U., Thailand. It is done in a group of three people, consisting of 
1. Sivakorn Lerttripinyo (which is me!)
2. Krittapasa Boontaveekul
3. Wirachapong Suwanphibun

This project is graded by three people, including one project advisor and two committees.
1. Advisor : Assoc. Prof. Chotirat Ratanamahatana, Ph.D
2. Committee Member : Asst. Prof. Kunwadee Sripanidkulchai, Ph.D
3. Committee Member : Lect. Aung Pyae, Ph.D

This blog will explain this project in an informal way, and in-depth details will be omitted. 

Although this project has already been concluded, this blog is not finished yet. Unfinished part in this blog will be filled with `--Underconstruction--`. However, you can read the slide I (and my friends) used for presenting the project [here](/files/slide_Machine_Learning_Bot_for_Financial_Market_final.pdf).


## Project Background
In the investment field, many people collect a set of history prices to analyze them to make a trading decision. For example, history prices of Bitcoin are collected to predict if the price is going to increase or decrease.

There is an idea that the computer maybe able to predict the price trend of these financial products by learning from the historical data, so a machine learning becomes more popular tools. If a robust model that can precisely predict the price trend can be trained, it will create a lot of profit to the user. 

However, implementing a robust machine learning model is, in fact, not a simple task since training the model does not involve only a training step. The model training is only a part of the entire machine learning system.

![mlsyscomponent](/images/senior_proj/ml-comp.png)

- A data collection and processing is required to be a reliable data source for training the models.
- Infrastructures, such as VMs and databases, is required for implementing a system.
- A configuration to train each model (such as a set of hyperparameters) should be recorded along with each trainded model.
- A system to manage the deployed is essential since we are going to train a lot of models.

So, this project is intended to design and implement the system going beyond the machine learning experiment. The system will show the system for ingesting and preparing data; systematically tracking the conducted experiments and storing related metadata including but not limited to training results, hyperparameters, and models; and deploying selected version of model to the real-world application.

This project chooses to use cryptocurrency data to implement the system, but it can be easily adapted to be used with other financial products, such as a stock price, as well. I mean the system is the same, but you just only change the dataset.

## Overview of this Project Structure
This project consists of two main components.
1. System Component, which is about how we design the system.
2. Model Training Component, which is about how we do a feature engineering, choose and tune the ML algorithms, and evaluate the training result.

## System Component

### Design Requirements
A machine learning system that targets for a model deployment involves the following steps.
- Data Extraction
- Data Analysis
- Data Preparation
- Model Training
- Model Evaluation
- Model Validation
- Model Serving
- Model Monitoring

I use MLOps maturity model to evaluate how much MLOps principles and practices are applied into the system. There is no standardized maturity model, but there are proposals from Google and Microsoft. For [Google](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning), the maturity level can be determined by the level of automation of these components. For [Microsoft](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/mlops-maturity-model), the maturity model is evaluated by the technical capability.

This project attempts to achieve features from Microsoft’s MLOps Level 2: Automated Training. Some requirements are as below.

- A data pipeline automatically gathers data.
- Experiment results are tracked.
- Both the training code and the resulting models are version-controlled.
- The models are released manually, which are managed by software engineering team.
- Implementing models are heavily reliant on data scientist expertise.
- Application code has unit tests.
- Basic integration tests exist for the model.

### Design Detailed Description
#### Infrastructure as Code (IaC)
--Underconstruction--
#### Database
--Underconstruction--
#### Data Ingestion
--Underconstruction--
#### Data Transformation
--Underconstruction--
#### Training Management System
--Underconstruction--
#### Model Monitoring
--Underconstruction--
#### Model Building and Serving
--Underconstruction--