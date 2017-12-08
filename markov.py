from random import choice

def generate1(source, length):
    
    # check if length is positive
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
    
    endPunct = ['.', '?', '!']
    counter = 0
    sentence = []
    
    capitalKeys = []
    for key in dict.keys():
        try:
            if key[0][0].isupper() == True and key[0][1].isupper() == False and key[0][-1] not in endPunct:  # Words with all caps or ending in punctuation won't start a sentence
                capitalKeys.append(key)
        except IndexError:
            continue
    
    noPunctKeys = []
    for key in dict.keys():
        if key[0][-1] not in endPunct and key[0][0].islower() == True:  # Lowercase words ending in punctuation won't start a sentence
            noPunctKeys.append(key)
    
    while(counter < length):
        
        if len(capitalKeys) == 0 and len(noPunctKeys) == 0:
            key = choice(list(dict))
        elif len(capitalKeys) == 0 and len(noPunctKeys) > 0:
            key = choice(noPunctKeys)
        elif len(capitalKeys) > 0 and len(noPunctKeys) == 0:
            key = choice(capitalKeys)
        else:
            key = choice(capitalKeys)
    

        first = key
        
        sentence.append(first)
        counter += 1
        if counter == length:
            continue
            
        while True:
            try:
                second = choice(dict[key])
            except KeyError:
                break # Should this be a return? How can this even happen?
            sentence.append(second)
            counter += 1
            if counter == length:
                break
            if second[-1] in endPunct:
                break
            key = second
            first = key
        
    return ' '.join(sentence), dict

def generate2(source, length):
    
    # check if length is positive
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
        
    # check if source is empty
    if len(dict) == 0:
        print("The source is empty!")
        return
    
    endPunct = ['.', '?', '!']
    counter = 0
    sentence = []
    
    capitalKeys = []
    for key in dict.keys():
        try:
            if key[0][0].isupper() == True and key[0][1].isupper() == False and key[0][-1] not in endPunct:  # Words with all caps or ending in punctuation won't start a sentence
                capitalKeys.append(key)
        except IndexError:
            continue
    
    noPunctKeys = []
    for key in dict.keys():
        if key[0][-1] not in endPunct and key[0][0].islower() == True:  # Lowercase words ending in punctuation won't start a sentence
            noPunctKeys.append(key)
    
    while(counter < length):
        
        if len(capitalKeys) == 0 and len(noPunctKeys) == 0:
            key = choice(list(dict))
        elif len(capitalKeys) == 0 and len(noPunctKeys) > 0:
            key = choice(noPunctKeys)
        elif len(capitalKeys) > 0 and len(noPunctKeys) == 0:
            key = choice(capitalKeys)
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
        
    return ' '.join(sentence), dict

def generate3(source, length):
    
    # check if length is positive
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
            fourth = words[i+3]
        except IndexError:
            break
        key = (first, second, third)
        if key not in dict:
            dict[key] = []
        dict[key].append(fourth)
        
    # check if source is empty
    if len(dict) == 0:
        print("The source is empty!")
        return
    
    endPunct = ['.', '?', '!']
    counter = 0
    sentence = []
    
    capitalKeys = []
    for key in dict.keys():
        try:
            if key[0][0].isupper() == True and key[0][1].isupper() == False and key[0][-1] not in endPunct:  # Words with all caps or ending in punctuation won't start a sentence
                capitalKeys.append(key)
        except IndexError:
            continue
    
    noPunctKeys = []
    for key in dict.keys():
        if key[0][-1] not in endPunct and key[0][0].islower() == True:  # Lowercase words ending in punctuation won't start a sentence
            noPunctKeys.append(key)
    
    while(counter < length):
        
        if len(capitalKeys) == 0 and len(noPunctKeys) == 0:
            key = choice(list(dict))
        elif len(capitalKeys) == 0 and len(noPunctKeys) > 0:
            key = choice(noPunctKeys)
        elif len(capitalKeys) > 0 and len(noPunctKeys) == 0:
            key = choice(capitalKeys)
        else:
            key = choice(capitalKeys)
    
       
        first, second, third = key
        
        sentence.append(first)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(second)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(third)
        counter += 1
        if counter == length:
            continue
        
        while True:
            try:
                fourth = choice(dict[key])
            except KeyError:
                break # Should this be a return? How can this even happen?
            sentence.append(fourth)
            counter += 1
            if counter == length:
                break
            if fourth[-1] in endPunct:
                break
            key = (second, third, fourth)
            first, second, third = key
        
    return ' '.join(sentence), dict

