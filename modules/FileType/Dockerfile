FROM ace2-base
RUN yum install -y file && pip3 install cryptography
COPY --from=ace2-lib-ace2 / /
