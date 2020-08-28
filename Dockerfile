FROM ubuntu:latest
COPY . /Metabolyze
WORKDIR /Metabolyze

ARG DEBIAN_FRONTEND=noninteractive



RUN set -e; \
    apt-get update && apt-get install -y \
    software-properties-common \
    tzdata \
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

RUN add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu disco-cran35/'
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
RUN apt-get install r-base

RUN python3 -m pip install -r requirements.txt

RUN R -e "install.packages('pheatmap',dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -e "install.packages('manhattanly',dependencies=TRUE, repos='http://cran.rstudio.com/')"


RUN alias python=python3

