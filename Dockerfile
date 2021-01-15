FROM python:3

WORKDIR /home/ariel8462/Code/FreeOnEpicBot

ADD . /home/ariel8462/Code/FreeOnEpicBot

RUN pip install -r /home/ariel8462/Code/FreeOnEpicBot/requirements.txt

ENV PORT 3000
EXPOSE $PORT

CMD [ "python", "/home/ariel8462/Code/FreeOnEpicBot/FreeOnEpicBot.py" ]
