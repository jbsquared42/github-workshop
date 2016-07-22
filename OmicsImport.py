#------------------------------------------------------------------------------
# Name          : OmicsImport.py
# Author        : John Boucher
# Last update   : 25/02/16
# Import Omics sample data - Called from Omics screen "Import rack file"
#------------------------------------------------------------------------------
import os
import shutil
import fnmatch
from django.db import connection
from meta import *
from datetime import datetime as dt, timedelta, timezone
from settings import *

def importOmicsFiles():
    print('\n**********************************************************\nrunning module OmicsImport.py\n')
    indir=OMICS_IMPORT_BASE
    print(indir)
    procdir=indir+os.sep+'Processed'
    now = dt.now(timezone.utc)
    timestamp=now.strftime("%Y%m%d")+'_'+now.strftime("%H%M%S")
    gelciC = connection.cursor()
    filenames=[]

    for f in os.listdir(indir):                                                    # get file list
        if fnmatch.fnmatch(f, '*.csv'):
            filenames.append(f)

    for f in filenames:                                                            # process file list
        filesuccess='Y'
        cleanbytes=[]
        print('PROCESSING : '+f+'\n')

        with open(indir+os.sep+f, 'rb') as f_in:                                       # omics files contain weird non-readable chars
            #f_in=open(indir+os.sep+f, 'rb')
            rawbytes = list(f_in.read())                                               # and quotes, so ..
            for index, i in enumerate(rawbytes):                                       # read file as bytes
              if i!=157 and i!=34 and i!=8:                                            #  remove wierd bytes, quotes, and backspaces
                  cleanbytes.append(i)
              if i==10 or index==len(rawbytes)-1:                                      #  at newline or EOF
                  strdata="".join(map(chr, cleanbytes))                                #   create clean string
                  cleanbytes=[]
                  data=strdata.split(",")                                              #  re-split data into list ..
                  if data[0]!='Participant ID':                                        #  and process ..
                    PID=data[0]                                                        #  Participant ID
                    BSID=data[1]                                                       #  blood specimen ID
                    sampletype=data[3]                                                 #  sample type
                    sampledate=data[4]                                                 #  blood_specimen_taken_dtm
                    fluidXid=data[6]                                                   #  omics_sample_id
                    vsend=data[7]                                                      #  blood_dna_volume_for_sending
                    labmeth=data[8]                                                    #  lab method
                    vbank=data[9]                                                      #  blood_dna_volume_for_banking
                    rackid=data[10]                                                    #  rack ID
                    sentdate=data[11]                                                  #  sent date
                    consign=data[12]                                                   #  consignment number
                    rackwell=data[13]                                                  #  rack well

                    meta='sample ID '+BSID+'  fluidXid ID '+fluidXid+'\n'
                    #print('-------------\nPID:'+PID+', BSID: '+BSID+', sampletype:'+sampletype+', sampledate: '+sampledate+', fluidXid: '+fluidXid+', vsend: '+vsend+', labmeth: '+labmeth)
                    #print('vbank: '+ vbank+',  rackid: '+rackid+',  sentdate: '+sentdate+',   consign: '+consign+',  rackwell: '+rackwell)

                    SQLstring = "select * from geldbx_sampleomic where omic_sample_id = '"+fluidXid+"' and file_sent <> 'Y'"
                    print(SQLstring)
                    gelciC.execute(SQLstring)                                          # check if omics sample with this
                    rowcount = gelciC.rowcount                                         # blood specimen ID exists ..
                    if rowcount==0:                                                    # if not - insert omics record

                        # if inserting we need to find the geldbx_sample table fk linked to this omics_sample_id
                        # and insert it into the omics table.
                        # Guessing that omics_sample_id here means geldbx_sample.blood_specimen_id ???
                        SQLstring="select id from geldbx_sample where blood_specimen_id = '"+BSID+"'"
                        gelciC.execute(SQLstring)
                        result = gelciC.fetchone()

                        if result:                                                     # associated sample set exists - insert linked omics record
                            print('inserting '+meta)
                            SQLstring="insert into geldbx_sampleomic (sample_table_fk_id, omic_sample_id, omic_sample_type, omic_sample_sent_date, omic_sample_consignment_number," \
                                      " omic_sample_rack_id, omic_sample_rack_well, data_ready, rack_ready, file_ready, file_sent) " \
                                      "values ('"+str(result[0])+"','"+fluidXid+"','"+sampletype+"','"+sentdate+"','"+consign+"','"+rackid+"','"+rackwell+"','Y','Y','N','N')"
                            #print(SQLstring)
                            filesuccess='Y'
                        else:                                                          # no accociated sample set exists - fail
                            print('insert fail for  '+meta)
                            importAuditWrite('Omics import',f,'sample set with specimen ID '+BSID+' not present')
                            filesuccess='N'

                    else:                                                              # .. otherwise update omics record
                        print('updating  '+meta)
                        SQLstring="update geldbx_sampleomic set omic_sample_type = '"+sampletype+"', omic_sample_sent_date = '"+sentdate+\
                                  "' , omic_sample_consignment_number = '"+consign+"', omic_sample_rack_id = '"+rackid+"', omic_sample_rack_well = '"+rackwell+\
                                  "', data_ready = 'Y', rack_ready = 'Y' where omic_sample_id = '"+fluidXid+"'"

                    gelciC.execute(SQLstring)

                    #print('gelciC.statusmessage:'+gelciC.statusmessage)
                    #if gelciC.statusmessage.find('0')>0:                               # set flag if any updates failed
                    #    filesuccess='N'

        if filesuccess=='Y':                                                       # if all updates successful ..
            print('\nfile:'+f+' - processed successfully\n')
            f1=f.split('.')[0]                                                     #   move test results file to processed dir
            shutil.move(indir+os.sep+f, procdir+os.sep+f1+'_proc_'+timestamp+'.csv')
        else:
            print('file:'+f+' - process failed\n')

    print('**********************************************************\n')


def importAuditWrite(logtype, filepath, logtext):
  try:
      gelciC2 = connection.cursor()
      SQLstring="INSERT INTO geldbx_file_transfer_log (log_type, log_dtm, file_path, log_text) VALUES (%s, %s, %s, %s)"
      values=(logtype, 'now()', filepath, logtext)
      gelciC2.execute(SQLstring, values)
      connection.commit()
  except:
      print('unable to insert to the database')