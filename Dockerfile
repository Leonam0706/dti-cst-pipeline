# Production Container Specification for dMRI CST Tractography Pipeline
FROM ubuntu:24.04

LABEL maintainer="Clinical dMRI Pipeline Team"
LABEL description="Reproducible container for CST tractography & clinical QA reporting"

ENV DEBIAN_FRONTEND=noninteractive
ENV FSLDIR=/usr/share/fsl/5.0
ENV PATH=$FSLDIR/bin:$PATH

# Install core system packages & Python environment
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-nibabel \
    python3-numpy \
    python3-pandas \
    python3-matplotlib \
    fsl-core \
    bash \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /pipeline

# Copy repository code
COPY . /pipeline

# Default entrypoint runs full pipeline
ENTRYPOINT ["/bin/bash", "run_pipeline.sh"]
