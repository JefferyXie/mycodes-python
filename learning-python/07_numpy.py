#!/usr/local/bin/python3

"""
A module tells how numpy lib works

Read from binary file with dtype
https://stackoverflow.com/questions/7569563/efficient-way-to-create-numpy-arrays-from-binary-files
https://docs.scipy.org/doc/numpy-1.13.0/reference/arrays.dtypes.html

Create array with nested dtype
https://stackoverflow.com/questions/19201868/how-to-set-dtype-for-nested-numpy-ndarray

numpty.dtype byteorder
https://docs.scipy.org/doc/numpy/reference/generated/numpy.dtype.byteorder.html


Unpack bytes with struct.unpack
https://stackoverflow.com/questions/444591/convert-a-string-of-bytes-into-an-int-python

Read/write csv
https://stackoverflow.com/questions/3518778/how-to-read-csv-into-record-array-in-numpy
https://stackoverflow.com/questions/41585078/how-do-i-read-and-write-csv-files-with-python

"""

import os, sys, datetime
import struct, argparse
import subprocess
import numpy as np

class util(object):

    @staticmethod
    def python_3_plus():
        return sys.version_info[0] >= 3

    @staticmethod
    def get_dir_from_alias(alias):
        try:
            out_bs  = subprocess.check_output(['/bin/bash', '-i', '-c',
                'alias '+alias])
            out_str = out_bs.decode(sys.stdout.encoding).strip()
            return out_str[out_str.index('/'):out_str.rindex("'")]
        except subprocess.CalledProcessError, e:
            print('{0}: {1}'.format(alias, e.output))

    @staticmethod
    def check_file(file_name):
        if not os.access(file_name, os.R_OK):
            print("Cannot read file '{0}', please check.".format(file_name))
            sys.exit()
        f_size = os.path.getsize(file_name)
        if f_size == 0:
            print("File '{0}' is empty, please check.".format(file_name))
            sys.exit()
        return f_size


class formatter(object):
    '''
    def __str__(self):
        sb = []
        for key in self.__dict__:
            sb.append("{key}={value}".
                format(key=key, value=self.__dict__[key]))
        return '{0}:{1}'.format(self.__class__.__name__, ','.join(sb))
    '''
    def __str__(self):
        return str(self.__class__.__name__) + ":" + str(self.__dict__)
    def __repr__(self):
        return self.__str__()
    def dump_csv(self):
        return ''

class bin_dtype(object):
    @classmethod
    def get_dtype(cls):
        return np.dtype([])

    @classmethod
    def bin_data_size(cls):
        return cls.get_dtype().itemsize

class pvec_hdr(formatter, bin_dtype):
    @classmethod
    def get_dtype(cls):
        return (np.dtype([
            ('magic',   '<u4'),
            ('segcap',  '<u4'),
            ('elemsz',  '<u4'),
            ('size',    '<u4')
        ]))

    def __init__(self, data):
        super(pvec_hdr, self).__init__()
        # for python 3.0+, we may use int.from_bytes(..)
        # MagicNum = 0xdead1234 = 3735884340
        (self.magic, self.segcap, self.elemsz, self.size) = (
            struct.unpack('IIII', data))

    def get_seg_padding_sz(self):
        page_sz = os.sysconf("SC_PAGE_SIZE")
        return page_sz - (self.bin_data_size()+self.segcap*self.elemsz)%page_sz

# base class of user_data
class user_data(formatter, bin_dtype):
    def __init__(self, data):
        super(user_data, self).__init__()

    @classmethod
    def from_bin(cls, bins, bins_len):
        if bins_len == user_data_cme.bin_data_size():
            return user_data_cme(bins)
        else:
            return user_data(bins)

class user_data_cme(user_data):
    @classmethod
    def get_dtype(cls):
        return (np.dtype([
            ('cme_id',      '<i4'),
            ('gbx_depth',   '<i4'),
            ('gbi_depth',   '<i4'),
            ('vtt_code',    '<i4'),
            ('dis_factor',  'd'),
            ('tick_sz',     'd'),
            ('cme_sym_len', 'u1'),
            ('cme_symbol',  'u1',   25),
            ('imnt_gr_len', 'u1'),
            ('imnt_group',  'u1',   13),
            ('sec_gr_len',  'u1'),
            ('sec_group',   'u1',   9),
            ('_padding',    '6b'),
            # itemsize = 88
        ]))

    def __init__(self, data):
        super(user_data_cme, self).__init__(data)
        fixed_sz = self.bin_data_size()
        if len(data) < fixed_sz:
            sys.exit('Error: user_data_cme has input data size less than {0}.'
                .format(fixed_sz))

        data = data[:fixed_sz]
        (self.cme_id, self.gbx_depth, self.gbi_depth, self.vtt_code,
        self.dis_factor, self.tick_sz, len1, self.cme_symbol,
        len2, self.imnt_group, len3, self.sec_group, _padding) = (
            struct.unpack('iiiiddB25sB13sB9s6s', data))

