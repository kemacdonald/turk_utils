""" Small set of tests for Turk audio files.

Tests to check that Turk audio files contain data
that are in the correct format for Kaldi processing.

Uses PySox which is wrapper for the CLT interface with the
SoX audio editing software.

"""

import re
import sox

def get_file_info(audio_path):
  file_info = sox.file_info.info(audio_path)
  file_info['file_type'] = sox.file_info.file_type(audio_path)
  return file_info

def is_notsilent(file_info):
  return not file_info['silent']

def is_mono(file_info):
  return file_info['channels'] == 1

def is_wav(file_info):
  return file_info['file_type'] == 'wav'

def is_signed(file_info):
  return not bool(re.match('unsigned', file_info['encoding'].lower()))

def is_16bit(file_info):
  return file_info['bitrate'] == 16

def is_16000hz(file_info):
  return file_info['sample_rate'] == 16000

def check_file(audio_path):
  this_file = get_file_info(audio_path)
  file_name = audio_path.split('/')[-1]
  if not is_notsilent(this_file):
    return 'error: {} has no audio'.format(file_name)
  elif not is_mono(this_file):
    return 'error: {} is not mono'.format(file_name)
  elif not is_wav(this_file):
    return 'error: {} is not wav format'.format(file_name)
  elif not is_signed(this_file):
    return 'error: {} is not signed'.format(file_name)
  elif not is_16bit(this_file):
    return 'error: {} is not 16 bit'.format(file_name)
  elif not is_16000hz(this_file):
    return 'error: {} is not 16000 hz'.format(file_name)
  else:
    return 'success: {} passed all tests'.format(file_name)
