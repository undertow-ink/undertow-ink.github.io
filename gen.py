# print('no');import sys;sys.exit()

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
    # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # filename = f"works/{timestamp}.md"
    filename = f"works/{s}.md"

    os.makedirs("works", exist_ok=True)
    with open(filename, 'w') as f:
        f.write(content)

    first_line = content.splitlines()[0]
    new_link = f"[{first_line}]({filename})"

    with open('README.md') as f:
        links = [line.strip() + "  " for line in f if line.strip()]
    links.append(new_link + "  ")  # two spaces at end of line forces newline in Github markdown
    links.sort(key=lambda x: x.split('[')[1].split('-')[0].strip())

    with open('README.md', 'w') as f:
        f.write('\n'.join(links))



with open('authors.txt') as f:
    lines = [line.strip() for line in f]

author1, author2 = random.sample(lines, 2)

prompt = f"""You are to write as a collaboration between {author1} and {author2}. 

Embody both authors and write a long piece as if it came from those two authors working together. Seamlessly interweave and combine the themes, tones, philosophies, and storytelling approaches of both authors. Match their writing styles, approaches, and tones. Make it emotionally compelling to the reader.

Do not mention any characters from their books. For non-fiction works, apply the ideas to different circumstances - zoom in or zoom out on the concepts. Focus on matching their argument styles and writing styles rather than specific beliefs.

Demonstrate a deep understanding of both works through your writing.

Create a fake author name not associated with the actual authors, a pseudonym.

Return only the creative work itself with '<pseudonym> - <title>' on the first line. No additional commentary.

Make the piece unafraid to draw conclusions that might unsettle or provoke. Present a clear thesis in the opening paragraph that asserts the deeper truth both authors are reaching for, as if the collaboration has distilled their shared philosophy into a single urgent statement. Let every subsequent section build on that claim with precision, weight, and emotional force, weaving analysis and aesthetic resonance so that form and content reinforce one another.

Allow the writing to move between abstraction and the concrete, balancing intellectual rigor with sensory detail or human stakes, so that ideas feel lived and consequential. Avoid hedging or neutrality; let the prose take risks, as if these two voices together have something vital to say about the world that cannot be left unsaid.

YOU CANNOT -- CANNOT!!! -- mention either author or either title!!! --- you are creating something NEW!!! DO NOT REHASH!!!

Imagine if one author tackled the project of the other authors book and then the other author took on the subject of their book. Then imagine this topsy terve concept collaborated on something completely new.

"""

client = anthropic.Anthropic()
print('sending API request to Claude')
response = client.messages.create(
    model="claude-opus-4-20250514",
    max_tokens=4000,
    messages=[{"role": "user", "content": prompt}]
)
print('received response from Claude')
claude_content = response.content[0].text
do_the_thing(claude_content)

client = OpenAI()
print('sending API request to ChatGPT')
response = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=4000,
    messages=[{"role": "user", "content": prompt}]
)
print('received response from ChatGPT')
chatgpt_content = response.choices[0].message.content
do_the_thing(chatgpt_content)

# subprocess.run(["git", "add", filename])
subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", f"{author1} / {author2}"])
print('pushing to github')
subprocess.run(["git", "push"])
