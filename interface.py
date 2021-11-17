from encoder.params_model import model_embedding_size as speaker_embedding_size
from utils.argutils import print_args
from utils.modelutils import check_model_paths
from synthesizer.inference import Synthesizer
from encoder import inference as encoder
from vocoder import inference as vocoder
from pathlib import Path
import numpy as np
import soundfile as sf
import librosa
import argparse
import torch
import sys
import os
from audioread.exceptions import NoBackendError

resultPath = '/volume'

print('Running test...\n')
if torch.cuda.is_available():
  device_id = torch.cuda.current_device()
  gpu_properties = torch.cuda.get_device_properties(device_id)
  ## Print some environment information (for debugging purposes)
  print('Found %d GPUs available. Using GPU %d (%s) of compute capability %d.%d with '
    '%.1fGb total memory.\n' % 
    (torch.cuda.device_count(),
    device_id,
    gpu_properties.name,
    gpu_properties.major,
    gpu_properties.minor,
    gpu_properties.total_memory / 1e9))
else:
  print('Using CPU for inference.\n')

enc_model_fpath = Path('encoder/saved_models/pretrained.pt')
syn_model_fpath = Path('synthesizer/saved_models/pretrained/pretrained.pt')
voc_model_fpath = Path('vocoder/saved_models/pretrained/pretrained.pt')

print('Check and load model...\n')
check_model_paths(encoder_path=enc_model_fpath,
                  synthesizer_path=syn_model_fpath,
                  vocoder_path=voc_model_fpath)

encoder.load_model(enc_model_fpath)
synthesizer = Synthesizer(syn_model_fpath)
vocoder.load_model(voc_model_fpath)

print('Process specification...\n')
if os.path.isdir(resultPath):
  if os.path.exists(resultPath + '/instruction.csv'):
    lastProcessedWav = ''

    count = 0
    embeds = []
    f = open(resultPath + '/instruction.csv', 'r')
    next(f)
    for line in f:
      count = count + 1
      if line == '':
        print('Line ' + str(count) + ' skipped\n')
        continue

      cells = line.split(';')
      referenceWav = resultPath + '/samples/' + cells[0]
      outFile = resultPath + "/" + cells[1]
      inText = [cells[2]]

      print('Process line ' + str(count) + '\n')
      
      if referenceWav != lastProcessedWav:
        lastProcessedWav = referenceWav
        processedWav = encoder.preprocess_wav(Path(referenceWav))
        originalWav, sampling_rate = librosa.load(referenceWav)
        preprocessedWav = encoder.preprocess_wav(originalWav, sampling_rate)
        
        embed = encoder.embed_utterance(preprocessedWav)
        embeds = [embed]

      specs = synthesizer.synthesize_spectrograms(inText, embeds)
      spec = specs[0]

      generatedWav = vocoder.infer_waveform(spec)
      generatedWav = np.pad(generatedWav, (0, synthesizer.sample_rate), mode='constant')
      generatedWav = encoder.preprocess_wav(generatedWav)

      sf.write(outFile, generatedWav.astype(np.float32), synthesizer.sample_rate)
      print(outFile)
    f.close()

print('Done.')