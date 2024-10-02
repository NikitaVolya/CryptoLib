#pragma once

extern "C" __declspec(dllexport) const uint16_t * des_fucntion(const uint16_t *, int, const char*, bool);

extern "C" __declspec(dllexport) bool save_as_file(const uint16_t*, int, const char*);

extern "C" __declspec(dllexport) uint64_t get_data_size_in_file(const char*);

extern "C" __declspec(dllexport) const uint16_t * read_file(const char*);