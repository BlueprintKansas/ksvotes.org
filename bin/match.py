
# match.py - KSVotes.org voter record matching against SoS voter file
# - Takes in three filenames as cmdline args: the tab-separated Statevoterfile.txt (vdf),the csv ksvotes production raw file (kdf),
#   and the already-processed file.  The 4th argument, also optional is YYYY/MM/DD cutoff for 18yo birthday (eg: 2002/04/04)
# - finds as many of the KSV registrants as it can in the vdf, and tags each with the method used to
#   match or disqualify each one ('match_status'). For matches, save vdf's text_registrant_id for the match.
# - It also outputs apparent duplicates in the voter file

# XXX - TODO
# - if vr_completed_at < 2 weeks prior to voter file date (need to make/derive this)
# -- need full dates to make this happen
# 

import sys, getopt
import pandas as pd
import numpy as np

# default is short voter file
voter_fn = 'F1K.txt'
ksv_fn = 'ksvotes-production_20200714.csv'
ksv_handled_fn = ''
dob18cutoff = '2002/08/04'

try:
	opts, args = getopt.getopt(sys.argv[1:],"hv:k:c:d:",["vfile=","kdfile=","hfile=","DOBcutoff="])
except getopt.GetoptError:
	print ('ERROR, bad arguments. Try -h')
	sys.exit(2)
for opt, arg in opts:
	if opt == '-h':
		print ('match.py -v <SOS voter file> -k <kdfile.csv> -c <KSVhandled.csv> -d <DOBcuttoff>')
		print ('  --vfile=')
		print ('  --kdfile=')
		print ('  --hfile=')
		print ('  --DOBcutoff= (eg: "August 4, 2020")')
		sys.exit
	elif opt in ("-k", "--kdfile"):
		ksv_fn = arg
	elif opt in ("-v", "--vfile"):
		voter_fn = arg
	elif opt in ("-c", "--hfile"):
		ksv_handled_fn = arg
	elif opt in ("-d", "--DOBcutoff"):
		dob18cutoff = arg
		print(f'DOBcutoff={dob18cutoff}')


# load current Kansas Voter File 
# Load dataset, tab-separated, create DataFrame
print(f'voter_file={voter_fn}')
vdf=pd.read_csv(voter_fn,index_col=False,sep='\t',error_bad_lines=False,warn_bad_lines=True,encoding='latin-1',low_memory=False)
print(f'voter_file shape: {vdf.shape}')

# Load KSVotes data file, skip first line, comma-separated, create DataFrame
print(f'kdfile={ksv_fn}')
kdf=pd.read_csv(ksv_fn,index_col=False,sep=',',error_bad_lines=True,encoding='latin-1',low_memory=False,header=1)

print(f'kdf shape: {kdf.shape}')

# times are already in pandas format='%Y-%m-%d %H:%M:%S.%f')

# Load KSVotes already completed file. ['text_registrant_id','(kdf)id'] comma-separated, create DataFrame
if(ksv_handled_fn):
	print(f'handled_file={ksv_handled_fn}')
	kdfh=pd.read_csv(ksv_handled_fn,index_col=False,sep=',',error_bad_lines=True,encoding='windows-1252',low_memory=False)
	print(f'handled_file shape: {kdfh.shape}')

# Delete null entries
kdf=kdf[kdf['id'].notnull()]

# for clarity in the rest of data, sort kdf by id
kdf = kdf.sort_values(by='id')
# XXX - is reset index necessary after sort?
kdf.reset_index(drop=True, inplace=True)

#print(f'post-null/sort/reset, kdf: {kdf.shape}')

# add dob/reg_date columns to vdb
# reorder/normalize date format for dob and reg_datev
vdf['dob'] = pd.to_datetime(vdf['date_of_birth'],errors='coerce').dt.strftime("%Y/%m/%d")
vdf['reg_date'] = pd.to_datetime(vdf['date_of_registration'],errors='coerce').dt.strftime("%Y/%m/%d")

