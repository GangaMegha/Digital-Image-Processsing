
#include <math.h>

#include "tiff.h"
#include "allocate.h"
#include "typeutil.h"
#include "filters.h"

void error(char *name);

int main (int argc, char **argv) 
{
  FILE *fp;
  struct TIFF_img input_img, out_img;
  char* outfile;
  int flag = 0;

  if (argc!=4 && argc != 6 && argc!=7) error( argv[0] );

  /* open image file */ 
  if(strcmp(argv[1], "nil")==0)
    flag = 1;
  
  if(flag==0)
  {
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

    /* check the type of image data */
    if ( input_img.TIFF_type != 'c' ) {
      fprintf ( stderr, "error:  image must be 24-bit color\n" );
      exit ( 1 );
    }
  }
  else
    get_TIFF(&input_img, 256, 256, 'c');

  /* Get appropriate filter :
      1 : FIR_low_pass_filter
      2 : FIR_sharpening_filter
      3 : IIR Filter            */

  int filter_type = atoi(argv[2]);
  get_TIFF(&out_img, input_img.height, input_img.width, 'c');   

  switch(filter_type) {
      case 1 :
          outfile = argv[5];
          apply_filter_type12(&input_img, &out_img, argv);
          break;
      case 2 :
          outfile = argv[6];
          apply_filter_type12(&input_img, &out_img, argv);
          break;
      case 3 :
          outfile = argv[3];
          apply_filter_type3(&input_img, &out_img, flag);
          break;
      default :
          fprintf ( stderr, "error:  Invalid filter_type : value must be 1, 2 or 3\n" );
          exit ( 1 );   
   }

  // open output image file 
  if ( ( fp = fopen ( outfile, "wb" ) ) == NULL ) {
    fprintf ( stderr, "cannot open file %s\n", outfile);
    exit ( 1 );
  }

  // write output image 
  if ( write_TIFF ( fp, &out_img ) ) {
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
    printf("usage:  %s  image.tiff \n\n",name);
    printf("this program reads in a 24-bit color TIFF image.\n");
    printf("It then horizontally filters the the image,\n");
    printf("using the specified filter type : \n");
    printf("\t{1 : FIR_low_pass_filter, 2 : FIR_sharpening_filter ,3 : IIR Filter}\n");
    printf("and generates an 8-bit color image,\n");
    printf("that is saved in the output folder");
    exit(1);
}

