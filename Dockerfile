FROM python:3.6.3

ADD ./main.py /

RUN pip install requests
RUN pip install requests_oauthlib

# Set environment variables before run script
# CMD python main.py