kdf['dob'] = pd.to_datetime(kdf['r_dob'],errors='coerce').dt.strftime("%Y/%m/%d")

# prepend v2- on all new ksv ids to distinguish from v1
kdf['new_id'] = 'v2-' + kdf['id'].fillna(0).astype(int).astype(str)

# initialize match_status for every record in ksv input to UNKNOWN
# create and initialize the saved voter-database logid for when a match is discovered
# save db_logid so you can compare to county supplied by kdf (and AB request)
kdf['match_status'] = 'M_UNKNOWN'
kdf['county_match_status'] = 'C_UNKNOWN'
kdf['saved_tr_id'] = '-1'
kdf['saved_db_logid'] = 'xxx'
kdf['saved_reg_date'] = '1900/1/1'

# rename columns of KSV data to match more closely the voter file's
kdf.rename(columns = {
	'r_name_first':'first',
	'r_name_middle':'middle',
	'r_name_last':'last',
	'r_phone':'phone',
	'r_addr':'home_addr',
	'r_unit':'home_addr2',
	'r_city':'home_city',
	'r_state':'home_state',
	'r_zip':'home_zip',
		},
		inplace = True)

#pd.set_option("display.max_rows",999)
#print(kdf.dtypes)
#print(kdf[kdf['r_has_prev_name'].astype(str).str.contains('True')])

#print(kdf[kdf['match_status'] == 'M_UNKNOWN'])

# first 'remove' incomplete registrations and the "test" county.  Note, example data file had none of these(?)
# vr_completed_at is a number/time so you must use .notnull().  Argh!

kdf.loc[(kdf['match_status'] == 'M_UNKNOWN') & pd.isna(kdf['vr_completed_at']) & pd.isna(kdf['ab_completed_at']),'match_status'] = 'M_NOTCOMPLETED'
kdf.loc[(kdf['match_status'] == 'M_UNKNOWN') & (kdf['county'] == 'TEST'),'match_status'] = 'M_TESTCOUNTY'

# create KSV house number, get first segment split on space, strip alpha characters in case 493B or 2600. or "2600 
kdf['address_nbr'] = kdf['home_addr'].str.replace(r"[\"\',]",'').str.strip().str.split().str[0].str.replace(r"[a-zA-Z.#]",'')

# also make sure leading character of home addr is numeric
kdf['address_nbr_isnumeric'] = (kdf['address_nbr'] != '') & kdf['address_nbr'].str.isnumeric() & kdf['home_addr'].str.strip().str[0].str.isnumeric()

kdf['zip5'] = kdf['home_zip'].str[:5].astype(float).fillna(0).astype(int)

# find folks who won't be 18 by the time of the next election. It's likely county will sit on their registration
kdf.loc[(kdf['match_status'] == 'M_UNKNOWN') & (kdf['dob'] > dob18cutoff),'match_status'] = 'M_UNDER18DOB'

# In preparation for soft comparisons, create lowercase/stripped and shortened version of names
# strip single-quote, double-quote, question-mark, and space from names
# initially, _lowN is 3, for 3 char matching. Later will be updated to 4 characters

kdf['first_low'] = kdf['first'].str.strip(' "?').str.replace("'","").str.lower()
kdf['last_low'] = kdf['last'].str.strip(' "?').str.replace("'","").str.lower()
kdf['first_lowN'] = kdf['first_low'].str[:3]	
kdf['last_lowN'] = kdf['last_low'].str[:3]

vdf['first_low'] = vdf['text_name_first'].str.strip(' "?').str.replace("'","").str.lower()
vdf['last_low'] = vdf['text_name_last'].str.strip(' "?').str.replace("'","").str.lower()
vdf['first_lowN'] = vdf['first_low'].str[:3]
vdf['last_lowN'] = vdf['last_low'].str[:3]

# use only first letter of party
vdf['party1'] = vdf.desc_party.str.lower().str[:1]
kdf['party1'] = kdf.party.str.lower().str[:1]

