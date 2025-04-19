output1_path = "outputs/compareOutputs_output1.txt"
output2_path = "outputs/compareOutputs_output2.txt"
inputs_path = "outputs/compareOutputs_input.txt"
commands_path = "outputs/compareOutputs_commands.txt"

def getArr(path):
    with open(path, 'r') as file:
        lines = file.readlines()
    processed_lines = [line.strip().replace('[', '').replace(']', '').split(',') for line in lines]
    return processed_lines

arr1 = getArr(output1_path)[0]
arr2 = getArr(output2_path)[0]
inputs = getArr(inputs_path)[0]
commands = getArr(commands_path)[0]

arr1_len = len(arr1)
arr2_len = len(arr2)

assert arr1_len == arr2_len, "Length of both outputs should be the same"

for i in range(arr1_len):
    item1 = arr1[i]
    item2 = arr2[i]
    command = commands[i]
    input = inputs[i]

    if (item1 != item2) and (command != '"getRandom"'):

        print(f"Items differ at index {i}\nitem1: {item1}\nitem2: {item2}\nCommand: {command}\nInput: {input}")
