# -*- coding: utf-8 -*-
"""vision_transformer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MfrUhu9mY8-D2YAxyXpFw7XuxpMiGhku
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
import os
from transformer_encoder import TransformerEncoder, PositionalEncoding
from einops.layers.torch import Rearrange
from einops import repeat
from torch import Tensor
import numpy as np
from numpy.core.numeric import outer

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class PatchEmbedding(nn.Module):
    def __init__(self, in_channels = 3, patch_size = 8, emb_size = 128):
        self.patch_size = patch_size
        super().__init__()
        self.projection = nn.Sequential(
            # break-down the image in s1 x s2 patches and flat them
            Rearrange('b c (h p1) (w p2) -> b (h w) (p1 p2 c)', p1=patch_size, p2=patch_size),
            nn.Linear(patch_size * patch_size * in_channels, emb_size)
        )

    def forward(self, x: Tensor) -> Tensor:
        x = self.projection(x)
        return x

class VisionTransformer(nn.Module):
    """
    In the model, we partition an image into non-overlapping patches. Each patch is treated as a token.
    We can get a sequence of such tokens by flattening the patches. Each token's embeddings is the
    flattened RGB pixel values. If the patch size is 4, then the embeddings' dimension is 4*4*3.
    You can check this paper https://arxiv.org/pdf/2010.11929.pdf for reference.
    """
    def __init__(self,
            in_channels: int, emb_dim: int, patch_size: int, num_heads: int,
            trx_ff_dim: int, num_trx_cells: int, num_class: int, dropout: float=0.1,
            hidden_dims: list = [32,64,128]
        ):
        """
        Inputs:
        - patch_size: Size of the non-overlapping patches
        - num_heads: Number of attention heads
        - trx_ff_dim: Hidden dimension of the feedforward network in a Transformer encoder
        - num_trx_cells: Number of TransformerEncoderCells
        - num_class: Number of image classes
        - dropout: Dropout ratio
        """
        super(VisionTransformer, self).__init__()

        self.patch_size = patch_size

        ###########################################################################
        # TODO: Define a TransformerEncoder that takens non-overlapping patches   #
        # of an image as input and another output layer for classification.       #
        #                                                                         #
        # Intuitively, we need 2D positional encodings for each patch according to#
        # its x and y coordinates. But this reference paper https://arxiv.org/pdf/2010.11929.pdf
        # shows there is no significance difference on accuracies. It is bit      #
        # weird. But you can simply use the 1D positional encoding you have       #
        # implemented earlier. You can experiment with 2D positional encodings    #
        # if you like to earn extra credits.                                      #
        ###########################################################################
        self.patch_embedding = PatchEmbedding(in_channels=in_channels, patch_size=patch_size, emb_size=emb_dim)
        self.pe = PositionalEncoding(emb_dim)
        self.cls_token = nn.Parameter(torch.rand(1, 1, emb_dim))
        self.t_e = TransformerEncoder(emb_dim, num_heads, trx_ff_dim, num_trx_cells, dropout)

        layers = []
        in_dim = emb_dim
        for hidden_dim in hidden_dims:
            layers.append(nn.Linear(in_dim, hidden_dim))
            layers.append(nn.ReLU())
            in_dim = hidden_dim
        self.ffn = nn.Sequential(*layers)

        self.out = nn.Linear(in_dim, num_class)

        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################

#     def init_weights(self):
#         initrange = 0.5
#         self.embedding.weight.data.uniform_(-initrange, initrange)
#         self.fc.weight.data.uniform_(-initrange, initrange)
#         self.fc.bias.data.zero_()

    def forward(self, image: torch.Tensor):

        image = image.to(device)
        b, c, h, w = image.shape

        # Partition image into patches
        img_embed = self.patch_embedding(image)
        cls_tokens = repeat(self.cls_token, '1 1 d -> b 1 d', b=b)
        img_embed = torch.cat([cls_tokens, img_embed], dim=1)

        # Add positional encoding
        x = self.pe(img_embed)

        # Transformer encoder
        trans_enc_out = self.t_e(x) ##these are just features of shape (B,L,C)

        hidden = self.ffn(trans_enc_out)

        # Regression output
        regs = self.out(hidden)

        # Flatten output and apply linear layer
        out = regs.squeeze(-1) # Assuming the regression output is the first token

        out = torch.mean(out, axis=1) #Actual Ouput in case of training
        feature_vectors = trans_enc_out.reshape(b, -1)

        return feature_vectors, out  # Squeeze to get rid of any unnecessary dimensions

