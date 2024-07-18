import sqlite3 as sql

class Database:
    def __init__(self) -> None:
        ...

    def create_tables(self):
        '''Creates tables'''
        self.conn = sql.connect('database.db')
        self.cur = self.conn.cursor()
        section_table = 'CREATE TABLE IF NOT EXISTS sections(user_id int primary_key, section text, callback text, date text)'
        snippet_table = 'CREATE TABLE IF NOT EXISTS snippets(user_id int primary_key, section text, snippet text, title text,callback text,date text)'
        self.cur.execute(section_table)
        self.cur.execute(snippet_table)
        self.conn.commit()
        self.conn.close()

    def insert_section(self, user_id, section, callback, date):
        '''Inserts a new section in user sections'''
        self.conn = sql.connect('database.db')
        self.cur = self.conn.cursor()
        insert_section = 'INSERT INTO sections VALUES(?, ?, ?, ?)'
        self.cur.execute(insert_section, [user_id, section, callback, date])
        self.conn.commit()
        self.conn.close()
        return True

    def insert_snippet(self, user_id, section, snippet, title, callback, date):
        '''Insert a new snippet in user snippet section'''
        self.conn = sql.connect('database.db')
        self.cur = self.conn.cursor()
        insert_snippet = 'INSERT INTO snippets VALUES(?, ?, ?, ?, ?, ?)'
        self.cur.execute(insert_snippet, [user_id, section, snippet, title, callback, date])
        self.conn.commit()
        self.conn.close()
        return True

    def get_snippets(self, user_id, section):
        '''Gets all snippets of a user section'''
        self.conn = sql.connect('database.db')
        self.cur = self.conn.cursor()
        select_snippets = 'SELECT * FROM snippets WHERE user_id=? AND section=?'
        self.cur.execute(select_snippets, [user_id, section])
        snippets_in_section = self.cur.fetchall()
        self.conn.close()
        return snippets_in_section
    
    def get_sections(self, user_id):
        '''Gets all sections of a user'''
        self.conn = sql.connect('database.db')
        self.cur = self.conn.cursor()
        select_sections = 'SELECT section, callback, date FROM sections WHERE user_id=?'
        self.cur.execute(select_sections, [user_id])
        user_sections = self.cur.fetchall()
        self.conn.close()
        return user_sections
    
    def get_specific_snippet(self, user_id, section, title):
        '''Gets a specific snippet of a user section'''
        self.conn = sql.connect('database.db')
        self.cur = self.conn.cursor()
        select_specific_snippet = 'SELECT * FROM snippets WHERE user_id=? AND section=? AND title=?'
        self.cur.execute(select_specific_snippet, [user_id, section, title])
        user_snippet = self.cur.fetchone()
        self.conn.close()
        return user_snippet