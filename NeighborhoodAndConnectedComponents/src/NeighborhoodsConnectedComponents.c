
#include <math.h>

#include "tiff.h"
#include "allocate.h"
#include "typeutil.h"
#include "subroutines.h"

void error(char *name);

int main (int argc, char **argv) 
{
	FILE *fp;
	struct TIFF_img input_img, out_img;
	char* outfile;
	int flag = 0;

	if (argc != 7) error( argv[0] );

	/* open image file */ 
	if ( ( fp = fopen ( argv[1], "rb" ) ) == NULL ) 
	{
		fprintf ( stderr, "cannot open file %s\n", argv[1] );
		exit ( 1 );
	}

	if ( read_TIFF ( fp, &input_img ) ) 
	{
		fprintf ( stderr, "error reading file %s\n", argv[1] );
		exit ( 1 );
	}

	/* close image file */
	fclose ( fp );

	/* check the type of image data : it's greyscale*/
	if ( input_img.TIFF_type != 'g' ) 
  {
		fprintf ( stderr, "error:	image must be greyscale\n" );
		exit ( 1 );
	}

  struct pixel s0;
  s0.m = atoi(argv[3]);
  s0.n = atoi(argv[4]);

  double T = atoi(argv[5]);
  int ClassLabel = 1;
  int *NumConPixels = 0;

  unsigned int **seg = (unsigned int **)get_img(input_img.width,
                                                  input_img.height,
                                                  sizeof(unsigned int));

  int filter_type = atoi(argv[6]);

	/* Get appropriate filter :
			 1 : ConnectedSet
			 2 : ImageSegmentation
			 3 : IIR Filter						*/

	get_TIFF(&out_img, input_img.height, input_img.width, 'c');	 

	switch(filter_type) {
			 case 1 :
            ConnectedSet(s0, T, input_img.mono, input_img.width, input_img.height, ClassLabel, seg, &NumConPixels);
					  break;
			 case 2 :
            ImageSegmentation(T, input_img.mono, input_img.width, input_img.height, seg, &NumConPixels);
            break;    
			 default :
					 fprintf ( stderr, "error:	Invalid filter_type : value must be 1 or 2\n" );
					 exit ( 1 );	 
		}

  get_TIFF(&out_img, input_img.height, input_img.width, 'g');

  for (int i = 0; i < input_img.height; i++) {
      for (int j = 0; j < input_img.width; j++) {
          if (seg[i][j] == ClassLabel) {
              out_img.mono[i][j] = 0;
          } else {
              out_img.mono[i][j] = 255;
          }
      }
  }

  free_img((void *)seg);


  // if ((fp = fopen("output-firlpf.tif", "wb")) == NULL) {
  //     fprintf(stderr, "cannot open file output.tif\n");
  //     exit(1);
  // }

  //  // write color image */
  // if(write_TIFF(fp, &input_img)) {
  //     fprintf(stderr, "error writing TIFF file %s\n", argv[2]);
  //     exit(1);
  // }

  outfile = argv[2];

	// open output image file 
	if ( ( fp = fopen ( outfile, "wb" ) ) == NULL ) 
  {
		fprintf ( stderr, "cannot open file %s\n", outfile);
		exit ( 1 );
	}

	// write output image 
	if ( write_TIFF ( fp, &out_img ) ) 
  {
		fprintf ( stderr, "error writing TIFF file %s\n", outfile );
		exit ( 1 );
	}

	// close output image file 
	fclose ( fp );
		

	// de-allocate space which was used for the images 
	free_TIFF ( &(input_img) );
	free_TIFF ( &(out_img) );

	return(0);
}

void error(char *name)
{
		printf("usage:	%s	image.tiff \n\n",name);
		printf("this program reads in a 24-bit color TIFF image.\n");
		printf("It then horizontally filters the the image,\n");
		printf("using the specified filter type : \n");
		printf("\t{1 : FIR_low_pass_filter, 2 : FIR_sharpening_filter ,3 : IIR Filter}\n");
		printf("and generates an 8-bit color image,\n");
		printf("that is saved in the output folder");
		exit(1);
}

