
# abmatch.py - KSVotes.org advanced-ballot matching user records against SoS sent/received/eip
# - Takes in up to 4 filenames as cmdline args: the kdf_finaloutput csv file (kdf)
#  -- and the SoS sent/received/eip CSV files
# - it takes an optional 5th argument, which is the text-based date of the election to
#  -- check for as stored in ksvotes-production (eg/default: "August 4, 2020")
# - finds as many of the kdf text registrants as it can in the kdf, and tags with ABMATCH_
# - saves output kdf as ab_kdf_processed.  

# Example output, July22nd, 2020
# AB_NOTREQUESTED                                      120411
# -- KSV sessions that did not request AB and don't have perm status
# ABMATCH_SENT                                          15386
# -- matched and sent
# AB_NOTREQUESTED_VIA_KSVOTES_BUT_SENT                  11663
# -- KSV voters who didn't request via KSV, but
# -- apparently requested via other means and ballot was sent
# AB_REQUESTED_FOR_ANOTHER_2020_ELECTION                 2895
# -- as described, including to help match counts
# -- against AB totals for year
# AB_REQUESTED                                           2724
# -- KSV votes who requested via KSV and not (yet?) sent
# ABMATCH_SENT_KSV_PERMANENT                              867
# -- KSV voter who applied for perm and was sent
# AB_KSV_PERMANENT_REQ                                    342
# -- KSV voter who applied for perm and was not (yet) sent
# AB_KSV_PERMANENT_NONREQ                                  23
# -- KSV voter who became perm some other way, sent
# AB_NOTREQUESTED_VIA_KSVOTES_BUT_SENT_AND_RETURNED         4
# -- KSV voter not requesting AB, but sent/returned already
# AB_EIP                                                    2
# -- KSV voter voting early-in-person

# XXX To do - election date month may be in Spanish as well


import sys, getopt
import pandas as pd
import numpy as np

kdf_fn = 'kdf_finaloutput.csv'
ab_sent_fn = ''
ab_returned_fn = ''
ab_eip_fn = ''
ab_electiondate = 'November 3, 2020'
ab_handled_fn = ''

try:
	opts, args = getopt.getopt(sys.argv[1:],"hk:s:r:e:d:c:",["kdfile=","sentfile=","returnedfile=","eipfile=","electiondate=","handledfile="])
except getopt.GetoptError:
	print ('ERROR, bad arguments. Try -h')
	sys.exit(2)
for opt, arg in opts:
	if opt == '-h':
		print ('abmatch.py -k <kdfile.csv> -s <SoSsentfile.csv> -r <SoSreturnedfile.csv> -e <SoSeipfile.csv> -c <ABhandled.csv> -d <electiondate>')
		print ('  --kdfile=')
		print ('  --sentfile=')
		print ('  --returnedfile=')
		print ('  --eipfile=')
		print ('  --electiondate= (eg: "August 4, 2020)"')
		print ('  --handledfile=')
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
	elif opt in ("-c", "--handledfile"):
		ab_handled_fn = arg
		print(f'ab_handledfile={ab_handled_fn}')
	elif opt in ("-d", "--electiondate"):
		ab_electiondate = arg
		print(f'ab_electiondate={ab_electiondate}')

# Load KSVotes data file comma-separated, create DataFrame
kdf=pd.read_csv(kdf_fn,index_col=False,sep=',',error_bad_lines=True,encoding='latin-1',low_memory=False)
print(f'kdf: {kdf.shape}')

# load ab sent file if it exists
if ab_sent_fn:
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

# load ab handled file (if it exists)
if ab_handled_fn:
	ahdf=pd.read_csv(ab_handled_fn,index_col=False,sep=',',error_bad_lines=False,warn_bad_lines=True,encoding='latin_1',low_memory=False)
	print(f'ahdf: {ahdf.shape}')

# for clarity in the rest of data, sort kdf by id
kdf = kdf.sort_values(by='id')
# XXX - is reset index necessary after sort?
kdf.reset_index(drop=True, inplace=True)

# initialize match_status for every record in ksv input to UNKNOWN
# create and initialize the saved voter-database logid for when a match is discovered
kdf['ab_status'] = 'AB_NOTREQUESTED'

# If ab completed and election matches current, only handles Spanish for April/May/November right now
ab_electiondate_spanish = ab_electiondate
if 'April' in ab_electiondate:
	ab_electiondate_spanish.replace('April','Abril')
if 'August' in ab_electiondate:
	ab_electiondate_spanish.replace('August','Agosto')
if 'November' in ab_electiondate:
	ab_electiondate_spanish.replace('November','Noviembre')

kdf.loc[(kdf['ab_status'] == 'AB_NOTREQUESTED') & pd.notnull(kdf['ab_completed_at']) & kdf['r_elections'].str.contains(ab_electiondate),'ab_status'] = 'AB_REQUESTED'
kdf.loc[(kdf['ab_status'] == 'AB_NOTREQUESTED') & pd.notnull(kdf['ab_completed_at']) & kdf['r_elections'].str.contains(ab_electiondate_spanish),'ab_status'] = 'AB_REQUESTED'

# If ab completed and it has a r_perm_reason this is a first-time request to make permanent
kdf.loc[(kdf['ab_status'] == 'AB_NOTREQUESTED') & pd.notnull(kdf['ab_completed_at']) & pd.notnull(kdf['r_perm_reason']),'ab_status'] = 'AB_KSV_PERMANENT_REQ'

