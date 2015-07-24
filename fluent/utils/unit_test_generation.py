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

from fluent.utils.csv_helper import readCSV, writeCSV

dataDir = "/Users/numenta/Documents/nupic.fluent/data/sample_reviews_unit"

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

def generateDataFile(inputData, type):
    """
    Generates a samples data file with all of the words in the sample
    reversed.

    @param  (str)               Path to input original samples data file
    @param  (TextPreprocess)    Processor to perform some text cleanup.

    """
    if type == "scrambled":
      fileName = "sample_reviews_data_training_scramble.csv"
    elif type == "reversed":
      fileName = "sample_reviews_data_training_reverse.csv"

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

    writeCSV(data, headers, os.path.join(dataDir, fileName))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputData",
                        type=str,
                        help="Path to input data file")
    args = parser.parse_args()

    generateDataFile(args.inputData, "scrambled")
    generateDataFile(args.inputData, "reversed")
