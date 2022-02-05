cd src/
make

	# /* Get appropriate filter :
	# 		 1 : ConnectedSet
	# 		 2 : ImageSegmentation				*/

#------------------------------ Connected Components ------------------------------
# code input_img output_img m n T filter_type
../bin/NeighborhoodsConnectedComponents ../images/img22gd2.tif img22gd2_out_67_45_1.tif 67 45 1 1
mv img22gd2_out_67_45_1.tif ../output

../bin/NeighborhoodsConnectedComponents ../images/img22gd2.tif img22gd2_out_67_45_2.tif 67 45 2 1
mv img22gd2_out_67_45_2.tif ../output

../bin/NeighborhoodsConnectedComponents ../images/img22gd2.tif img22gd2_out_67_45_3.tif 67 45 3 1
mv img22gd2_out_67_45_3.tif ../output




#------------------------------ Image Segmentation ------------------------------
# code input_img output_img m n T filter_type
../bin/NeighborhoodsConnectedComponents ../images/img22gd2.tif img22gd2_out_0_0_1.tif 0 0 1 2
mv img22gd2_out_0_0_1.tif ../output

../bin/NeighborhoodsConnectedComponents ../images/img22gd2.tif img22gd2_out_0_0_2.tif 0 0 2 2
mv img22gd2_out_0_0_2.tif ../output

../bin/NeighborhoodsConnectedComponents ../images/img22gd2.tif img22gd2_out_0_0_3.tif 0 0 3 2
mv img22gd2_out_0_0_3.tif ../output



#------------------------------ Save Image Segmentation Images ------------------------------
python3 ImageSegmentation_display.py ../output/img22gd2_out_67_45_1.tif ../output_png/img22gd2_out_67_45_1.png
python3 ImageSegmentation_display.py ../output/img22gd2_out_67_45_2.tif ../output_png/img22gd2_out_67_45_2.png
python3 ImageSegmentation_display.py ../output/img22gd2_out_67_45_3.tif ../output_png/img22gd2_out_67_45_3.png


python3 ImageSegmentation_display.py ../output/img22gd2_out_0_0_1.tif ../output_png/img22gd2_out_0_0_1.png
python3 ImageSegmentation_display.py ../output/img22gd2_out_0_0_2.tif ../output_png/img22gd2_out_0_0_2.png
python3 ImageSegmentation_display.py ../output/img22gd2_out_0_0_3.tif ../output_png/img22gd2_out_0_0_3.png