def generate4(source, length):
    
    # check if length is positive
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
            fourth = words[i+3]
            fifth = words[i+4]
        except IndexError:
            break
        key = (first, second, third, fourth)
        if key not in dict:
            dict[key] = []
        dict[key].append(fifth)
        
    # check if source is empty
    if len(dict) == 0:
        print("The source is empty!")
        return
    
    endPunct = ['.', '?', '!']
    counter = 0
    sentence = []
    
    capitalKeys = []
    for key in dict.keys():
        try:
            if key[0][0].isupper() == True and key[0][1].isupper() == False and key[0][-1] not in endPunct:  # Words with all caps or ending in punctuation won't start a sentence
                capitalKeys.append(key)
        except IndexError:
            continue
    
    noPunctKeys = []
    for key in dict.keys():
        if key[0][-1] not in endPunct and key[0][0].islower() == True:  # Lowercase words ending in punctuation won't start a sentence
            noPunctKeys.append(key)
    
    while(counter < length):
        
        if len(capitalKeys) == 0 and len(noPunctKeys) == 0:
            key = choice(list(dict))
        elif len(capitalKeys) == 0 and len(noPunctKeys) > 0:
            key = choice(noPunctKeys)
        elif len(capitalKeys) > 0 and len(noPunctKeys) == 0:
            key = choice(capitalKeys)
        else:
            key = choice(capitalKeys)
    
       
        first, second, third, fourth = key
        
        sentence.append(first)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(second)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(third)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(fourth)
        counter += 1
        if counter == length:
            continue
        
        while True:
            try:
                fifth = choice(dict[key])
            except KeyError:
                break # Should this be a return? How can this even happen?
            sentence.append(fifth)
            counter += 1
            if counter == length:
                break
            if fifth[-1] in endPunct:
                break
            key = (second, third, fourth, fifth)
            first, second, third, fourth = key
        
    return ' '.join(sentence), dict

def generate5(source, length):
    
    # check if length is positive
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
            fourth = words[i+3]
            fifth = words[i+4]
            sixth = words[i+5]
        except IndexError:
            break
        key = (first, second, third, fourth, fifth)
        if key not in dict:
            dict[key] = []
        dict[key].append(sixth)
        
    # check if source is empty
    if len(dict) == 0:
        print("The source is empty!")
        return
    
    endPunct = ['.', '?', '!']
    counter = 0
    sentence = []
    
    capitalKeys = []
    for key in dict.keys():
        try:
            if key[0][0].isupper() == True and key[0][1].isupper() == False and key[0][-1] not in endPunct:  # Words with all caps or ending in punctuation won't start a sentence
                capitalKeys.append(key)
        except IndexError:
            continue
    
    noPunctKeys = []
    for key in dict.keys():
        if key[0][-1] not in endPunct and key[0][0].islower() == True:  # Lowercase words ending in punctuation won't start a sentence
            noPunctKeys.append(key)
    
    while(counter < length):
        
        if len(capitalKeys) == 0 and len(noPunctKeys) == 0:
            key = choice(list(dict))
        elif len(capitalKeys) == 0 and len(noPunctKeys) > 0:
            key = choice(noPunctKeys)
        elif len(capitalKeys) > 0 and len(noPunctKeys) == 0:
            key = choice(capitalKeys)
        else:
            key = choice(capitalKeys)
    
       
        first, second, third, fourth, fifth = key
        
        sentence.append(first)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(second)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(third)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(fourth)
        counter += 1
        if counter == length:
            continue
        
        sentence.append(fifth)
        counter += 1
        if counter == length:
            continue
        
        while True:
            try:
                sixth = choice(dict[key])
            except KeyError:
                break # Should this be a return? How can this even happen?
            sentence.append(sixth)
            counter += 1
            if counter == length:
                break
            if sixth[-1] in endPunct:
                break
            key = (second, third, fourth, fifth, sixth)
            first, second, third, fourth, fifth = key
        
    return ' '.join(sentence), dict

