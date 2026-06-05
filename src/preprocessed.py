import pandas as pd
import json
import os

# Load Hamlet utterances
file_path='data/raw/hamlet_utterances.jsonl'
df_hamletUt=pd.read_json(file_path, lines=True)

# Clean text and remove unwanted rows
df_hamletUt['text'] = df_hamletUt['text'].str.replace(r'\[.*?\]', '', regex=True)
df_hamletUt['text'] = df_hamletUt['text'].str.replace(r'[\[\]]', '', regex=True)
df_hamletUt = df_hamletUt[df_hamletUt['speaker'] != 'STAGE_DIRECTION']
df_hamletUt['text'] = df_hamletUt['text'].str.strip()
df_hamletUt = df_hamletUt[(df_hamletUt['act'] != 0) & (df_hamletUt['scene'] != 0)]

print(df_hamletUt.isnull().sum())

# Save cleaned Hamlet utterances
os.makedirs('data/processed', exist_ok=True)
df_hamletUt.to_json('data/processed/hamlet_ut.jsonl', orient='records', lines=True)

# Load Macbeth utterances
file_path='data/raw/macbeth_utterances.jsonl'
df_mcbethUt=pd.read_json(file_path, lines=True)

# Clean text and remove unwanted rows
df_mcbethUt['text'] = df_mcbethUt['text'].str.replace(r'\[.*?\]', '', regex=True)
df_mcbethUt['text'] = df_mcbethUt['text'].str.replace(r'[\[\]]', '', regex=True)
df_mcbethUt = df_mcbethUt[df_mcbethUt['speaker'] != 'STAGE_DIRECTION']
df_mcbethUt['text'] = df_mcbethUt['text'].str.strip()
df_mcbethUt = df_mcbethUt[(df_mcbethUt['act'] != 0) & (df_mcbethUt['scene'] != 0)]

print(df_mcbethUt.isnull().sum())

# Save cleaned Macbeth utterances
df_mcbethUt.to_json('data/processed/mcbeth_ut.jsonl', orient='records', lines=True)

# Load Romeo and Juliet utterances
file_path='data/raw/romeo_and_juliet_utterances.jsonl'
df_romeo_julietUt=pd.read_json(file_path, lines=True)

# Clean text and remove unwanted rows
df_romeo_julietUt['text'] = df_romeo_julietUt['text'].str.replace(r'\[.*?\]', '', regex=True)
df_romeo_julietUt['text'] = df_romeo_julietUt['text'].str.replace(r'[\[\]]', '', regex=True)
df_romeo_julietUt = df_romeo_julietUt[df_romeo_julietUt['speaker'] != 'STAGE_DIRECTION']
df_romeo_julietUt['text'] = df_romeo_julietUt['text'].str.strip()
df_romeo_julietUt = df_romeo_julietUt[(df_romeo_julietUt['act'] != 0) & (df_romeo_julietUt['scene'] != 0)]

# Save cleaned Romeo and Juliet utterances
df_romeo_julietUt.to_json('data/processed/romeo_juliet_ut.jsonl', orient='records', lines=True)

# Combine all three plays into one file
df_all_plays = pd.concat([df_hamletUt, df_mcbethUt, df_romeo_julietUt], ignore_index=True)
print(df_all_plays['play'].value_counts())
print(df_all_plays.shape)
df_all_plays.to_json('data/processed/all_plays_ut.jsonl', orient='records', lines=True)

# Load scene chunks for all three plays
df_hamlet_scenes = pd.read_json('data/raw/hamlet_scene_chunks.jsonl', lines=True)
df_macbeth_scenes = pd.read_json('data/raw/macbeth_scene_chunks.jsonl', lines=True)
df_romeo_juliet_scenes = pd.read_json('data/raw/romeo_and_juliet_scene_chunks.jsonl', lines=True)

# Combine all scene chunks
df_all_scenes = pd.concat([df_hamlet_scenes, df_macbeth_scenes, df_romeo_juliet_scenes], ignore_index=True)
print(df_all_scenes.columns.tolist())
print(df_all_scenes['play'].value_counts())

# Clean scene text
df_all_scenes['text'] = df_all_scenes['text'].str.replace(r'^[A-Z][a-zA-Z\s,]+\.\s*\n', '', regex=True)
df_all_scenes['text'] = df_all_scenes['text'].str.replace(r'\n\s*\n', '\n', regex=True)
df_all_scenes['text'] = df_all_scenes['text'].str.strip()

# Save cleaned scene chunks
df_all_scenes.to_json('data/processed/all_scenes.jsonl', orient='records', lines=True)

# Print chunk size stats
print("Scene chunks:", len(df_all_scenes))
print("Avg text length:", df_all_scenes['text'].str.len().mean())
print("Max text length:", df_all_scenes['text'].str.len().max())
print("Min text length:", df_all_scenes['text'].str.len().min())

print("Utterance chunks:", len(df_all_plays))
print("Avg text length:", df_all_plays['text'].str.len().mean())
print("Max text length:", df_all_plays['text'].str.len().max())
print("Min text length:", df_all_plays['text'].str.len().min())

print(df_all_scenes['play'].value_counts())
print(df_all_plays['play'].value_counts())

# Flag chunks that are too long for retrieval
df_all_scenes['too_long'] = df_all_scenes['text'].str.len() > 2000
print(df_all_scenes['too_long'].value_counts())

df_all_plays['too_long'] = df_all_plays['text'].str.len() > 2000
print(df_all_plays['too_long'].value_counts())
