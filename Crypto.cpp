#include "DESfunctions.h"

#include <fstream>

#include "utils.h"
#include "Header.h"


extern "C" __declspec(dllexport) const uint16_t * des_fucntion(const uint16_t * values, int size, const char* key_data, bool encrypt)
{
	uint16_t* data_16bit = new uint16_t[size];
	for (int i = 0; i < size; i++)
		data_16bit[i] = values[i];

	des((uint64_t*)(data_16bit), key_data, size / 4, encrypt);
	return data_16bit;
}

extern "C" __declspec(dllexport) bool save_as_file(const uint16_t * values, int size, const char* file_name)
{
	std::ofstream write_file(file_name, std::ios::out | std::ios::binary);

	if (!write_file)
	{
		std::cout << "Cannot open file!" << std::endl;
		return false;
	}

	write_file.write((char*) values, sizeof(uint16_t) * size);
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

extern "C" __declspec(dllexport) const uint16_t* read_file(const char* file_name)
{
	uint64_t data_size = get_data_size_in_file(file_name) / 16;
	std::ifstream read_file(file_name, std::ios::in | std::ios::binary);

	if (data_size < 1)
		return new uint16_t(0);

	if (!read_file) {
		std::cerr << "Unable to open file: " << file_name << std::endl;
		return new uint16_t(0);
	}

	uint16_t* rep = new uint16_t[data_size];
	read_file.read((char*)rep, sizeof(uint16_t) * data_size);
	read_file.close();

	return rep;
}