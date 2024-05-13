from openai import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd
from tqdm import tqdm
import time

load_dotenv()

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

def getChatGPT35Response(systemInstructions, prompt):
    # sleep to avoid api limits, should take ~15 minutes in total
    time.sleep(1)
    #return 'something'
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": f"{systemInstructions}"},
            {"role": "user", "content": f"{prompt}"}
        ]
    )

    return completion.choices[0].message.content

def getLLMResponse(systemInstructions, prompt):
    return getChatGPT35Response(systemInstructions, prompt)

def getBaseAnswers(dataDf):
    BASE_ANS_DIR = './results.json'

    saveDf = None#pd.DataFrame(columns=['question', 'reasoning', 'subproblems', 'label'])
    #saveDf = #saveDf.astype(str)
    
    for index, row in tqdm(dataDf.iterrows(), total=len(dataDf)):
        systemInstructions = "You are a helpful bot that can answer reasoning questions based off board game sitations"
        prompt = row['example'] + "\n The label is what (proved, disproved, unknown)?"
        response = getLLMResponse(systemInstructions, prompt)
        if saveDf is None:
            saveDf = pd.DataFrame(columns=['question', 'reasoning', 'subproblems', 'label'])
            saveDf = saveDf.astype(str)
        else:
            saveDf = pd.read_json(BASE_ANS_DIR, dtype=str)

        new_record = {
            'question': row['example'],
            'gold-reasoning': row['proof'],
            'subproblems': '',
            'chat-gpt-3.5-turbo-ans': response,
            'label': row['label'],
        }
        temp_df = pd.DataFrame([new_record])
        saveDf = pd.concat([saveDf, temp_df], ignore_index=True)
        saveDf.to_json(BASE_ANS_DIR, orient='records')




def main():
    dataPath = "./data/test.json"

    df = pd.read_json(dataPath, dtype=str)
    getBaseAnswers(df)

if __name__ == "__main__":
    main()

    # Load data
    # get initial response
    # break down questions using reasoning (custom model, LLAMA)
# Iteratively answer the subquestions based on the model, context, and subquestions
# get a final answer
# compare