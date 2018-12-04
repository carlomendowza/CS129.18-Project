import math
positive = []
negative = []
neutral = []

SOURCE = 'data/tokens.txt'

def save_to_files(num):
    print('Saving to files')
    with open('data/{}/positive.txt'.format(num), 'w+') as f:
        for line in positive:
            f.write('{}'.format(line))
        
    with open('data/{}/negative.txt'.format(num), 'w+') as f:
        for line in negative:
            f.write('{}'.format(line))

    with open('data/{}/neutral.txt'.format(num), 'w+') as f:
        for line in neutral:
            f.write('{}'.format(line))

def get_file_size():
    with open(SOURCE, 'r') as f:
        for i, l in enumerate(f):
            pass
        return i + 1

def split_file(num):
    size = get_file_size()
    segment = math.floor(size/4)
    start_index = 0
    dataset = []

    start_index = segment*(num-1)
    end_index = start_index + (segment)
    print('Starting at index:', start_index)

    # Create appropriate dataset
    with open(SOURCE, 'r') as f:
        text = f.readlines()
        for index, line in enumerate(text):
            if index < end_index and index >= start_index:
                dataset.append(line)
            elif index < start_index:
                pass
            else:
                # If you go beyond the end index
                break
    print('Dataset created. First word:', dataset[0], 'Last word:', dataset[-1])
    return dataset



def label_loop(dataset):
    for line in dataset:
        print(line, end='')
        choice = str(input("Pos (p), Neg (n), or neutral (enter)?"))
        if choice == 'p':
            positive.append(line)
        elif choice == 'stop':
            break
        elif choice == '':
            neutral.append(line)
        else:
            negative.append(line)
        print()

# Split tokens.txt into appropriate sets of 1k each
print('Which set to parse?\n1:Gomer\n2:Carlo\n3:Brian\n4:Gab')
num = int(input())
dataset = split_file(num)  # List of tokens under a specific set
label_loop(dataset)
save_to_files(num)




