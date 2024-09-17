#include "utils.h"

#include "iostream"

void copy_string(char*& destination, const char* source, size_t size)
{
	if (!destination)
		destination = new char[size];

	for (int i = 0; i < size; i++)
		destination[i] = source[i];
}