# Real-Time-Voice-Cloning-Containerized
I'm not a big fan of installing tons of software to test something.
Therefore I have create an Docker image so you can run [Real-Time-Voice-Cloning
](https://github.com/CorentinJ/Real-Time-Voice-Cloning) just by having Docker.

## Build
Build the image:
```shell
docker build -t rtvcc .
```

## Run image
Before you run the image, configure it. 
Add your reference voice files to `./volume/samples` or use the provided files.
Open the `./volume/instruction.csv` and add what you want to generate:
```
Reference Speech;Output File Name;Speak the text;
reference_speech_1.mp3;filename_of_first_sentence.wav;Thing to say with first reference;
reference_speech_2.mp3;filename_of_second_sentence.wav;Thing to say with second reference;
```

Run the image on Windows:
```bash
docker run --name rtvcc \
  -v <path-to-pwd>/volume:/volume rtvcc \
  ; docker rm rtvcc
```

Run the image on Unix:
```shell
docker run --name rtvcc \
  -v $(pwd)/volume:/volume rtvcc \
  rtvcc \
  ; docker rm rtvcc
```

## Delete all images
If you want to delete all images
```shell
docker rmi -f $(docker images -aq)
```