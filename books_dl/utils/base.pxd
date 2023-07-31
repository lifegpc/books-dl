cdef extern from "Python.h":
    object PyBytes_FromStringAndSize(const char *v, Py_ssize_t len)