vdf['text_res_address_nbr'] = vdf['text_res_address_nbr'].fillna(0).astype(int).astype(str)



def match_kdf_vdf(round,kdf_match_on,vdf_match_on,match_party,assigned_match):
	global vdf
	global kdf

	print(f'Round {round}')


	# do merge, duplicate column names from right side get '_r' tacked on
	newdf = pd.merge(kdf, vdf, how='left',
		left_on = kdf_match_on, right_on = vdf_match_on,
		indicator=True,suffixes=('','_r'))

	#print(f'post-merge newdf {newdf.shape}')
	newdf_length = newdf.shape[0]

	if match_party == True:
		# first tag perfect5 matches if the party matches
		newdf.loc[ (newdf['match_status'] == 'M_UNKNOWN') & 
				(newdf['_merge'] == 'both') &
				(newdf['party1'] == newdf['party1_r']), 
				'temp_match_status' ] = assigned_match	

		newdf.loc[ (newdf['match_status'] == 'M_UNKNOWN') & 
				(newdf['_merge'] == 'both') &
				(pd.isna(newdf['party'])), 
				'temp_match_status' ] = assigned_match
	else:
		newdf.loc[ (newdf['match_status'] == 'M_UNKNOWN') & 
				(newdf['_merge'] == 'both'),
				'temp_match_status' ] = assigned_match	

	# print(newdf['temp_match_status'].value_counts())

	# tempdf=newdf[['id','first','middle','last','dob','party','party1','first_low','last_low','zip5','address_nbr','address_nbr_isnumeric','temp_match_status','saved_tr_id','home_addr','match_status']]
	# tempdf.to_csv('post-merge'+str(round)+'dump.csv',sep=',')

    # first, find duplicates
	dupdf = newdf[newdf.duplicated('id',keep=False)]
	# print(f'shape of dupdf {dupdf.shape}')
	dupdf.to_csv(f'dups-{round}.csv',sep=',')
	del dupdf

	# after merge, using kdf 'id', drop duplicate Voter file matches... 23 of them in Round1 against 121818 file
	newdf = newdf.drop_duplicates(subset='id',keep='first')
	newdf.reset_index(drop=True, inplace=True)

	# print(f'post-dropdup newdf {newdf.shape}')
	print(f"Round {round} found {(newdf_length - newdf.shape[0])} duplicate vdb entries")

	# Nuke all columns except these

	newdf = newdf[['text_registrant_id','temp_match_status','reg_date','db_logid']]

	# re-apply the merged data back to kdb with the vdb logid and the _merge status

	kdf = pd.concat([kdf, newdf], axis=1)

	# using the appended data to apply what we know to permanent rows
	kdf.loc[(kdf['temp_match_status'] == assigned_match),'match_status'] = assigned_match
	kdf.loc[(kdf['match_status'] == assigned_match),'saved_tr_id'] = kdf['text_registrant_id'].fillna(0).astype(int).astype(str)
	kdf.loc[(kdf['match_status'] == assigned_match),'saved_db_logid'] = kdf['db_logid']
	kdf.loc[(kdf['match_status'] == assigned_match),'saved_reg_date'] = kdf['reg_date']
	kdf.loc[(kdf['match_status'] == assigned_match),'county_match_status'] = 'C_NOMATCH'
	kdf.loc[(kdf['match_status'] == assigned_match) & (kdf['county'].str.lower() == kdf['db_logid'].str.lower()),'county_match_status'] = 'C_MATCH'


	# then delete the temporary columns and temp df
	del kdf['temp_match_status']
	del kdf['text_registrant_id']
	del kdf['db_logid']
	del kdf['reg_date']
	del newdf

	print(f'end Round {round} kdf {kdf.shape}')

# ---------- end of def match_kdf_vdf

