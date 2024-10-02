#pragma once
#include <iostream>

void copy_string(char*& destination, const char* source, size_t size);

template <typename T>
T create_mask(int size)
{
	T mask = 0;
	for (int i = 0; i < size; i++)
		mask |= 1 << i;
	return mask;
}

template <typename T>
T to_binary_data(const char* block, int string_size)
{
	T res = 0;
	for (int i = 0; i < string_size; i++)
		res = (res << 8) | (uint8_t)block[i];
	return res;
}

template <typename T, int size>
void data_slide(T* data, int positions)
{
	if (positions > 0)
		*data = ((*data << positions) | (*data >> (size - positions))) & create_mask<T>(size);
	else
		*data = (*data >> -positions) | ((*data & create_mask<T>(-positions)) << (size + positions));
}

template <typename SOURCE_TYPE, typename OUTPUT_TYPE, int size>
void split_data(OUTPUT_TYPE* a, OUTPUT_TYPE* b, const SOURCE_TYPE& source)
{
	int half_part_size = size / 2;
	*a = source >> half_part_size;
	*b = source & create_mask<long long>(half_part_size);
}

template <typename INPUT_TYPE, typename OUTPUT_TYPE, int size>
OUTPUT_TYPE concatenation_data(const INPUT_TYPE& a, const INPUT_TYPE& b)
{
	return (OUTPUT_TYPE(a) << (size / 2)) | OUTPUT_TYPE(b);
}