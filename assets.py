from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_page = '''
**Welcome {}.**
**This is a Snippet-Code Bot.**

**You can make new sections that differ from the language. 🗂**
**You can share your snippets with your collaborators. 🤝**
**Manage your snippets as you see fit. 🧑‍💻**

**You just have to paste your code to make the magic happen. 🔮**
**PS: Insert 'Snippet:' at the start of your snippet to make it works.**

**[COMMANDS]**
- /start - Start the Snippet Bot
- /my_snippets - Check all of your snippets
__Made by JackForme (24-06-2024)__ - **BETA VERSION**
'''

sections_page = '''
**Welcome {}.**
**This is the sections page.**

**You can get all of your snippets here. 🗃**

__Made by JackForme (24-06-2024)__ - **BETA VERSION**
'''

snippet_input_page = '''
**{0} SnippetCode - {1}**\n\n {2}
'''
snippet_page = '''
**Viewing {0}. \n\n{1}
'''

snippet_section_page = '''
**Viewing {} section.\nSelect a snippet to continue**
'''

def make_buttons(texts, callbacks, page_to_go):
    '''Makes buttons'''
    texts = sorted(list(set(texts)))
    callbacks = sorted(list(set(callbacks)))
    buttons = len(texts)
    list_of_buttons = []
    for button in range(buttons):
        buttons_row = []
        text = texts[button]
        callback = callbacks[button]
        buttons_row.append(InlineKeyboardButton(text, callback))
        list_of_buttons.append(buttons_row)
    back_button = InlineKeyboardButton('Back', page_to_go)
    list_of_buttons.append([back_button])
    buttons = InlineKeyboardMarkup(list_of_buttons)
    return buttons

