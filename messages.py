from assets import *
from datetime import datetime
from utils import Database
import time
from math import ceil

class MessagesHandler:
    def __init__(self):
        '''Handles messages'''
        self.database = Database()

    async def get_message(self, client, ms):
        '''Main method for messages. Handles every message'''
        # information about user
        self.ms = ms
        self.user_id = ms.from_user.id
        self.user_name = ms.from_user.username
        self.day = datetime.now().strftime("%d/%m/%Y")

        # delete every message that is not a command or a snippet
        await ms.delete() 

        # checks for commands
        if self.ms.text == '/start':
            await ms.reply(start_page.format(self.user_name))

        if self.ms.text == '/my_snippets':
            get_sections = self.database.get_sections(self.user_id)
            sections_texts = [section[0] for section in get_sections]
            sections_callbacks = [section[1] for section in get_sections]
            await ms.reply(sections_page.format(self.user_name), reply_markup=make_buttons(sections_texts, sections_callbacks, 'start_page'))

        if 'snippet:' in self.ms.text.lower():
            # it formats the message to code
            self.ms.text = self.ms.text.lower().replace('snippet:', '').strip()
            self.format_text = f"""<pre>{self.ms.text}</pre>""" 
            await ms.reply(f'**SnippetCode - {self.day}**\n\n {self.format_text}')
            self.formatted_message = await client.get_messages(self.ms.from_user.id, self.ms.id + 1)
            get_language = (self.formatted_message.entities[1].language).capitalize() # check the language of code
            if get_language == "": get_language = 'Text' 
            options_texts = [f'Add to {get_language}', 'Delete']
            options_callbacks = ['add_snippet_to_section', 'delete_snippet']
            await self.formatted_message.edit(snippet_input_page.format(get_language, self.day, self.format_text), reply_markup=make_buttons(options_texts, options_callbacks, 'start_page'))
        
        # checks if the message is the title of the snippet
        try:
            if self.ms.id-1 == self.formatted_message.id:
                    
                    await client.edit_message_text(
                        chat_id=self.ms.from_user.id,
                        message_id=self.formatted_message.id,
                        text=f'**Set Title: {self.ms.text}**'
                        )
                    
                    # if the section doesn't exist it'll add it to db, then it'll add the snippet to db
                    sections_user = self.database.get_sections(self.user_id)
                    get_language = (self.formatted_message.entities[1].language).capitalize()
                    if get_language == "": get_language = 'Text'
                    add_section = False

                    if not sections_user: add_section = True
                    for section in sections_user:
                        if not get_language in section: add_section = True

                    if add_section: self.database.insert_section(self.user_id, get_language, f'{get_language}_callback',self.day)
                    sections_user = self.database.get_sections(self.user_id)
                    self.database.insert_snippet(self.user_id, get_language, self.format_text, self.ms.text, f'{self.ms.text}_callback',self.day)

                    await client.edit_message_text(
                        chat_id=self.ms.from_user.id,
                        message_id=self.formatted_message.id,
                        text=f'**Snippet added to your archive ✅**'
                        )
        except:     
            ...