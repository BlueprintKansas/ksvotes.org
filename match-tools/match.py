
# XXX - TODO
# - if vr_completed_at < 2 weeks prior to voter file date (need to make/derive this)
# -- need full dates to make this happen




# match.py
# - Takes in three filenames as cmdline args: the tab-separated Statevoterfile.txt (vdf),the csv ksvotes production file (kdf),
#   and the already-processed file.  The 4th argument, also optional is YYYY/MM/DD cutoff for 18yo birthday (eg: 2002/04/04)
# - finds as many of the KSV registrants as it can in the vdf, and tags each with the method used to
#   match or disqualify each one ('match_status'). For matches, save vdf's text_registrant_id for the match.

import sys 
import pandas as pd
import numpy as np


# default is short voter file
voter_fn = sys.argv[1] if len(sys.argv) > 1 else 'F1K.txt'

ksv_fn = sys.argv[2] if len(sys.argv) > 2 else 'ksvotes-production_copy.csv'
ksv_completed_fn = sys.argv[3] if len(sys.argv) > 3 else 'ksv_complete_2018.csv'
dob18cutoff = sys.argv[4] if len(sys.argv) > 4 else '2002/04/04'

# load current Kansas Voter File 
# Load dataset, tab-separated, create DataFrame
vdf=pd.read_csv(voter_fn,index_col=False,sep='\t',error_bad_lines=False,warn_bad_lines=True,encoding='latin-1',low_memory=False)

# Load KSVotes data file comma-separated, create DataFrame
kdf=pd.read_csv(ksv_fn,index_col=False,sep=',',error_bad_lines=True,encoding='latin-1',low_memory=False)

# Load KSVotes already completed file. ['text_registrant_id','(kdf)id'] comma-separated, create DataFrame
kdfc=pd.read_csv(ksv_completed_fn,index_col=False,sep=',',error_bad_lines=True,encoding='latin-1',low_memory=False)

print(f'pre-null-delete, kdf: {kdf.shape}')

# Delete null entries
kdf=kdf[kdf['id'].notnull()]

# for clarity in the rest of data, sort kdf by id
kdf = kdf.sort_values(by='id')
# XXX - is reset index necessary after sort?
kdf.reset_index(drop=True, inplace=True)

print(f'post-null/sort/reset, kdf: {kdf.shape}')

# add dob/reg_date columns to vdb
# reorder/normalize date format for dob and reg_datev
vdf['dob'] = pd.to_datetime(vdf['date_of_birth'],errors='coerce').dt.strftime("%Y/%m/%d")
vdf['reg_date'] = pd.to_datetime(vdf['date_of_registration'],errors='coerce').dt.strftime("%Y/%m/%d")

kdf['dob'] = pd.to_datetime(kdf['r_dob'],errors='coerce').dt.strftime("%Y/%m/%d")

# prepend v2- on all new ksv ids to distinguish from v1
kdf['new_id'] = 'v2-' + kdf['id'].fillna(0).astype(int).astype(str)

# initialize match_status for every record in ksv input to UNKNOWN
# create and initialize the saved voter-database logid for when a match is discovered
kdf['match_status'] = 'M_UNKNOWN'
kdf['saved_tr_id'] = '-1'
kdf['saved_reg_date'] = '-1'

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

# first 'remove' incomplete registrations and the "test" county.  Note, example data file had none of these(?)
# vr_completed_at is a number/time so you must use .notnull().  Argh!

kdf.loc[(kdf['match_status'] == 'M_UNKNOWN') & pd.isna(kdf['vr_completed_at']) & pd.isna(kdf['ab_completed_at']),'match_status'] = 'M_NOTCOMPLETED'
kdf.loc[(kdf['match_status'] == 'M_UNKNOWN') & pd.isna(kdf['vr_completed_at']) & pd.notnull(kdf['ab_completed_at']),'match_status'] = 'M_ONLYABCOMPLETED'
kdf.loc[(kdf['match_status'] == 'M_UNKNOWN') & (kdf['county'] == 'TEST'),'match_status'] = 'M_TESTCOUNTY'

