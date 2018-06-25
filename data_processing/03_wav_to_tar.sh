# compress audio files and add them to the exisiting tarballs
# unzip the tar pkl file

cd ../all_person_orders

# loop this over the directories
for tar_file in *.tar.gz; do
  dir_name="$(echo $tar_file | cut -d_ -f -1)"
  echo $dir_name
  mkdir -p $dir_name
  tar -xvzf $tar_file -C $dir_name
  #cp ../processed_audio/wav_no_ids/$dir_name/*.wav $dir_name/
  cp ../raw_audio/no_turk_ids/$dir_name/*.wav $dir_name/
  tar -czf $tar_file $dir_name
  rm -rf $dir_name
done
