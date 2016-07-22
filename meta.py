__author__ = 'boucherj'

meta = {
"hello":"hello jb, how nice to see you!",
"CLARITY_ODBC":"DRIVER={SQL Server};SERVER=10.229.78.191,4018;DATABASE=CLARITY;UID=Finance;PWD=F1n@nc3",
"GELCI_ODBC":"dbname='geldbx_rel' user='admin' host='10.229.78.63' port='10000' password='admin'",
"STUDY_DEMOGS_SQL":"select isnull(p.PAT_ID,'') AS patEpicId, REPLACE(isnull(p.SSN,''), ' ', '') AS patNhsNumber, isnull(p.PAT_MRN_ID,'') AS patCuhMrn, isnull(p.PAT_LAST_NAME,'') AS patLastName, isnull(p.PAT_FIRST_NAME,'') AS patFirstName, isnull(p.BIRTH_DATE,'') AS patDob, isnull(ps.NAME,'') AS patGender, isnull(p.ADD_LINE_1,'') AS patAdd1, isnull(p.ADD_LINE_2,'') AS patAdd2, isnull(p.CITY,'') AS patCity, isnull(p.ZIP,'') AS patPostCode, isnull(e.STUDY_ALIAS,'') AS patParticpantId, isnull(es.NAME,'') AS patStatus FROM PATIENT AS p INNER JOIN ENROLL_INFO e ON p.PAT_ID = e.PAT_ID LEFT OUTER JOIN ZC_SEX AS ps ON p.SEX_C = ps.RCPT_MEM_SEX_C LEFT OUTER JOIN ZC_ENROLL_STATUS AS es ON e.ENROLL_STATUS_C = es.ENROLL_STATUS_C WHERE e.RESEARCH_STUDY_ID = '233' and isnull(es.NAME,'')='Consented'",


"FAMILY_SQL":"select e.STUDY_ALIAS, substring(t.NOTE_TEXT, charindex('Family ID number',t.NOTE_TEXT), 40) from HNO_NOTE_TEXT t, ENROLL_INFO e, patient p where e.STUDY_ALIAS is not null and t.NOTE_ID = e.ENROLL_CMT_NOTE_ID and e.PAT_ID = p.PAT_ID and (t.NOTE_TEXT like '%Family ID number%') union select e.STUDY_ALIAS, substring(t.NOTE_TEXT, charindex('Family ID no',t.NOTE_TEXT), 40) from HNO_NOTE_TEXT t, ENROLL_INFO e, patient p where e.STUDY_ALIAS is not null and t.NOTE_ID = e.ENROLL_CMT_NOTE_ID and e.PAT_ID = p.PAT_ID and (t.NOTE_TEXT like '%Family ID no%') union select e.STUDY_ALIAS, substring(t.NOTE_TEXT, charindex('Family number',t.NOTE_TEXT), 40) from HNO_NOTE_TEXT t, ENROLL_INFO e, patient p where e.STUDY_ALIAS is not null and t.NOTE_ID = e.ENROLL_CMT_NOTE_ID and e.PAT_ID = p.PAT_ID and (t.NOTE_TEXT like '%Family number%')",

"FAMILY_SQL1":"select e.STUDY_ALIAS, substring(t.NOTE_TEXT, charindex('1110',t.NOTE_TEXT), 9) from HNO_NOTE_TEXT t, ENROLL_INFO e, patient p where e.STUDY_ALIAS is not null and t.NOTE_ID = e.ENROLL_CMT_NOTE_ID and e.PAT_ID = p.PAT_ID and (NOTE_TEXT like '%family numb%' or NOTE_TEXT like '%family ID%' or NOTE_TEXT like '%family no%') and NOTE_TEXT like '%110%'",

"RACK_READY_SQL":"select clinical_sample_id, coalesce(lab_sample_rack_id, ''), coalesce(blood_dna_sample_rack_well,''), coalesce(ff_dna_used,'Y'), coalesce(ff_dna_sample_rack_well,''), coalesce(ffpe_dna_used,'Y'), coalesce(ffpe_dna_sample_rack_well,''), coalesce(lab_sample_sent,'Y') from geldbx_sample",
}

