# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2015, Numenta, Inc.  Unless you have purchased from
# Numenta, Inc. a separate commercial license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------
"""
This file contains CSV utility functions to use with nupic.fluent experiments.
"""

import argparse
import os
import random
import string

from fluent.utils.csv_helper import readCSV, writeCSV



def cleanTokens(tokens):
    """ Traverses list of tokens and generates new list of tokens
    with [identifier deleted] as one token

    @param  (str)               List of tokens generated by splitting samples
                                by white space.

    @return (list)              List of tokens with '[identifier deleted]' as
                                one token instead of two.
    """
    cleanTokens = []
    for token in tokens:
      if token == "[identifier":
        cleanTokens.append("[identifier deleted]")
      elif token != "deleted]":
        cleanTokens.append(token)
    return cleanTokens


def generateDataFile(inputData, outputDataDir, type):
    """
    Generates a samples data file with all of the words in the sample
    reversed.

    @param  (str)               Path to input original samples data file
    @param  (TextPreprocess)    Processor to perform some text cleanup.

    """
    if not os.path.exists(outputDataDir):
        os.makedirs(outputDataDir)

    fileName = string.join(inputData.split(".")[:-1], ".") + "_" + type + ".csv"
    dataDict = readCSV(inputData, 2, 3)
    headers = ["QID", "QuestionText", "Response", "Classification1", "Classification2",
               "Classification3"]
    data = []
    for sample in dataDict.items():
      response = sample[1][0]
      tokens = response.split(" ")
      tokens = cleanTokens(tokens)

      response = None
      if type == "scrambled":
        random.shuffle(tokens)
        response = " ".join(tokens)
      elif type == "reversed":
        response = " ".join(tokens[::-1])

      dataToWrite = [sample[0], "", response]
      dataToWrite.extend(sample[1][1])
      data.append(dataToWrite)

    writeCSV(data, headers, os.path.join(outputDataDir, fileName))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputData",
                        type=str,
                        required=True,
                        help="Path to input data file")
    parser.add_argument("--outputDataDir",
                        type=str,
                        default='data/sample_reviews_unit',
                        help="Desired directory for output data file")
    args = parser.parse_args()

    generateDataFile(args.inputData, args.outputDataDir, "scrambled")
    generateDataFile(args.inputData, args.outputDataDir, "reversed")