def generate6(source, length):
    
    # check if length is positive
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
            fourth = words[i+3]
            fifth = words[i+4]
            sixth = words[i+5]
            seventh = words[i+6]
        except IndexError:
            break
        key = (first, second, third, fourth, fifth, sixth)
        if key not in dict:
            dict[key] = []
        dict[key].append(seventh)
        
    # check if source is empty
    if len(dict) == 0:
        print("The source is empty!")
        return
    
    endPunct = ['.', '?', '!']
    counter = 0
    sentence = []
    
    capitalKeys = []
    for key in dict.keys():
        try:
            if key[0][0].isupper() == True and key[0][1].isupper() == False and key[0][-1] not in endPunct:  # Words with all caps or ending in punctuation won't start a sentence
                capitalKeys.append(key)
        except IndexError:
            continue
    
    noPunctKeys = []
    for key in dict.keys():
        if key[0][-1] not in endPunct and key[0][0].islower() == True:  # Lowercase words ending in punctuation won't start a sentence
            noPunctKeys.append(key)
    
    while(counter < length):
        
        if len(capitalKeys) == 0 and len(noPunctKeys) == 0:
            key = choice(list(dict))
        elif len(capitalKeys) == 0 and len(noPunctKeys) > 0:
            key = choice(noPunctKeys)
        elif len(capitalKeys) > 0 and len(noPunctKeys) == 0:
            key = choice(capitalKeys)
        else:
            key = choice(capitalKeys)
    
       
        first, second, third, fourth, fifth, sixth = key
        
        sentence.append(first)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(second)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(third)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(fourth)
        counter += 1
        if counter == length:
            continue
        
        sentence.append(fifth)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(sixth)
        counter += 1
        if counter == length:
            continue
        
        while True:
            try:
                seventh = choice(dict[key])
            except KeyError:
                break # Should this be a return? How can this even happen?
            sentence.append(seventh)
            counter += 1
            if counter == length:
                break
            if seventh[-1] in endPunct:
                break
            key = (second, third, fourth, fifth, sixth, seventh)
            first, second, third, fourth, fifth, sixth = key
        
    return ' '.join(sentence), dict

def generate7(source, length):
    
    # check if length is positive
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
            fourth = words[i+3]
            fifth = words[i+4]
            sixth = words[i+5]
            seventh = words[i+6]
            eighth = words[i+7]
        except IndexError:
            break
        key = (first, second, third, fourth, fifth, sixth, seventh)
        if key not in dict:
            dict[key] = []
        dict[key].append(eighth)
        
    # check if source is empty
    if len(dict) == 0:
        print("The source is empty!")
        return
    
    endPunct = ['.', '?', '!']
    counter = 0
    sentence = []
    
    capitalKeys = []
    for key in dict.keys():
        try:
            if key[0][0].isupper() == True and key[0][1].isupper() == False and key[0][-1] not in endPunct:  # Words with all caps or ending in punctuation won't start a sentence
                capitalKeys.append(key)
        except IndexError:
            continue
    
    noPunctKeys = []
    for key in dict.keys():
        if key[0][-1] not in endPunct and key[0][0].islower() == True:  # Lowercase words ending in punctuation won't start a sentence
            noPunctKeys.append(key)
    
    while(counter < length):
        
        if len(capitalKeys) == 0 and len(noPunctKeys) == 0:
            key = choice(list(dict))
        elif len(capitalKeys) == 0 and len(noPunctKeys) > 0:
            key = choice(noPunctKeys)
        elif len(capitalKeys) > 0 and len(noPunctKeys) == 0:
            key = choice(capitalKeys)
        else:
            key = choice(capitalKeys)
    
       
        first, second, third, fourth, fifth, sixth, seventh = key
        
        sentence.append(first)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(second)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(third)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(fourth)
        counter += 1
        if counter == length:
            continue
        
        sentence.append(fifth)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(sixth)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(seventh)
        counter += 1
        if counter == length:
            continue
        
        while True:
            try:
                eighth = choice(dict[key])
            except KeyError:
                break # Should this be a return? How can this even happen?
            sentence.append(eighth)
            counter += 1
            if counter == length:
                break
            if eighth[-1] in endPunct:
                break
            key = (second, third, fourth, fifth, sixth, seventh, eighth)
            first, second, third, fourth, fifth, sixth, seventh = key
        
    return ' '.join(sentence), dict