# ROUND1 - PERFECT matches on 4 columns, soft match on party columns. 
match_kdf_vdf(round='M_PERFECT5', kdf_match_on= ['address_nbr','dob','first_low','last_low'],
				vdf_match_on = ['text_res_address_nbr','dob','first_low','last_low'],
				match_party = True, assigned_match = 'M_PERFECT5')

# ROUND2 - finds SHORTENED 3-char name matches on these 4 columns. 
match_kdf_vdf(round='M_SHORT3NAME_DOB', kdf_match_on= ['address_nbr','dob','first_lowN','last_lowN'],
				vdf_match_on = ['text_res_address_nbr','dob','first_lowN','last_lowN'],
				match_party = True, assigned_match = 'M_SHORT3NAME_DOB')


# update lowN to be 4 characters
kdf['first_lowN'] = kdf['first_low'].str[:4]	
kdf['last_lowN'] = kdf['last_low'].str[:4]	
vdf['first_lowN'] = vdf['first_low'].str[:4]	
vdf['last_lowN'] = vdf['last_low'].str[:4]	

# ROUND3 - finds SHORTENED 4-char name matches on these 4 columns, no dob
match_kdf_vdf(round='M_SHORT4NAME_NODOB', kdf_match_on= ['address_nbr','first_lowN','last_lowN'],
				vdf_match_on = ['text_res_address_nbr','first_lowN','last_lowN'],
				match_party = True, assigned_match = 'M_SHORT4NAME_NODOB')

print('Round M_HANDLED')
# ROUND4 - create a temp merged db that finds entries that were matched in prior work ("handled")

if(ksv_handled_fn):
	# remove null entries from handled list also
	kdfh = kdfh[kdfh['text_registrant_id'].notnull()]
	kdfh.reset_index(drop=True, inplace=True)

	# the 'id' field from kdfh will get renamed id_r during the merge because of collision
	# so dedup can still operate on id
	newdf = pd.merge(kdf, kdfh, how='left',
			 left_on=['new_id'],
			right_on=['id'],
				indicator=True,suffixes=('','_r'))

	newdf_length = newdf.shape[0]

	# after merge, using kdf 'id', drop duplicate Voter file matches... 63 of them in 121818 file
	newdf = newdf.drop_duplicates(subset='id',keep='first')
	newdf.reset_index(drop=True, inplace=True)

	print(f"ROUND4 found {(newdf_length - newdf.shape[0])} duplicate vdb entries")

	#NUKE all but these two columns
	newdf = newdf[['text_registrant_id','_merge']]

	# re-apply the merged data back to kdb with the vdb logid and the _merge status
	kdf = pd.concat([kdf, newdf], axis=1)

	# use concat-ed data to tag M_ type and store db_logidk
	kdf.loc[(kdf['match_status'] == 'M_UNKNOWN') & (kdf['_merge'] == 'both'),'match_status'] = 'M_HANDLED'
	kdf.loc[(kdf['match_status'] == 'M_HANDLED'),'saved_tr_id'] = kdf['text_registrant_id'].fillna(0).astype(int).astype(str)

	del kdf['_merge']
	del kdf['text_registrant_id']
	del newdf

# experimental - uses dob, skips address, finds SHORTENED 4-char name matches on these columns
match_kdf_vdf(round='M_DOB_WITHOUTADDR', kdf_match_on= ['dob','first_low','last_low'],
				vdf_match_on = ['dob','first_low','last_low'],
				match_party = True, assigned_match = 'M_DOB_WITHOUTADDR')

# experimental - uses dob, finds SHORTENED 4-char name matches on these 4 columns
match_kdf_vdf(round='M_DOB_WITHOUTPARTY', kdf_match_on= ['address_nbr','dob','first_low','last_low'],
				vdf_match_on = ['text_res_address_nbr','dob','first_low','last_low'],
				match_party = False, assigned_match = 'M_DOB_WITHOUTPARTY')


# must convert from object to string for comparison to succeed. Why? Other fields don't have this issue
kdf.loc[(kdf['match_status'] == 'M_UNKNOWN'),'r_has_prev_name'] = kdf['r_has_prev_name'].astype(str)

