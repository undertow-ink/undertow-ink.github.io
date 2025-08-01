# print('paused');import sys;sys.exit()
# import time; time.sleep(5)

import random
import anthropic
from openai import OpenAI
import subprocess
from datetime import datetime
import os
import re
import string
from dotenv import load_dotenv

load_dotenv()


def do_the_thing(content):
    s = content.splitlines()[0]
    s = '-'.join([w for w in s.encode('ascii', errors='ignore').decode().split() if w not in string.punctuation])
    filename = f"works/{s}.md"

    os.makedirs("works", exist_ok=True)
    with open(filename, 'w') as f:
        f.write(content)

    first_line = content.splitlines()[0]
    
    # Truncate title if too long (following existing pattern)
    author_name, title = first_line.split(' - ', 1) if ' - ' in first_line else ('Unknown', first_line)
    if len(title) > 25:
        title_truncated = title[:20] + '…'
        display_title = f"{author_name} - {title_truncated}"
    else:
        display_title = first_line
    
    new_link = f"[{display_title}](/{filename.split('.')[0]}.html) `0 🩶`"

    # Read existing content and append new link at bottom
    with open('index.md') as f:
        content = f.read()
    
    # Ensure proper formatting
    if not content.endswith('\n'):
        content += '\n'
    content += new_link + "  \n"
    
    with open('index.md', 'w') as f:
        f.write(content)
    
    return new_link


def update_picker_file(picker, new_link):
    picker_file = f"picks/{picker.lower()}.md"
    
    with open(picker_file) as f:
        content = f.read()
    
    # Simply append the new link at the end
    if not content.endswith('\n'):
        content += '\n'
    content += new_link + "  \n"
    
    with open(picker_file, 'w') as f:
        f.write(content)


authors_by_picker = {
    'Kelley': [
        ('Ann Patchett', 'Sarah Coleman'),
        ('Elizabeth Gilbert', 'Mara Ellingsen'),
        ('Kristin Hannah', 'Rachel Pierce'),
        ('Danzy Senna', 'Maya Cortez'),
        ('Emily Habeck', 'Claire Donovan'),
    ],
    'Brian': [
        ('Karl Ove Knausgaard', 'Erik Lindqvist'),
        ('Ted Chiang', 'David Chen'),
        ('Leonora Carrington', 'Helena Cross'),
        ('Anne Carson', 'Ruth Sterling'),
        ('J. M. Coetzee', 'Michael Hartley'),
    ],
    'Phyllis': [
        ('George R. R. Martin', 'Thomas Grey'),
        ('Nick Bantock', 'Alex Rivers'),
        ('Barry Hannah', 'Jake Morrison'),
        ('James M. Cain', 'Robert Kane'),
        ('Bernard Cornwell', 'Daniel Wells'),
    ],
    'Linda': [
        ('Anita Shreve', 'Laura Mitchell'),
        ('Judith McNaught', 'Victoria Blake'),
        ('Diane Chamberlain', 'Susan Fielding'),
        ('Liane Moriarty', 'Kate Morrison'),
        ('Colleen Hoover', 'Emma Clarke'),
    ],
    'Mercy': [
        ('C.S. Lewis', 'John Bradley'),
        ('David Wallace Wells', 'Mark Stevens'),
        ('Madeline L\'Engle', 'Sarah Bennett'),
        ('Susan Collins', 'Anne Parker'),
        ('Ray Bradbury', 'Robert Hayes'),
    ],
    'Gina': [
        ('Daphne du Maurier', 'Clara Whitmore'),
        ('Wilkie Collins', 'Edgar Langley'),
        ('Harper Lee', 'Julia Trent'),
        ('Jane Austen', 'Evelyn Marlowe'),
        ('William Shakespeare', 'Thomas Fairchild'),
    ],
    'Avery': [
        ('Lois Lowry', 'Margaret Ellison'),
        ('E. Lockhart', 'Nora Caldwell'),
        ('Han Kang', 'Elena Park'),
        ('Sylvia Plath', 'Clara Winslow'),
        ('Kate Quinn', 'Isabel Harrington'),
    ],
}

picker = random.choice(list(authors_by_picker.keys()))
authors = authors_by_picker[picker]
random.shuffle(authors)  # in-place

