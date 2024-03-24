import numpy as np
import torch

from langtorch.api.call import get_embedding
from langtorch.tensors import TextTensor

class EmbeddingModule(torch.nn.Module):
    input_class = TextTensor
    output_class = TextTensor

    def __init__(self, model="text-embedding-3-small"):
        super(EmbeddingModule, self).__init__()
        self.model = model

    def forward(self, x: 'TextTensor') -> torch.Tensor:
        # Collect all the texts from the TextTensor into a list
        # if not isinstance(x, TextTensor): x = TextTensor(x)
        shape = x.shape
        texts = [str(m) for m in x.content.flat if str(m)]
        with open("embed_temp.txt", 'w') as f:
            f = ''
        with open("embed_temp_log.txt", 'w') as f:
            f = ''
        # Get the embeddings for these texts
        embeddings = get_embedding(texts, "embed_temp.txt", as_np=True, api_key=self.api_key)

        # Convert the embeddings into a PyTorch tensors
        embedding_tensor = torch.from_numpy(np.array(embeddings))

        # # Reshape the tensors to match the shape of the input TextTensor
        # embedding_tensor = embedding_tensor.view(*x.content.shape, embedding_tensor.shape[-1])
        x.embedding = embedding_tensor
        return x


class OpenAIEmbeddings(torch.nn.Module):
    def __init__(self, model=""):
        super(EmbeddingModule, self).__init__()

    def forward(self, x: 'TextTensor') -> torch.Tensor:
        shape = x.shape
        texts = [str(m) for m in x.content.flat if str(m)]
        with open("embed_temp.txt", 'w') as f:
            f = ''
        with open("embed_temp_log.txt", 'w') as f:
            f = ''
        # Get the embeddings for these texts
        embeddings = get_embedding(texts, "embed_temp.txt", as_np=True, api_key=self.api_key)

        # Convert the embeddings into a PyTorch tensors
        embedding_tensor = torch.from_numpy(np.array(embeddings))

        # # Reshape the tensors to match the shape of the input TextTensor
        # embedding_tensor = embedding_tensor.view(*x.content.shape, embedding_tensor.shape[-1])
        x.embedding = embedding_tensor
        return x