kdf.loc[(kdf['match_status'] == 'M_UNKNOWN') & (kdf['r_has_prev_name'] == 'True'),'first_lowN'] = kdf['r_prev_name_first'].str.strip(' "?').str.replace("'","").str.lower()
kdf.loc[(kdf['match_status'] == 'M_UNKNOWN') & (kdf['r_has_prev_name'] == 'True'),'last_lowN'] = kdf['r_prev_name_last'].str.strip(' "?').str.replace("'","").str.lower()

# experimental - uses dob, address, party, uses first name only
match_kdf_vdf(round='M_PREVIOUSNAME', kdf_match_on= ['address_nbr','dob','first_lowN','last_lowN'],
				vdf_match_on = ['text_res_address_nbr','dob','first_low','last_low'],
				match_party = True, assigned_match = 'M_PREVIOUSNAME')

# experimental - uses dob, address, party, uses first name only
match_kdf_vdf(round='M_FIRSTNAMEONLY', kdf_match_on= ['address_nbr','dob','first_low'],
				vdf_match_on = ['text_res_address_nbr','dob','first_low'],
				match_party = True, assigned_match = 'M_FIRSTNAMEONLY')

# experimental - uses dob, address, party, uses first name only
match_kdf_vdf(round='M_NONAME', kdf_match_on= ['address_nbr','dob'],
				vdf_match_on = ['text_res_address_nbr','dob'],
				match_party = True, assigned_match = 'M_NONAME')

# if the _nbr is not a number or empty, its a PO Box or something else and will be marked M_BADADDRESS
# there are 10,900 empty addresses that this hits.
# XXX- also, "493B" fails, even though it should probably pass
# "== False" is necessary.  "is False" does _not_ work... why?
# moved to the end at Kate's request

kdf.loc[(kdf['match_status'] == 'M_UNKNOWN') & (kdf['address_nbr_isnumeric'] == False),'match_status'] = 'M_BADADDRESS'

# is the zipcode inside Kansas? (float needed to handle NaN case)
kdf.loc[(kdf['match_status'] == 'M_UNKNOWN') & ((kdf['zip5'] > 67954) | (kdf['zip5'] < 66002)),'match_status'] = 'M_BADZIPCODE'

# is there any way just to direct compare this?
kdf['tmp_updated_at'] = pd.to_datetime(kdf['updated_at'])
kdf['saved_reg_date'] = pd.to_datetime(kdf['saved_reg_date'])

kdf.loc[kdf.match_status.isin(['M_BADADDRESS','M_BADZIPCODE','M_UNKNOWN',
							'M_DOB_WITHOUTADDR','M_DOB_WITHOUTPARTY','M_FIRSTNAMEONLY']) & 
							(kdf['saved_reg_date'] > kdf['tmp_updated_at']),
							'match_status'] = 'M_NEWER_REG'
kdf.drop(['tmp_updated_at'],axis=1,inplace=True)

# hack check to get ab_completed_at count
#kdf.loc[(kdf['match_status'] != 'M_NOTCOMPLETED') & kdf['ab_completed_at'].str.contains('2020'),'match_status'] = 'M_ABCOMPLETEDAT'

# this is simplified output with just IDs and match status
#newdf = kdf[['id','new_id','_merge','match_status','ab_completed_at','vr_completed_at','saved_tr_id','text_registrant_id','saved_reg_date','saved_db_logid','county_match_status','tmp_updated_at']]
#newdf.to_csv('merged-status.csv',sep=',')

# this is the output of the whole thing
kdf.to_csv('kdf_finaloutput.csv',sep=',')

# write the match_status counts to a file
match_status_outputfile = open('match_status.txt','w')
print(kdf['match_status'].value_counts(),file=match_status_outputfile)
match_status_outputfile.close()

print(kdf['match_status'].value_counts())
print(kdf['county_match_status'].value_counts())

