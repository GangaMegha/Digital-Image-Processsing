#include <stdlib.h>
#include <string.h>

#include "allocate.h"
#include "tiff.h"

struct pixel 
{
	int m,n; /* m=row, n=col */
}; 

// A structure to represent a stack
struct StackNode 
{
	struct pixel data;
	struct StackNode* next;
};
 
struct StackNode* newNode(struct pixel data)
{
	struct StackNode* stackNode = (struct StackNode*) malloc(sizeof(struct StackNode));
	stackNode->data = data;
	stackNode->next = NULL;
	return stackNode;
}
 
int isEmpty(struct StackNode* root)
{
	return !root;
}
 
void push(struct StackNode** root, struct pixel data)
{
	struct StackNode* stackNode = newNode(data);
	stackNode->next = *root;
	*root = stackNode;
}
 
struct pixel pop(struct StackNode** root)
{
	if (isEmpty(*root))
	{
		struct pixel tmp;
		return tmp;
	}
	struct StackNode* temp = *root;
	*root = (*root)->next;
	struct pixel popped = temp->data;
	free(temp);
 
	return popped;
}


void ConnectedNeighbors(struct pixel s, double T, unsigned char **img, int width, int height, int *M, struct pixel c[4])
{
	*M = 0;

	if(s.m-1>=0 && abs(img[s.m-1][s.n]-img[s.m][s.n])<=T)
	{
		c[*M].m = s.m-1; 
		c[*M].n = s.n; 
		*M += 1;
	}
	if(s.m+1<height && abs(img[s.m+1][s.n]-img[s.m][s.n])<=T)
	{
		c[*M].m = s.m+1; 
		c[*M].n = s.n; 
		*M += 1;
	}
	if(s.n-1>=0 && abs(img[s.m][s.n-1]-img[s.m][s.n])<=T)
	{
		c[*M].m = s.m; 
		c[*M].n = s.n-1; 
		*M += 1;
	}
	if(s.n+1<width && abs(img[s.m][s.n+1]-img[s.m][s.n])<=T)
	{
		c[*M].m = s.m; 
		c[*M].n = s.n+1; 
		*M += 1;

	}
}


void ConnectedSet(struct pixel s0, double T, unsigned char **img, int width, int height, int ClassLabel, unsigned int **seg, int *NumConPixels)
{
	struct pixel s;
	struct pixel c[4];
	int M = 0;//*

	struct StackNode* B = NULL;
	push(&B, s0);
	*NumConPixels = 1;

	while(!isEmpty(B))
	{
		// pop top element from B
		s = pop(&B);
 
		// Assign pixel value of s as connected
		seg[s.m][s.n] = ClassLabel;

		// Get all neighbours of s
		ConnectedNeighbors(s, T, img, width, height, &M, c);

		// Update B with the neighbors of s that aren't already labelled using ClassLabel
		for(int i=0; i<M; i++)
		{
			if(seg[c[i].m][c[i].n] == 0)
			{
				push(&B, c[i]);
				*NumConPixels += 1;
			}
		}
	}
}


void ImageSegmentation(double T, unsigned char **img, int width, int height, unsigned int **seg, int *NumConPixels)
{
	int ClassLabel = 2;

	struct pixel s0;

	// unsigned int **seg_tmp = (unsigned int **)get_img(width, height, sizeof(unsigned int));

	for(int i=0; i<height; i++)
		for(int j=0; i<width; j++)
			if(seg[i][j]!=0)
			{
				// // // Initialize seg_tmp
				// // for(int k=0; k<height; k++)
				// // 	for(int l=0; l<width; l++)
				// // 		seg_tmp[k][l] = seg[k][l];

				// s0.m = i;
				// s0.n = j;

				// ConnectedSet(s0, T, img, width, height, ClassLabel, seg, NumConPixels);

				// if(NumConPixels<=100)
				// {
				// 	// Copy seg_tmp to seg
				// 	for(int k=0; k<height; k++)
				// 		for(int l=0; l<width; l++)
				// 			if(seg[k][l]==ClassLabel)
				// 				seg[k][l] = 1;
				// }
				// else
				// 	ClassLabel++;
					

			}
	// free_img((void *)seg_tmp);
}