# create KSV house number, get first segment split on space, strip alpha characters in case 493B or 2600. or "2600 
kdf['address_nbr'] = kdf['home_addr'].str.replace(r"[\"\',]",'').str.strip().str.split().str[0].str.replace(r"[a-zA-Z.#]",'')

# also make sure leading character of home addr is numeric
kdf['address_nbr_isnumeric'] = (kdf['address_nbr'] != '') & kdf['address_nbr'].str.isnumeric() & kdf['home_addr'].str.strip().str[0].str.isnumeric()

kdf['zip5'] = kdf['home_zip'].str[:5].astype(float).fillna(0).astype(int)

# XXX
kdf.loc[(kdf['match_status'] == 'M_UNKNOWN') & kdf['r_county'].notnull() & (kdf['r_county'] != kdf['county']),'match_status'] = 'M_COUNTYMISMATCH'

newdf=kdf[['id','match_status','vr_completed_at','ab_completed_at','county','home_addr','address_nbr','address_nbr_isnumeric']]
newdf.to_csv("newdf.csv",sep=',')

kdf.to_csv("kdf_postaddrcheck.csv",sep=',')

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

#if (len(sys.argv) > 4):
#   print(kdf[(kdf['first_low'] == sys.argv[3]) and (kdf['last_low'] == sys.argv[4])])


def match_kdf_vdf(round,kdf_match_on,vdf_match_on,match_party,assigned_match):
	global vdf
	global kdf

	print(f'Round {round}')


	# do merge, duplicate column names from right side get '_r' tacked on
	newdf = pd.merge(kdf, vdf, how='left',
		left_on = kdf_match_on, right_on = vdf_match_on,
		indicator=True,suffixes=('','_r'))

	print(f'post-merge newdf {newdf.shape}')
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
	dupdf.to_csv(f'Round{round}-dups.csv',sep=',')
	del dupdf

	# after merge, using kdf 'id', drop duplicate Voter file matches... 23 of them in Round1 against 121818 file
	newdf = newdf.drop_duplicates(subset='id',keep='first')
	newdf.reset_index(drop=True, inplace=True)

	# print(f'post-dropdup newdf {newdf.shape}')
	print(f"ROUND {round} found {(newdf_length - newdf.shape[0])} duplicate vdb entries")

	# Nuke all columns except these two

	newdf = newdf[['text_registrant_id','temp_match_status','reg_date']]

	# print(f'post-nuke newdf {newdf.shape}')

	# re-apply the merged data back to kdb with the vdb logid and the _merge status

	kdf = pd.concat([kdf, newdf], axis=1)

	# using the appended data to apply what we know to permanent rows
	kdf.loc[(kdf['temp_match_status'] == assigned_match),'match_status'] = assigned_match
	kdf.loc[(kdf['match_status'] == assigned_match),'saved_tr_id'] = kdf['text_registrant_id'].fillna(0).astype(int).astype(str)
	kdf.loc[(kdf['match_status'] == assigned_match),'saved_reg_date'] = kdf['reg_date']

	# then delete the temporary columns and temp df
	del kdf['temp_match_status']
	del kdf['text_registrant_id']
	del kdf['reg_date']
	del newdf

	print(kdf['match_status'].value_counts())

	print(f'end ROUND {round} kdf {kdf.shape}')

# ---------- end of def match_kdf_vdf

# ROUND1 - PERFECT matches on 4 columns, soft match on party columns. 
match_kdf_vdf(round=1, kdf_match_on= ['address_nbr','dob','first_low','last_low'],
				vdf_match_on = ['text_res_address_nbr','dob','first_low','last_low'],
				match_party = True, assigned_match = 'M_PERFECT5')

# ROUND2 - finds SHORTENED 3-char name matches on these 4 columns. 
match_kdf_vdf(round=2, kdf_match_on= ['address_nbr','dob','first_lowN','last_lowN'],
				vdf_match_on = ['text_res_address_nbr','dob','first_lowN','last_lowN'],
				match_party = True, assigned_match = 'M_SHORT3NAME')



