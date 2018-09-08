# -*- coding: utf-8 -*-
# @Time    : 2018/9/9 20:49
# @Author  : geekspeng
# @Email   : geekspeng@icloud.com
import os
import re
import subprocess
import sys
from shutil import rmtree

from flask import current_app


def get_sorted_author(value):
    try:
        regexes = ["^(JR|SR)\.?$", "^I{1,3}\.?$", "^IV\.?$"]
        combined = "(" + ")|(".join(regexes) + ")"
        value = value.split(" ")
        if re.match(combined, value[-1].upper()):
            value2 = value[-2] + ", " + " ".join(value[:-2]) + " " + value[-1]
        else:
            value2 = value[-1] + ", " + " ".join(value[:-1])
    except Exception:
        value2 = value
    return value2


def resolve_folder_conflict(base_path, folder):
    if os.path.exists(os.path.join(base_path, folder)):
        count = 0
        while True:
            count = count + 1
            new_folder = '%s(%d)' % (folder, count)
            if not os.path.exists(os.path.join(base_path, new_folder)):
                return new_folder
    else:
        return folder


def delete_book(file_path):
    if os.path.exists(file_path):
        rmtree(file_path)


def convert_book(convert_tool_path, old_file_path, new_file_path):
    try:
        if (os.name == 'posix') and (sys.version_info > (3, 0)):
            command = [convert_tool_path, old_file_path, new_file_path]
        p = subprocess.Popen(command, stdout=subprocess.PIPE, universal_newlines=True)
    except OSError as e:
        return "ebook-converter failed"
    p.communicate()
    if (0 == p.returncode) and (os.path.isfile(new_file_path)):
        return None
    else:
        return "ebook-converter failed"
