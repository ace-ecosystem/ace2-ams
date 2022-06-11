FROM public.ecr.aws/lambda/python:3.9 AS ace2-base
# set install path
ENV ACE2 "/opt/ace2"
# update python path to include /opt
ENV PYTHONPATH "${PYTHONPATH}:/opt"


FROM ace2-base AS ace2
# install deps
RUN pip3 install boto3 pydantic pytest pytest-datadir pyyaml
# install source
COPY ace2 ${ACE2}
# install config if one exists
ARG env
COPY config-$env.ym[l] ${ACE2}/config.yml
# test
COPY tests tests
RUN pytest -vv && rm -rf tests/ace2
