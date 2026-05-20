# Use the official Ubuntu 18.04 as a base image
FROM ubuntu:18.04
# Install necessary repositories and core dependencies
RUN apt-get update && \
    apt-get install -y software-properties-common lsb-release wget build-essential libssl-dev zlib1g-dev \
    libncurses5-dev libnss3-dev libgdbm-dev libreadline-dev libffi-dev curl libbz2-dev
# Install Python 3.10 from source
RUN wget https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz && \
    tar -xf Python-3.10.0.tgz && \
    cd Python-3.10.0 && \
    ./configure --enable-optimizations && \
    make -j $(nproc) && \
    make altinstall && \
    ln -s /usr/local/bin/python3.10 /usr/bin/python3.10
# Install core system capabilities required
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    bc \
    build-essential \
    curl \
    dc \
    git \
    libegl1-mesa-dev \
    libopenblas-dev \
    nano \
    python2.7 \
    tar \
    tcsh \
    tzdata \
    unzip \
    wget \
    x11-apps \
    x11-xserver-utils
# Ensure python3 points to python3.10
RUN ln -sf /usr/local/bin/python3.10 /usr/bin/python3
# Download and install pip using curl with -k option to bypass SSL certificate validation
RUN curl -k https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3 get-pip.py && \
    ln -sf /usr/local/bin/pip3 /usr/bin/pip3
# Upgrade pip and install necessary Python packages
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install tqdm numpy==1.21.0
# Copy project files into the container
COPY . .
COPY src /src
COPY requirements.txt .
# Ensure any scripts to be executed are executable
#RUN chmod +x install.sh
# Run the install script
#CMD ["./install.sh"]

# Add NeuroDebian repository and install FSL
#RUN wget -O- http://neuro.debian.net/lists/bionic.us-tn.full | tee /etc/apt/sources.list.d/neurodebian.sources.list && \
#    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 0xA5D32F012649A5A9 || \
#    apt-key adv --keyserver hkp://keyserver.keyserver.ubuntu.com:80 --recv-keys 0xA5D32F012649A5A9 || \
#    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys A5D32F012649A5A9 || \
#    (gpg --keyserver keyserver.ubuntu.com --recv-keys A5D32F012649A5A9 && gpg --export --armor A5D32F012649A5A9 | apt-key add -) && \
#    apt-get update && \
#    apt-get install -y fsl-core
# Set FSL environment variables
#ENV FSLDIR=/usr/share/fsl/6.0
#ENV PATH=${FSLDIR}/bin:${PATH}
#ENV FSLOUTPUTTYPE=NIFTI_GZ
# RUN echo ". /opt/fsl/etc/fslconf/fsl.sh" >> ~/.bashrc
 #CMD ["/bin/bash", "-c", "source /opt/fsl/etc/fslconf/fsl.sh && /bin/bash"]

RUN wget https://fsl.fmrib.ox.ac.uk/fsldownloads/fsl-5.0.11-centos6_64.tar.gz && \
    tar zxvf fsl-5.0.11-centos6_64.tar.gz -C /opt && \
    /opt/fsl/etc/fslconf/fslpython_install.sh -f /opt/fsl && \
    rm fsl-5.0.11-centos6_64.tar.gz
#RUN wget -O- http://neuro.debian.net/lists/xenial.cn-bj1.full | sudo tee /etc/apt/sources.list.d/neurodebian.sources.list
#RUN sudo apt-key adv --recv-keys --keyserver hkp://pool.sks-keyservers.net:80 0xA5D32F012649A5A9
#RUN apt-get update && apt-get install -y \
#    fsl#-5.0-complete
###############################################################################
RUN apt-get update && apt-get install -y \
    wget \
    git \
    g++ \
    gcc \
    zlib1g-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libexpat1-dev \
    libbz2-dev \
    libx11-dev \
    libglu1-mesa-dev \
    libxt-dev \
    libfftw3-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*
# Install CMake 3.22.0
RUN wget https://github.com/Kitware/CMake/releases/download/v3.22.0/cmake-3.22.0-linux-x86_64.sh \
    && chmod +x cmake-3.22.0-linux-x86_64.sh \
    && ./cmake-3.22.0-linux-x86_64.sh --skip-license --prefix=/usr/local \
    && rm cmake-3.22.0-linux-x86_64.sh
# Clone ANTs repository and build
#RUN git clone https://github.com/ANTsX/ANTs.git /opt/ANTs \
#    && cd /opt/ANTs \
#    && mkdir build \
#    && cd build \
#    && cmake ../ \
#    && make -j $(nproc)
#RUN git clone https://github.com/ANTsX/ANTs.git /opt/ANTs \
#    && cd /opt/ANTs \
#    && mkdir build \
#    && cd build \
#    && cmake -DBUILD_TESTING=OFF ../ \
#    && make -j $(nproc)


