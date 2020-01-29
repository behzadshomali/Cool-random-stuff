/* Copyright (C) Fateme Chaji, Ferdowsi Univerity of Mashhad
* 25 Esfand 1396(Hijri shamsi)
* 16 March 2018
* Author: Fateme Chaji
*/

#pragma once

template <class T>
class FiveWayPartition {
public:
	void Partition(T* A, T pivot1, T pivot2, int p, int r, int& q1, int& q2, int& q3, int& q4) {
		int i = p,
		j = p,
		k = r+1,  
		z = r+1,
		s = r+1;
		while(j < s){
			if(A[j] < pivot1){
				T temp = A[i];
				A[i] = A[j];
				A[j] = temp;
				j++; i++;
			}
			else if(A[j] == pivot1){
				j++;
			}
			else if(A[j] > pivot1 && A[j] < pivot2){
				T temp = A[j];
				A[j] = A[s-1];
				A[s-1] = temp;
				s--;
			}
			else if(A[j] == pivot2){
				T temp = A[j];
				A[j] = A[s-1];
				A[s-1] = A[z-1];
				A[z-1] = temp;
				z--; s--;
			}
			else{
				T temp = A[j];
				A[j] = A[s-1];
				A[s-1] = A[z-1];
				A[z-1] = A[k-1];
				A[k-1] = temp;
				s--; z--; k--;
			}
		}
		q1 = i;
		q2 = s;
		q3 = z;
		q4 = k;
	}
};


