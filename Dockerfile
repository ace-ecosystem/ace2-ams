# set the base image in single location
ARG base=public.ecr.aws/lambda/python:3.9

# build ace2 base image
FROM $base AS ace2
    # install ace2 deps
    RUN pip3 install boto3 pydantic pytest pytest-datadir pyyaml

    # install ace2 source
    COPY ace2 ace2

    # run tests
    # remove test files
    COPY tests tests
    RUN pytest -vv &&\
        rm -rf tests/ace2 &&\
        rm -rf /tmp/pytest* &&\
        find / \( -name "*.pyc" -or -name ".pytest_cache" -or -name "__pycache__" \) -exec rm -rf {} +

# build service image
FROM $base AS service
    DEPENDENCIES

    # copy everything from ace2 base image
    COPY --from=ace2 / /

    # install source
    ARG name
    COPY services/$name ./

    # rename desired settings file
    # remove unused settings files
    # run tests
    # remove test files and dependencies
    ARG settings
    RUN mv $settings settings.yml || true &&\
        rm settings-*.yml || true &&\
        pytest -vv &&\
        rm -rf tests &&\
        rm -rf /tmp/pytest* &&\
        find / \( -name "*.pyc" -or -name ".pytest_cache" -or -name "__pycache__" \) -exec rm -rf {} + &&\
        pip3 uninstall -y pytest-datadir pytest

    # set entrypoint
    CMD [ "service.run" ]
