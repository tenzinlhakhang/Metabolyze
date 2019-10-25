library('MetaboAnalystR',quietly = TRUE)
library('filesstrings',quietly = TRUE)
args = commandArgs(trailingOnly=TRUE)

setwd(args[1])

output_path = args[2]
files <- list.files(pattern = "\\corrected.csv")


perform_pathways <- function(file){
  
  comparison <- read.csv(file)
  comparison <- comparison[ which(comparison$ttest_pval < 0.05), ]
  
  if (nrow(comparison) == 0) {
  print('No Significant Metabolites Detected')
  } else {
  tmp.vec <- comparison$Metabolite
  
  # Create mSetObj for storing objects created during your analysis
  mSet<-InitDataObjects("conc", "pathora", FALSE)
  
  # Set up mSetObj with the list of compounds
  mSet<-Setup.MapData(mSet, tmp.vec);
  
  # Cross reference list of compounds against libraries (hmdb, pubchem, chebi, kegg, metlin)
  mSet<-CrossReferencing(mSet, "name");
  
  mSet<-CreateMappingResultTable(mSet);
  
  #mSet<-GetCandidateList(mSet);
  
  # Select the pathway library, ranging from mammals to prokaryotes
  mSet<-SetKEGG.PathLib(mSet, "hsa")
  
  # Set the metabolite filter
  mSet<-SetMetabolomeFilter(mSet, F);
  
  # Calculate the over representation analysis score, here we selected to use the hypergeometric test (alternative is Fisher's exact test)
  # A results table "pathway_results.csv" will be created and found within your working directory
  mSet<-CalculateOraScore(mSet, "rbc", "hyperg")
  
  
  output_name <- paste(file,'.pathway.csv')
  
  output_name = gsub(".corrected.csv ", "", output_name, fixed = TRUE)
  
  
  file.rename('pathway_results.csv',output_name )
  file.move(output_name,output_path)
  
  }

}


message(" ========== Performing Pathway Analysis ========== ")


lapply(files,perform_pathways)

file.remove('hsa.rda')
file.remove('syn_nms.rds')
file.remove('name_map.csv')
file.remove('compound_db.rds')

message(" ========== Pipeline Finished ========== ")

