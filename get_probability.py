def create_dictionary1(source):
    
    words = source.split()
    
    # Create dictionary from source
    dict = {}
    for i, word in enumerate(words):
        try:
            first = words[i]
            second = words[i+1]
        except IndexError:
            break
        key = first
        if key not in dict:
            dict[key] = []
        dict[key].append(second)
        
    # check if the source is empty   
    if len(dict) == 0:
        print("The source is empty!")
        return

    return dict

def create_dictionary2(source):
    
    words = source.split()
    
    # Create dictionary from source
    dict = {}
    for i, word in enumerate(words):
        try:
            first = words[i]
            second = words[i+1]
            third = words[i+2]
        except IndexError:
            break
        key = first, second
        if key not in dict:
            dict[key] = []
        dict[key].append(third)
        
    # check if the source is empty   
    if len(dict) == 0:
        print("The source is empty!")
        return

    return dict

def create_dictionary3(source):
    
    words = source.split()
    
    # Create dictionary from source
    dict = {}
    for i, word in enumerate(words):
        try:
            first = words[i]
            second = words[i+1]
            third = words[i+2]
            fourth = words[i+3]
        except IndexError:
            break
        key = first, second, third
        if key not in dict:
            dict[key] = []
        dict[key].append(fourth)
        
    # check if the source is empty   
    if len(dict) == 0:
        print("The source is empty!")
        return

    return dict

def create_dictionary4(source):
    
    words = source.split()
    
    # Create dictionary from source
    dict = {}
    for i, word in enumerate(words):
        try:
            first = words[i]
            second = words[i+1]
            third = words[i+2]
            fourth = words[i+3]
            fifth = words[i+4]
        except IndexError:
            break
        key = first, second, third, fourth
        if key not in dict:
            dict[key] = []
        dict[key].append(fifth)
        
    # check if the source is empty   
    if len(dict) == 0:
        print("The source is empty!")
        return
    
    return dict

def create_dictionary5(source):
    
    words = source.split()
    
    # Create dictionary from source
    dict = {}
    for i, word in enumerate(words):
        try:
            first = words[i]
            second = words[i+1]
            third = words[i+2]
            fourth = words[i+3]
            fifth = words[i+4]
            sixth = words[i+5]
        except IndexError:
            break
        key = first, second, third, fourth, fifth
        if key not in dict:
            dict[key] = []
        dict[key].append(sixth)
        
    # check if the source is empty   
    if len(dict) == 0:
        print("The source is empty!")
        return
    
    return dict

def create_dictionary6(source):
    
    words = source.split()
    
    # Create dictionary from source
    dict = {}
    for i, word in enumerate(words):
        try:
            first = words[i]
            second = words[i+1]
            third = words[i+2]
            fourth = words[i+3]
            fifth = words[i+4]
            sixth = words[i+5]
            seventh = words[i+6]
        except IndexError:
            break
        key = first, second, third, fourth, fifth, sixth
        if key not in dict:
            dict[key] = []
        dict[key].append(seventh)
        
    # check if the source is empty   
    if len(dict) == 0:
        print("The source is empty!")
        return
    
    return dict

def create_dictionary7(source):
    
    words = source.split()
    
    # Create dictionary from source
    dict = {}
    for i, word in enumerate(words):
        try:
            first = words[i]
            second = words[i+1]
            third = words[i+2]
            fourth = words[i+3]
            fifth = words[i+4]
            sixth = words[i+5]
            seventh = words[i+6]
            eighth = words[i+7]
        except IndexError:
            break
        key = first, second, third, fourth, fifth, sixth, seventh
        if key not in dict:
            dict[key] = []
        dict[key].append(eighth)
        
    # check if the source is empty   
    if len(dict) == 0:
        print("The source is empty!")
        return
    
    return dict

def create_dictionary8(source):
    
    words = source.split()
    
    # Create dictionary from source
    dict = {}
    for i, word in enumerate(words):
        try:
            first = words[i]
            second = words[i+1]
            third = words[i+2]
            fourth = words[i+3]
            fifth = words[i+4]
            sixth = words[i+5]
            seventh = words[i+6]
            eighth = words[i+7]
            ninth = words[i+8]
        except IndexError:
            break
        key = first, second, third, fourth, fifth, sixth, seventh, eighth
        if key not in dict:
            dict[key] = []
        dict[key].append(ninth)
        
    # check if the source is empty   
    if len(dict) == 0:
        print("The source is empty!")
        return
    
    return dict

def create_dictionary9(source):
    
    words = source.split()
    
    # Create dictionary from source
    dict = {}
    for i, word in enumerate(words):
        try:
            first = words[i]
            second = words[i+1]
            third = words[i+2]
            fourth = words[i+3]
            fifth = words[i+4]
            sixth = words[i+5]
            seventh = words[i+6]
            eighth = words[i+7]
            ninth = words[i+8]
            tenth = words[i+9]
        except IndexError:
            break
        key = first, second, third, fourth, fifth, sixth, seventh, eighth, ninth
        if key not in dict:
            dict[key] = []
        dict[key].append(tenth)
        
    # check if the source is empty   
    if len(dict) == 0:
        print("The source is empty!")
        return
    
    return dict

def create_dictionary10(source):
    
    words = source.split()
    
    # Create dictionary from source
    dict = {}
    for i, word in enumerate(words):
        try:
            first = words[i]
            second = words[i+1]
            third = words[i+2]
            fourth = words[i+3]
            fifth = words[i+4]
            sixth = words[i+5]
            seventh = words[i+6]
            eighth = words[i+7]
            ninth = words[i+8]
            tenth = words[i+9]
            eleventh = words[i+10]
        except IndexError:
            break
        key = first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth
        if key not in dict:
            dict[key] = []
        dict[key].append(eleventh)
        
    # check if the source is empty   
    if len(dict) == 0:
        print("The source is empty!")
        return
    
    return dict

def create_dictionary(source, lookback):
    if lookback <= 0:
        print("Please enter a valid lookback length between 1 and 10.")
        return
    elif lookback == 1:
        return create_dictionary1(source)
    elif lookback == 2:
        return  create_dictionary2(source)
    elif lookback == 3:
        return  create_dictionary3(source)
    elif lookback == 4:
        return  create_dictionary4(source)
    elif lookback == 5:
        return  create_dictionary5(source)
    elif lookback == 6:
        return  create_dictionary6(source)
    elif lookback == 7:
        return  create_dictionary7(source)
    elif lookback == 8:
        return  create_dictionary8(source)
    elif lookback == 9:
        return  create_dictionary9(source)
    elif lookback == 10:
        return  create_dictionary10(source)
    else:
        return print("Please enter a valid lookback length between 1 and 10.")

from collections import defaultdict

# Call create dictionary on the source before using get_probability!

def get_probability(dictionary, key):
    if key not in dictionary:
        print("Please enter a valid key.")
        return
    counter = defaultdict(int)
    for item in dictionary[key]:
        counter[item]+= 1
    count = len(dictionary[key])
    return [(key,counter[key]/count) for key in counter.keys()]