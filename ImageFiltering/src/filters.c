#include <stdlib.h>
#include <string.h>

#include "allocate.h"
#include "tiff.h"


double **get_Delta(int32_t wd, int32_t ht)
{
	// Initialize delta
	double **delta = (double **)get_img(wd, ht ,sizeof(double));

	for(int i=0; i<ht; i++)
		for(int j=0; j<wd; j++)
			if(i==ht/2 && j==wd/2)
				delta[i][j] = 1.0;
			else
				delta[i][j] = 0.0;

	return(delta);
}

double **FIR_low_pass_filter(int32_t wd, int32_t ht)
{
	double **filter = (double **)get_img(wd, ht ,sizeof(double));

	for(int i=0; i<ht; i++)
		for(int j=0; j<wd; j++)
			filter[i][j] = 1.0/(ht*wd);

	return(filter);
}

double **FIR_sharpening_filter(int32_t wd, int32_t ht, float lambda)
{
	//  Allocate memory for filter
	double **filter = (double **)get_img(wd, ht ,sizeof(double));

	// Get low pass filter
	double **low_pass_filter = FIR_low_pass_filter(wd, ht);

	// Get delta
	double **delta = get_Delta(wd, ht);

	// Initialize filter
	for(int i=0; i<ht; i++)
		for(int j=0; j<wd; j++)
			filter[i][j] = delta[i][j] + lambda * ( delta[i][j] - low_pass_filter[i][j] );	

	// Clear used memory for delta and low_pass_filter
	free_img( (void**)low_pass_filter );
	free_img( (void**)delta );  

	return(filter);
}

uint8_t fix_boundary_clip_val(double pixel_val)
{
	if(pixel_val>255)
		return(255);
	else if(pixel_val<0)
		return(0);
	else
		return((uint8_t) pixel_val);
}


// Apply FIL low pass filter or sharpening filter on the input image
void apply_filter_type12(struct TIFF_img *input_img, struct TIFF_img *out_img, char **argv)
{
	int row, col;

	int filter_type = atoi(argv[2]);
	int filter_wd = atoi(argv[3]);
	int filter_ht = atoi(argv[4]);

	double **filter;
	if(filter_type==1)
		filter = FIR_low_pass_filter(filter_wd, filter_ht);
	else
	{
		float lambda = atof(argv[5]);
		filter = FIR_sharpening_filter(filter_wd, filter_ht, lambda);
	}

	// Apply the filter on the input image to get the output image
	for(int c=0; c<3; c++)
		for(int i=0; i<(input_img->height); i++)
			for(int j=0; j<(input_img->width); j++)
			{
				double pixel_val = 0.0;
				for (int fi=0; fi<filter_ht; fi++)
					for(int fj=0; fj<filter_wd; fj++)
					{
						row = i - filter_ht/2 + fi;
						col = j - filter_wd/2 + fj;

						if( row>=0 && col>=0 && row<input_img->height && col<input_img->width )
							pixel_val += filter[fi][fj] * input_img->color[c][row][col];
					}
				out_img->color[c][i][j] = fix_boundary_clip_val(pixel_val);
			}


	// Clear used memory for filter
	free_img( (void**)filter );
}


// Apply IIR Filter on the input image
void apply_filter_type3(struct TIFF_img *input_img, struct TIFF_img *out_img, int flag)
{
	double pixel_val;

	// If flag==1 : Create a 256×256 image of the form x(m, n) = δ(m−127, n−127).
	if(flag==1)
	{
		double **delta = get_Delta(input_img->width, input_img->height);
		for(int c=0; c<3; c++)
			for(int i=0; i<(input_img->height); i++)
				for(int j=0; j<(input_img->width); j++)
					input_img->color[c][i][j] = (uint8_t) delta[i][j];
	}

	// Apply the filter on the input image to get the output image
	for(int c=0; c<3; c++)
		for(int i=0; i<(input_img->height); i++)
			for(int j=0; j<(input_img->width); j++)
			{
				// y(m, n) = 0.01x(m, n) + 0.9(y(m − 1, n) + y(m, n − 1)) − 0.81y(m − 1, n − 1)
				if(i>=1 && j>=1)
					pixel_val =  0.01 * input_img->color[c][i][j] + 0.9 * ( out_img->color[c][i-1][j] + out_img->color[c][i][j-1] ) - 0.81 * out_img->color[c][i-1][j-1]; 
				else if(i>=1)
					pixel_val =  0.01 * input_img->color[c][i][j] + 0.9 * ( out_img->color[c][i-1][j] );
				else if(j>=1)
					pixel_val =  0.01 * input_img->color[c][i][j] + 0.9 * ( out_img->color[c][i][j-1] );
				else
					pixel_val =  0.01 * input_img->color[c][i][j];

				if(flag==0)
					out_img->color[c][i][j] = fix_boundary_clip_val(pixel_val);
				else
					out_img->color[c][i][j] = fix_boundary_clip_val(255*100*pixel_val);

			}
}
