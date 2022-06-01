# parent image should already have ace2 lib installed
# FROM ace2-base AS FileType
FROM test-module-base-image AS module-filetype

# add the module script to the image
ADD module.py module.py

# add dependencies
RUN pip3 install cryptography
RUN yum install file -y