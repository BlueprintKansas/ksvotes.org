
# abmatch.py
# - Takes in two filenames as cmdline args: the kdf_processed csv file (kdf) 
# -- and the SoS ab_processed CSV file
# - it takes a 3rd argument, which is the text-based date of the election to check for as stored in ksvotes-production (eg/default: "August 4, 2020")
# - finds as many of the kdf text registrants as it can in the kdf, and tags with ABM_MATCH
# - saves output kdf as ab_kdf_processed.  

import sys, getopt
import pandas as pd
import numpy as np

kdf_fn = 'kdf_processed.csv'
ab_sent_fn = 'sent_20200715.csv'
ab_received_fn = 'sent_20200715.csv'
ab_electiondate = 'August 4, 2020'

try:
	opts, args = getopt.getopt(sys.argv[1:],"hk:s:r:d:",["kdfile=","sentfile=","receivedfile=","electiondate="])
except getopt.GetoptError:
	print ('ERROR, bad arguments. Try -h')
	sys.exit(2)
for opt, arg in opts:
	if opt == '-h':
		print ('abmatch.py -k <kdfile.csv> -s <SoSsentfile.csv> -r <SoSreceivedfile.csv> -d <electiondate>')
		print ('  --kdfile=')
		print ('  --sentfile=')
		print ('  --receivedfile=')
		print ('  --electiondate= (eg: "August 4, 2020)"')
		sys.exit
	elif opt in ("-k", "--kdfile"):
		kdf_fn = arg
		print(f'kdfile={kdf_fn}')
	elif opt in ("-s", "--sentfile"):
		ab_sent_fn = arg
		print(f'ab_sent_file={ab_sent_fn}')
	elif opt in ("-r", "--receivedfile"):
		ab_received_fn = arg
		print(f'ab_received_file={ab_received_fn}')
	elif opt in ("-d", "--electiondate"):
		ab_electiondate = arg
		print(f'ab_electiondate={ab_electiondate}')

# Load KSVotes data file comma-separated, create DataFrame
kdf=pd.read_csv(kdf_fn,index_col=False,sep=',',error_bad_lines=True,encoding='latin-1',low_memory=False)
print(f'kdf: {kdf.shape}')

# load ab sent file
asdf=pd.read_csv(ab_sent_fn,index_col=False,sep=',',error_bad_lines=False,warn_bad_lines=True,encoding='latin-1',low_memory=False)
print(f'asdf: {asdf.shape}')

# load ab received file (if it exists)
if ab_received_fn:
	ardf=pd.read_csv(ab_received_fn,index_col=False,sep=',',error_bad_lines=False,warn_bad_lines=True,encoding='latin-1',low_memory=False)
	print(f'ardf: {ardf.shape}')




# for clarity in the rest of data, sort kdf by id
kdf = kdf.sort_values(by='id')
# XXX - is reset index necessary after sort?
kdf.reset_index(drop=True, inplace=True)

# initialize match_status for every record in ksv input to UNKNOWN
# create and initialize the saved voter-database logid for when a match is discovered
kdf['ab_status'] = 'AB_UNKNOWN'

# first 'remove' incomplete registrations and the "test" county.  Note, example data file had none of these(?)
# vr_completed_at is a number/time so you must use .notnull().  Argh!

kdf.loc[(kdf['ab_status'] == 'AB_UNKNOWN') & pd.notnull(kdf['ab_completed_at']) & kdf['r_elections'].str.contains(ab_electiondate),'ab_status'] = 'AB_REQCOMPLETED'

print('Processing sent')
newdf = pd.merge(kdf, asdf, how='left',
		 left_on=['saved_tr_id'],
		right_on=['text_registrant_id'],
			indicator='s_merge_match')

# If there was a match on text_registrant_id and an AB requested and there was a match("both"), then mark as such, otherwise mark as not yet sent
newdf.loc[(newdf['s_merge_match'] == 'both') & (newdf['ab_status'] == 'AB_REQCOMPLETED'),'ab_status'] = 'ABMATCH_SENT'

# check if a KSVotes voter requested a ballot via another mechanism
newdf.loc[(newdf['s_merge_match'] == 'both') & (newdf['ab_status'] == 'AB_UNKNOWN'),'ab_status'] = 'AB_SENT'

print(newdf.shape)

if ab_received_fn:

	# delete the text_registrant_id from the prior received file
	del newdf['text_registrant_id']
	print('Processing received')
	newdf = pd.merge(newdf, ardf, how='left',
			 left_on=['saved_tr_id'],
			right_on=['text_registrant_id'],
				indicator='r_merge_match')

	# If there was a match on text_registrant_id and an AB requested and there was a match("both"), then mark as such, otherwise mark as not yet sent
	newdf.loc[(newdf['r_merge_match'] == 'both') & (newdf['ab_status'] == 'ABMATCH_SENT'),'ab_status'] = 'ABMATCH_RECEIVED'
	# This should be an error condition with SoS... just checking
	newdf.loc[(newdf['r_merge_match'] == 'both') & (newdf['ab_status'] == 'AB_REQCOMPLETED'),'ab_status'] = 'ABMATCH_RECEIVED_BUT_NOT_SENT'

	# Advanced ballot sent/received but not requested via KSVotes
	newdf.loc[(newdf['r_merge_match'] == 'both') & (newdf['ab_status'] == 'AB_SENT'),'ab_status'] = 'AB_RECEIVED'
	# This should be an error condition with SoS... just checking
	newdf.loc[(newdf['r_merge_match'] == 'both') & (newdf['ab_status'] == 'AB_UNKNOWN'),'ab_status'] = 'AB_RECEIVED_BUT_NOT_SENT'
	print(newdf.shape)



tempdf = newdf[['id','match_status','ab_completed_at','saved_tr_id','text_registrant_id','ab_status']]
tempdf.to_csv('ab_kdf_processed.csv',sep=',')

print(tempdf['ab_status'].value_counts())

# write the match_status counts to a file
sent_status_outputfile = open('absent_status.txt','w')
print(tempdf['ab_status'].value_counts(),file=sent_status_outputfile)
sent_status_outputfile.close()

del kdf
del asdf
if ab_received_fn:
	del ardf
del newdf
del tempdf
