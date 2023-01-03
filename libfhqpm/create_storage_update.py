#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys
import random
import glob2
import string


class CreateStorageUpdate:
    def __init__(self):
        self.__updates = []
        self.__end_points = []
        self.__max_weight = 0
    
    def recoursive_search_endpoints(self, spoint, weight):
        found = False
        for v in self.__updates:
            if v["from"] == spoint:
                found = True
                self.recoursive_search_endpoints(v["to"], weight + 1)
        if not found:
            if weight > self.__max_weight:
                self.__max_weight = weight
            self.__end_points.append({
                "point": spoint,
                "weight": weight
            })

    def create(self):
        self.__max_weight = 0
        self.__updates = []
        self.__end_points = []

        updatespath =  os.path.join("src", "storages", "updates")

        _cpp_files = glob2.glob(
            os.path.join(updatespath, "*.cpp")
        )

        # print(_cpp_files)

        pattern = r'.*WsjcppStorageUpdateBase.*\(.*"([a-zA-Z0-9]*)".*,.*"([a-zA-Z0-9]*)".*,.*\).*'

        for filepath in _cpp_files:
            # print(filepath)
            with open(filepath) as f:  
                line = f.readline()
                while line:
                    line = line.strip()
                    if re.match(pattern, line):
                        versions = re.search(pattern, line, re.IGNORECASE)
                        if versions:
                            self.__updates.append({
                                "from": versions.group(1),
                                "to": versions.group(2),
                            })
                    line = f.readline()

        # print(self.__updates)
        # print all updates
        for v in self.__updates:
           print("[" + v["from"] + "] -> [" + v["to"] + "]")

        # find the ends in graph
        self.recoursive_search_endpoints("", 0)

        # print(self.__end_points)

        if len(self.__end_points) == 0:
            print("Not found updates")
            sys.exit(-1)

        endpoint = ""

        for i in self.__end_points:
            if i["weight"] == self.__max_weight and endpoint == "":
                endpoint = i["point"]
            elif i["weight"] == self.__max_weight and endpoint != "":
                print("WARNING: Found points with same weights, will be used first. Ignored: " + i["point"])

        print("Found point: " + endpoint + " weight: " + str(self.__max_weight))
        newpoint = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))

        newpoint_upper = newpoint.upper()
        endpoint_upper = endpoint.upper()

        filename_h = "update_" + endpoint + "_" + newpoint + ".h"
        filename_cpp = "update_" + endpoint + "_" + newpoint + ".cpp"

        filename_h = os.path.join(updatespath, filename_h)
        filename_cpp = os.path.join(updatespath, filename_cpp)

        print("Generate header file: " + filename_h)

        f_h = open(filename_h, 'w')
        f_h.write("/*\n")
        f_h.write("MIT License\n")
        f_h.write("\n")
        f_h.write("Copyright (c) 2011-2023 FreeHackQuest <freehackquest@gmail.com>\n")
        f_h.write("\n")
        f_h.write("Permission is hereby granted, free of charge, to any person obtaining a copy\n")
        f_h.write("of this software and associated documentation files (the \"Software\"), to deal\n")
        f_h.write("in the Software without restriction, including without limitation the rights\n")
        f_h.write("to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n")
        f_h.write("copies of the Software, and to permit persons to whom the Software is\n")
        f_h.write("furnished to do so, subject to the following conditions:\n")
        f_h.write("\n")
        f_h.write("The above copyright notice and this permission notice shall be included in all\n")
        f_h.write("copies or substantial portions of the Software.\n")
        f_h.write("\n")
        f_h.write("THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n")
        f_h.write("IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n")
        f_h.write("FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n")
        f_h.write("AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n")
        f_h.write("LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n")
        f_h.write("OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n")
        f_h.write("SOFTWARE.\n")
        f_h.write("*/\n\n")
        f_h.write("#ifndef UPDATE_" + endpoint_upper + "_" + newpoint_upper + "_H\n")
        f_h.write("#define UPDATE_" + endpoint_upper + "_" + newpoint_upper + "_H\n")
        f_h.write("\n")
        f_h.write("#include <wsjcpp_storages.h>\n")
        f_h.write("\n")
        f_h.write("class Update_" + endpoint + "_" + newpoint + " : public WsjcppStorageUpdateBase {\n")
        f_h.write("    public:\n")
        f_h.write("        Update_" + endpoint + "_" + newpoint + "();\n")
        f_h.write("};\n")
        f_h.write("\n")
        f_h.write("#endif // UPDATE_" + endpoint_upper + "_" + newpoint_upper + "_H\n")
        f_h.close()

        print("Generate source file: " + filename_cpp)

        f_cpp = open(filename_cpp, 'w')
        f_cpp.write("/*\n")
        f_cpp.write("MIT License\n")
        f_cpp.write("\n")
        f_cpp.write("Copyright (c) 2011-2023 FreeHackQuest <freehackquest@gmail.com>\n")
        f_cpp.write("\n")
        f_cpp.write("Permission is hereby granted, free of charge, to any person obtaining a copy\n")
        f_cpp.write("of this software and associated documentation files (the \"Software\"), to deal\n")
        f_cpp.write("in the Software without restriction, including without limitation the rights\n")
        f_cpp.write("to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n")
        f_cpp.write("copies of the Software, and to permit persons to whom the Software is\n")
        f_cpp.write("furnished to do so, subject to the following conditions:\n")
        f_cpp.write("\n")
        f_cpp.write("The above copyright notice and this permission notice shall be included in all\n")
        f_cpp.write("copies or substantial portions of the Software.\n")
        f_cpp.write("\n")
        f_cpp.write("THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n")
        f_cpp.write("IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n")
        f_cpp.write("FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n")
        f_cpp.write("AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n")
        f_cpp.write("LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n")
        f_cpp.write("OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n")
        f_cpp.write("SOFTWARE.\n")
        f_cpp.write("*/\n\n")
        f_cpp.write("#include \"update_" + endpoint + "_" + newpoint + ".h\"\n")
        f_cpp.write("\n")
        f_cpp.write("REGISTRY_WSJCPP_STORAGE_UPDATE(Update_" + endpoint + "_" + newpoint + ")\n")
        f_cpp.write("\n")
        f_cpp.write("Update_" + endpoint + "_" + newpoint + "::Update_" + endpoint + "_" + newpoint + "()\n")
        f_cpp.write("    : WsjcppStorageUpdateBase(\"" + endpoint + "\", \"" + newpoint + "\", \"TODO\") {\n")
        f_cpp.write("    \n")
        f_cpp.write("    // fill the array with struct changes\n")
        f_cpp.write("}\n")
        f_cpp.write("\n")
        f_cpp.close()
