FROM python:2-alpine
WORKDIR /opt/redfish
COPY . /opt/redfish/
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python emulator.py -port 5000
