FROM public.ecr.aws/lambda/python:3.9

# create ace2 directory layout
RUN mkdir /opt/ace2 /opt/ace2/lib /opt/ace2/etc /opt/ace2/etc/modules /opt/ace2/etc/services

# update python path to include /opt/ace2/lib
ENV PYTHONPATH "${PYTHONPATH}:/opt/ace2/lib"
