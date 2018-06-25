# remove turk ids from filenames
# find the number of "_" in a filename
# grabs the Turk ID after the final _
# replaces the file in that directory

cd ../raw_audio
mkdir -p wav_no_ids
cd wav_batch
dir=person*/*

for file in $dir; do
  res="${file//[^_]}"
  nfields=${#res}
  filename="$(echo $file | cut -d_ -f -$nfields)"
  dirname="$(echo $filename | cut -d"/" -f 1)"
  echo $filename
  if [ ! -f "../wav_no_ids/${filename}.wav" ]; then
    mkdir -p "../wav_no_ids/$dirname"
    cp "$file" "../wav_no_ids/${filename}.wav"
    echo "file does not exist, trimming turk id";
  else
    echo "$file already exists, skipping"
  fi
done
