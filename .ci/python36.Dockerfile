FROM python:3.6

RUN adduser --uid 1000 jenkins

USER jenkins