tempDF = kdf[['id','first','middle','last','dob','party','first_lowN','last_lowN','zip5','address_nbr','address_nbr_isnumeric','county','saved_db_logid','match_status','county_match_status','saved_tr_id','home_addr','saved_reg_date','ab_completed_at','r_elections']]
tempDF.to_csv('kdf_processed.csv',sep=',')

# Kate specified output files
# create action file
tempDF = kdf[kdf.match_status.isin(['M_BADADDRESS','M_BADZIPCODE','M_UNKNOWN','M_NEWER_REG',
									'M_DOB_WITHOUTADDR','M_FIRSTNAMEONLY','M_PREVIOUSNAME','M_NONAME'])]
print(f'Shape of Action File: {tempDF.shape}')
tempDF.to_csv('kdf_actionfile.csv',sep=',',index=False)

# create dump file
tempDF = kdf[kdf.match_status.isin(['M_ONLYABCOMPLETED','M_TESTCOUNTY','M_NOTCOMPLETED','M_UNDER18DOB'])]
print(f'Shape of Dump File: {tempDF.shape}')
tempDF.to_csv('kdf_dumpfile.csv',sep=',',index=False)

# create complete file
tempDF = kdf[kdf.match_status.isin(['M_PERFECT5','M_HANDLED','M_SHORT4NAME_NODOB','M_SHORT3NAME_DOB'])]
print(f'Shape of Complete File (all fields): {tempDF.shape}')
tempDF.to_csv('kdf_completefile_all_fields.csv',sep=',',index=False)

# create kdf_completefile with only fields necessary to input back into match.py as the "complete file"
tempDF = tempDF[['saved_tr_id','new_id']]
tempDF.rename(columns = {
	'saved_tr_id':'text_registrant_id',
	'new_id':'id'
		},
		inplace = True)
print(f'Shape of Complete File: {tempDF.shape}')
tempDF.to_csv('kdf_completefile.csv',sep=',',index=False)

# create party file
tempDF = kdf[kdf.match_status.isin(['M_DOB_WITHOUTPARTY'])]
print(f'Shape of WithoutPartyMatch File: {tempDF.shape}')
tempDF.to_csv('kdf_withoutpartymatchfile.csv',sep=',',index=False)


tempDF = kdf[['id','first','saved_tr_id','saved_db_logid','match_status','saved_reg_date']]
tempDF = tempDF.astype({"id": int})
tempDF.to_csv('kdf_processed_noPII.csv',sep=',',index=False)

# tempDF = kdf[['id','first','middle','last','dob','party','first_lowN','last_lowN','zip5','address_nbr','address_nbr_isnumeric','match_status','saved_tr_id','home_addr','r_sos_reg']]
# tempDF.to_csv('kdf_sos_reg_processed.csv',sep=',')

kdf = kdf[['address_nbr','address_nbr_isnumeric','match_status','home_addr']]
kdf.to_csv('kdf_address_nbr_only_processed.csv',sep=',')

print('find duplicates in vdf, specifically: first/last/dob')
dupdf = vdf[vdf.duplicated(['first_low','last_low','dob'],keep=False)].sort_values(by=['last_low','first_low'])
cols = ['dob'] + [col for col in dupdf if col != 'dob']
cols = ['first_low'] + [col for col in cols if col != 'first_low']
cols = ['last_low'] + [col for col in cols if col != 'last_low']
dupdf = dupdf[cols]
dupdf.reset_index(drop=True, inplace=True)
print(f'shape of dupvdf {dupdf.shape}')
dupdf.to_csv('dups-vdf.csv',sep=',')
del dupdf

vdf = vdf[['text_name_first','text_name_last','dob','desc_party','first_lowN','last_lowN','text_res_zip5','text_res_address_nbr','reg_date','text_registrant_id']]
vdf.to_csv('vdf_processed.csv',sep=',')

del kdf
del vdf
del tempDF
del kdfh