kdf['first_lowN'] = kdf['first_low'].str[:4]	
kdf['last_lowN'] = kdf['last_low'].str[:4]	
vdf['first_lowN'] = vdf['first_low'].str[:4]	
vdf['last_lowN'] = vdf['last_low'].str[:4]	

# ROUND3 - finds SHORTENED 4-char name matches on these 4 columns, no dob
match_kdf_vdf(round=3, kdf_match_on= ['address_nbr','first_lowN','last_lowN'],
				vdf_match_on = ['text_res_address_nbr','first_lowN','last_lowN'],
				match_party = True, assigned_match = 'M_SHORT4NAME')

# experimental ROUND3.5 - uses dob, skips address, finds SHORTENED 4-char name matches on these 4 columns, no dob
match_kdf_vdf(round=3.5, kdf_match_on= ['dob','first_low','last_low'],
				vdf_match_on = ['dob','first_low','last_low'],
				match_party = True, assigned_match = 'M_MATCHWITHOUTADDR')

# experimental ROUND3.6 - uses dob, skips address, finds SHORTENED 4-char name matches on these 4 columns, no dob
match_kdf_vdf(round=3.6, kdf_match_on= ['address_nbr','dob','first_low','last_low'],
				vdf_match_on = ['text_res_address_nbr','dob','first_low','last_low'],
				match_party = False, assigned_match = 'M_MATCHWITHOUTPARTY')

print('ROUND4')
# ROUND4 - create a temp merged db that finds entries that were matched in prior runs (but no longer exist)

print(kdfc.shape)
# remove null entries from _completed_ list also
kdfc = kdfc[kdfc['text_registrant_id'].notnull()]
kdfc.reset_index(drop=True, inplace=True)
print(kdfc.shape)

# the 'id' field from kdfc will get renamed id_r during the merge because of collision
# so dedup can still operate on id
newdf = pd.merge(kdf, kdfc, how='left',
		 left_on=['new_id'],
		right_on=['id'],
			indicator=True,suffixes=('','_r'))

print(newdf.shape)

newdf_length = newdf.shape[0]

# after merge, using kdf 'id', drop duplicate Voter file matches... 63 of them in 121818 file
newdf = newdf.drop_duplicates(subset='id',keep='first')
newdf.reset_index(drop=True, inplace=True)

print(newdf.shape)
print(f"ROUND4 found {(newdf_length - newdf.shape[0])} duplicate vdb entries")

#NUKE all but these two columns
newdf = newdf[['text_registrant_id','_merge']]

print(newdf.shape)
print(kdf.shape)

# re-apply the merged data back to kdb with the vdb logid and the _merge status
kdf = pd.concat([kdf, newdf], axis=1)

print(kdf.shape)

# use concat-ed data to tag M_ type and store db_logid
kdf.loc[(kdf['match_status'] == 'M_UNKNOWN') & (kdf['_merge'] == 'both'),'match_status'] = 'M_PREVIOUS_NOWNOT'
kdf.loc[(kdf['match_status'] == 'M_PREVIOUS_NOWNOT'),'saved_tr_id'] = kdf['text_registrant_id'].fillna(0).astype(int).astype(str)

# if the _nbr is not a number or empty, its a PO Box or something else and will be marked M_BADADDRESS
# there are 10,900 empty addresses that this hits.
# XXX- also, "493B" fails, even though it should probably pass
# "== False" is necessary.  "is False" does _not_ work... why?
# moved to the end at Kate's request

kdf.loc[(kdf['match_status'] == 'M_UNKNOWN') & (kdf['address_nbr_isnumeric'] == False),'match_status'] = 'M_BADADDRESS'

#kdf.loc[(kdf['match_status'] == 'M_UNKNOWN') & kdf['r_county'].notnull() & (kdf['r_county'] != kdf['county']),'match_status'] = 'M_COUNTYMISMATCH'

# is the zipcode inside Kansas? (float needed to handle NaN case)
kdf.loc[(kdf['match_status'] == 'M_UNKNOWN') & ((kdf['zip5'] > 67954) | (kdf['zip5'] < 66002)),'match_status'] = 'M_BADZIPCODE'

