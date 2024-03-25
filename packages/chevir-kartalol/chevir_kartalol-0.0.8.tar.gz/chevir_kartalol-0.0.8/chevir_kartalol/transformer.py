from torch import nn
import torch
if torch.cuda.is_available():  
  dev = "cuda:0" 
  print("gpu up")
else:  
  dev = "cpu"  
device = torch.device(dev)

class TranslateTransformer(nn.Module):
    def __init__(
        self,
        embedding_size,
        src_vocab_size,
        trg_vocab_size,
        src_pad_idx,
        num_heads,
        num_encoder_layers,
        num_decoder_layers,
        max_len,
    ):
        super(TranslateTransformer, self).__init__()
        self.srcEmbeddings = nn.Embedding(src_vocab_size,embedding_size)
        self.trgEmbeddings= nn.Embedding(trg_vocab_size,embedding_size)
        self.srcPositionalEmbeddings= nn.Embedding(max_len,embedding_size)
        self.trgPositionalEmbeddings= nn.Embedding(max_len,embedding_size)
        self.transformer = nn.Transformer(
            embedding_size,
            num_heads,
            num_encoder_layers,
            num_decoder_layers,
        )
        self.fc_out = nn.Linear(embedding_size, trg_vocab_size)
        self.dropout = nn.Dropout(0.1)
        self.src_pad_idx = src_pad_idx
        self.max_len = max_len
    
    def make_src_mask(self, src):
        src_mask = src.transpose(0,1) == self.src_pad_idx

        return src_mask.to(device)

    def forward(self,x,trg):
        src_seq_length = x.shape[0]
        N = x.shape[1]
        trg_seq_length = trg.shape[0]
        #adding zeros is an easy way
        src_positions = (
            torch.arange(0, src_seq_length)
            .reshape(src_seq_length,1)  + torch.zeros(src_seq_length,N) 
        ).to(device)
        
        trg_positions = (
            torch.arange(0, trg_seq_length)
            .reshape(trg_seq_length,1)  + torch.zeros(trg_seq_length,N) 
        ).to(device)


        srcWords = self.dropout(self.srcEmbeddings(x.long()) +self.srcPositionalEmbeddings(src_positions.long()))
        trgWords = self.dropout(self.trgEmbeddings(trg.long())+self.trgPositionalEmbeddings(trg_positions.long()))
        
        src_padding_mask = self.make_src_mask(x)
        trg_mask = self.transformer.generate_square_subsequent_mask(trg_seq_length).to(device)
        
        
        out = self.transformer(srcWords,trgWords, src_key_padding_mask=src_padding_mask,tgt_mask=trg_mask )
        out= self.fc_out(out)
        return out
