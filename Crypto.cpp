#include "DESfunctions.h"

#include <fstream>

#include "utils.h"
#include "Header.h"

extern "C" __declspec(dllexport) const uint64_t * uint16_to_uint64(const uint16_t * values, size_t size)
{
	size_t new_size = size / 4;
	uint64_t* new_arr = new uint64_t[new_size];
	for (int i = 0; i < new_size; i++)
		new_arr[i] = 0;
	for (int i = 0; i < size; i++)
	{
		int index = i / 4;
		int slide = 3 - i % 4;
		new_arr[index] |= uint64_t(values[i]) << (slide * 16);
	}
	return new_arr;
}

extern "C" __declspec(dllexport) const uint16_t * uint64_to_uint16(const uint64_t * values, size_t size)
{
	size_t new_size = size * 4;
	uint16_t* new_arr = new uint16_t[new_size];
	for (int i = 0; i < new_size; i++)
	{
		int index = i / 4;
		int slide = 3 - i % 4;
		new_arr[i] = uint16_t(values[index] >> (slide * 16));
	}
	return new_arr;
}

extern "C" __declspec(dllexport) const uint64_t * des_fucntion(const uint64_t * values, size_t size, const char* key_data, bool encrypt)
{
	uint64_t* tmp = new uint64_t[size];
	for (int i = 0; i < size; i++)
		tmp[i] = values[i];

	for (int i = 0; i < size / 2; i++)
		des(tmp + i, key_data, size / 2, encrypt);
	return tmp;
}

extern "C" __declspec(dllexport) bool save_as_file(const uint64_t * values, size_t size, const char* file_name)
{
	std::ofstream write_file(file_name, std::ios::out | std::ios::binary);

	if (!write_file)
	{
		std::cout << "Cannot open file!" << std::endl;
		return false;
	}

	for (int i = 0; i < size; i++)
		write_file.write((char*) &values[i], sizeof(uint64_t));

	write_file.close();

	if (!write_file.good())
	{
		std::cout << "Error occurred at writing time!" << std::endl;
		return false;
	}
	return true;
}

extern "C" __declspec(dllexport) uint64_t get_data_size_in_file(const char* file_name)
{
	std::ifstream read_file(file_name, std::ios::in | std::ios::binary);

	if (!read_file) {
		std::cerr << "Unable to open file: " << file_name << std::endl;
		return 0;
	}

	read_file.seekg(0, std::ios::end);
	uint64_t file_size_in_bites = static_cast<size_t>(read_file.tellg()) * 8;
	read_file.close();

	return file_size_in_bites;
}

extern "C" __declspec(dllexport) const uint64_t* read_file(const char* file_name)
{
	uint64_t data_size = get_data_size_in_file(file_name) / 64;
	std::ifstream read_file(file_name, std::ios::in | std::ios::binary);

	if (data_size < 1)
		return new uint64_t(0);

	if (!read_file) {
		std::cerr << "Unable to open file: " << file_name << std::endl;
		return new uint64_t(0);
	}

	uint64_t* rep = new uint64_t[data_size];
	for (int i = 0; i < data_size; i++)
		read_file.read((char*)&rep[i], sizeof(uint64_t));
	read_file.close();

	return rep;
}