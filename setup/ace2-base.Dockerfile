FROM public.ecr.aws/lambda/python:3.9

# update python path to include /opt/ace2/lib
ENV PYTHONPATH "${PYTHONPATH}:/opt/ace2/lib"
