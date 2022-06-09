FROM public.ecr.aws/lambda/python:3.9

# set install path
ENV ACE2 "/opt/ace2"

# update python path to include lib
ENV PYTHONPATH "${PYTHONPATH}:${ACE2}/lib"
