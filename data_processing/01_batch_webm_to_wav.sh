# convert webm video/audio files to wav format
# checks if file already exists in the wav directory so we don't duplicate effort
# puts the wav files in a separate directory

cd ../raw_audio
mkdir -p wav_batch
cd webm_batch

for file in person*/*; do
  check_file=${file%.webm}
  if [ ! -f ../wav_batch/$check_file.wav ]; then
    dirname="$(echo $file | cut -d/ -f -1)"
    mkdir -p ../wav_batch/$dirname
    ffmpeg -hide_banner -loglevel panic -y -i "$file" -ar 16000 -ac 1 -c:a pcm_s16le "../wav_batch/${file%.webm}".wav;
    echo "file does not exist, converting to wav"
  else
    echo "$file already exists, skipping"
  fi
done
