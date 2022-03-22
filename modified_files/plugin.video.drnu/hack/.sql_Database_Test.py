import sqlite3

conn = sqlite3.connect('drtv_project.db')

c = conn.cursor()
c.execute('DELETE FROM lastUpdate')
c.execute("INSERT INTO lastUpdate(update_date) VALUES (date('now'))")


data = [{'Type': 'ProgramCard', 'SeriesTitle': 'Quizdyrene', 'SeriesSlug': 'quizdyrene', 'SeriesUrn': 'urn:dr:mu:bundle:583a2bdca11f9f17605f9e8f', 'SeasonEpisodeNumberingValid': True, 'SeasonTitle': 'Quizdyrene II', 'SeasonSlug': 'quizdyrene-ii', 'SeasonUrn': 'urn:dr:mu:bundle:5a19fc70a11f9f0848510100', 'SeasonNumber': 2, 'PrimaryChannel': 'dr.dk/mas/whatson/channel/TVR', 'PrimaryChannelSlug': 'dr-ramasjang', 'PrePremiere': False, 'ExpiresSoon': False, 'OnlineGenreText': '', 'PrimaryAsset': {'Kind': 'VideoResource', 'Uri': 'https://www.dr.dk/mu-online/api/1.4/bar/5dfa97a36187cb18186303e8', 'DurationInMilliseconds': 719800, 'Downloadable': True, 'RestrictedToDenmark': False, 'StartPublish': '2017-12-14T05:00:00Z', 'EndPublish': '2023-03-28T21:59:00Z', 'Target': 'Default', 'Encrypted': False}, 'HasPublicPrimaryAsset': True, 'AssetTargetTypes': 'Default', 'PrimaryBroadcastDay': '2022-03-28T00:00:00Z', 'PrimaryBroadcastStartTime': '2022-03-28T06:35:00Z', 'SortDateTime': '2022-03-28T06:35:00Z', 'Slug': 'quizdyrene-ii-9-kamelen-abu', 'Urn': 'urn:dr:mu:programcard:5a272942a11f9f22c842ed3d', 'PrimaryImageUri': 'https://www.dr.dk/mu-online/api/1.4/bar/5f3885ef71401441844c05f5', 'PresentationUri': 'https://www.dr.dk/tv/se/boern/ramasjang/quizdyrene/quizdyrene-ii/quizdyrene-ii-9-kamelen-abu', 'PresentationUriAutoplay': 'https://www.dr.dk/tv/se/boern/ramasjang/quizdyrene/quizdyrene-ii/quizdyrene-ii-9-kamelen-abu#!/,autoplay=true', 'AgeClassification': {'Authority': 'MRAM', 'Rating': 'MRAM-ALL', 'Description': 'Alle'}, 'Title': 'Quizdyrene II (9) - Kamelen Abu'}, {'Type': 'ProgramCard', 'SeriesTitle': "Q's Barbershop - Vollsmose forever!", 'SeriesSlug': 'q-s-barbershop', 'SeriesUrn': 'urn:dr:mu:bundle:5c7dc4be6187a40c04005cde', 'SeasonEpisodeNumberingValid': False, 'SeasonTitle': "Q's Barbershop", 'SeasonSlug': 'q-s-barbershop-2', 'SeasonUrn': 'urn:dr:mu:bundle:5c9e209f6187aa0ffcc276fc', 'SeasonNumber': 1, 'PrimaryChannel': 'dr.dk/mas/whatson/channel/DR3', 'PrimaryChannelSlug': 'dr3', 'PrePremiere': False, 'ExpiresSoon': False, 'OnlineGenreText': 'Dokumentar', 'PrimaryAsset': {'Kind': 'VideoResource', 'Uri': 'https://www.dr.dk/mu-online/api/1.4/bar/5fd0f28d539f02147059d4df', 'DurationInMilliseconds': 3623765, 'Downloadable': False, 'RestrictedToDenmark': True, 'StartPublish': '2020-12-15T05:00:00Z', 'EndPublish': '2023-12-14T22:59:00Z', 'Target': 'Default', 'Encrypted': False}, 'HasPublicPrimaryAsset': True, 'AssetTargetTypes': 'Default SpokenSubtitles', 'PrimaryBroadcastDay': '2019-08-24T00:00:00Z', 'PrimaryBroadcastStartTime': '2019-08-24T17:15:00Z', 'SortDateTime': '2019-08-24T17:15:00Z', 'Slug': 'q-s-barbershop', 'Urn': 'urn:dr:mu:programcard:5c7dc4be6187a40c04005cdc', 'PrimaryImageUri': 'https://www.dr.dk/mu-online/api/1.4/bar/5f38860871401441844c061d', 'PresentationUri': 'https://www.dr.dk/tv/se/q-s-barbershop/q-s-barbershop-2/q-s-barbershop', 'PresentationUriAutoplay': 'https://www.dr.dk/tv/se/q-s-barbershop/q-s-barbershop-2/q-s-barbershop#!/,autoplay=true', 'AgeClassification': {'Authority': 'MRAM', 'Rating': 'MRAM-ALL', 'Description': 'Alle'}, 'Title': "Q's Barbershop - Vollsmose forever!"}]