def generate8(source, length):
    
    # check if length is positive
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
            fourth = words[i+3]
            fifth = words[i+4]
            sixth = words[i+5]
            seventh = words[i+6]
            eighth = words[i+7]
            ninth = words[i+8]
        except IndexError:
            break
        key = (first, second, third, fourth, fifth, sixth, seventh, eighth)
        if key not in dict:
            dict[key] = []
        dict[key].append(ninth)
        
    # check if source is empty
    if len(dict) == 0:
        print("The source is empty!")
        return
    
    endPunct = ['.', '?', '!']
    counter = 0
    sentence = []
    
    capitalKeys = []
    for key in dict.keys():
        try:
            if key[0][0].isupper() == True and key[0][1].isupper() == False and key[0][-1] not in endPunct:  # Words with all caps or ending in punctuation won't start a sentence
                capitalKeys.append(key)
        except IndexError:
            continue
    
    noPunctKeys = []
    for key in dict.keys():
        if key[0][-1] not in endPunct and key[0][0].islower() == True:  # Lowercase words ending in punctuation won't start a sentence
            noPunctKeys.append(key)
    
    while(counter < length):
        
        if len(capitalKeys) == 0 and len(noPunctKeys) == 0:
            key = choice(list(dict))
        elif len(capitalKeys) == 0 and len(noPunctKeys) > 0:
            key = choice(noPunctKeys)
        elif len(capitalKeys) > 0 and len(noPunctKeys) == 0:
            key = choice(capitalKeys)
        else:
            key = choice(capitalKeys)
    
       
        first, second, third, fourth, fifth, sixth, seventh, eighth = key
        
        sentence.append(first)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(second)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(third)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(fourth)
        counter += 1
        if counter == length:
            continue
        
        sentence.append(fifth)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(sixth)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(seventh)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(eighth)
        counter += 1
        if counter == length:
            continue
        
        while True:
            try:
                ninth = choice(dict[key])
            except KeyError:
                break # Should this be a return? How can this even happen?
            sentence.append(ninth)
            counter += 1
            if counter == length:
                break
            if ninth[-1] in endPunct:
                break
            key = (second, third, fourth, fifth, sixth, seventh, eighth, ninth)
            first, second, third, fourth, fifth, sixth, seventh, eighth = key
        
    return ' '.join(sentence), dict

