from libc.stdlib cimport malloc, free

cdef extern from "Python.h":
    object PyBytes_FromStringAndSize(const char *v, Py_ssize_t len)

def xorDecoder(data: bytes, decode: bytes):
    cdef int xorLoc = 0
    cdef int decodeLen = len(decode)
    cdef int dataLen = len(data)
    cdef unsigned char* output = <unsigned char*> malloc(dataLen)
    try:
        j = 0
        for i in data:
            output[j] = i ^ decode[xorLoc]
            xorLoc += 1
            if xorLoc >= decodeLen:
                xorLoc = 0
            j += 1
        return PyBytes_FromStringAndSize(<const char*>output, dataLen)
    finally:
        free(output)