create_table_programs = """CREATE TABLE programs(
				Type								VARCHAR,
				SeriesTitle							VARCHAR,
				SeriesSlug							VARCHAR,
				SeriesUrn							VARCHAR,
				SeasonEpisodeNumberingValid			INTEGER,
				SeasonTitle							VARCHAR,
				SeasonSlug							VARCHAR,
				SeasonUrn							VARCHAR,
				SeasonNumber						INTEGER,
				PrimaryChannel						VARCHAR,
				PrimaryChannelSlug					VARCHAR,
				PrePremiere							INTEGER,
				ExpiresSoon							INTEGER,
				OnlineGenreText						VARCHAR,
				PrimaryAsset_Kind					VARCHAR,
				PrimaryAsset_Uri					VARCHAR,
				PrimaryAsset_DurationInMilliseconds	INTEGER,
				PrimaryAsset_Downloadable			INTEGER,
				PrimaryAsset_RestrictedToDenmark	INTEGER,
				PrimaryAsset_StartPublish			VARCHAR,
				PrimaryAsset_EndPublish				VARCHAR,
				PrimaryAsset_Target					VARCHAR,
				PrimaryAsset_Encrypted				VARCHAR,
				HasPublicPrimaryAsset				INTEGER,
				AssetTargetTypes 					VARCHAR,
				PrimaryBroadcastDay 				VARCHAR,
				PrimaryBroadcastStartTime 			VARCHAR,
				SortDateTime 						VARCHAR,
				Slug 								VARCHAR,
				Urn 								VARCHAR,
				PrimaryImageUri 					VARCHAR,
				PresentationUri 					VARCHAR,
				PresentationUriAutoplay 			VARCHAR,
				AgeClassification_Authority			VARCHAR,
				AgeClassification_Rating			VARCHAR,
				AgeClassification_Description		VARCHAR,
				Title 								VARCHAR,
				Url 								VARCHAR
)"""

#c.execute(create_table_programs)
#c.execute("CREATE TABLE lastUpdate (update_date text)")



c.execute('DELETE FROM programs')

insert_into_table_programs = 'INSERT INTO programs VALUES ("{}", "{}", "{}", "{}", {}, "{}", "{}", "{}", {}, "{}", "{}", {}, {}, "{}", "{}", "{}", {}, {}, {}, "{}", "{}", "{}", {}, {}, "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'

for d in data:
	sql = insert_into_table_programs.format(d['Type'], d['SeriesTitle'], d['SeriesSlug'], d['SeriesUrn'], d['SeasonEpisodeNumberingValid'], d['SeasonTitle'], d['SeasonSlug'], d['SeasonUrn'], 
		d['SeasonNumber'], d['PrimaryChannel'], d['PrimaryChannelSlug'], d['PrePremiere'], d['ExpiresSoon'], d['OnlineGenreText'], d['PrimaryAsset']['Kind'], d['PrimaryAsset']['Uri'], 
		d['PrimaryAsset']['DurationInMilliseconds'], d['PrimaryAsset']['Downloadable'], d['PrimaryAsset']['RestrictedToDenmark'], d['PrimaryAsset']['StartPublish'], d['PrimaryAsset']['EndPublish'], 
		d['PrimaryAsset']['Target'], d['PrimaryAsset']['Encrypted'], d['HasPublicPrimaryAsset'], d['AssetTargetTypes'], d['PrimaryBroadcastDay'], d['PrimaryBroadcastStartTime'],d['SortDateTime'], 
		d['Slug'], d['Urn'], d['PrimaryImageUri'], d['PresentationUri'], d['PresentationUriAutoplay'], d['AgeClassification']['Authority'], d['AgeClassification']['Rating'], 
		d['AgeClassification']['Description'],d['Title'], '<none>')
	c.execute(sql)



conn.commit()
conn.close()






# Test content
# ---------------------------------------------------------"
conn2 = sqlite3.connect('drtv_project.db')
d = conn2.cursor()
test = d.execute("SELECT * FROM programs")
for row in test:
 	for v in row:
 		print(v)



# print(testProgram.fetchall())
# print(insert_into_table_programs)
# testDate = c.execute("SELECT * FROM lastUpdate")
# print(testDate.fetchone())







