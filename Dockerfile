FROM python:3.8

ENV WEBAPP_DIR=/spaceiz_chat

RUN mkdir $WEBAPP_DIR
WORKDIR $WEBAPP_DIR

ENV DJANGO_SETTINGS_MODULE spaceiz_chat.settings
ADD requirements.txt $WEBAPP_DIR/
RUN pip install -r requirements.txt