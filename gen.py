import random
import anthropic
import subprocess
from datetime import datetime
import os
import re
import string
from dotenv import load_dotenv

load_dotenv()

with open('authors.txt') as f:
    lines = [line.strip() for line in f]

author1, author2 = random.sample(lines, 2)

prompt = f"""You are to write as a collaboration between {author1} and {author2}. 

Embody both authors and write a long piece as if it came from those two authors working together. Seamlessly interweave and combine the themes, tones, philosophies, and storytelling approaches of both authors. Match their writing styles, approaches, and tones. Make it emotionally compelling to the reader.

Do not mention any characters from their books. For non-fiction works, apply the ideas to different circumstances - zoom in or zoom out on the concepts. Focus on matching their argument styles and writing styles rather than specific beliefs.

Demonstrate a deep understanding of both works through your writing.

Create a fake author name not associated with the actual authors, a pseudonym.

Return only the creative work itself with '<pseudonym> - <title>' on the first line. No additional commentary."""

client = anthropic.Anthropic()

print('sending API request to Claude')
response = client.messages.create(
    model="claude-opus-4-20250514",
    max_tokens=4000,
    messages=[{"role": "user", "content": prompt}]
)

print('received response from Claude')
content = response.content[0].text
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
    links = [line.strip() for line in f if line.strip()]
links.append(new_link + "  ")  # two spaces at end of line forces newline in Github markdown
links.sort(key=lambda x: x.split('[')[1].split('-')[0].strip())

with open('README.md', 'w') as f:
    f.write('\n'.join(links))

# subprocess.run(["git", "add", filename])
subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", f"Add collaboration: {author1} x {author2}"])
print('pushing to github')
subprocess.run(["git", "push"])