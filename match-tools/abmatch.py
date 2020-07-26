
# abmatch.py
# - Takes in two filenames as cmdline args: the kdf_processed csv file (kdf) 
# -- and the SoS ab_processed CSV file
# - it takes a 3rd argument, which is the text-based date of the election to check for as stored in ksvotes-production (eg/default: "August 4, 2020")
# - finds as many of the kdf text registrants as it can in the kdf, and tags with ABMATCH_
# - saves output kdf as ab_kdf_processed.  

import sys, getopt
import pandas as pd
import numpy as np

kdf_fn = 'kdf_finaloutput.csv'
ab_sent_fn = 'sent_20200715.csv'
ab_returned_fn = ''
ab_eip_fn = ''
ab_electiondate = 'August 4, 2020'

try:
	opts, args = getopt.getopt(sys.argv[1:],"hk:s:r:e:d:",["kdfile=","sentfile=","returnedfile=","eipfile=","electiondate="])
except getopt.GetoptError:
	print ('ERROR, bad arguments. Try -h')
	sys.exit(2)
for opt, arg in opts:
	if opt == '-h':
		print ('abmatch.py -k <kdfile.csv> -s <SoSsentfile.csv> -r <SoSreturnedfile.csv> -d <electiondate>')
		print ('  --kdfile=')
		print ('  --sentfile=')
		print ('  --returnedfile=')
		print ('  --eipfile=')
		print ('  --electiondate= (eg: "August 4, 2020)"')
		sys.exit
	elif opt in ("-k", "--kdfile"):
		kdf_fn = arg
		print(f'kdfile={kdf_fn}')
	elif opt in ("-s", "--sentfile"):
		ab_sent_fn = arg
		print(f'ab_sent_file={ab_sent_fn}')
	elif opt in ("-r", "--returnedfile"):
		ab_returned_fn = arg
		print(f'ab_returned_file={ab_returned_fn}')
	elif opt in ("-e", "--eipfile"):
		ab_eip_fn = arg
		print(f'ab_eipfile={ab_eip_fn}')
	elif opt in ("-d", "--electiondate"):
		ab_electiondate = arg
		print(f'ab_electiondate={ab_electiondate}')

# Load KSVotes data file comma-separated, create DataFrame
kdf=pd.read_csv(kdf_fn,index_col=False,sep=',',error_bad_lines=True,encoding='latin-1',low_memory=False)
print(f'kdf: {kdf.shape}')

# load ab sent file
asdf=pd.read_csv(ab_sent_fn,index_col=False,sep=',',error_bad_lines=False,warn_bad_lines=True,encoding='latin-1',low_memory=False)
print(f'asdf: {asdf.shape}')

# load ab returned file (if it exists)
if ab_returned_fn:
	ardf=pd.read_csv(ab_returned_fn,index_col=False,sep=',',error_bad_lines=False,warn_bad_lines=True,encoding='latin-1',low_memory=False)
	print(f'ardf: {ardf.shape}')

# load ab eip file (if it exists)
if ab_eip_fn:
	aedf=pd.read_csv(ab_eip_fn,index_col=False,sep=',',error_bad_lines=False,warn_bad_lines=True,encoding='latin-1',low_memory=False)
	print(f'aedf: {aedf.shape}')


# for clarity in the rest of data, sort kdf by id
kdf = kdf.sort_values(by='id')
# XXX - is reset index necessary after sort?
kdf.reset_index(drop=True, inplace=True)

# initialize match_status for every record in ksv input to UNKNOWN
# create and initialize the saved voter-database logid for when a match is discovered
kdf['ab_status'] = 'AB_NOTREQUESTED'

# first 'remove' incomplete registrations and the "test" county.  Note, example data file had none of these(?)
# vr_completed_at is a number/time so you must use .notnull().  Argh!


kdf.loc[(kdf['ab_status'] == 'AB_NOTREQUESTED') & pd.notnull(kdf['ab_completed_at']) & kdf['r_elections'].str.contains(ab_electiondate),'ab_status'] = 'AB_REQUESTED'
kdf.loc[(kdf['ab_status'] == 'AB_NOTREQUESTED') & pd.notnull(kdf['ab_completed_at']) & pd.notnull(kdf['r_perm_reason']),'ab_status'] = 'AB_KSV_PERMANENT_REQ'
kdf.loc[(kdf['ab_status'] == 'AB_NOTREQUESTED') & pd.notnull(kdf['ab_completed_at']) & kdf['r_elections'].str.contains(", 2020"),'ab_status'] = 'AB_REQUESTED_FOR_ANOTHER_2020_ELECTION'

print('Processing sent')
newdf = pd.merge(kdf, asdf, how='left',
		 left_on=['saved_tr_id'],
		right_on=['text_registrant_id'],
			indicator='s_merge_match')

# If there was a match on text_registrant_id and an AB requested and there was a match("both"), then mark as such
kdf.loc[(newdf['s_merge_match'] == 'both') & (newdf['ab_status'] == 'AB_REQUESTED'),'ab_status'] = 'ABMATCH_SENT'
kdf.loc[(newdf['s_merge_match'] == 'both') & (newdf['ab_status'] == 'AB_KSV_PERMANENT_REQ'),'ab_status'] = 'ABMATCH_SENT_KSV_PERMANENT'

# check if a KSVotes voter requested a ballot via another mechanism
kdf.loc[(newdf['s_merge_match'] == 'both') & (newdf['ab_status'] == 'AB_NOTREQUESTED'),'ab_status'] = 'AB_NOTREQUESTED_VIA_KSVOTES_BUT_SENT'

