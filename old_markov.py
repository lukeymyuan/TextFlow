from random import choice

def generate(source, length):
    
    # Need better error handling? / move these conditions elsewhere?
    if length <= 0:
        print("Length must be a value greater than zero!")
        return
    
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
        key = (first, second)
        if key not in dict:
            dict[key] = []
        dict[key].append(third)
    
    # Need better error handling? / move these conditions elsewhere?
    if len(dict) == 0:
        print("The source is empty!")
        return
    
    endPunct = ['.', '?', '!']
    counter = 0
    sentence = []
    
    capitalKeys = []
    for key in dict.keys():
        if key[0][0].isupper() == True:
            capitalKeys.append(key)
    
    while(counter < length):
        
        # If the dictionary is entirely lowercase, 
        # some weird/incorrect punctuation can occur at the beginning of a sentence
        # e.g. "this. is" or "again! my".
        # Also this implementation may start a sentence from capitalized words in the middle 
        # of a sentence.
        if len(capitalKeys) == 0:
            key = choice(list(dict))
        else:
            key = choice(capitalKeys)
    
       
        first, second = key
        
        sentence.append(first)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(second)
        counter += 1
        if counter == length:
            continue
        
        while True:
            try:
                third = choice(dict[key])
            except KeyError:
                break # Should this be a return? How can this even happen?
            sentence.append(third)
            counter += 1
            if counter == length:
                break
            if third[-1] in endPunct:
                break
            key = (second, third)
            first, second = key
        
    return ' '.join(sentence)