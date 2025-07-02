FROM python:3.13-rc-alpine3.18

RUN ["mkdir", "/household-budget-shipper"]
RUN ["python3", "-m", "pip", "install", "requests", "chardet"]
WORKDIR /household-budget-shipper
COPY ./source .

ENTRYPOINT ["./entrypoint.sh"]