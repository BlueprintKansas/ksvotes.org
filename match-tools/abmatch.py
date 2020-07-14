
# abmatch.py
# - Takes in two filenames as cmdline args: the kdf_processed csv file (kdf) 
# -- and the SoS ab_processed CSV file
# - finds as many of the kdf text registrants as it can in the kdf, and tags with ABM_MATCH
# - saves output kdf as ab_kdf_processed.  

import sys 
import pandas as pd
import numpy as np


# default is short voter file
kdf_fn = sys.argv[1] if len(sys.argv) > 1 else 'kdf_processed.csv'

ab_fn = sys.argv[2] if len(sys.argv) > 2 else 'ab_sent_sample.csv'

# load ab complted file
# Load dataset, tab-separated, create DataFrame
adf=pd.read_csv(ab_fn,index_col=False,sep=',',error_bad_lines=False,warn_bad_lines=True,encoding='latin-1',low_memory=False)

# Load KSVotes data file comma-separated, create DataFrame
kdf=pd.read_csv(kdf_fn,index_col=False,sep=',',error_bad_lines=True,encoding='latin-1',low_memory=False)

print(f'kdf: {kdf.shape}')

# for clarity in the rest of data, sort kdf by id
kdf = kdf.sort_values(by='id')
# XXX - is reset index necessary after sort?
kdf.reset_index(drop=True, inplace=True)

# initialize match_status for every record in ksv input to UNKNOWN
# create and initialize the saved voter-database logid for when a match is discovered
kdf['ab_sent_status'] = 'AB_UNKNOWN'

# first 'remove' incomplete registrations and the "test" county.  Note, example data file had none of these(?)
# vr_completed_at is a number/time so you must use .notnull().  Argh!

kdf.loc[(kdf['ab_sent_status'] == 'AB_UNKNOWN') & pd.notnull(kdf['ab_completed_at']),'ab_sent_status'] = 'AB_ABREQCOMPLETED'

print(kdf.shape)
print(adf.shape)

newdf = pd.merge(kdf, adf, how='left',
		 left_on=['saved_tr_id'],
		right_on=['text_registrant_id'],
			indicator=True)

# If there was a match on text_registrant_id and an AB requested and one sent, then mark as such, otherwise mark as not yet sent
newdf.loc[(newdf['_merge'] == 'both') & (newdf['ab_sent_status'] == 'AB_ABREQCOMPLETED') & newdf['ballot_sent'],'ab_sent_status'] = 'ABMATCH_SENT'
newdf.loc[(newdf['_merge'] == 'both') & (newdf['ab_sent_status'] == 'AB_ABREQCOMPLETED'),'ab_sent_status'] = 'ABMATCH_NOTSENTYET'
print(newdf.shape)

tempdf = newdf[['id','match_status','ab_completed_at','saved_tr_id','text_registrant_id','ab_sent_status']]
tempdf.to_csv('ab_kdf_processed.csv',sep=',')

print(tempdf['ab_sent_status'].value_counts())

# write the match_status counts to a file
sent_status_outputfile = open('absent_status.txt','w')
print(tempdf['ab_sent_status'].value_counts(),file=sent_status_outputfile)
sent_status_outputfile.close()

del kdf
del adf
del newdf
del tempdf
