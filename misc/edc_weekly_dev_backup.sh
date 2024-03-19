#!/bin/bash

EDC_BACKUPDIR=/opt/informatica/edc_backup
EDC_LOGFILES=/opt/informatica/edc_backup

currdate=`date +"%Y%m%d%H%M%S"`
DOMAIN=DOM_BIGDATA
MRS=MRS_EDC_DEV
EDC_SVC_NM=ICS_EDC_DEV
DOMAIN_DATABASE=INFA_DOM_BIGDATA

#Set these environment variables in .bash_profile
#export INFA_DEFAULT_DOMAIN_USER=infa_svc_acct
#export INFA_DEFAULT_DOMAIN_PASSWORD='xQ6OX6O+H0bGqjWwTpW/3Fpy5PZVmXAy8jBvDZogWks='

# Logfile
LOGFILE=$EDC_LOGFILES/Dev_Backup_Script_$currdate.log

# Domain backup file name
DOMAIN_BACKUP_FILE=$EDC_BACKUPDIR/Dev_EDC_Domain_backup_$currdate.mrep

# MRS backup file name
MRS_BACKUP_FILE=$EDC_BACKUPDIR/Dev_MRS_Backup_$currdate.mrep

# EDC/LDM backup file name
EDC_BACKUP_FILE=$EDC_BACKUPDIR/Dev_LDM_Backup_$currdate.zip

#Domain Database JDBC Connect String
JDBC_STRING="jdbc:informatica:sqlserver://ASNAWESTSQLDB01:1433;DatabaseName=INFA_DOM_BIGDATA;SnapshotSerializable=true;allowPortWithNamedInstance=true"

source /home/infaadm/.bash_profile

echo `date +"%Y%m%d%H%M%S"`":INFO:############## S T A R T   B A C K U P  #######################" | tee -a $LOGFILE

cd $EDC_BACKUPDIR 
#This section of code is really for Network Attached Drives to verify the drive is mounted
if [[ $? != "0" ]]
then  
  echo `date +"%Y%m%d%H%M%S"`":WARN: $EDC_BACKUPDIR is not mounted, re-starting autoofs" | tee -a $LOGFILE
  #sudo /sbin/systemctl restart autofs
fi
echo " "
# retest change directory or fail out if autofs folder is not mounted
cd $EDC_BACKUPDIR
if [ $? -ne 0 ]; then
  echo `date +"%Y%m%d%H%M%S"`":FAIL: $EDC_BACKUPDIR is not mounted, Failed restart of autoofs" | tee -a $LOGFILE
  exit 1
fi


################################### Domain Backup ##########################
echo `date +"%Y%m%d%H%M%S"`":INFO: ################## Start Domain Backup ################# " | tee -a $LOGFILE
echo `date +"%Y%m%d%H%M%S"`":INFO: Dev Domain Backup begin on $HOSTNAME  " | tee -a $LOGFILE
cmdtext="infasetup.sh BackupDomain -cs $JDBC_STRING -du sa -dt mssqlserver -bf $DOMAIN_BACKUP_FILE -dn  $DOMAIN"
echo `date +"%Y%m%d%H%M%S"`":INFO: Command: $cmdtext" | tee -a $LOGFILE
infasetup.sh BackupDomain -cs $JDBC_STRING -du sa -dt mssqlserver -bf $DOMAIN_BACKUP_FILE -dn $DOMAIN

if [ $? -ne 0 ];  then
   echo `date +"%Y%m%d%H%M%S"`":FAIL: EDC Dev Domain Backup step failed with error co.de $?" | tee -a $LOGFILE
   exit 1
 else
   echo `date +"%Y%m%d%H%M%S"`":INFO: EDC Dev Domain Backup process completed on $HOSTNAME  " | tee -a $LOGFILE
   echo `date +"%Y%m%d%H%M%S"`":INFO: DOMAIN Backup file created:$DOMAIN_BACKUP_FILE  " | tee -a $LOGFILE
