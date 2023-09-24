# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "/Users/inga/esp/esp-idf/components/bootloader/subproject"
  "/Users/inga/Desktop/NT@B/emg-neurowrist/firmware/read_analog/build/bootloader"
  "/Users/inga/Desktop/NT@B/emg-neurowrist/firmware/read_analog/build/bootloader-prefix"
  "/Users/inga/Desktop/NT@B/emg-neurowrist/firmware/read_analog/build/bootloader-prefix/tmp"
  "/Users/inga/Desktop/NT@B/emg-neurowrist/firmware/read_analog/build/bootloader-prefix/src/bootloader-stamp"
  "/Users/inga/Desktop/NT@B/emg-neurowrist/firmware/read_analog/build/bootloader-prefix/src"
  "/Users/inga/Desktop/NT@B/emg-neurowrist/firmware/read_analog/build/bootloader-prefix/src/bootloader-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "/Users/inga/Desktop/NT@B/emg-neurowrist/firmware/read_analog/build/bootloader-prefix/src/bootloader-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "/Users/inga/Desktop/NT@B/emg-neurowrist/firmware/read_analog/build/bootloader-prefix/src/bootloader-stamp${cfgdir}") # cfgdir has leading slash
endif()
