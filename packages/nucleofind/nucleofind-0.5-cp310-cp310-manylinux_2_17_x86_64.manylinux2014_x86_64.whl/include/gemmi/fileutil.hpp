// Copyright 2018 Global Phasing Ltd.
//
// File-related utilities.

#ifndef GEMMI_FILEUTIL_HPP_
#define GEMMI_FILEUTIL_HPP_

#include <cstdio>    // for FILE, fopen, fclose
#include <cstdint>
#include <cstring>   // strlen
#include <initializer_list>
#include <memory>    // for unique_ptr
#include "fail.hpp"  // for sys_fail
#include "input.hpp"  // for CharArray

#if defined(_WIN32) && !defined(GEMMI_USE_FOPEN)
#include "utf.hpp"
#endif

namespace gemmi {

// strip directory and suffixes from filename
inline std::string path_basename(const std::string& path,
                                 std::initializer_list<const char*> exts) {
  size_t pos = path.find_last_of("\\/");
  std::string basename = pos == std::string::npos ? path : path.substr(pos + 1);
  for (const char* ext : exts) {
    size_t len = std::strlen(ext);
    if (basename.size() > len &&
        basename.compare(basename.length() - len, len, ext, len) == 0)
      basename.resize(basename.length() - len);
  }
  return basename;
}

// file operations
typedef std::unique_ptr<std::FILE, decltype(&std::fclose)> fileptr_t;

inline fileptr_t file_open(const char* path, const char* mode) {
  std::FILE* file;
#if defined(_WIN32) && !defined(GEMMI_USE_FOPEN)
  std::wstring wpath = UTF8_to_wchar(path);
  std::wstring wmode = UTF8_to_wchar(mode);
  if ((file = ::_wfopen(wpath.c_str(), wmode.c_str())) == nullptr)
#else
  if ((file = std::fopen(path, mode)) == nullptr)
#endif
    sys_fail(std::string("Failed to open ") + path +
             (*mode == 'w' ? " for writing" : ""));
  return fileptr_t(file, &std::fclose);
}

// helper function for treating "-" as stdin or stdout
inline fileptr_t file_open_or(const char* path, const char* mode,
                              std::FILE* dash_stream) {
  if (path[0] == '-' && path[1] == '\0')
    return fileptr_t(dash_stream, [](std::FILE*) { return 0; });
  return file_open(path, mode);
}

inline std::size_t file_size(std::FILE* f, const std::string& path) {
  if (std::fseek(f, 0, SEEK_END) != 0)
    sys_fail(path + ": fseek failed");
  long length = std::ftell(f);
  if (length < 0)
    sys_fail(path + ": ftell failed");
  if (std::fseek(f, 0, SEEK_SET) != 0)
    sys_fail(path + ": fseek failed");
  return length;
}

// helper function for working with binary files
inline bool is_little_endian() {
  std::uint32_t x = 1;
  return *reinterpret_cast<char *>(&x) == 1;
}

inline void swap_two_bytes(void* start) {
  char* bytes = static_cast<char*>(start);
  std::swap(bytes[0], bytes[1]);
}

inline void swap_four_bytes(void* start) {
  char* bytes = static_cast<char*>(start);
  std::swap(bytes[0], bytes[3]);
  std::swap(bytes[1], bytes[2]);
}

inline void swap_eight_bytes(void* start) {
  char* bytes = static_cast<char*>(start);
  std::swap(bytes[0], bytes[7]);
  std::swap(bytes[1], bytes[6]);
  std::swap(bytes[2], bytes[5]);
  std::swap(bytes[3], bytes[4]);
}

// reading file into a memory buffer
inline CharArray read_file_into_buffer(const std::string& path) {
  fileptr_t f = file_open(path.c_str(), "rb");
  size_t size = file_size(f.get(), path);
  CharArray buffer(size);
  if (std::fread(buffer.data(), size, 1, f.get()) != 1)
    sys_fail(path + ": fread failed");
  return buffer;
}

inline CharArray read_stdin_into_buffer() {
  size_t n = 0;
  CharArray buffer(16 * 1024);
  for (;;) {
    n += std::fread(buffer.data() + n, 1, buffer.size() - n, stdin);
    if (n != buffer.size()) {
      buffer.set_size(n);
      break;
    }
    buffer.resize(2*n);
  }
  return buffer;
}

template<typename T>
inline CharArray read_into_buffer(T&& input) {
  if (input.is_stdin())
    return read_stdin_into_buffer();
  if (input.is_compressed())
    return input.uncompress_into_buffer();
  return read_file_into_buffer(input.path());
}

} // namespace gemmi
#endif
