# voice-style-transfer-backend


## Create Enviroment and Install requirements

- conda create --name <env> --file requirements.txt


## Run 

- uvicorn main:app --reload

### Check it

- http://127.0.0.1:8000/ 


### Interactive API docs (Swagger UI)

- http://127.0.0.1:8000/docs


### Alternative API docs (ReDoc)

- http://127.0.0.1:8000/redoc


# Docker

- docker build -t myimage .

- docker run -d --name mycontainer -p 80:80 myimage

- --host 0.0.0.0