fi

################################### MRS Backup ##########################
echo `date +"%Y%m%d%H%M%S"`":INFO: ################## Start MRS Backup ################# " | tee -a $LOGFILE
echo `date +"%Y%m%d%H%M%S"`":INFO: Dev MRS Backup begin on $HOSTNAME  " | tee -a $LOGFILE
echo `date +"%Y%m%d%H%M%S"`":INFO: Dev MRS Backup File Name :  $MRS_BACKUP_FILE" | tee -a $LOGFILE

cmdtext="infacmd.sh mrs backupcontents -dn $Domain -un $INFA_DEFAULT_DOMAIN_USER -sn $MRS -of $MRS_BACKUP_FILE"
echo `date +"%Y%m%d%H%M%S"`":INFO: Command: $cmdtext" | tee -a $LOGFILE
infacmd.sh mrs backupcontents -dn $DOMAIN -un $INFA_DEFAULT_DOMAIN_USER -sn $MRS -of $MRS_BACKUP_FILE

if [ $? -ne 0 ];  then
        echo `date +"%Y%m%d%H%M%S"`":FAIL: MRS Backup step failed with error code $?" | tee -a $LOGFILE
        exit 1
else
        echo `date +"%Y%m%d%H%M%S"`":INFO: MRS Backup step completed on $HOSTNAME  " | tee -a $LOGFILE
        echo `date +"%Y%m%d%H%M%S"`":INFO: MRS Backup file created: $MRS_BACKUP_FILE  " | tee -a $LOGFILE
fi

################################### Catalog Service Backup ##########################
echo `date +"%Y%m%d%H%M%S"`":INFO: ################## Start Catalog Service Backup ################# " | tee -a $LOGFILE
echo `date +"%Y%m%d%H%M%S"`":INFO: Dev EDC Catalog backup begin on $HOSTNAME  " | tee -a $LOGFILE
echo `date +"%Y%m%d%H%M%S"`":INFO: EDC File Name :  $EDC_BACKUP_FILE" | tee -a $LOGFILE

cmdtext="$INFA_HOME/isp/bin/infacmd.sh ldm BackupContents -dn $DOMAIN -un $INFA_DEFAULT_DOMAIN_USER -sdn Native -sn $EDC_SVC_NM -of $EDC_BACKUP_FILE"
echo `date +"%Y%m%d%H%M%S"`":INFO: Command: $cmdtext" | tee -a $LOGFILE

$INFA_HOME/isp/bin/infacmd.sh ldm BackupContents -dn $DOMAIN -un $INFA_DEFAULT_DOMAIN_USER -sdn Native -sn $EDC_SVC_NM -of $EDC_BACKUP_FILE

export Ret_Cd=$?
echo "Ret Cd right after infacmd.sh " $Ret_Cd 

if [ $Ret_Cd -ne 0 ];  then
        echo `date +"%Y%m%d%H%M%S"`":FAIL: EDC Catalog backup process failed with error code $Ret_Cd" |tee -a $LOGFILE
        #mv $EDC_BACKUP_FILE $EDC_BACKUP_FILE_SHARED
        #echo "Ret cd after move:" $?
        exit 1
else
        echo `date +"%Y%m%d%H%M%S"`":INFO: EDC Catalog service backup process completed on $HOSTNAME  " | tee -a $LOGFILE
        echo `date +"%Y%m%d%H%M%S"`":INFO: EDC Catalog service backup file created:$EDCBACKUPFILE  " | tee -a $LOGFILE
        #mv $EDC_BACKUP_FILE $EDC_BACKUP_FILE_SHARED
        #echo "Ret cd after move:" $?
fi


echo `date +"%Y%m%d%H%M%S"`":INFO: EDC Backup process completed on $HOSTNAME  " | tee -a $LOGFILE
echo "############################################################################" | tee -a $LOGFILE

