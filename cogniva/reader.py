# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
#  This file is part of the cogniva parsing tool.                            #
#                                                                            #
#  cogniva is free software: you can redistribute it and/or modify           #
#  it under the terms of the GNU General Public License as published by      #
#  the Free Software Foundation, either version 3 of the License, or         #
#  (at your option) any later version.                                       #
#                                                                            #
#  cogniva is distributed in the hope that it will be useful,                #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the              #
#  GNU General Public License for more details.                              #
#                                                                            #
#  You should have received a copy of the GNU General Public License         #
#  along with cogniva. If not, see <http://www.gnu.org/licenses/>.           #
#                                                                            #
##############################################################################

import re

log_patt1 = re.compile(r"""lmod:[ ]
                       source=ModUsageTrack,[ ]
                       time=(?P<timestamp>[0-9]+.[0-9]*),[ ]
                       host=(?P<host>[\S]+),[ ]
                       user=(?P<user>[\S]+),[ ]
                       action=(?P<action>load),[ ]
                       module=(?P<module>[\S]+),[ ]
                       path=(?P<path>[\S]+)
                       """, re.VERBOSE)

# dataset sample
#
# ...
# source=ModUsageTrack,
# time=1578697200,
# host=debug01,
# user=jay,
# action=load,
# module=ifort/2020,
# path=/opt/modulefiles/lib/ifort/3030,
# cat=ifort,
# version=2020,
# shell=bash,
# job_id=4,
# job_acc=prod,
# job_part=ai

log_patt2 = re.compile(r"""source=ModUsageTrack,[ ]
                       time=(?P<timestamp>[0-9]+.[0-9]*),[ ]
                       host=(?P<host>[\S]+),[ ]
                       user=(?P<user>[\S]+),[ ]
                       action=(?P<action>load),[ ]
                       module=(?P<module>[\S]+),[ ]
                       path=(?P<path>[\S]+),[ ]
                       cat=(?P<cat>[\S]+),[ ]
                       version=(?P<version>[\S]+),[ ]
                       shell=(?P<shell>[\S]+),[ ]
                       job_id=(?P<job_id>[0-9]+),[ ]
                       job_acc=(?P<job_acc>[\S]+),[ ]
                       job_part=(?P<job_part>[\S]+)
                       """, re.VERBOSE)

# m01.log
#
# Mar
# 1
# 14:07:30
# i01
# lmod:
# user=obiwan
# host=merak
# submit_host=merak
# job_id=883208
# partition=gpu
# qos=gpu
# account=lpdi
# module=gcc/8.4.0-cuda
# path=/merak/linux-rhel7-x86_64/Core/gcc/8.4.0-cuda.lua
# time=1646140050.316728

log_patt3 = re.compile(r"""lmod:[ ]
                       user=(?P<user>[\S]+)[ ]
                       host=(?P<host>[\S]+)[ ]
                       submit_host=(?P<submit_host>[\S]+)[ ]
                       job_id=(?P<job_id>[0-9]+)[ ]
                       partition=(?P<partition>[\S]+)[ ]
                       qos=(?P<qos>[\S]+)[ ]
                       account=(?P<account>[\S]+)[ ]
                       module=(?P<module>[\S]+)[ ]
                       path=(?P<path>[\S]+)[ ]
                       time=(?P<timestamp>[0-9]+.[0-9]*)
                       """, re.VERBOSE)

PATT = log_patt3

def _open_file(file):
    ''' Returns correct open command.
       Checks if file is compressed and returns the
       correct open command to handle the file.
    '''
    from binascii import hexlify
    def is_gz_file(filepath):
        with open(filepath, 'rb') as test_f:
            return hexlify(test_f.read(2)) == b'1f8b'

    if is_gz_file(file):
        from gzip import open as open_gzip
        result = open_gzip(file)
    else:
        result = open(file)
    return(result)

def read_users(params):
    ''' Reads log file.
    This function will count the number of modules
    that have been loaded by distinct users.
    '''
    dic = {}
    file, start_date, end_date, module = params
    with _open_file(file) as fp:
        for line in fp:
            if PATT.search(line) is not None:

                if module is not None:
                    if PATT.search(line).groupdict()['module'] not in module:
                        continue
                if start_date is not None:
                    if float(PATT.search(line).groupdict()['timestamp']) < start_date:
                        continue
                if end_date is not None:
                    if float(PATT.search(line).groupdict()['timestamp']) > end_date:
                        continue

                dic[ (PATT.search(line).groupdict()['module'], PATT.search(line).groupdict()['user']) ] = True
    return {file : list(dic.keys())}

