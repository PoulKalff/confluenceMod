# Databse 'drtv' MUST exist!

import sys
import datetime
import mysql.connector


# --- Variables -----------------------------------------------------------------------------------


# --- Classes -------------------------------------------------------------------------------------

class HandleDB:
	""" all DB operations for program drtv """

	current = False
	errorCount = 0

	def __init__(self):
		""" init DB connection and ensure DB is ready """
		self.conn = mysql.connector.connect( host="localhost",  user="xbmc",  password="xbmc", database='drtv')
		self.cursor = self.conn.cursor()
		# ensure tables exists
		self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'drtv';")
		reply = self.cursor.fetchall()
		tables = []
		for row in reply:
			tables.append(row[0])
		if 'lastUpdate' in tables:
			print('  Checking that tables exist................', end='')
			self.cursor.execute("SELECT * FROM lastUpdate;")
			reply = self.cursor.fetchall()[0][0]
			self.current = True if reply == datetime.date.today().strftime("%Y-%m-%d") else False
			print('done!')
		else:
			print('  Creating all tables.......................', end='')
			self.dropTables()
			self.createTables()
			self.current = True
			print('done!')


	def clearTables(self):
		self.cursor.execute('DELETE FROM episodes')
		self.cursor.execute('DELETE FROM programs')
		self.cursor.execute('DELETE FROM lastUpdate')
		self.cursor.execute('DELETE FROM programIndexes')
		self.cursor.execute("INSERT INTO lastUpdate(update_date) VALUES (CURDATE())")
		self.conn.commit()


	def dropTables(self):
		self.cursor.execute("DROP TABLE IF EXISTS episodes")
		self.cursor.execute("DROP TABLE IF EXISTS programs")
		self.cursor.execute("DROP TABLE IF EXISTS lastUpdate")
		self.cursor.execute("DROP TABLE IF EXISTS programIndexes")
		self.conn.commit()


	def createTables(self):
		print('Creating lastUpdate')
		self.cursor.execute("CREATE TABLE lastUpdate (update_date text)")
		print('Inserting to lastUpdate')
		self.cursor.execute("INSERT INTO lastUpdate(update_date) VALUES (CURDATE())")
		print('Creating programindexes')
		self.cursor.execute("CREATE TABLE programIndexes(Title VARCHAR(255), Source VARCHAR(255), TotalSize INTEGER, _Param VARCHAR(255))")
		print('Creating programs')
		self.cursor.execute("CREATE TABLE programs(Title VARCHAR(255), Uri VARCHAR(255), PrimaryImageUri VARCHAR(255), SeriesSlug VARCHAR(255), indexLetter VARCHAR(255))")
		print('Creating episodes')
		self.cursor.execute("CREATE TABLE episodes(Title VARCHAR(255), PrimaryImageUri VARCHAR(255), Slug VARCHAR(255), SortDateTime VARCHAR(255), Uri VARCHAR(255), SeriesSlug VARCHAR(255), SeriesTitle VARCHAR(255), Description MEDIUMTEXT, Duration INTEGER)")
		self.conn.commit()



	def getProgramsByIndex(self, letter):
		""" Get all programs with the given index """
		self.cursor.execute("SELECT Title FROM programIndexes")
		reply = self.cursor.fetchall()
		indexes = [item for t in reply for item in t]
		if letter.upper() in indexes:
			self.cursor.execute("SELECT * FROM programs WHERE indexLetter = '{}';".format(letter.upper()))
			return self.cursor.fetchall()
		else:
			return 0


	def writeEpisodes(self, data):
		""" Write all given episodes to DB """
		for d in data:
			sql = "INSERT INTO episodes VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {})".format(
				d['Title'].replace("'",''), d['PrimaryImageUri'], d['Slug'], d['SortDateTime'], d['PrimaryAsset']['Uri'], d['SeriesSlug'], d['SeriesTitle'].replace("'",''),
				d['Description'].replace("'",'"'), d['PrimaryAsset']['DurationInMilliseconds'])
			try:
				self.cursor.execute(sql)
			except:
				print('Failed SQL INSERT statement in writeEpisodes() :', sql)
				self.errorCount += 1
		self.conn.commit()



	def writeProgramIndexes(self, data):
		""" Write all known program indexes to DB """
		for d in data:
			sql = "INSERT INTO programIndexes VALUES ('{}', '{}', {}, '{}')".format(d['Title'], d['Source'], d['TotalSize'], d['_Param'])
			try:
				self.cursor.execute(sql)
			except:
				print('Failed SQL INSERT statement in writeProgramIndexes() :', sql)
				self.errorCount += 1
		self.conn.commit()



	def writePrograms(self, data):
		""" Write all known programs to DB """
		insert_into_table_programs = "INSERT INTO programs VALUES ('{}', '{}', '{}', '{}', '{}')"
		for key, val in data.items():
			for d in data[key]:
				sql = insert_into_table_programs.format(d['Title'].replace("'",""), d['PrimaryAsset']['Uri'], d['PrimaryImageUri'], d['SeriesSlug'], key)
				try:
					self.cursor.execute(sql)
				except (Exception, Error) as error:
					print("Error while connecting to PostgreSQL", error)
					self.errorCount += 1
		self.conn.commit()






# --- Main ----------------------------------------------------------------------------------------

test = HandleDB()
#print('No errors found, but do not run me, import me!')


