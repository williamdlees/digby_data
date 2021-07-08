library(stringr)
library(dplyr)
library(plyr)
library(tidyr)


DS2_geno_path <- "DS2/genotypes/"
DS2_geno_files <- list.files(path=DS2_geno_path)

for (geno_file in DS2_geno_files) {
  geno <- read.csv(paste0(DS2_geno_path, geno_file), sep = "\t", stringsAsFactors = F)
  geno <- geno[grepl("TRB", geno$gene),]
  write.table(geno, file = paste0(DS2_geno_path,  geno_file),quote = F,row.names = F,sep = "\t")
}


DS2_haplo_path <- "DS2/haplotypes/"
DS2_haplo_files <- list.files(path=DS2_haplo_path)

for (haplo_file in DS2_haplo_files) {
  haplo <- read.csv(paste0(DS2_haplo_path, haplo_file), sep = "\t", stringsAsFactors = F)
  haplo <- haplo[grepl("TRB", haplo$gene),]
  write.table(haplo, file = paste0(DS2_haplo_path,  haplo_file),quote = F,row.names = F,sep = "\t")
}

