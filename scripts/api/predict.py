import os
import re
import random
import torch
import torch.nn as nn
from rich.console import Console
from transformers import T5Tokenizer, T5ForConditionalGeneration
from collections import defaultdict

console = Console(record = True)

torch.cuda.manual_seed(3007)
torch.manual_seed(3007)

class PredictionModelObject(object):

    def __init__(self):

        self.model = T5ForConditionalGeneration.from_pretrained('../../models/model_files')
        self.tokenizer = T5Tokenizer.from_pretrained('../../models/model_files')

    
    def beamSearch(self, text, seq_len, seq_num):

        outputDict = dict()
        outputDict["plots"] = {}
        input_ids = self.tokenizer.encode(text, return_tensors = "pt")
        beamOp = self.model.generate(
            input_ids,
            max_length = seq_len,
            do_sample = True,
            top_k = 100,
            top_p = 0.95,
            num_return_sequences = seq_num
        )

        for ix, sample_op in enumerate(beamOp):
            outputDict["plots"][ix+1] = self.tokenizer.decode(sample_op, skip_special_tokens = True)
            
        
        return outputDict


    def genreToPlot(self, genre, seq_len, seq_num):

        text = f"generate plot for genre: {genre}"

        return self.beamSearch(text, seq_len, seq_num)

    def genreDirectorToPlot(self, genre, director, seq_len, seq_num):

        text = f"generate plot for genre: {genre} and director: {director}"
        
        return self.beamSearch(text, seq_len, seq_num)

    def genreDirectorCastToPlot(self, genre, director, cast, seq_len, seq_num):

        text = f"generate plot for genre: {genre} director: {director} cast: {cast}"

        return self.beamSearch(text, seq_len, seq_num)

    def genreDirectorCastEthnicityToPlot(self, genre, director, cast, ethnicity, seq_len, seq_num):

        text = f"generate plot for genre: {genre} director: {director} cast: {cast} and ethnicity: {ethnicity}"

        return self.beamSearch(text, seq_len, seq_num)
    
    def genreCastToPlot(self, genre, cast, seq_len, seq_num):

        text = f"genreate plot for genre: {genre} and cast: {cast}"

        return self.beamSearch(text, seq_len, seq_num)

    def genreEthnicityToPlot(self, genre, ethnicity, seq_len, seq_num):

        text = f"generate plot for genre: {genre} and ethnicity: {ethnicity}"

        return self.beamSearch(text, seq_len, seq_num)

    def returnPlot(self, genre, director, cast, ethnicity, seq_len, seq_num):
        console.log('Got genre: ', genre, 'director: ', director, 'cast: ', cast, 'seq_len: ', seq_len, 'seq_num: ', seq_num, 'ethnicity: ',ethnicity)
        seq_len = int(seq_len) if not seq_len else 200
        seq_num = int(seq_num) if not seq_num else 2

        if not director and not cast and not ethnicity:

            return self.genreToPlot(genre, seq_len, seq_num), "Pass"
        
        elif genre and director and not cast and not ethnicity:

            return self.genreDirectorToPlot(genre, director, seq_len, seq_num), "Pass"

        elif genre and director and cast and not ethnicity:

            return self.genreDirectorCastToPlot(genre, director, cast, seq_len, seq_num), "Pass"

        elif genre and director and cast and ethnicity:

            return self.genreDirectorCastEthnicityToPlot(genre, director, cast, ethnicity, seq_len, seq_num), "Pass"

        elif genre and cast and not director and not ethnicity:

            return self.genreCastToPlot(genre, cast, seq_len, seq_num), "Pass"
        
        elif genre and ethnicity and not director and not cast:

            return self.genreEthnicityToPlot(genre, ethnicity, seq_len, seq_num), "Pass"

        else:

            return "Genre cannot be empty", "Fail"

# console.log("Loading Model Object")
# predictionObject = PredictionModelObject()
# console.log("Loaded Model Object")

# console.log("Comeday Action")
# console.log(predictionObject.returnPlot(
#     "comedy action", None, None, None, 1000, 2
# ))

# console.log("Suspense Thriller - Joe Russo")
# console.log(predictionObject.returnPlot(
#     "suspense thriller", "Joe Russo", None, None, 1000, 2
# ))

# console.log("Drama Romance - Karan Johar - Ranbir Kapoor Deepika Padukone")
# console.log(predictionObject.returnPlot(
#     "drama romance", "Karan Johar", "Ranbir Kapoor, Deepika Padukone", None, 1000, 2
# ))

# console.log("murder mystery - Anurag Kashyap - Nawazidin Siddique - Bollywood")
# console.log(predictionObject.returnPlot(
#     "murder mystery", "Anurag Kashyap", "Nawazidin Siddique", "Bollywood", 1000, 2
# ))

# console.save_text("prediction-op-1.txt")