prompt_0 = f"""
This is a creative exercise. Pretend {authors[0][0]} and {authors[1][0]} both read one work each by {authors[2][0]} and {authors[3][0]}. {authors[0][0]} and {authors[1][0]} record a transcript of a conversation they have. They are collaborating and brainstorming. They are both inspired by the works of {authors[2][0]} and {authors[3][0]} (choose one specific work by each.) They see many common themes. They collaborate on a plan for a short story in ten parts, a creative and genuinely new work but inspired by combining the works they read by the other two authors. Print the transcript of this conversation. Include instructions to the would-be author (which is neither of them, so they really need to describe the gist of the new writing in detail.) Their editor is going to send it to another established author (unknown to them) to complete the new creative fictional work. A short story in ten parts. Do not mention any of the authors, titles, characters, etc. from existing material. But do give names to places and characters (mix up name, and pronouns to add variation, maybe at times name by relationship- mom, uncle, etc. but don't overdo it, maybe at times nickname or shortened name but don't overdo it - mainly stick to the writing style of the authors you are emulating. In the dialog, just say "Person 1" and "Person 2". Don't write any details that identify the works they read. But be very precise and detailed about crafting this new creative work of fiction. Not wishy washy stuff. A concrete setting. Concrete characters. Concrete plot. All named. Not surface stuff. What is the essence? What is the tone? What is the symbolism. This isn't writing 101. Don't mention general writing advice. Write only things that would be helpful to an established author, but these two are creating everything about the book, the author is just translating it to their own  writing style and executing. The why for every decision. The symbolism, metaphor, allegory. Embody these authors - what do you know about their motivations and techniques given their body of existing work? Avoid overused terms like ghost, whisper, and neon. Drop the reader into the story. One example is to use dialog between the characters when they are having a conversation. Don't write something like "He told her ...". Have a dialog. In general this aligns to the rule to "Show don't tell" - adhere to the writing style of the authors - but these authors are extremely capable and they no doubt drop the reader into a world, a context, a character - the writing is the world, the character, the place, the emotions, the relationships, the conflicts, the philosophy. The writing hardly ever describes those elements.
"""

# Claude version - using Sonnet for cost savings
client = anthropic.Anthropic()
print('sending API request to Claude Sonnet for conversation')
response = client.messages.create(
    model="claude-sonnet-4-20250514",  # much cheaper than opus
    max_tokens=4000,
    messages=[{"role": "user", "content": prompt_0}]
)
print('received response from Claude')
conversation_response = response.content[0].text

prompt_1 = f"""
This is a creative exercise. Do not mention {authors[4][0]}'s name. Instead act as {authors[4][0]}. Analyzing what has been sent to her below as if you were her. Then writing in her style. No formatting. Only ASCII text characters. No commentary. The first line is the pseudonym {authors[4][1]} and the title separated by " - ".  Then a blank line and the content of the short story. No markdown formatting. The 10 parts/sections are not numbered or delineated in any way. Avoid overused terms like ghost and neon. name places and characters (mix up name, and pronouns to add variation, maybe at times name by relationship- mom, uncle, etc. but don't overdo it, maybe at times nickname or shortened name but don't overdo it - mainly stick to the writing style of the author you are emulating. Drop the reader into the story. One example is to use dialog between the characters when they are having a conversation. Don't write something like "He told her ...". Have a dialog. In general this aligns to the rule to "Show don't tell" - adhere to the writing style of the author - but the author is extremely capable and they no doubt drop the reader into a world, a context, a character - the writing is the world, the character, the place, the emotions, the relationships, the conflicts, the philosophy. The writing hardly ever describes those elements. You, acting as a fictional {authors[4][0]}, receive the following and get to work on part 1 of 10:

    {conversation_response}

"""

print('starting story writing session')
messages = [{"role": "user", "content": prompt_1}]
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4000,
    messages=messages
)
story_content = response.content[0].text
messages.append({"role": "assistant", "content": story_content})

for i in range(2, 10):
    prompt_i = f"""
    Continue with part {i} out of 10. Follow previous guidance. No numbering or delineation. Do not repeat the title or author.
    """
    messages.append({"role": "user", "content": prompt_i})
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=messages
    )
    part_content = response.content[0].text
    story_content += "\n\n" + part_content
    messages.append({"role": "assistant", "content": part_content})

prompt_10 = f"""
Continue with part 10 out of 10. This is it. The final part and the ending. Follow previous guidance. No numbering or delineation. Do not repeat the title or author.
"""
messages.append({"role": "user", "content": prompt_10})
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4000,
    messages=messages
)
final_part = response.content[0].text
story_content += "\n\n" + final_part

new_link = do_the_thing(story_content)
update_picker_file(picker, new_link)
subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", f"{authors[0][0]} + {authors[1][0]} plan, {authors[4][0]} writes (Claude)"])


print('pushing to github')
subprocess.run(["git", "push"])

# import sys;sys.exit()


# ChatGPT version
picker = random.choice(list(authors_by_picker.keys()))
authors = authors_by_picker[picker]
random.shuffle(authors)

