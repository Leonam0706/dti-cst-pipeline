FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-nibabel \
    python3-numpy \
    python3-pandas \
    python3-matplotlib \
    bash \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set up pipeline directory
WORKDIR /pipeline
COPY . /pipeline

# Mock FSL environment variables for container execution
ENV FSLDIR=/usr/share/fsl
ENV PATH=$FSLDIR/bin:$PATH
ENV FSLOUTPUTTYPE=NIFTI_GZ

CMD ["bash", "run_pipeline.sh"]
