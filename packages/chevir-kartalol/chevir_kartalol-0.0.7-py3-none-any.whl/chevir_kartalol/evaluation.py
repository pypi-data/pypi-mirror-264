import torch
from torchtext import data
import re
import os
from urllib.request import urlretrieve
from pathlib import Path
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
from spacy.lang.azb import South_Azerbaijani 
from .transformer import TranslateTransformer

if torch.cuda.is_available():  
  dev = "cuda:0"
else:  
  dev = "cpu"  
device = torch.device(dev)
enNLP = English()
arNLP = South_Azerbaijani()

enTokenizer = Tokenizer(enNLP.vocab)
arTokenizer =  Tokenizer(arNLP.vocab)


class Dilmanc:
    def __init__(self):
        # Initialize fields with tokenization and special tokens
        self.SRC = data.Field(tokenize=self.myTokenizerEN, batch_first=False, init_token="<sos>", eos_token="<eos>")
        self.TARGET = data.Field(tokenize=self.myTokenizerAR, batch_first=False, init_token="باشلانغیج", eos_token="سوْن")
        # Load vocabularies
        self.model_file_path = Path(__file__).parent /'azb_model202402.pt'
        self.download_model_files()
        self.SRC.vocab = torch.load(Path(__file__).parent /'src_vocab202402.pt')
        self.TARGET.vocab = torch.load(Path(__file__).parent /'target_vocab202402.pt')
        
        # Extract vocabulary sizes
        src_vocab_size = len(self.SRC.vocab)
        trg_vocab_size = len(self.TARGET.vocab)
        
        # Transformer model parameters
        num_heads = 8
        num_encoder_layers = 6
        num_decoder_layers = 6
        max_len = 170
        embedding_size = 256
        src_pad_idx = self.SRC.vocab.stoi["<pad>"]
        
        # Initialize the model
        self.model = TranslateTransformer(
            embedding_size,
            src_vocab_size,
            trg_vocab_size,
            src_pad_idx,
            num_heads,
            num_encoder_layers,
            num_decoder_layers,
            max_len
        ).to(device)
        
        # Load model weights
        self.model.load_state_dict(torch.load(Path(__file__).parent /'azb_model202402.pt', map_location=device))
        self.model.to(device)
        self.model.eval()
        
        # Set device
        self.device = device
    
    def download_model_files(self):
        if not os.path.exists():
            print(f"Downloading model file to {self.model_file_path}...")
            urlretrieve('https://drive.usercontent.google.com/download?id=1o38vwHskSU7SN-IdXJwTqsDFFrwZnxR_&export=download&authuser=0&confirm=t&uuid=a4675024-a0ac-46bf-bade-a04985525d73&at=APZUnTXTxdh1VRUixTTLJUIcWQUZ:1711293439520',
                self.model_file_path)
            print("Download complete.")


    def chevir(self, sentence):
        # Process the sentence
        processed_sentence = self.SRC.process([self.myTokenizerEN(sentence)]).to(self.device)
        trg = ["باشلانغیج"]
        for _ in range(60):
            trg_indices = [self.TARGET.vocab.stoi[word] for word in trg]
            outputs = torch.Tensor(trg_indices).unsqueeze(1).to(self.device)
            outputs = self.model(processed_sentence, outputs)
            
            next_word = self.TARGET.vocab.itos[outputs.argmax(2)[-1:].item()]
            if next_word == "<unk>":
                continue
            trg.append(next_word)
            if next_word == "سوْن":
                break
        return " ".join([word for word in trg if word != "<unk>"][1:-1])

    def myTokenizerEN(self, x):
        return  [word.text for word in 
            enTokenizer(re.sub(r"\s+\s+"," ",re.sub(r"[\.\'\`\"\r+\n+]"," ",x.lower())).strip())]
    def myTokenizerAR(self, x):
        return  [word.text for word in 
            arTokenizer(re.sub(r"\s+\s+"," ",re.sub(r"[\.\'\`\"\r+\n+]"," ",x.lower())).strip())]


if __name__ == "__main__":
    translator = Dilmanc()
    print(translator.chevir("When do you want to grow up?"))
    print(translator.chevir("what do you want"))