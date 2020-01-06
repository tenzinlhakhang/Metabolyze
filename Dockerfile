FROM ubuntu:latest
COPY . /app
WORKDIR /app
RUN apt-get update && apt-get install -y r-base
RUN set -e; \
    apt-get update && apt-get install -y \
    r-base \
    linux-headers-generic \
    pkg-config \
    python3-pip \
    gcc \
    libc-dev \
    freetype2-demos \
    python3-dev \
    libpng-dev \
    libjpeg8-dev \
    libfreetype6-dev \
    libxml2-dev \
    libxslt-dev \
        ;
RUN python3 -m pip install -r requirements.txt

RUN R -e "install.packages('pheatmap',dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -e "install.packages('manhattanly',dependencies=TRUE, repos='http://cran.rstudio.com/')"




EXPOSE 5000
CMD python3 ./metabolyze.py


