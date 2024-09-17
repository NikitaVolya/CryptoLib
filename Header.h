#pragma once

extern "C" __declspec(dllexport) const uint64_t * uint16_to_uint64(const uint16_t *, size_t);

extern "C" __declspec(dllexport) const uint16_t * uint64_to_uint16(const uint64_t *, size_t);

extern "C" __declspec(dllexport) const uint64_t * des_fucntion(const uint64_t*, size_t, const char*, bool);

extern "C" __declspec(dllexport) bool save_as_file(const uint64_t*, size_t, const char*);

extern "C" __declspec(dllexport) uint64_t get_data_size_in_file(const char*);

extern "C" __declspec(dllexport) const uint64_t * read_file(const char*);