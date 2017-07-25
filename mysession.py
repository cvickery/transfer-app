""" Attempting to reinvent the wheel for Flask sessions.
    The issue is the size of the session, with too many replacement options to learn. Can I roll my
    own in a reasonable amount of time?

    Plan: sessions is a table in the cuny_courses.db sqlite db. Key-value pairs. Unique keys from
    urandom. Blobs for value. I want the following operations to work, where key is not the db
    key, but is the app's key for an item stored in the db.

      mysession = MySession(session)
      mysession[key] = anything
      anything = mysession[key]
      del mysession

    Flask session gets "mysession"
    purge expired sessions somehow (low prio: how many user sessions will there actually be?)
    use namedtuples for session values

    I think you have to read the session blob from the db for for each get and both to read and
    write it for each put.

    sqlite> .schema sessions
      CREATE TABLE sessions (
      session_key text primary key,
      session_dict blob,
      expiration_time float);
"""
import time, datetime
import pickle
from uuid import uuid4
import sqlite3
import logging

logger = logging.getLogger('mysession')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('debugging.log')
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

sql_logger = logging.getLogger('sqlite3')
sql_logger.setLevel(logging.DEBUG)
sfh = logging.FileHandler('debugging.log')
sformatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
sfh.setFormatter(sformatter)
sql_logger.addHandler(sfh)

sqlite3.enable_callback_tracebacks(True)

class MySession:

  def __init__(self, app, session_key=None):
    logger.debug('__init__({}) {}'.format(session_key, type(session_key)))
    self.initialized = False
    self.connection = sqlite3.connect('static/db/cuny_catalog.db')
    self.connection.set_trace_callback(sql_logger.debug)
    logger.debug(self.connection)
    self.connection.row_factory = sqlite3.Row
    logger.debug(self.connection.row_factory)
    self.cursor = self.connection.cursor()
    logger.debug(self.cursor)

    if session_key == None:
      self.session_key = str(uuid4())
      logger.debug('created new session_key: {}'.format(self.session_key))
    else:
      # Attempting to connect to an existing session. Be sure it exists and hasn't expired
      logger.debug('type of session_key is {}'.format(type(session_key)))
      self.session_key = session_key
      logger.debug('self.session_key is now {}'.format(self.session_key))
      if self.is_expired(self.session_key):
        logger.debug('{} is expired: deleting')
        self.cursor.execute('delete from sessions where session_key = ?', (self.session_key,))
        raise Exception('Unable to clone: session expired')
      else:
        self.initialized = True
    logger.debug('self.initialized is {}'.format(self.initialized))
    if not self.initialized:
      self.cursor.execute("insert into sessions values(?, ?, ?)", (self.session_key,
          pickle.dumps(dict()),
          time.time() + datetime.timedelta(minutes=120).total_seconds()))
    self.connection.commit()

  def __str__(self):
    logger.debug('__str__()')
    self.cursor.execute("select session_dict from sessions where session_key = ?", (self.session_key,))
    self.mydict = pickle.loads(self.cursor.fetchone()[0])
    return 'Mysession[{}] {} keys'.format(self.session_key, len(self.mydict))

  def __del__(self):
    logger.debug('__del__()')
    if self.is_expired(self.session_key):
      self.cursor.execute("delete from sessions where session_key = ?", (self.session_key,))
      self.connection.commit()
      logger.debug('Session expired: deleted')
    else:
      logger.debug('Session not expired: not deleted')

  def __setitem__(self, key, value):
    logger.debug('__setitem__({}, {})'.format(key, value))
    self.cursor.execute("select session_dict from sessions where session_key = ?", (self.session_key,))
    self.mydict = pickle.loads(self.cursor.fetchone()[0])
    self.mydict[key] = value
    self.cursor.execute("update sessions set session_dict = ? where session_key = ?",
      (pickle.dumps(self.mydict), self.session_key))
    self.connection.commit()

  def __getitem__(self, key):
    logger.debug('__getitem__({})'.format(key))
    self.cursor.execute("select session_dict from sessions where session_key = ?", (self.session_key,))
    self.mydict = pickle.loads(self.cursor.fetchone()[0])
    return self.mydict[key] # KeyError if key not in session

  def __len__(self):
    logger.debug('__len__()')
    self.cursor.execute("select session_dict from sessions where session_key = ?", (self.session_key,))
    self.mydict = pickle.loads(self.cursor.fetchone()[0])
    return len(self.mydict)

  def __bool__(self):
    logger.debug('__bool__()')
    return True

  def keys(self):
    logger.debug('keys()')
    self.cursor.execute("select session_dict from sessions where session_key = ?", (self.session_key,))
    self.mydict = pickle.loads(self.cursor.fetchone()[0])
    return [key for key in self.mydict]

  def is_expired(self, session_key):
    self.cursor.execute("select expiration_time from sessions where session_key = ?",(session_key,))
    row = self.cursor.fetchone()
    if row == None or len(row) == 0: return True
    expiration_time = row[0]
    if expiration_time != None and expiration_time > time.time(): return False
    return True