# Install CMake 3.22.0 (pinned - do not upgrade)
RUN apt-get update && apt-get install -y --no-install-recommends wget ca-certificates \
    && wget -q https://github.com/Kitware/CMake/releases/download/v3.22.0/cmake-3.22.0-linux-x86_64.sh \
    && chmod +x cmake-3.22.0-linux-x86_64.sh \
    && ./cmake-3.22.0-linux-x86_64.sh --skip-license --prefix=/usr/local \
    && rm cmake-3.22.0-linux-x86_64.sh

# Clone ANTs at specific commit (pinned - matches cmake 3.22.0 requirement)
RUN git clone https://github.com/ANTsX/ANTs.git /opt/ANTs \
    && cd /opt/ANTs \
    && git checkout v2.4.3 \
    && mkdir build \
    && cd build \
    && cmake -DBUILD_TESTING=OFF ../ \
    && make -j $(nproc)


# List build output (for debug)
RUN ls -R /opt/ANTs/build

# Move ANTs binaries to /usr/local/bin
RUN find /opt/ANTs/build -name "ants*" -type f -executable -exec cp {} /usr/local/bin/ \;

# Add ANTs to PATH
ENV PATH="/usr/local/bin:$PATH"

# Test the installation
RUN antsRegistration --version || true



# Set FSLDIR environment variable
ENV FSLDIR=/opt/fsl
ENV PATH=$FSLDIR/bin:$PATH
ENV FSLOUTPUTTYPE=NIFTI_GZ

RUN cat > /opt/fsl/bin/imcp <<'EOF'
#!/usr/bin/env bash
set -e
# Minimal replacement for FSL imcp
# Usage: imcp <input> <output>
in="$1"
out="$2"
if [ -z "$in" ] || [ -z "$out" ]; then
  echo "Usage: imcp <input> <output>" >&2
  exit 1
fi
cp -f "$in" "$out"
EOF
RUN chmod +x /opt/fsl/bin/imcp && ls -l /opt/fsl/bin/imcp



# Upgrade pip, setuptools, and wheel
RUN pip3 install --upgrade pip setuptools wheel

RUN cd

# Install packaging separately as requested
RUN pip3 install packaging

# Upgrade pip again as requested
RUN pip3 install --upgrade pip

# Install HDF5 (Ubuntu 18.04 Bionic package names)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libhdf5-100 \
    libhdf5-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Pre-install h5py using pre-built wheel (no compilation needed)
RUN pip3 install --only-binary=h5py "h5py==3.8.0"

# Copy requirements.txt into the working directory
COPY requirements.txt .

# Install the rest of the dependencies from requirements.txt
RUN pip3 install -r requirements.txt

# reinstall SimpleITK
RUN python3.10 -m pip install SimpleITK==2.1.1.2

# Move ANTs binaries to /usr/local/bin from the correct directory
RUN cp -r /opt/ANTs/build/ANTS-build/Examples/* /usr/local/bin/

RUN pip3 install fuzzy-c-means
RUN ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=8
RUN export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS
WORKDIR /

RUN mkdir -p /src/Template
RUN wget http://packages.bic.mni.mcgill.ca/mni-models/icbm152/mni_icbm152_lin_nifti.zip
RUN wget http://www.bic.mni.mcgill.ca/~vfonov/icbm/2009/mni_icbm152_nlin_asym_09c_nifti.zip
RUN unzip -p mni_icbm152_nlin_asym_09c_nifti.zip mni_icbm152_nlin_asym_09c/mni_icbm152_wm_tal_nlin_asym_09c.nii >/src/Template/mni_icbm152_wm_tal_nlin_asym_09c.nii
RUN unzip -p mni_icbm152_nlin_asym_09c_nifti.zip mni_icbm152_nlin_asym_09c/mni_icbm152_t2_tal_nlin_asym_09c.nii >/src/Template/mni_icbm152_t2_tal_nlin_asym_09c.nii
RUN unzip -p mni_icbm152_lin_nifti.zip icbm_avg_152_t1_tal_lin.nii >/src/Template/icbm_avg_152_t1_tal_lin.nii
RUN gzip /src/Template/icbm_avg_152_t1_tal_lin.nii

# Update and install required packages
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    cmake \
    zlib1g-dev \
    libopenjp2-7-dev \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

# Clone and build dcm2niix
RUN git clone https://github.com/rordenlab/dcm2niix.git /opt/dcm2niix \
    && cd /opt/dcm2niix \
    && mkdir build && cd build \
    && cmake -DZLIB_IMPLEMENTATION=Cloudflare -DUSE_JPEGLS=ON -DUSE_OPENJPEG=ON .. \
    && make \
    && make install

# Set the PATH to include dcm2niix binary
ENV PATH="/opt/dcm2niix/build:${PATH}"

RUN mkdir -p /data/logs

ENTRYPOINT ["sh", "-c", "mkdir -p /data/logs && python3 -u $0 \"$@\" 2>&1 | tee /data/logs/pipeline_$(date +%Y%m%d_%H%M%S).log; chown -R $(stat -c '%u:%g' /data) /data"]
