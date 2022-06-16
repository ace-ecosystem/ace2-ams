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
# install settings
ARG env
COPY settings-$env.ym[l] ${ACE2}/settings.yml
# test
COPY tests tests
RUN pytest -vv && rm -rf tests/ace2 /tmp/pytest* && find / -type d -name ".pytest_cache" -exec rm -rf {} +
