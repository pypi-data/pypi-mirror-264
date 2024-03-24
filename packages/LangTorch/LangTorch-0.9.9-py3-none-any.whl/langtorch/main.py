import sys

import langtorch.semantic_algebra

sys.path.append("..")
import langtorch
from langtorch import TextTensor
from langtorch.tt.functional import dropout
from langtorch import Session
import numpy as np
import torch



quit()


def modularize(func):
    def forward(tt):
        print(tt)
        assert isinstance(tt, TextTensor)
        result = np.array(func(tt.content.tolist()), dtype=object)
        if len(result) == tt.content.size:
            tt.content = result.reshape(tt.content.shape)
        elif (len(result) / tt.content.size) % 1 < 0.0001:
            tt.content = result.reshape(list(tt.shape) + [len(result) // tt.size])
        else:
            tt.content = result
        return tt

    result = torch.nn.Module()
    result.forward = forward
    return result


def translation_tool(eng_text: str, dutch_text: str, french_text: str) -> str:
    """
    Translates the input text from English to Dutch and French.
    """
    import yaml
    print(yaml.dump({"eng_text": eng_text, "dutch_text": dutch_text, "french_text": french_text}))


tool_activation = Activation(tools=[translation_tool])
# print(tool_activation(TextTensor("translate this text to all 3 languages, use the tool provided:\n'vertaal deze tekst'")))


x = TextTensor([1, 2, 3, 4, 5, 6, 7, 8, 9], requires_grad=True).reshape(3, 3)
print(langtorch.semantic_algebra.mean(x, dim=0), langtorch.semantic_algebra.mean(x, dim=1))
x2 = x + "\nnumber"
print(x)
print("Tensor stack\n", torch.stack([x, x]))
print("Dropout", langtorch.tt.functional.dropout(x))

act = Activation()
# print(modularize(lambda xx: [f"_{x}_" for x in xx])(TextTensor([1,2,3,4,5,6,7,8,9]).reshape(3,3)))
chats = TextTensor([["a", "b", "c"], ["d", "e", "f"]], key="user")

from langtorch.tensors.chattensor import AIMessage

chats = chats + AIMessage("g")
# emb =chats.embed()
# print(torch.cosine_similarity(chats, chats))
# print(torch.cosine_similarity())


chain = torch.nn.Sequential(
    TextModule("Calculate this equation:\n"),
    langtorch.methods.CoT,
    Activation(),
    TextModule("Is this reasoning correct?\n"),
    Activation(T=0.)
)

# p = Text(("greeting","Hello, world!")).add_key_("prompt")
# # Example usage:
# input = (User([f"Is {word} positive?" for word in ["love", "chair", "non-negative"]]) * Assistant(
#     ["Yes", "No", "Yes"])).requires_grad_()
# target = TextTensor(['Yes', "No", "No"]).requires_grad_()  # Dummy tensors-like object with .content attribute
# print(torch.mean(input, dim = 0))


# print(torch.broadcast_tensors(input, target.unsqueeze(0)))

# loss_fn = TextLoss(prompt="")  # Create the loss function instance
# loss = loss_fn(input, target)  # Compute the loss
# loss.backward()  # Backpropagate the loss


from torch.utils.data import DataLoader, TensorDataset

# Define the dataset
input_data = (User([f"Is {word} positive?" for word in ["love", "chair", "non-negative"]]) * Assistant(
    ["Yes", "No", "Yes"])).requires_grad_()
target_data = TextTensor(['Yes', "No", "No"]).requires_grad_()

# Wrap the data in a TensorDataset and then create a DataLoader
dataset = TensorDataset(input_data, target_data)
dataloader = DataLoader(dataset, batch_size=1)  # Adjust the batch size as needed

# Define your TextModule
text_module = TextModule("{*}")  # Initialize your TextModule here

# Loop over the DataLoader
for i, (inputs, targets) in enumerate(dataloader):
    # Pass the batch through the TextModule
    outputs = text_module(inputs)

    # Compare outputs to targets and save the results
    # Here, you can define your own comparison logic
    # For example, you can save the results in a list or write them to a file
    print(f"Batch {i}:")
    print("Inputs:", inputs)
    print("Predicted:", outputs)
    print("Targets:", targets)
    print("----")