del newdf

if ab_returned_fn:

	print('Processing returned')
	newdf = pd.merge(kdf, ardf, how='left',
			 left_on=['saved_tr_id'],
			right_on=['text_registrant_id'],
				indicator='r_merge_match')

	# If there was a match on text_registrant_id and an AB requested and there was a match("both"), then mark as such, otherwise mark as not yet sent
	kdf.loc[(newdf['r_merge_match'] == 'both') & (newdf['ab_status'] == 'ABMATCH_SENT'),'ab_status'] = 'ABMATCH_RETURNED'
	kdf.loc[(newdf['r_merge_match'] == 'both') & (newdf['ab_status'] == 'ABMATCH_SENT_KSV_PERMANENT'),'ab_status'] = 'ABMATCH_RETURNED_KSV_PERMANENT'

	# This should be an error condition with SoS... just checking
	kdf.loc[(newdf['r_merge_match'] == 'both') & (newdf['ab_status'] == 'AB_REQUESTED'),'ab_status'] = 'ABMATCH_RETURNED_BUT_NOT_SENT'

	# Advanced ballot sent/returned but not requested via KSVotes
	kdf.loc[(newdf['r_merge_match'] == 'both') & (newdf['ab_status'] == 'AB_NOTREQUESTED_VIA_KSVOTES_BUT_SENT'),'ab_status'] = 'AB_NOTREQUESTED_VIA_KSVOTES_BUT_SENT_AND_RETURNED'
	# This should be an error condition with SoS... just checking
	kdf.loc[(newdf['r_merge_match'] == 'both') & (newdf['ab_status'] == 'AB_NOTREQUESTED'),'ab_status'] = 'AB_RETURNED_BUT_NOT_SENT'

	del newdf

if ab_eip_fn:

	print('Processing eip')
	newdf = pd.merge(kdf, aedf, how='left',
			 left_on=['saved_tr_id'],
			right_on=['text_registrant_id'],
				indicator='e_merge_match')

	# If there was a match on text_registrant_id and an AB requested and there was a match("both"), then mark as such, otherwise mark as not yet sent
	kdf.loc[(newdf['e_merge_match'] == 'both') & (newdf['ab_status'] == 'ABMATCH_SENT'),'ab_status'] = 'ABMATCH_SENT_EIP'
	# This should be an error condition with SoS... just checking
	kdf.loc[(newdf['e_merge_match'] == 'both') & (newdf['ab_status'] == 'AB_REQUESTED'),'ab_status'] = 'ABMATCH_UNSENT_EIP'

	# If there was a match on text_registrant_id and an AB requested and there was a match("both"), then mark as such, otherwise mark as not yet sent
	kdf.loc[(newdf['e_merge_match'] == 'both') & (newdf['ab_status'] == 'ABMATCH_RETURNED'),'ab_status'] = 'ABMATCH_RETURNED_EIP_YIPES'

	kdf.loc[(newdf['e_merge_match'] == 'both') & (newdf['ab_status'] == 'AB_RETURNED'),'ab_status'] = 'AB_RETURNED_EIP_YIPES'

	# Advanced ballot sent/returned but not requested via KSVotes
	kdf.loc[(newdf['e_merge_match'] == 'both') & (newdf['ab_status'] == 'AB_SENT'),'ab_status'] = 'AB_SENT_EIP'

	# This KSVoter voted early in person and never requested an AB
	kdf.loc[(newdf['e_merge_match'] == 'both') & (newdf['ab_status'] == 'AB_NOTREQUESTED'),'ab_status'] = 'AB_EIP'


kdf.to_csv('ab_kdf_processed.csv',sep=',')

print(kdf['ab_status'].value_counts())

# write the match_status counts to a file
sent_status_outputfile = open('ab_sent_status.txt','w')
print(kdf['ab_status'].value_counts(),file=sent_status_outputfile)
sent_status_outputfile.close()

# Kate specified output files
# create dumpfile
tempdf = kdf[kdf.ab_status.isin(['AB_NOTREQUESTED','AB_NOTREQUESTED_VIA_KSVOTES_BUT_SENT','AB_NOTREQUESTED_VIA_KSVOTES_SENT_AND_RETURNED','AB_EIP','AB_SENT_EIP','AB_RECEIVED_EIP'])]
print(f'Shape of Dump File: {tempdf.shape}')
tempdf.to_csv('ab_dumpfile.csv',sep=',',index=False)

# create completefile
tempdf = kdf[kdf.ab_status.isin(['ABMATCH_SENT','ABMATCH_RETURNED','ABMATCH_SENT_EIP','ABMATCH_RECEIVED_EIP','ABMATCH_SENT_KSV_PERMANENT'])]
print(f'Shape of Complete File: {tempdf.shape}')
tempdf.to_csv('ab_completefile.csv',sep=',',index=False)

# create workfile
tempdf = kdf[kdf.ab_status.isin(['AB_REQUESTED','ABMATCH_UNSENT_EIP','ABMATCH_RETURNED_BUT_NOT_SENT','AB_KSV_PERMANENT_REQ'])]
print(f'Shape of Work File: {tempdf.shape}')
tempdf.to_csv('ab_workfile.csv',sep=',',index=False)

del kdf
del asdf
if ab_returned_fn:
	del ardf
if ab_eip_fn:
	del aedf
del tempdf