def read_users_cat(params):
    ''' Reads log file.
    This function will count the number of modules
    that have been loaded by distinct users. Results
    are grouped by category
    '''
    dic = {}
    file, start_date, end_date, module = params
    with _open_file(file) as fp:
        for line in fp:
            if PATT.search(line) is not None:

                if module is not None:
                    if PATT.search(line).groupdict()['module'] not in module:
                        continue
                if start_date is not None:
                    if float(PATT.search(line).groupdict()['timestamp']) < start_date:
                        continue
                if end_date is not None:
                    if float(PATT.search(line).groupdict()['timestamp']) > end_date:
                        continue

                dic[ (PATT.search(line).groupdict()['cat'],
                     (PATT.search(line).groupdict()['module'], PATT.search(line).groupdict()['user'])) ] = True
    return {file : list(dic.keys())}

def read_users_path(params):
    ''' Reads log file.
    This function will count the number of modules
    that have been loaded by distinct users. Results
    are grouped by path.
    '''
    dic = {}
    file, start_date, end_date, module = params
    with _open_file(file) as fp:
        for line in fp:
            if PATT.search(line) is not None:

                if module is not None:
                    if PATT.search(line).groupdict()['module'] not in module:
                        continue
                if start_date is not None:
                    if float(PATT.search(line).groupdict()['timestamp']) < start_date:
                        continue
                if end_date is not None:
                    if float(PATT.search(line).groupdict()['timestamp']) > end_date:
                        continue

                path = PATT.search(line).groupdict()['path']
                dic[ (path[:path.find('/',1)],
                     (PATT.search(line).groupdict()['module'], PATT.search(line).groupdict()['user'])) ] = True
    return {file : list(dic.keys())}

def read_jobs(params):
    ''' Reads log file.
    This function will count the number of modules
    that have been loaded by distinct jobs.
    '''
    dic = {}
    file, start_date, end_date, module = params
    with _open_file(file) as fp:
        for line in fp:
            #print(line)
            if PATT.search(line) is not None:

                if module is not None:
                    if PATT.search(line).groupdict()['module'] not in module:
                        continue
                if start_date is not None:
                    if float(PATT.search(line).groupdict()['timestamp']) < start_date:
                        continue
                if end_date is not None:
                    if float(PATT.search(line).groupdict()['timestamp']) > end_date:
                        continue

                dic[ (PATT.search(line).groupdict()['module'], PATT.search(line).groupdict()['job_id']) ] = True
    return {file : list(dic.keys())}

def read_jobs_cat(params):
    ''' Reads log file.
    This function will count the number of modules
    that have been loaded by distinct jobs. Results
    are grouped by category.
    '''
    dic = {}
    file, start_date, end_date, module = params
    with _open_file(file) as fp:
        for line in fp:
            if PATT.search(line) is not None:

                if module is not None:
                    if PATT.search(line).groupdict()['module'] not in module:
                        continue
                if start_date is not None:
                    if float(PATT.search(line).groupdict()['timestamp']) < start_date:
                        continue
                if end_date is not None:
                    if float(PATT.search(line).groupdict()['timestamp']) > end_date:
                        continue

                dic[ (PATT.search(line).groupdict()['cat'],
                     (PATT.search(line).groupdict()['module'], PATT.search(line).groupdict()['job_id'])) ] = True
    return {file : list(dic.keys())}

def read_jobs_path(params):
    ''' Reads log file.
    This function will count the number of modules
    that have been loaded by distinct jobs. Results
    are grouped by path.
    '''
    dic = {}
    file, start_date, end_date, module = params
    with _open_file(file) as fp:
        for line in fp:
            if PATT.search(line) is not None:

                if module is not None:
                    if PATT.search(line).groupdict()['module'] not in module:
                        continue
                if start_date is not None:
                    if float(PATT.search(line).groupdict()['timestamp']) < start_date:
                        continue
                if end_date is not None:
                    if float(PATT.search(line).groupdict()['timestamp']) > end_date:
                        continue

                path = PATT.search(line).groupdict()['path']
                dic[ (path[:path.find('/',1)],
                     (PATT.search(line).groupdict()['module'], PATT.search(line).groupdict()['job_id'])) ] = True
    return {file : list(dic.keys())}

