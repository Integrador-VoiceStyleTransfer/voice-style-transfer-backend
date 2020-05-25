FROM conda/miniconda3

WORKDIR /app

COPY ./app /app

RUN conda create --name conda_vst --file requirements.txt

CMD uvicorn main:app --reload

