from datetime import datetime
from utils import Database
from assets import make_buttons
from assets import start_ms, snippet_page, sections_page, snippet_section_page

class CallbackHandler:
    def __init__(self):
        '''Handles callback'''
        self.snippets_callbacks = None
        self.section_callback = None
        self.snippets_titles = None
        self.database = Database()
        self.callback_back_page = ['start_page', 'sections_page', 'snippet_section_page']

    async def get_callback(self, client, cbq):
        '''Main method for callback. Handles button presses'''
        # information about user
        self.cbq = cbq
        self.user_id = cbq.from_user.id
        self.user_name = cbq.from_user.username
        self.day = datetime.now().strftime("%d/%m/%Y")
        self.get_section_callback = tuple(set(self.database.get_sections(self.user_id)))
        self.user_sections = [section[1] for section in self.get_section_callback]

        # checks if user has pressed a section button
        for section_callback in self.user_sections:
            if self.cbq.data == section_callback:
                snippets = self.database.get_snippets(self.user_id, self.cbq.data[:-9])
                snippet_titles = [snippet[3] for snippet in snippets]
                snippet_callbacks = [snippet[4] for snippet in snippets]
                # add the current section and snippets in variables
                self.snippets_callbacks = snippet_callbacks
                self.snippets_titles = snippet_titles
                self.section_callback = section_callback
                await self.cbq.message.edit(snippet_section_page.format(section_callback[:-9]), reply_markup=make_buttons(snippet_titles, snippet_callbacks, 'sections_page'))
        
        # there must be a condition otherwise it won't find any snippets or section
        if not self.snippets_callbacks is None and not self.section_callback is None:
            # checks if user has pressed a snippet button in a section
            for snippet_callback in self.snippets_callbacks:
                if self.cbq.data == snippet_callback:
                    selected_snippet = self.database.get_specific_snippet(self.user_id, self.section_callback[:-9], snippet_callback[:-9])
                    await self.cbq.message.edit(snippet_page.format(snippet_callback[:-9], selected_snippet[2]), reply_markup=make_buttons([], [], 'snippet_section_page'))
        
        # checks if user has pressed add button
        if self.cbq.data == 'add_snippet_to_section':
            await self.cbq.message.edit("**Insert a title for this snippet**")

        if self.cbq.data == 'delete_snippet':
            ...
        # checks if user has pressed a back button
        for callback_back in self.callback_back_page:
            if self.cbq.data == callback_back:
                if callback_back == 'start_page':
                    await self.cbq.message.edit(start_ms.format(self.user_name))
                elif callback_back == 'sections_page':
                    texts = [section[0] for section in self.get_section_callback]
                    await self.cbq.message.edit(sections_page, reply_markup=make_buttons(texts, self.user_sections, 'start_page'))
                elif callback_back == 'snippet_section_page':
                    await self.cbq.message.edit(snippet_section_page.format(section_callback[:-9]), reply_markup=make_buttons(self.snippets_titles, self.snippets_callbacks, 'sections_page'))
