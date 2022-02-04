cd src/
make

# # code input_img output_img m n T filter_type
# ../bin/NeighborhoodsConnectedComponents ../images/img22gd2.tif img22gd2_out.tif 67 45 2 1
# mv img22gd2_out.tif ../output


# code input_img output_img m n T
../bin/NeighborhoodsConnectedComponents ../images/img22gd2.tif img22gd2_out.tif 67 45 2 2
mv img22gd2_out.tif ../output


# #****************** RUN C# Scipts for Image Filtering ********************
# # FIR Low Pass Filter
# echo "\n\n\n\nRun FilterImage function using FIR_low_pass_filter on images/img03.tif with a 9x9 filter...\n"
# bin/FilterImage images/img03.tif 1 9 9 img03_FIR_low_pass_filter.tif
# mv img03_FIR_low_pass_filter.tif output
# echo "Output saved in output/img03_FIR_low_pass_filter.tif"


# # FIR Sharpening Filter
# echo "\n\n\n\nRun FilterImage function using FIR_sharpening_filter on images/imgblur.tif with a 9x9 filter...\n"
# bin/FilterImage images/imgblur.tif  2 9 9 0.2 imgblur_FIR_sharpening_filter_02.tif
# mv imgblur_FIR_sharpening_filter_02.tif output
# echo "lambda = 0.2 : output saved in output/imgblur_FIR_sharpening_filter_02.tif\n\n"

# bin/FilterImage images/imgblur.tif  2 9 9 0.8 imgblur_FIR_sharpening_filter_08.tif
# mv imgblur_FIR_sharpening_filter_08.tif output
# echo "lambda = 0.8 : output saved in output/imgblur_FIR_sharpening_filter_08.tif\n\n"

# bin/FilterImage images/imgblur.tif  2 9 9 1.5 imgblur_FIR_sharpening_filter_15.tif
# mv imgblur_FIR_sharpening_filter_15.tif output
# echo "lambda = 1.5 : output saved in output/imgblur_FIR_sharpening_filter_15.tif\n\n"


# # IIR Filter
# echo "\n\n\n\nRun FilterImage function using IIR_filter on images/img03.tif...\n"
# bin/FilterImage images/img03.tif 3 img03_IIR_filter.tif
# mv img03_IIR_filter.tif output
# echo "Output saved in output/img03_IIR_filter.tif"

# # IIR Filter using delta as input image
# echo "\n\n\n\nRun FilterImage function using IIR_filter on a 256×256 image of the form x(m, n) = δ(m−127, n−127)...\n"
# bin/FilterImage nil 3 delta_IIR_filter.tif
# mv delta_IIR_filter.tif output
# echo "Output saved in output/delta_IIR_filter.tif"



# #*************************** Run python scripts ***************************
# # IIR Filter using delta as input image
# echo "\n\n\n\nGenerate point spread of IIR_filter on a 256×256 image of the form x(m, n) = δ(m−127, n−127)...\n"
# python3 src/iir_point_spread.py 256 256 3 output/py_point_spread.tif
# echo "Output saved in output/py_point_spread.tif"


# #******************** Convert all tiff images to png **********************
# echo "\n\n\n\nConverting all .tif files into png format using tif_to_png.py...\n"
# python3 src/tif_to_png.py images/img03.tif output_png/img03.png
# python3 src/tif_to_png.py images/imgblur.tif output_png/imgblur.png

# python3 src/tif_to_png.py C-code-main/demo/output/color.tif output_png/color.png
# python3 src/tif_to_png.py C-code-main/demo/output/green.tif output_png/green.png


# python3 src/tif_to_png.py output/img03_FIR_low_pass_filter.tif output_png/py_img03_FIR_low_pass_filter_out.png
# python3 src/tif_to_png.py output/imgblur_FIR_sharpening_filter_02.tif output_png/py_imgblur_FIR_sharpening_filter_02_out.png
# python3 src/tif_to_png.py output/imgblur_FIR_sharpening_filter_08.tif output_png/py_imgblur_FIR_sharpening_filter_08_out.png
# python3 src/tif_to_png.py output/imgblur_FIR_sharpening_filter_15.tif output_png/py_imgblur_FIR_sharpening_filter_15_out.png
# python3 src/tif_to_png.py output/img03_IIR_filter.tif output_png/img03_IIR_filter.png
# python3 src/tif_to_png.py output/delta_IIR_filter.tif output_png/delta_IIR_filter.png

# python3 src/tif_to_png.py output/py_point_spread.tif output_png/py_point_spread.png
# echo "Outputs saved in output_png/"



# #*************************** Plot DSFT ***************************
# echo "\n\n\n\nGenerating the DSFT magnitude of frequency response plots for different filters...\n"
# python3 src/plot_DSFT.py lpf FIR_low_pass_filter output_png/DSFT_FIR_low_pass_filter.png 0
# python3 src/plot_DSFT.py sharp_h FIR_sharpening_filter_H output_png/DSFT_FIR_sharpening_filter_H.png 0.2
# python3 src/plot_DSFT.py sharp_g FIR_sharpening_filter_G output_png/DSFT_FIR_sharpening_filter_G_02.png 0.2
# python3 src/plot_DSFT.py sharp_g FIR_sharpening_filter_G output_png/DSFT_FIR_sharpening_filter_G_08.png 0.8
# python3 src/plot_DSFT.py sharp_g FIR_sharpening_filter_G output_png/DSFT_FIR_sharpening_filter_G_15.png 1.5
# python3 src/plot_DSFT.py iir IIR_filter output_png/DSFT_IIR_filter.png 0

