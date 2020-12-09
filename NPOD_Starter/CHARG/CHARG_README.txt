###########################################
#  Papers Past newspaper open data pilot  #
###########################################

#Thank you for downloading this data and participating in our pilot project. If you have any comments, feedback or just want to tell us about what you have done with this data, please email us at paperspast@natlib.govt.nz


############################
#         Metadata         #
############################

#Key metadata fields for this title are included in this file in machine-readable YAML format. A file containing bibliographic data in MARC format is also included to provide additional context. This data is taken from the National Library of New Zealand catalogue (also available in the Publications New Zealand dataset). 


############################
#      Data structure      #
############################

#[Title level folder]  Will be saved under the acronym that Papers Past uses to identify titles e.g. Kumara Times is KUMAT
## - Title.yaml   <- this file
## - Title.mrc  <- The original source for the metadata contained in this file (in MARC format).
#######[Year level folder] Will be a year e.g. 1896
############[Issue level folder] This will be named using the title's acronym and the date in year-month-day format e.g. KUMAT_18960601
############ - mets.xml     There will always be one METS file per issue and 
############ - 0001.xml      one ALTO XML file for every page in the issue.
############ - 0002.xml
############ - 0003.xml
############ - 0004.xml


###########################
#   Further information   #
###########################

#More information on the newspaper open data pilot can be found at:
#https://natlib.govt.nz/about-us/open-data/papers-past-metadata/papers-past-newspaper-open-data-pilot

#Find out more about Papers Past here:
#https://paperspast.natlib.govt.nz/about

#More information on the formats provided can be found at:

#METS Standard: http://www.loc.gov/standards/mets/
#ALTO Standard: https://www.loc.gov/standards/alto/
#What is METS/ALTO?: https://veridiansoftware.com/knowledge-base/metsalto/
#MARC Standards: https://www.loc.gov/marc/


############################
#      Contact us at:      #
############################

#Paperspast@natlib.govt.nz


#########################################
#        Bibliographic metadata        #
#########################################
#This can be extracted quickly using a YAML parser
Title: Charleston argus.
RelationReplacedBy:
- Charleston herald
Publisher: '[Charleston, N.Z. : John Tyrrell],'
Frequency: Semiweekly
DatesOfPublication: Began with vol. 1, no. 1 (March 2, 1867)?; ceased in December
  1867?
Coverage: Charleston (N.Z.)
FormatExtant: v. ; 56 cm
Identifier:
  NLNZalma: '999276783502836'
  OCLC: '946807834'
  DigitalNZ: '38112390'
Subject:
- Charleston (N.Z.) -- Newspapers.
- New Zealand newspapers. local Nz
Rights: No known copyright
Attribution: Papers Past, National Library of New Zealand - https://paperspast.natlib.govt.nz/
PapersPastURL: https://paperspast.natlib.govt.nz/newspapers/charleston-argus
PapersPastAcronym: CHARG

#Note some titles may have multiple bibliographic records but only one has been supplied here.

###################################################################
#  Terms of Use: Papers Past historic newspaper data (1839-1899)  #
###################################################################
#Last updated 17/12/2019

##############################
#            Pilot           #
##############################

#The National Library of New Zealand has released the Papers Past historic newspaper data (1839-1899) dataset (“the dataset”) as a pilot. It will be available for 12 months from the release date. We do not intend to update the data during this period, although we retain the right to remove all or part of the dataset if needed. 
#We are undertaking this pilot because we’d like to know if people are interested in using this data, what the data can be used for, and whether the METS/ALTO format is the best way to make this available. Because this is a pilot, we strongly encourage you to provide feedback about your experience of using the dataset so that we can work to improve the service. 

#Please email us at paperspast@natlib.govt.nz – we look forward to hearing from you. 

#############################
#          Dataset          #
#############################

#Papers Past is a website of historic newspapers, periodicals and other full-text material created by the National Library of New Zealand (https://paperspast.natlib.govt.nz). The digitised newspapers are created from microfilm copies, which are then scanned and OCR’d. As part of this process the metadata, page layout and text are captured in the METS/ALTO files. You can find more about the METS/ALTO standards at https://veridiansoftware.com/knowledge-base/metsalto/
#The dataset consists of METS/ALTO xml files from 78 historic New Zealand newspapers published before 1 January 1900. It does not contain the page images of these newspapers. You can find a list of the titles and date ranges in the dataset at https://natlib.govt.nz/about-us/open-data/papers-past-metadata/papers-past-newspaper-open-data-pilot
#This dataset is a subset of the material available through Papers Past, as not all the data can be made available due to copyright, contractual, or other collection and data management reasons.

#############################
#    Copyright and re-use    #
#############################

#To the best of the Department of Internal Affairs’ knowledge, under New Zealand law:
#    •	Copyright in the material contained within the original newspapers captured in the Papers Past pre-1900 dataset in New Zealand has expired;
#    •	It may be copied and otherwise re-used in New Zealand without copyright related restriction. However, before re-using, users should check the status of any third party intellectual property rights in any of the materials provided.

#############################
#  Attribution  #
#############################

#If you publish, distribute or otherwise disseminate this work to the public without adapting it, the following attribution to the National Library should be used:

#Source: Papers Past, National Library of New Zealand
#Where practicable, please hyperlink the name of Papers Past to https://paperspast.natlib.govt.nz

#If you adapt this work in any way or include it in a collection, and publish, distribute or otherwise disseminate that adaptation or collection to the public, the following attribution to the National Library should be used:

#This [work/product/application/etc] uses data sourced from Papers Past, National Library of New Zealand. 
#Where practicable, please hyperlink the name of Papers Past to https://paperspast.natlib.govt.nz 

##############################
#   Exclusion of liability   #
##############################

#Under no circumstances is the National Library of New Zealand or the Department of Internal Affairs (of which the National Library of New Zealand is part) liable to you, any user or any third party on account of your or that party’s use or misuse of or reliance on the collection.
