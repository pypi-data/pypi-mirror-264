from typing import List, Optional, Union, Tuple

import numpy as np
import torch

import re
import langtorch

TextTensor = langtorch.TextTensor
Text = langtorch.Text
set_defaults_from_ctx = langtorch.decorators.set_defaults_from_ctx
def parse_kwargs(desc):
    """Maps a description of args to a dictionary of {argname: description}.
    Input:
        ('    weight (Tensor): a weight tensor\n' +
         '        Some optional description')
    Output: {
        'weight': \
        'weight (Tensor): a weight tensor\n        Some optional description'
    }
    """
    # Split on exactly 4 spaces after a newline
    regx = re.compile(r"\n\s{4}(?!\s)")
    kwargs = [section.strip() for section in regx.split(desc)]
    kwargs = [section for section in kwargs if len(section) > 0]
    return {desc.split(" ")[0]: desc for desc in kwargs}

common_args = parse_kwargs(
    """
    input (Tensor): the input tensor.
    generator (:class:`torch.Generator`, optional): a pseudorandom number generator for sampling
    out (Tensor, optional): the output tensor.
    memory_format (:class:`torch.memory_format`, optional): the desired memory format of
        returned tensor. Default: ``torch.preserve_format``.
"""
)



def stack(texttensors: Union[Tuple[TextTensor, ...], List[TextTensor]], dim: int=0, *, out: Optional[TextTensor]=None) -> TextTensor:
    r"""
   stack(texttensors, dim=0, *, out=None) -> Tensor

   Concatenates a sequence of tensors along a new dimension.

   All tensors need to be of the same size.

   Arguments:
       texttensors (sequence of TextTensor): sequence of TextTensors to concatenate
       dim (int): dimension to insert. Has to be between 0 and the number
           of dimensions of concatenated tensors (inclusive)
         out (Tensor, optional): the output tensor.
         """

    # Validate the input tensors
    if not all(isinstance(t, TextTensor) for t in texttensors):
        raise TypeError("All inputs must be TextTensor instances")
    # Assert that all the tensors have aligned shapes
    if len(texttensors[0].shape) != 0 and not all(t.shape[dim] == texttensors[0].shape[dim] for t in texttensors):
        raise ValueError(f"All input tensors must have the same shape at dimension {dim}")

    # Stack the contents
    stacked_content = np.stack([t.content for t in texttensors], axis=dim)
    # Merge the metadata
    merged_metadata = {}
    for key in texttensors[0].metadata.keys():
        if isinstance(texttensors[0].metadata[key], torch.Tensor):
            # For tensor-like metadata, stack them along the specified dimension
            if isinstance(texttensors[0].metadata[key], TextTensor):
                matadata_to_stack = [
                    t.metadata[key] if key in t.metadata and t.metadata[key] else langtorch.zeros_like(t) for t in
                    texttensors]
                merged_metadata[key] = stack(matadata_to_stack, dim=dim)
            else:
                matadata_to_stack = [
                    t.metadata[key] if key in t.metadata and t.metadata[key] is not None else torch.full(
                        t.shape if len(texttensors[0].metadata[key].shape) == len(texttensors[0].shape) else list(
                            t.shape) + [texttensors[0].metadata[key].shape[-1]], torch.nan) for t in texttensors]
                merged_metadata[key] = torch.stack(matadata_to_stack, dim=dim)
        elif isinstance(texttensors[0].metadata[key], np.ndarray):
            merged_metadata[key] = np.stack([t.metadata[key] if key in t.metadata and t.metadata[
                key] is not None else np.full_like(t.content, np.nan) for t in texttensors], axis=dim)
        else:
            # For scalar or non-tensor metadata, use the metadata from the first tensor
            merged_metadata[key] = texttensors[0].metadata[key]

    # Create a new TextTensor with the stacked content and merged metadata
    stacked_tensor = TextTensor(metadata=merged_metadata, content=stacked_content, parse=False)

    # Handle the 'out' argument if provided
    if out is not None:
        if not isinstance(out, TextTensor):
            raise TypeError("The 'out' argument must be a TextTensor instance")
        out.metadata = stacked_tensor.metadata
        out.content = stacked_tensor.content
        return out

    return stacked_tensor

def cat(texttensors: Union[Tuple[TextTensor, ...], List[TextTensor]], dim: int=0, *, out: Optional[TextTensor]=None) -> TextTensor:
    r"""
    cat(texttensors, dim=0, *, out=None) -> Tensor

    Concatenates the given sequence of :attr:`seq` TextTensors in the given dimension.
    All tensors must either have the same shape (except in the concatenating
    dimension) or be empty.

    :func:`torch.cat` can be seen as an inverse operation for :func:`torch.split`
    and :func:`torch.chunk`.

    :func:`torch.cat` can be best understood via examples.

    Args:
        texttensors (sequence of Tensors): any python sequence of TextTensors.
            Non-empty tensors provided must have the same shape, except in the
            cat dimension.
        dim (int, optional): the dimension over which the tensors are concatenated
"""
    # Step 1: Increase dimension
    tensors_unsqueezed = [torch.unsqueeze(tt, dim+1) for tt in texttensors]

    # Step 2: Stack
    stacked = stack(tensors_unsqueezed, dim+1)

    # Step 3: Reshape to match torch.cat output
    shape = list(stacked.shape)
    del shape[dim+1]  # Remove the added dimension
    concatenated = stacked.reshape(shape)

    return concatenated

def cosine_similarity(x1: TextTensor, x2: TextTensor, dim: int=-1, eps: float=1e-8) -> TextTensor:
    if not isinstance(x1, TextTensor):
        x1 = TextTensor(x1)
    if not isinstance(x2, TextTensor):
        x2 = TextTensor(x2)
    if not x1.embedding:
        x1.embed()
    if not x2.embedding:
        x2.embed()
    x1, x2 = x1.embedding, x2.embedding
    return torch.nn.functional.cosine_similarity(x1, x2, -1, eps)

def squeeze(input: TextTensor, *args, **kwargs):
    return input.squeeze(*args, **kwargs)

def unsqueeze(input: TextTensor, *args, **kwargs):
    return input.unsqueeze(*args, **kwargs)

def reshape(input: TextTensor, *args, **kwargs):
    return input.reshape(*args, **kwargs)

def swapaxes(input: TextTensor, *args, **kwargs):
    return input.swapaxes(*args, **kwargs)


def sum(input: TextTensor, *args, **kwargs):
    return input.sum(*args, **kwargs)

def swapaxes(input: TextTensor, *args, **kwargs):
    return input.swapaxes(*args, **kwargs)

def swapaxes(input: TextTensor, *args, **kwargs):
    return input.swapaxes(*args, **kwargs)
