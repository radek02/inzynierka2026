# Overview
Main recommendation service, responsible to generation of recommendations

# Run localy 
## .env
.env file should be created in RecommendationService\ directory and filled according to .env.example template. 

## Install dependencies
`pip install -r requirements.txt`

## Run 
`python -m app.main` will expose endpoints at `localhost:8001`, view Swagger at `localhost:8001/docs`

# Current functonality
## Generate user recommendation
Service expose one endpoint via address:
```
http://{host}:{port}/api/v1/Recommendations/user-recommendations/{user_id}
```
Calling this endoint you will get simple recommendations (some modules is not integrated yet).
 