# If ab not completed, but VR was  completed, but r_election contains permanent, this must have come from VV and its KSV voter, but someone who had asked for permanent via other mechanism
kdf.loc[(kdf['ab_status'] == 'AB_NOTREQUESTED') & ~kdf['match_status'].str.contains('M_NOTCOMPLETED') & kdf['r_elections'].str.contains('permanent'),'ab_status'] = 'AB_KSV_PERMANENT_NONREQ'

# Check for other elections just to help understand counts better
kdf.loc[(kdf['ab_status'] == 'AB_NOTREQUESTED') & pd.notnull(kdf['ab_completed_at']) & kdf['r_elections'].str.contains(", 2020"),'ab_status'] = 'AB_REQUESTED_FOR_ANOTHER_2020_ELECTION'

if ab_sent_fn:
	print('Processing sent')
	newdf = pd.merge(kdf, asdf, how='left',
			 left_on=['saved_tr_id'],
			right_on=['text_registrant_id'],
				indicator='s_merge_match')

	# If there was a match on text_registrant_id and an AB requested and there was a match("both"), then mark as such
	kdf.loc[(newdf['s_merge_match'] == 'both') & (newdf['ab_status'] == 'AB_REQUESTED'),'ab_status'] = 'ABMATCH_SENT'
	kdf.loc[(newdf['s_merge_match'] == 'both') & (newdf['ab_status'] == 'AB_KSV_PERMANENT_REQ'),'ab_status'] = 'ABMATCH_SENT_KSV_PERMANENT'
	kdf.loc[(newdf['s_merge_match'] == 'both') & (newdf['ab_status'] == 'AB_KSV_PERMANENT_NONREQ'),'ab_status'] = 'ABMATCH_SENT_KSV_PERMANENT'

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

	del newdf


# now process the already "completed" file that contains entries that have been
# hand evaluated and processed
if(ab_handled_fn):

	print('Processing Handled file')

		# remove null entries from _completed_ list also
	ahdf = ahdf[ahdf['text_registrant_id'].notnull()]
	ahdf.reset_index(drop=True, inplace=True)

	# the 'id' field from acdf will get renamed id_r during the merge because of collision
	# so dedup can still operate on id
	newdf = pd.merge(kdf, ahdf, how='left',
			 left_on=['new_id'],
			right_on=['id'],
				indicator='h_merge_match',suffixes=('','_r'))

	newdf_length = newdf.shape[0]
	print(newdf.shape)

	# after merge, using kdf 'id', drop duplicate matches... 
	newdf = newdf.drop_duplicates(subset='id',keep='first')
	newdf.reset_index(drop=True, inplace=True)
	print(f"Handled file, found {(newdf_length - newdf.shape[0])} duplicate kdf entries")

	# use loc from newdf and kdf because they are exactly aligned. data to tag AB_ type
	kdf.loc[(kdf['ab_status'] == 'AB_REQUESTED') & (newdf['h_merge_match'] == 'both'),'ab_status'] = 'AB_HANDLED_NOTYET_SENT'

	del newdf


kdf.to_csv('ab_kdf_processed.csv',sep=',')

print(kdf['ab_status'].value_counts())

# write the match_status counts to a file
sent_status_outputfile = open('ab_sent_status.txt','w')
print(kdf['ab_status'].value_counts(),file=sent_status_outputfile)
sent_status_outputfile.close()

# Kate specified output files
# create dumpfile
tempdf = kdf[kdf.ab_status.isin(['AB_NOTREQUESTED',
								'AB_NOTREQUESTED_VIA_KSVOTES_BUT_SENT',
								'AB_NOTREQUESTED_VIA_KSVOTES_BUT_SENT_AND_RETURNED',
								'AB_RETURNED_BUT_NOT_SENT',
								'AB_REQUESTED_FOR_ANOTHER_2020_ELECTION',
								'AB_EIP',
								'AB_SENT_EIP',
								'AB_RECEIVED_EIP'])]
print(f'Shape of Dump File: {tempdf.shape}')
tempdf.to_csv('ab_dumpfile.csv',sep=',',index=False)

# create completefile
tempdf = kdf[kdf.ab_status.isin(['ABMATCH_SENT',
								'ABMATCH_RETURNED',
								'ABMATCH_SENT_EIP',
								'ABMATCH_RECEIVED_EIP',
								'ABMATCH_SENT_KSV_PERMANENT',
								'ABMATCH_RETURNED_KSV_PERMANENT',
								'AB_HANDLED_NOTYET_SENT'])]
print(f'Shape of Complete File: {tempdf.shape}')
tempdf.to_csv('ab_completefile.csv',sep=',',index=False)

# create workfile
tempdf = kdf[kdf.ab_status.isin(['AB_REQUESTED',
								'ABMATCH_UNSENT_EIP',
								'ABMATCH_RETURNED_BUT_NOT_SENT',
								'AB_KSV_PERMANENT_REQ',
								'AB_KSV_PERMANENT_NONREQ'])]
print(f'Shape of Work File: {tempdf.shape}')
tempdf.to_csv('ab_workfile.csv',sep=',',index=False)

del kdf
if ab_sent_fn:
	del asdf
if ab_returned_fn:
	del ardf
if ab_eip_fn:
	del aedf
if ab_handled_fn:
	del ahdf
del tempdf
