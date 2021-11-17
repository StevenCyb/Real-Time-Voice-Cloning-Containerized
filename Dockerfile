FROM ubuntu:18.04

# install python3
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 --no-cache-dir install --upgrade pip \
  && rm -rf /var/lib/apt/lists/*

# install PyTorch
RUN pip3 install torch==1.10.0+cpu torchvision==0.11.1+cpu torchaudio==0.10.0+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html

# install ffmpeg
RUN apt-get update && \
    apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:jonathonf/ffmpeg-4 \
    && apt install -y ffmpeg 

# copy stuff and install requirements
WORKDIR /app
COPY Real-Time-Voice-Cloning/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY interface.py interface.py
COPY ./Real-Time-Voice-Cloning .

# TODO run test and check out result if everhing is ok
CMD ["python3", "-u", "interface.py"]