#!/bin/bash
# 221_WPout, 222_EPout, 223_ALout, 224_SHout, 225_IOout, 226_CPout
path_in="/bk2/noodles/tcsa-cnn/Dataset_all_basins/226_CPout"
path_out="/wk171/ccl/data/6_CP"

# loop for TCs
for TC_in in ${path_in}/*; do
  if [[ -d $TC_in ]]; then
  #if [[ ${TC_in:(-5):2} == '19' ||  ${TC_in:(-5):2} == '20' ]]; then
    echo "Start TC $TC_in"
    # prepare environment path
    export TC_input_path=$TC_in

    nc_path="$path_out/${TC_in:(-7):7}"
    mkdir -p $nc_path
    export NC_save_path=$nc_path

	# do docker-compose
    docker-compose run --rm  predict_GAN
  fi
done