prompt_0 = f"""
This is a creative exercise. Pretend {authors[0][0]} and {authors[1][0]} both read one work each by {authors[2][0]} and {authors[3][0]}. {authors[0][0]} and {authors[1][0]} record a transcript of a conversation they have. They are collaborating and brainstorming. They are both inspired by the works of {authors[2][0]} and {authors[3][0]} (choose one specific work by each.) They see many common themes. They collaborate on a plan for a short story in ten parts, a creative and genuinely new work but inspired by combining the works they read by the other two authors. Print the transcript of this conversation. Include instructions to the would-be author (which is neither of them, so they really need to describe the gist of the new writing in detail.) Their editor is going to send it to another established author (unknown to them) to complete the new creative fictional work. A short story in ten parts. Do not mention any of the authors, titles, characters, etc. from existing material. But do give names to places and characters (mix up name, and pronouns to add variation, maybe at times name by relationship- mom, uncle, etc. but don't overdo it, maybe at times nickname or shortened name but don't overdo it - mainly stick to the writing style of the authors you are emulating. In the dialog, just say "Person 1" and "Person 2". Don't write any details that identify the works they read. But be very precise and detailed about crafting this new creative work of fiction. Not wishy washy stuff. A concrete setting. Concrete characters. Concrete plot. All named. Not surface stuff. What is the essence? What is the tone? What is the symbolism. This isn't writing 101. Don't mention general writing advice. Write only things that would be helpful to an established author, but these two are creating everything about the book, the author is just translating it to their own  writing style and executing. The why for every decision. The symbolism, metaphor, allegory. Embody these authors - what do you know about their motivations and techniques given their body of existing work? Avoid overused terms like ghost and neon. Drop the reader into the story. One example is to use dialog between the characters when they are having a conversation. Don't write something like "He told her ...". Have a dialog. In general this aligns to the rule to "Show don't tell" - adhere to the writing style of the authors - but these authors are extremely capable and they no doubt drop the reader into a world, a context, a character - the writing is the world, the character, the place, the emotions, the relationships, the conflicts, the philosophy. The writing hardly ever describes those elements.
"""

client = OpenAI()
print('sending API request to ChatGPT for conversation')
response = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=4000,
    messages=[
        {"role": "system", "content": "write long response"},
        {"role": "user", "content": prompt_0},
    ],
)
print('received response from ChatGPT')
conversation_response = response.choices[0].message.content

prompt_1 = f"""
This is a creative exercise. Do not mention {authors[4][0]}'s name. Instead act as {authors[4][0]}. Analyzing what has been sent to her below as if you were her. Then writing in her style. No formatting. Only ASCII text characters. No commentary. The first line is the pseudonym {authors[4][1]} and the title separated by " - ".  Then a blank line and the content of the short story. No markdown formatting. The 10 parts/sections are not numbered or delineated in any way. Avoid overused terms like ghost and neon. name places and characters (mix up name, and pronouns to add variation, maybe at times name by relationship- mom, uncle, etc. but don't overdo it, maybe at times nickname or shortened name but don't overdo it - mainly stick to the writing style of the author you are emulating. Drop the reader into the story. One example is to use dialog between the characters when they are having a conversation. Don't write something like "He told her ...". Have a dialog. In general this aligns to the rule to "Show don't tell" - adhere to the writing style of the author - but the author is extremely capable and they no doubt drop the reader into a world, a context, a character - the writing is the world, the character, the place, the emotions, the relationships, the conflicts, the philosophy. The writing hardly ever describes those elements. Work hard to create a cohesive narrative where the reader forms a moving picture in their mind as they read, but don't over do it, don't over explain for sure, and in fact ignore this advice if you determine that the author you are embodying would make an intentional artistic choice NOT to follow this guidance. You, acting as a fictional {authors[4][0]}, receive the following and get to work on part 1 of 10:

    {conversation_response}

"""

print('starting story writing session')
messages = [
    {"role": "system", "content": "write long response"},
    {"role": "user", "content": prompt_1}
]
response = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=4000,
    messages=messages
)
story_content = response.choices[0].message.content
messages.append({"role": "assistant", "content": story_content})

for i in range(2, 10):
    prompt_i = f"""
    Continue with part {i} out of 10. Follow previous guidance. No numbering or delineation. Do not repeat the title or author.
    """
    messages.append({"role": "user", "content": prompt_i})
    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=4000,
        messages=messages
    )
    part_content = response.choices[0].message.content
    story_content += "\n\n" + part_content
    messages.append({"role": "assistant", "content": part_content})

prompt_10 = f"""
Continue with part 10 out of 10. This is it. The final part and the ending. Follow previous guidance. No numbering or delineation. Do not repeat the title or author.
"""
messages.append({"role": "user", "content": prompt_10})
response = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=4000,
    messages=messages
)
final_part = response.choices[0].message.content
story_content += "\n\n" + final_part

new_link = do_the_thing(story_content)
update_picker_file(picker, new_link)
subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", f"{authors[0][0]} + {authors[1][0]} plan, {authors[4][0]} writes (ChatGPT)"])
print('pushing to github')
subprocess.run(["git", "push"])