# this is simplified output with just IDs and match status
newdf = kdf[['id','new_id','_merge','match_status','ab_completed_at','vr_completed_at','saved_tr_id','text_registrant_id']]
newdf.to_csv('merged-status.csv',sep=',')

# this is the output of the whole thing
kdf.to_csv('kdf_finaloutput.csv',sep=',')

# write the match_status counts to a file
match_status_outputfile = open('match_status.txt','w')
print(kdf['match_status'].value_counts(),file=match_status_outputfile)
match_status_outputfile.close()

# delete the temporary columns
del kdf['_merge']
del kdf['text_registrant_id']
del newdf

print(kdf.shape)
print(kdf['match_status'].value_counts())

tempDF = kdf[['id','first','middle','last','dob','party','first_lowN','last_lowN','zip5','address_nbr','address_nbr_isnumeric','county','r_county','match_status','saved_tr_id','home_addr','saved_reg_date','ab_completed_at','r_elections']]
tempDF.to_csv('kdf_processed.csv',sep=',')

# Kate specified output files
# create action file
tempDF = kdf[kdf.match_status.isin(['M_BADADDRESS','M_BADZIPCODE','M_UNKNOWN','M_MATCHWITHOUTADDR'])]
print("Shape of Action File:")
print(tempDF.shape)
tempDF.to_csv('kdf_actionfile.csv',sep=',',index=False)

# create dump file
tempDF = kdf[kdf.match_status.isin(['M_ONLYABCOMPLETED','M_TESTCOUNTY','M_NOTCOMPLETED','M_UNDER18DOB'])]
print("Shape of Dump File:")
print(tempDF.shape)
tempDF.to_csv('kdf_dumpfile.csv',sep=',',index=False)

# create complete file
tempDF = kdf[kdf.match_status.isin(['M_PERFECT5','M_PREVIOUS_NOWNOT','M_SHORT4NAME','M_SHORT3NAME'])]
print("Shape of Complete File:")
print(tempDF.shape)
tempDF.to_csv('kdf_completefile.csv',sep=',',index=False)

# create party file
tempDF = kdf[kdf.match_status.isin(['M_MATCHWITHOUTPARTY'])]
print("Shape of WithoutPartyMatch File:")
print(tempDF.shape)
tempDF.to_csv('kdf_withoutpartymatchfile.csv',sep=',',index=False)


tempDF = kdf[['id','first','saved_tr_id','match_status','saved_reg_date']]
tempDF = tempDF.astype({"id": int})
tempDF.to_csv('kdf_processed_noPII.csv',sep=',',index=False)

# tempDF = kdf[['id','first','middle','last','dob','party','first_lowN','last_lowN','zip5','address_nbr','address_nbr_isnumeric','match_status','saved_tr_id','home_addr','r_sos_reg']]
# tempDF.to_csv('kdf_sos_reg_processed.csv',sep=',')

kdf = kdf[['address_nbr','address_nbr_isnumeric','match_status','home_addr']]
kdf.to_csv('kdf_address_nbr_only_processed.csv',sep=',')

# find duplicates in vdf, specifically
dupdf = vdf[vdf.duplicated(['first_low','last_low','dob'],keep=False)].sort_values(by=['last_low','first_low'])
cols = ['dob'] + [col for col in dupdf if col != 'dob']
cols = ['first_low'] + [col for col in cols if col != 'first_low']
cols = ['last_low'] + [col for col in cols if col != 'last_low']
dupdf = dupdf[cols]
dupdf.reset_index(drop=True, inplace=True)
print(f'shape of dupvdf {dupdf.shape}')
dupdf.to_csv('vdf-dups.csv',sep=',')
del dupdf

vdf = vdf[['text_name_first','text_name_last','dob','desc_party','first_lowN','last_lowN','text_res_zip5','text_res_address_nbr','reg_date','text_registrant_id']]
vdf.to_csv('vdf_processed.csv',sep=',')



del kdf
del vdf
del tempDF
del kdfc
