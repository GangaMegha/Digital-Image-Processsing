#ifndef _SUBROUTINES_H_
#define _SUBROUTINES_H_

#include <stdlib.h>


struct pixel 
{
	int m,n; /* m=row, n=col */
}; 

void ConnectedNeighbors(struct pixel s, double T, unsigned char **img, int width, int height, int *M, struct pixel c[4]);

void ConnectedSet(struct pixel s0, double T, unsigned char **img, int width, int height, int ClassLabel, unsigned int **seg, int *NumConPixels);

void ImageSegmentation(double T, unsigned char **img, int width, int height, unsigned int **seg, int *NumConPixels);

#endif /* _FILTERS_H_ */


