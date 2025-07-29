import random

authors = [
    ('Ann Patchett', 'Sarah Coleman'),
    ('Elizabeth Gilbert', 'Mara Ellingsen'),
    ('Kristin Hannah', 'Rachel Pierce'),
    ('Danzy Senna', 'Maya Cortez'),
    ('Emily Habeck', 'Claire Donovan'),
]

random.shuffle(authors)  # in-place

prompt_0 = f"""
This is a creative exercise. Pretend {authors[0][0]} and {authors[1][0]} both read one work each by {authors[2][0]} and {authors[3][0]}. {authors[0][0]} and {authors[1][0]} record a transcript of a conversation they have. They are collaborating and brainstorming. They are both inspired by the works of {authors[2][0]} and {authors[3][0]} (choose one specific work by each.) They see many common themes. They collaborate on a plan for a short story in ten parts, a creative and genuinely new work but inspired by combining the works they read by the other two authors. Print the transcript of this conversation. Include instructions to the would-be author (which is neither of them, so they really need to describe the gist of the new writing in detail.) Their editor is going to send it to another established author (unknown to them) to complete the new creative fictional work. A short story in ten parts. Do not mention any of the authors, titles, characters, etc. from existing material. But do give names to places and characters (mix up name, and pronouns to add variation, maybe at times name by relationship- mom, uncle, etc. but don't overdo it, maybe at times nickname or shortened name but don't overdo it - mainly stick to the writing style of the authors you are emulating. In the dialog, just say "Person 1" and "Person 2". Don't write any details that identify the works they read. But be very precise and detailed about crafting this new creative work of fiction. Not wishy washy stuff. A concrete setting. Concrete characters. Concrete plot. All named. Not surface stuff. What is the essence? What is the tone? What is the symbolism. This isn't writing 101. Don't mention general writing advice. Write only things that would be helpful to an established author, but these two are creating everything about the book, the author is just translating it to their own  writing style and executing. The why for every decision. The symbolism, metaphor, allegory. Embody these authors - what do you know about their motivations and techniques given their body of existing work? Avoid overused terms like ghost and neon. Drop the reader into the story. One example is to use dialog between the characters when they are having a conversation. Don't write something like "He told her ...". Have a dialog. In general this aligns to the rule to "Show don't tell" - adhere to the writing style of the authors - but these authors are extremely capable and they no doubt drop the reader into a world, a context, a character - the writing is the world, the character, the place, the emotions, the relationships, the conflicts, the philosophy. The writing hardly ever describes those elements.
"""

print(prompt_0)
print('---')

response = "<<response goes here>>"

promtp_1 = f"""
This is a creative exercise. Do not mention {authors[4][0]}'s name. Instead act as {authors[4][0]}. Analyzing what has been sent to her below as if you were her. Then writing in her style. No formatting. Only ASCII text characters. No commentary. The first line is the pseudonym {authors[4][1]} and the title separated by " - ".  Then a blank line and the content of the short story. No markdown formatting. The 10 parts/sections are not numbered or delineated in any way. Avoid overused terms like ghost and neon. name places and characters (mix up name, and pronouns to add variation, maybe at times name by relationship- mom, uncle, etc. but don't overdo it, maybe at times nickname or shortened name but don't overdo it - mainly stick to the writing style of the author you are emulating. Drop the reader into the story. One example is to use dialog between the characters when they are having a conversation. Don't write something like "He told her ...". Have a dialog. In general this aligns to the rule to "Show don't tell" - adhere to the writing style of the author - but the author is extremely capable and they no doubt drop the reader into a world, a context, a character - the writing is the world, the character, the place, the emotions, the relationships, the conflicts, the philosophy. The writing hardly ever describes those elements. You, acting as a fictional {authors[4][0]}, receive the following and get to work on part 1 of 10:

    {response}

"""

print(promtp_1)
print('---')

for i in range(2, 10):

    prompt_i = f"""
    Continue with part {i} out of 10. Follow previous guidance. No numbering or delineation. Do not repeat the title or author.
    """

    print(prompt_i)
    print('---')

prompt_10 = f"""
Continue with part 10 out of 10. This is it. The final part and the ending. Follow previous guidance. No numbering or delineation. Do not repeat the title or author.
"""

print(prompt_10)
print('---')
