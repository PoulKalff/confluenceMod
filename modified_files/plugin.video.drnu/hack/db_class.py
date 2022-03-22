import sys
import sqlite3
import datetime

# --- Variables -----------------------------------------------------------------------------------


# --- Classes -------------------------------------------------------------------------------------

class HandleDB:
	""" all DB operations for program drtv """

	current = False
	errorCount = 0

	def __init__(self):
		""" init DB connection and ensure DB is ready """
		self.conn = sqlite3.connect('drtv.db')
		self.cursor = self.conn.cursor()
		# ensure tables exists
		query = self.cursor.execute("SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%'").fetchall()
		tables = []
		for row in query:
			tables.append(row[0])
		if 'lastUpdate' in tables:
			dbDate = self.cursor.execute("SELECT * FROM lastUpdate").fetchall()[0][0]
			self.current = True if dbDate == datetime.date.today().strftime("%Y-%m-%d") else False
		else:
			self.createTables()


	def clearTables(self):
		self.cursor.execute('DELETE FROM episodes')
		self.cursor.execute('DELETE FROM programIndexes')
		self.cursor.execute('DELETE FROM programs')
		self.cursor.execute('DELETE FROM lastUpdate')
		self.cursor.execute("INSERT INTO lastUpdate(update_date) VALUES (date('now'))")
		self.conn.commit()



	def createTables(self):
		self.cursor.execute("CREATE TABLE lastUpdate (update_date text)")
		self.cursor.execute("CREATE TABLE programIndexes(Title VARCHAR, Source VARCHAR, TotalSize INTEGER, _Param VARCHAR)")
		self.cursor.execute("CREATE TABLE programs(Title VARCHAR, Uri VARCHAR, PrimaryImageUri VARCHAR, SeriesSlug VARCHAR, indexLetter VARCHAR)")
		self.cursor.execute("CREATE TABLE episodes(Title VARCHAR, PrimaryImageUri VARCHAR, Slug VARCHAR, SortDateTime VARCHAR, Uri VARCHAR, SeriesSlug VARCHAR, SeriesTitle VARCHAR, Description VARCHAR)")
		self.cursor.execute("INSERT INTO lastUpdate(update_date) VALUES (date('now'))")
		self.conn.commit()



	def getProgramsByIndex(self, letter):
		""" Get all programs with the given index """
		tempIndexes = self.cursor.execute("SELECT Title from programIndexes").fetchall()
		indexes = [item for t in tempIndexes for item in t]
		if letter.upper() in indexes:
			reply = self.cursor.execute("SELECT * FROM programs WHERE indexLetter = '{}'".format(letter.upper()))
			return reply.fetchall()
		else:
			return 0


	def writeEpisodes(self, data):
		""" Write all given episodes to DB """
		for d in data:
			sql = 'INSERT INTO episodes VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(
				d['Title'].replace('"',"'"), d['PrimaryImageUri'], d['Slug'], d['SortDateTime'], d['PrimaryAsset']['Uri'], d['SeriesSlug'], d['SeriesTitle'].replace('"',"'"), d['Description'].replace('"',"'"))
			try:
				self.cursor.execute(sql)
			except:
				print('Failed SQL INSERT statement in writeEpisodes() :', sql)
				self.errorCount += 1
		self.conn.commit()



	def writeProgramIndexes(self, data):
		""" Write all known program indexes to DB """
		for d in data:
			sql = 'INSERT INTO programIndexes VALUES ("{}", "{}", {}, "{}")'.format(d['Title'], d['Source'], d['TotalSize'], d['_Param'])
			try:
				self.cursor.execute(sql)
			except:
				print('Failed SQL INSERT statement in writeProgramIndexes() :', sql)
				self.errorCount += 1
		self.conn.commit()



	def writePrograms(self, data):
		""" Write all known programs to DB """
		insert_into_table_programs = 'INSERT INTO programs VALUES ("{}", "{}", "{}", "{}", "{}")'
		for key, val in data.items():
			for d in data[key]:
				sql = insert_into_table_programs.format(d['Title'].replace('"',"'"), d['PrimaryAsset']['Uri'], d['PrimaryImageUri'], d['SeriesSlug'], key)
				try:
					self.cursor.execute(sql)
				except:
					print('Failed SQL INSERT statement in writePrograms() :', sql)
					self.errorCount += 1
		self.conn.commit()





# --- Main ----------------------------------------------------------------------------------------

#test = HandleDB()
#print('No errors found, but do not run me, import me!')


