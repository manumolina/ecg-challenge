# Product Software Engineer Backend

<p style="text-align:center;" align="center"><a href="https://idoven.ai/"><img align="center" style="margin-bottom:20px;" src="https://dayonecaixabank.es/wp-content/uploads/2020/07/Cabecera_idoven.jpg"  width="30%" /></a><br /><br /></p>

This API is created under the requeriments proposed by Idoven, for the job offer:  
"Product Software Engineer Backend at Idoven".  
<a href="https://github.com/idoven/backend-challenge/blob/main/README.md">Backend Coding Challenge</a>

At Idoven, we have a specific requirement. We aim to implement a microservice that accepts electrocardiograms (ECG) and provides various insights about them, such as calculating the number of zero crossings of the signal.

## Table of contents
* [General info](#general-info)
* [Requirements](#requirements)
* [Technical Specifications](#technical-specifications)
* [Technologies and libraries](#technologies-and-libraries)
* [Setup](#setup)
* [Technical decisions](#technical-decisions)
* [Documentation](#documentation)
* [Tests](#tests)
* [Status](#status)
* [Contact](#contact)

## General info
This technical task is divided in two services.
* the first one contains the API server, using FastAPI as a main framework.
* the second one is database server, using MongoDB.

## Requirements

Create an API that offers two main endpoints:
1. An endpoint to receive the ECGs for processing.
* Users can access only the ECGs they've uploaded.
2. An endpoint to return the associated insights.
* The information to be returned by the endpoint should indicate the number of times each ECG channel crosses zero. At this stage, we don't require any other data.

In addition to these two, some user administration endpoints were generated.
All of them are only allowed to authenticated users with the admin role.
1. Login
2. Get list of users
3. Creates a new user

## Technical Specifications

In undertaking this assignment, you're afforded the autonomy to select your preferred programming language, technologies, frameworks, documentation techniques, and testing strategy.  

We highly value solutions that prioritize readability, maintainability, and the thoughtful application of design patterns and architectural principles. While you have flexibility, keep in mind our primary tech stack revolves around Python and FastAPI.

## Technologies and libraries
API
* Python 3.10 (primary language)
* FastAPI 0.95.1 (framework)
* Uvicorn (server) 
* Nginx (proxy)
* Coverage (testing)
* Pytest (testing)
* Ruff (linting + code formatting)

## Setup
The easiest way to work with this server program is working with Docker containers.  
I recommend you the next steps:
> git clone https://github.com/manumolina/idoven-challenge/  
> cd idoven-challenge  
> docker-compose build  
> docker-compose up -d  

## Technical decisions
The back-end chosen to complete this task is [FastAPI](https://fastapi.tiangolo.com/). The main reasons are:
* simplicity of the framework 
* short development time
* very fast responses
* support for asynchronous code
* easy testing
* include OpenAPI specification to describe our entire API

Regarding the database, I decided to work with PostgreSQL because:
* totally integrated with Python and SQLModel
* possibility to use multidimensional arrays
* simple installation

User Management:  
* Because the user management is not included in the scope of the challenge, users can't add its own password.  
* Passwords are generated automatically and returned to the user to be saved.

## Documentation
You can find the complete documentation of the API 
(metadata, endpoints, schemas, operation parameters, etc..) in the next URLs provided by FastAPI: 

http://localhost:5001/docs  
http://localhost:5001/redoc

## Tests
To check the current coverage of the server program:  
> docker exec -it idoven-challenge-api /bin/bash  
> poetry run pytest --cov -v -p no:warnings --no-cov-on-fail tests/  

or  

> docker exec idoven-challenge-api poetry run pytest --cov -v -p no:warnings --no-cov-on-fail tests/  

At the time the environment is created, three test users are also created:  
> admin@idoven-challenge.com:VYZfg8w7xvIUR7GdzjrIgYUNnjIKFM9R  
> user_1@idoven-challenge.com:gCPiYzbjE3VrUXYzFLq3TIA0HlScjFdS  
> user_2@idoven-challenge.com:smz4Ui79xCNxZKaTgKkP82Yy0T1az0XU  

More users can be created using the appropriate endpoint.  

## Status
Project is: _in progress_  

## Contact
Created by [@manumolina](https://github.com/manumolina) - I hope to hear from you soon.