def generate9(source, length):
    
    # check if length is positive
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
            fourth = words[i+3]
            fifth = words[i+4]
            sixth = words[i+5]
            seventh = words[i+6]
            eighth = words[i+7]
            ninth = words[i+8]
            tenth = words[i+9]
        except IndexError:
            break
        key = (first, second, third, fourth, fifth, sixth, seventh, eighth, ninth)
        if key not in dict:
            dict[key] = []
        dict[key].append(tenth)
        
    # check if source is empty
    if len(dict) == 0:
        print("The source is empty!")
        return
    
    endPunct = ['.', '?', '!']
    counter = 0
    sentence = []
    
    capitalKeys = []
    for key in dict.keys():
        try:
            if key[0][0].isupper() == True and key[0][1].isupper() == False and key[0][-1] not in endPunct:  # Words with all caps or ending in punctuation won't start a sentence
                capitalKeys.append(key)
        except IndexError:
            continue
    
    noPunctKeys = []
    for key in dict.keys():
        if key[0][-1] not in endPunct and key[0][0].islower() == True:  # Lowercase words ending in punctuation won't start a sentence
            noPunctKeys.append(key)
    
    while(counter < length):
        
        if len(capitalKeys) == 0 and len(noPunctKeys) == 0:
            key = choice(list(dict))
        elif len(capitalKeys) == 0 and len(noPunctKeys) > 0:
            key = choice(noPunctKeys)
        elif len(capitalKeys) > 0 and len(noPunctKeys) == 0:
            key = choice(capitalKeys)
        else:
            key = choice(capitalKeys)
    
       
        first, second, third, fourth, fifth, sixth, seventh, eighth, ninth = key
        
        sentence.append(first)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(second)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(third)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(fourth)
        counter += 1
        if counter == length:
            continue
        
        sentence.append(fifth)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(sixth)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(seventh)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(eighth)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(ninth)
        counter += 1
        if counter == length:
            continue
        
        while True:
            try:
                tenth = choice(dict[key])
            except KeyError:
                break # Should this be a return? How can this even happen?
            sentence.append(tenth)
            counter += 1
            if counter == length:
                break
            if tenth[-1] in endPunct:
                break
            key = (second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth)
            first, second, third, fourth, fifth, sixth, seventh, eighth, ninth = key
        
    return ' '.join(sentence), dict

def generate10(source, length):
    
    # check if length is positive
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
        key = (first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth)
        if key not in dict:
            dict[key] = []
        dict[key].append(eleventh)
        
    # check if source is empty
    if len(dict) == 0:
        print("The source is empty!")
        return
    
    endPunct = ['.', '?', '!']
    counter = 0
    sentence = []
    
    capitalKeys = []
    for key in dict.keys():
        try:
            if key[0][0].isupper() == True and key[0][1].isupper() == False and key[0][-1] not in endPunct:  # Words with all caps or ending in punctuation won't start a sentence
                capitalKeys.append(key)
        except IndexError:
            continue
    
    noPunctKeys = []
    for key in dict.keys():
        if key[0][-1] not in endPunct and key[0][0].islower() == True:  # Lowercase words ending in punctuation won't start a sentence
            noPunctKeys.append(key)
    
    while(counter < length):
        
        if len(capitalKeys) == 0 and len(noPunctKeys) == 0:
            key = choice(list(dict))
        elif len(capitalKeys) == 0 and len(noPunctKeys) > 0:
            key = choice(noPunctKeys)
        elif len(capitalKeys) > 0 and len(noPunctKeys) == 0:
            key = choice(capitalKeys)
        else:
            key = choice(capitalKeys)
    
       
        first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth = key
        
        sentence.append(first)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(second)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(third)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(fourth)
        counter += 1
        if counter == length:
            continue
        
        sentence.append(fifth)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(sixth)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(seventh)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(eighth)
        counter += 1
        if counter == length:
            continue
            
        sentence.append(ninth)
        counter += 1
        if counter == length:
            continue
        
        sentence.append(tenth)
        counter += 1
        if counter == length:
            continue
        
        while True:
            try:
                tenth = choice(dict[key])
            except KeyError:
                break # Should this be a return? How can this even happen?
            sentence.append(tenth)
            counter += 1
            if counter == length:
                break
            if tenth[-1] in endPunct:
                break
            key = (second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh)
            first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth = key
        
    return ' '.join(sentence), dict

def generate(source, length, lookback, request_d = False):
    funcs = [generate1, generate2, generate3, generate4, generate5, generate6, generate7, generate8, generate9, generate10]
    if lookback == '':
        lookback = 1
    lookback = int(lookback)

    if lookback <= 0 or lookback > 10:
        print("Please enter a valid lookback length between 1 and 10.")
        return
    try:
        text, d = funcs[lookback-1](source, length)
    except:
        return funcs[lookback-1](source,length)
    if request_d:
        return text, d
    return text


