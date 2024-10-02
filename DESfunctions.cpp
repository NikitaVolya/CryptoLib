#include "DESfunctions.h"
#include "utils.h"
#include "permitation_tables.h"

#include <iostream>

template <typename T>
void permitation(const int* table, const int table_size, T* data, const int data_size)
{
	T res = 0;
	for (int i = 0; i < table_size; i++)
		res |= (*data >> (data_size - table[i]) & 1) << i;
	*data = res;
}

int slide_number(size_t round)
{
	switch (round) {
		case 1: case 2: case 9: case 16: return 1;
		default: return 2;
	}
}

void string_resize(char*& value, int& old_size, const int new_size)
{
	char* new_string = new char[new_size];

	for (int i = 0; i < new_size; i++)
		if (i < old_size)
			new_string[i] = value[i];
		else
			new_string[i] = '\0';
	delete[] value;
	value = new_string;
	old_size = new_size;
}


void split_to_6bit_array(uint8_t b[8], uint64_t data)
{
	uint8_t mask = create_mask<uint8_t>(6);
	for (int i = 0; i < 8; i++)
		b[i] = (data >> (42 - i * 6)) & mask;
}

void transformations_s(uint8_t b[8], uint8_t s[8])
{
	for (int i = 0; i < 8; i++)
	{
		uint8_t first = (b[i] >> 4 & 2) | b[i] & 1;
		uint8_t second = (b[i] >> 1) & 15;
		s[i] = S[i][first][second];
	}
}

uint32_t subtitutions(uint64_t data)
{
	uint32_t rep = 0;
	uint8_t b[8];
	uint8_t s[8];

	split_to_6bit_array(b, data);
	transformations_s(b, s);

	for (int i = 0; i < 8; i++)
		rep |= s[i] << (7 - i) * 4;
	

	return rep;
}


uint64_t function_F(uint64_t R, uint64_t key)
{
	permitation<uint64_t>(EP, 48, &R, 32);
	permitation<uint64_t>(CP, 48, &key, 56);
	
	uint32_t midle_block = subtitutions(R ^ key);

	permitation<uint32_t>(P, 32, &midle_block, 32);

	return midle_block;
}


void block_des(uint64_t* block, uint64_t key, bool encrypt)
{
	permitation<uint64_t>(PC, 64, block, 64);

	uint32_t L;
	uint32_t R;
	uint32_t C;
	uint32_t D;

	split_data<uint64_t, uint32_t, 64>(&L, &R, *block);
	split_data<uint64_t, uint32_t, 56>(&C, &D, key);

	if (!encrypt)
	{
		data_slide<uint32_t, 28>(&C, 1);
		data_slide<uint32_t, 28>(&D, 1);
	}

	for (int i = 1; i <= 16; i++)
	{
		int slide = encrypt ? slide_number(i) : -slide_number(i);
		data_slide<uint32_t, 28>(&C, slide);
		data_slide<uint32_t, 28>(&D, slide);

		uint64_t round_key = concatenation_data<uint32_t, uint64_t, 56>(C, D);

		if (encrypt)
		{
			uint32_t LN = R;
			R = L ^ function_F((uint64_t)R, round_key);
			L = LN;
		}
		else
		{
			uint32_t RN = L;
			L = R ^ function_F((uint64_t)L, round_key);
			R = RN;
		}
	}
	*block = concatenation_data<uint32_t, uint64_t, 64>(L, R);
	permitation<uint64_t>(PC_REVERS, 64, block, 64);
}

void des(uint64_t* values, const char key_data[8], int size, bool encrypt)
{
	uint64_t key = to_binary_data<uint64_t>(key_data, 8);
	permitation<uint64_t>(IP, 56, &key, 64);

	for (int i = 0; i < size; i++)
		block_des(values + i, key, encrypt);
}