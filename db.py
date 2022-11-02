import sqlite3

class dbbot:
	def __init__(self, db_file):
		self.conn = sqlite3.connect(db_file, check_same_thread=False)
		self.cursor = self.conn.cursor()

	def user_exists(self, user_id):
		result = self.cursor.execute("SELECT `uid` FROM `lang` WHERE `uid` = ?", (user_id,))
		return bool(len(result.fetchall()))

	def printlang(self, user_id):
		self.cursor.execute("SELECT `value` FROM `lang` WHERE `uid` = ?", (user_id,))
		practic = self.cursor.fetchone()
		print(practic[0])

	def get_user_lang(self, user_id):
		result = self.cursor.execute("SELECT `value` FROM `lang` WHERE `uid` = ?", (user_id,))
		return result.fetchone()[0]

	def add_user(self, user_id):
		self.cursor.execute("INSERT INTO `lang` (`uid`) VALUES (?)", (user_id,))
		return self.conn.commit()

	def change_user_lang(self, user_id, ulang):
		self.cursor.execute("UPDATE `lang` SET `value` = ? WHERE `uid` = ?", (ulang, user_id))
		return self.conn.commit()

	def close(self):
		self.conn.close()