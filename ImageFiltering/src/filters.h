#ifndef _FILTERS_H_
#define _FILTERS_H_

#include <stdlib.h>

double **get_Delta(int32_t wd, int32_t ht);
double **FIR_low_pass_filter(int32_t wd, int32_t ht);
double **FIR_sharpening_filter(int32_t wd, int32_t ht, float lambda);
uint8_t fix_boundary_clip_val(double pixel_val);
void apply_filter_type12(struct TIFF_img *input_img, struct TIFF_img *out_img, char ***argv);

#endif /* _FILTERS_H_ */


