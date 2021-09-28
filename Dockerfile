FROM python:3

RUN python3 -m venv /opt/venv

WORKDIR $HOME/service

COPY . .

EXPOSE 80

RUN . /opt/venv/bin/activate && pip install -r requirements.txt

CMD . /opt/venv/bin/activate && uvicorn service.app.main:app --debug --host 0.0.0.0 --port 80

