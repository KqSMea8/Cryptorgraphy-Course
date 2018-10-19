cmake_minimum_required(VERSION 3.12)
project(polynomial)

set(CMAKE_CXX_STANDARD 14)

add_executable(polynomial main.cpp Polynomial.cpp Polynomial.h testBSGS.cpp testPolynomial.cpp testHeader.h)