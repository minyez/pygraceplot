# -*- coding: utf-8 -*-
"""helper function in dealing with data, digits and mathematics"""
import numpy as np

class Data(object):
    """Object for storage and extraction of data

    Args:
        x, y, z (array-like) : positional, data columns in order
        datatype (str) : the data type. See datatypes
        label (str)
        comment (str) : extra comment for the data
        error should be parsed by using keywords arguments, supported are
            dx
            dxl (l means lower)
            dy
            dyl
            dz
            dzl

    Class attributes:
        available_types : available data types

    Public methods:
        get
        get_extra
        export
        export_extra

    Constants:
        DATATYPES (dict) : available datatypes
            key is the acronym of the data type
            value a list, optional arguments for left-and-right errors
    """
    extra_data = ['dx', 'dxl', 'dy', 'dyl', 'size']
    DATATYPES = {
        'xy': (2, []),
        'bar': (2, []),
        'xysize': (2, ['size']),
        'xydx': (2, ['dx']),
        'xydy': (2, ['dy']),
        'bardy': (2, ['dy']),
        'xydxdx': (2, ['dx', 'dxl']),
        'xydydy': (2, ['dy', 'dyl']),
        'bardydy': (2, ['dy', 'dyl']),
        'xydxdy': (2, ['dx', 'dy']),
        'xydxdxdydy': (2, ['dx', 'dxl', 'dy', 'dyl']),
        }
    available_types = tuple(DATATYPES.keys())

    def __init__(self, x, y, datatype=None, label=None, comment=None, **extras):
        datatype, self._extra_cols = Data._check_data_type(datatype=datatype, **extras)
        if datatype.startswith("bar") or datatype.startswith("xy"):
            self.x, self.y = x, y
            self.x = np.array(self.x)
            self.y = np.array(self.y)
            self._data_cols = ['x', 'y']
        else:
            raise ValueError("Unsupported datatype", datatype)
        for opt in self._extra_cols:
            self.__setattr__(opt, extras[opt])
        self.label = label
        self.comment = comment
        self.datatype = datatype

    def xmin(self):
        """get the min value of abscissa"""
        return self.x.min()

    def xmax(self):
        """get the max value of abscissa"""
        return self.x.max()

    def max(self):
        """get the max value among data point"""
        return self.y.max()

    def min(self):
        """get the min value among data point"""
        return self.y.min()

    def _get(self, data_cols, scale=1.0, transpose=False):
        """get all data value

        default as 
                (x1, y1, z1),
                (x2, y2, z2),
                ...

        Args:
            transpose (bool) : if True, the output will be
                x1, x2, x3...
                y1, y2, y3...
                z1, z2, z3...
        """
        d = np.stack([self.__getattribute__(arg) for arg in data_cols])
        if transpose:
            d = d.transpose()
        return d * scale

    def _export(self, data_cols, form=None, transpose=False, sep=None):
        """export data/error to a list, each member as a line of string for data

        Default output will be one line for each data type, i.e.

            'x1[sep]y1[sep]z1'
            'x2[sep]y2[sep]z2'
            'x3[sep]y3[sep]z3'
            ...

        Set `transpose` to True will get

            'x1[sep]x2[sep]x3 ...'
            'y1[sep]y2[sep]y3 ...'
            'z1[sep]z2[sep]z3 ...'

        Args:
            transpose (bool)
            sep (str)
            form (formatting string or its list/tuple) : formatting string
                default to use float
                if a str is parsed, this format apply to all data columns
                if Iterable, each form will be parsed respectively.
        """
        slist = []
        # check if format string is valid 
        if form is not None and isinstance(form, (tuple, list)):
            if len(form) != len(data_cols):
                msg = "format string does not conform data columns"
                raise ValueError(msg, form, len(data_cols))

        data_all = self._get(data_cols)
        return _export_2d_data(data_all, transpose=transpose, form=form, sep=sep)

    def get_data(self, transpose=False):
        """get all data values

        Default as
            (x1, y1, z1),
            (x2, y2, z2),
            ...

        Args:
            transpose (bool) : if True, the output will be
                x-array,
                y-array,
                ...
        """
        return self._get(self._data_cols, transpose=transpose)

    def get_extra(self, transpose=False):
        """get all error value
       
        Default as 
            (xel1, xer1, yel1, yer1, ...),
            (xel2, xer2, yel2, yer2, ...),

        Args:
            transpose (bool) : if True, the output will be
                xel1, xel2, xel3, ...
                xer1, xer2, xer3, ...
                yel1, yel2, yel3, ...
                ...
        """
        return self._get(self._extra_cols, transpose=transpose)

    def get(self, transpose=False):
        """get all data and extra value

        Default as
                (x1, y1, z1, xel1, xer1, yel1, yer1, ...),
                (x2, y2, z2, xel2, xer2, yel2, yer2, ...),

        Args:
            transpose (bool) : if True, the output will be
                x1, x2, x3, ...
                y1, y2, y3, ...
                ...
                xel1, xel2, xel3, ...
                ...
        """
        return self._get(self._data_cols + self._extra_cols, transpose=transpose)

    def export_data(self, form=None, transpose=False, sep=None):
        """Export the data as a list of strings
        
        See get for the meaning of transpose

        Args:
            sep (str)
            form (formatting string or its list/tuple) : formatting string
                if a str is parsed, this format apply to all data columns
                if Iterable, each form will be parsed respectively.
        """
        return self._export(self._data_cols, form=form, transpose=transpose, sep=sep)

    def export_extra(self, form=None, transpose=False, sep=None):
        """Export extra data as a list of strings

        See get_extra for the meaning of transpose

        Args:
            sep(str)
            form (formatting string or its list/tuple) : formatting string
                if a str is parsed, this format apply to all data columns
                if Iterable, each form will be parsed respectively.
        """
        return self._export(self._extra_cols, form=form, transpose=transpose, sep=sep)

    def export(self, form=None, transpose=False, sep=None):
        """Export both data and extras as a list of strings
        
        See get_all for the meaning of transpose

        Args:
            sep (str)
            form (formatting string or its list/tuple) : formatting string
                if a str is parsed, this format apply to all data columns
                if Iterable, each form will be parsed respectively.
        """
        return self._export(self._data_cols + self._extra_cols,
                            form=form, transpose=transpose, sep=sep)

    @classmethod
    def _check_data_type(cls, datatype=None, **extras):
        """confirm the data type of input. Valid types are declared in Data.DATATYPES
    
        Args:
            datatype (str) : type of data. None for automatic detect
            extras for parsing extra data such as error
                d(x,y) (float) : error. when the according l exists, it becomes the upper error
                d(x,y)l (float) : lower error
                size (float) : size of marker

        Returns:
            str, list
        """
        extra_cols = []
        # automatic detect
        t = 'xy'
        if datatype is None:
            for dt, (n, ec) in cls.DATATYPES.items():
                if dt.startswith(t):
                    find_all = all([extras.get(required_e, None) for required_e in ec])
                    if find_all:
                        extra_cols = ec
                        return dt, extra_cols
            raise ValueError("cannot determine the datatype")
        # check consistency
        t = datatype.lower()
        if t in cls.available_types:
            _, extra_cols = cls.DATATYPES[t]
            find_all = all([required_e in extras for required_e in extra_cols])
            if not find_all:
                raise ValueError("Inconsistent extra data and specified datatype ", datatype)
        else:
            raise ValueError("Unsupported datatype", datatype)
        # some error is parsed
        return t, extra_cols

def _export_2d_data(data, form=None, transpose=False, sep=None):
    """print the 2-dimension data into list of strings

    Args:
        data (2d array)
        form (str or tuple/list): format string of each type of data.
        transpose (bool) : control the application of format `form` when it is iterable.
            Set False for column-wise, i.e. data[:][i] in same format form[i],
            True for row-wise, i.e. data[i][:] in same format form[i]
        sep (str)

    """
    slist = []
    if form is None:
        if transpose:
            l = len([x[0] for x in data])
        else:
            l = len(data[0])
        form = ['{:f}',] * l

    if sep is None:
        sep = " "
    if transpose:
        data = np.transpose(data)
    for i, array in enumerate(data):
        if isinstance(form, str):
            s = sep.join([form.format(x) for x in array])
        elif isinstance(form, (list, tuple)):
            if transpose:
                # array = (x1, y1, z1)
                s = sep.join([f.format(x) for f, x in zip(form, array)])
            else:
                # array = (x1, x2, x3)
                s = sep.join([form[i].format(x) for x in array])
        else:
            raise ValueError("invalid format string {:s}".format(form))
        slist.append(s)
    return slist