class leg(formatter, bin_dtype):
    @classmethod
    def get_dtype(cls):
        return (np.dtype([
            ('iid',         '<i4'),
            ('secType',     'u1'),
            ('_reserved',   'u1'),
            ('ratioQty',    '<i2'),
            ('price',       '<i8'),
            ('delta',       '<i4'),
            # c++ will padding 4 bytes to make size multiple of 8 (@price)
            # dt_leg_def.itemsize = 24
            ('_padding',    '4b'),
        ]))

    def __init__(self, data):
        super(leg, self).__init__()
        self.iid        = data['iid']
        self.secType    = data['secType']

class complx(formatter, bin_dtype):
    @classmethod
    def get_dtype(cls):
        return (np.dtype([
            ('cplxAttrib',  'u1'),
            ('_reserved',   'u1'),
            ('noLegs',      'u1'),
            ('nUserData',   'u1'),
            # c++ will padding 4 bytes to make size multiple of 8 (leg@price)
            # itemsize = 1224
            ('_padding',    '4b'),
            ('legs',    leg.get_dtype(), (util.max_leg_num(),)),
            ('userData',    'u1',   (util.max_user_data(),)),
        ]))

    def __init__(self, data):
        super(complx, self).__init__()
        self.noLegs     = data['noLegs']
        #self.legs       = data['legs']
        self.legs       = []
        for i in range(0, self.noLegs):
            self.legs.append(leg(data['legs'][i]))
        self.nUserData  = data['nUserData']
        self.userData = user_data.from_bin(data['userData'], self.nUserData)


class instrument(formatter, bin_dtype):
    # what if not use '<'?
    @classmethod
    def get_dtype(cls):
        return (np.dtype([
            ('dIId',        '<i4'),
            ('refUlId',     '<i4'),
            ('imntType',    'u1'),
            ('imntAction',  'u1'),
            ('imntSrc',     'u1'),
            ('version',     'u1'),
            # c++ will padding 4 bytes to make size multiple of 8 (leg@price)
            # itemsize = 1240
            ('_padding',    '4b'),
            ('complex',     complx.get_dtype())
        ]))

    def __init__(self, data):
        super(instrument, self).__init__()
        self.dIId       = data['dIId']
        self.refUlId    = data['refUlId']
        self.version    = data['version']
        #self.complex    = data['complex']
        self.complex    = complx(data['complex'])

class instruments_db(formatter):
    instruments = {}

    @classmethod
    def init(cls, fn):
        print("Loading '{0}'...".format(fn))
        all_instrs = np.genfromtxt(fn, delimiter=',', dtype=str)
        #ZB:OZBH8:20180223:151:C,20660413
        for instr in all_instrs:
            desc = instr[0][(instr[0].index(':')+1):]
            v_id = int(instr[1])
            cls.instruments[v_id] = desc
        print("Finished loading '{0}', {1} instruments loaded.".format(
            fn, len(cls.instruments)))

    @classmethod
    def get_desc(cls, v_id):
        return cls.instruments.get(v_id, '')


def process_pvec(in_pvec, out_csv):
    f_size = util.check_file(in_pvec)
    print("File '{0}' size is '{1}'.".format(in_pvec, f_size))

    with open(in_pvec, 'r+b') as f:
        with open(out_csv, mode='w') as of:
            of.write(util.dump_csv_hdr())

            seg_idx = 0
            num_instr = 0
            while f_size > 0:
                hdr = pvec_hdr(f.read(pvec_hdr.bin_data_size()))

                # check if segment is empty
                if hdr.segcap == 0 or hdr.size == 0:
                    print('''Finished loading '{0}', {1} instruments loaded.'''.
                          format(in_pvec, num_instr))
                    return

                print('------------- Segment {0} -------------'.format(seg_idx))
                print(hdr)

                instrs = []
                records = np.fromfile(f,
                    dtype = instrument.get_dtype(), count = hdr.size)

                # dump to csv file
                for record in records:
                    instr = instrument(record)
                    instrs.append(instr)
                    #print(instr)
                    instr_csv = instr.dump_csv()
                    of.write(instr_csv)
                    num_instr += 1

                # ignore the padding bytes
                f.seek(hdr.get_seg_padding_sz(), 1)

                seg_idx += 1

if __name__ == "__main__":
    pvec_file = ''
    out_file  = ''
    instr_fn  = ''
    arg_parser = argparse.ArgumentParser(
        description='Dump instruments from dsid pvec file to csv')
    arg_parser.add_argument('-i', type=str, default=pvec_file,
        help='The input dsid pvec file')
    arg_parser.add_argument('-o', type=str, default=out_file,
        help='The output csv file')

    args = arg_parser.parse_args()
    pvec_file = args.i
    out_file  = args.o

    now = datetime.datetime.now()
    today = datetime.datetime.strftime(now, '%Y%m%d')
    if not pvec_file:
        cdv_dir = util.get_dir_from_alias('cdv')
        pvec_file = '{0}/dsid.{1}.imnts'.format(cdv_dir, today)

    if not out_file:
        cdd_dir = util.get_dir_from_alias('cdd')
        out_file = '{0}/dsid.{1}.imnts.csv'.format(cdd_dir, today)

    process_pvec(pvec_file, out_file)
