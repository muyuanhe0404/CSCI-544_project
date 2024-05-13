import re

import pandas as pd

df = pd.read_json('output.json')

df['label'].value_counts()

d = {'proved': 0, 'disproved': 0, 'unknown': 0}
k = len(df)
df['chatgpt-guess-label'] = ''
unsure = []
i = 0
for index, row in df.iterrows():
    text = row['chat-gpt-3.5-turbo-ans'].lower()
    proved = re.search(r'\bproved\b(?!disproved)', text)
    disproved = re.search(r'disproved', text)
    unknown = re.search(r'unknown', text) 
    if (proved and disproved) or (proved and unknown) or (disproved and unknown) or (not proved and not disproved and not unknown):
        isFixed = False
        while not isFixed:
            print(f'Proved: {proved}, Disproved: {disproved}, Unknown: {unknown}, {k} left')
            print('######################################################################')
            print(row['question'].split('Based on the game state and the rules and preferences,',1)[-1])
            print(text)
            userInput = input('Proved (1), disproved (2), unknown (3): ')
            try:
                userInt = int(userInput)
                if userInt <= 0 or userInt >= 4:
                    raise ValueError()
                isFixed = True
                
                if userInt == 1:
                    proved, disproved, unknown = True, False, False
                elif userInt == 2:
                    proved, disproved, unknown = False, True, False
                elif userInt == 3:
                    proved, disproved, unknown = False, False, True
            except ValueError:
                print(f'Bad value entered ({userInput} w as entered), try again')
    
    if proved:
        d['proved'] += 1
        df.at[index, 'chatgpt-guess-label'] = 'proved'
    elif disproved:
        d['disproved'] += 1
        df.at[index, 'chatgpt-guess-label']  = 'disproved'
    elif unknown:
        d['unknown'] += 1
        df.at[index, 'chatgpt-guess-label']  = 'unknown'
    k -= 1
df.to_json('./output-with-chat-gpt-label.json', orient='records')
#ChatGPT base Answers
# {'proved': 604, 'disproved': 263, 'unknown': 133} 0
print(d, i)