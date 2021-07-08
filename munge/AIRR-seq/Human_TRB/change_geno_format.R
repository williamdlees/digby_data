library(stringr)
library(dplyr)
library(plyr)
library(tidyr)


DS1_geno_path <- "DS1/genotypes/"
DS1_geno_files <- list.files(path=DS1_geno_path)

for (geno_file in DS1_geno_files) {
  geno <- read.csv(paste0(DS1_geno_path, geno_file), sep = "\t", stringsAsFactors = F)
  names(geno)[1:10] <- tolower(names(geno)[1:10])
  geno$Freq_by_Clone <- geno$counts
  temp_multi_alleles <- geno[grepl(",", geno$Freq_by_Clone),]
  geno$Freq_by_Clone[grepl(",", geno$Freq_by_Clone)] <- unlist(lapply(1:nrow(temp_multi_alleles), function(i){
    num_of_alleles <- str_count(temp_multi_alleles$GENOTYPED_ALLELES[i], ",") + 1;
    seq_num <- unlist(lapply(strsplit(temp_multi_alleles$Freq_by_Clone[i], ","), "[", 1:num_of_alleles));
    return(paste(seq_num, collapse = ";"))
  }))
  # geno$Freq_by_Clone[grepl("TRBV", geno$gene)] <- geno$total[grepl("TRBV", geno$gene)] / sum(geno$total[grepl("TRBV", geno$gene)]) 
  # geno$Freq_by_Clone[grepl("TRBD", geno$gene)] <- geno$total[grepl("TRBD", geno$gene)] / sum(geno$total[grepl("TRBD", geno$gene)]) 
  # geno$Freq_by_Clone[grepl("TRBJ", geno$gene)] <- geno$total[grepl("TRBJ", geno$gene)] / sum(geno$total[grepl("TRBVJ", geno$gene)]) 
  geno$Freq_by_Seq <- geno$Freq_by_Clone
  write.table(geno, file = paste0(DS1_geno_path,  geno_file),quote = F,row.names = F,sep = "\t")
}


DS2_geno_path <- "DS2/genotypes/"
DS2_geno_files <- list.files(path=DS2_geno_path)

for (geno_file in DS2_geno_files) {
  geno <- read.csv(paste0(DS2_geno_path, geno_file), sep = "\t", stringsAsFactors = F)
  names(geno)[1:10] <- tolower(names(geno)[1:10])
  geno$Freq_by_Clone <- geno$counts
  temp_multi_alleles <- geno[grepl(",", geno$Freq_by_Clone),]
  geno$Freq_by_Clone[grepl(",", geno$Freq_by_Clone)] <- unlist(lapply(1:nrow(temp_multi_alleles), function(i){
    num_of_alleles <- str_count(temp_multi_alleles$GENOTYPED_ALLELES[i], ",") + 1;
    seq_num <- unlist(lapply(strsplit(temp_multi_alleles$Freq_by_Clone[i], ","), "[", 1:num_of_alleles));
    return(paste(seq_num, collapse = ";"))
  }))
  # geno$Freq_by_Clone[grepl("TRBV", geno$gene)] <- geno$total[grepl("TRBV", geno$gene)] / sum(geno$total[grepl("TRBV", geno$gene)]) 
  # geno$Freq_by_Clone[grepl("TRBD", geno$gene)] <- geno$total[grepl("TRBD", geno$gene)] / sum(geno$total[grepl("TRBD", geno$gene)]) 
  # geno$Freq_by_Clone[grepl("TRBJ", geno$gene)] <- geno$total[grepl("TRBJ", geno$gene)] / sum(geno$total[grepl("TRBVJ", geno$gene)]) 
  geno$Freq_by_Seq <- geno$Freq_by_Clone
  write.table(geno, file = paste0(DS2_geno_path,  geno_file),quote = F,row.names = F,sep = "\t")
}


DS3_geno_path <- "DS3/genotypes/"
DS3_geno_files <- list.files(path=DS3_geno_path)

for (geno_file in DS3_geno_files) {
  geno <- read.csv(paste0(DS3_geno_path, geno_file), sep = "\t", stringsAsFactors = F)
  names(geno)[1:10] <- tolower(names(geno)[1:10])
  geno$Freq_by_Clone <- geno$counts
  temp_multi_alleles <- geno[grepl(",", geno$Freq_by_Clone),]
  geno$Freq_by_Clone[grepl(",", geno$Freq_by_Clone)] <- unlist(lapply(1:nrow(temp_multi_alleles), function(i){
    num_of_alleles <- str_count(temp_multi_alleles$GENOTYPED_ALLELES[i], ",") + 1;
    seq_num <- unlist(lapply(strsplit(temp_multi_alleles$Freq_by_Clone[i], ","), "[", 1:num_of_alleles));
    return(paste(seq_num, collapse = ";"))
  }))
  # geno$Freq_by_Clone[grepl("TRBV", geno$gene)] <- geno$total[grepl("TRBV", geno$gene)] / sum(geno$total[grepl("TRBV", geno$gene)]) 
  # geno$Freq_by_Clone[grepl("TRBD", geno$gene)] <- geno$total[grepl("TRBD", geno$gene)] / sum(geno$total[grepl("TRBD", geno$gene)]) 
  # geno$Freq_by_Clone[grepl("TRBJ", geno$gene)] <- geno$total[grepl("TRBJ", geno$gene)] / sum(geno$total[grepl("TRBVJ", geno$gene)]) 
  geno$Freq_by_Seq <- geno$Freq_by_Clone
  write.table(geno, file = paste0(DS3_geno_path,  geno_file),quote = F,row.names = F,sep = "\t")
}

DS4_geno_path <- "DS4/genotypes/"
DS4_geno_files <- list.files(path=DS4_geno_path)

for (geno_file in DS4_geno_files) {
  geno <- read.csv(paste0(DS4_geno_path, geno_file), sep = "\t", stringsAsFactors = F)
  names(geno)[1:10] <- tolower(names(geno)[1:10])
  geno$Freq_by_Clone <- geno$counts
  temp_multi_alleles <- geno[grepl(",", geno$Freq_by_Clone),]
  geno$Freq_by_Clone[grepl(",", geno$Freq_by_Clone)] <- unlist(lapply(1:nrow(temp_multi_alleles), function(i){
    num_of_alleles <- str_count(temp_multi_alleles$GENOTYPED_ALLELES[i], ",") + 1;
    seq_num <- unlist(lapply(strsplit(temp_multi_alleles$Freq_by_Clone[i], ","), "[", 1:num_of_alleles));
    return(paste(seq_num, collapse = ";"))
  }))
  # geno$Freq_by_Clone[grepl("TRBV", geno$gene)] <- geno$total[grepl("TRBV", geno$gene)] / sum(geno$total[grepl("TRBV", geno$gene)]) 
  # geno$Freq_by_Clone[grepl("TRBD", geno$gene)] <- geno$total[grepl("TRBD", geno$gene)] / sum(geno$total[grepl("TRBD", geno$gene)]) 
  # geno$Freq_by_Clone[grepl("TRBJ", geno$gene)] <- geno$total[grepl("TRBJ", geno$gene)] / sum(geno$total[grepl("TRBVJ", geno$gene)]) 
  geno$Freq_by_Seq <- geno$Freq_by_Clone
  write.table(geno, file = paste0(DS4_geno_path,  geno_file),quote = F,row.names = F,sep = "\t")
}

