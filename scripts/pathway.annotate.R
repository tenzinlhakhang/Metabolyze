library('MetaboAnalystR')
library('KEGGREST')
args = commandArgs(trailingOnly=TRUE)

print(args[1])
comparison <- read.csv(args[1])
comparison <- comparison[ which(comparison$ttest_pval < 0.05), ]

tmp.vec <- comparison$Metabolite
print(tmp.vec)

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


# Plot of the Pathway Analysis Overview 
pathway_list = list()
#kegg_hsa_list = list()


hsa_values <- row.names((mSet$analSet$ora.mat))

  
get_metabolites <- function(hsa){
  metabolites <- paste(unlist(names(mSet$analSet$ora.hits[[hsa]])),collapse=',')

  print(metabolites)
}

metabolite_list <- lapply(hsa_values, get_metabolites)
names(metabolite_list) <- hsa_values
#try(keggGet('hsa00460'))
metabolite_df <- as.data.frame(t(as.data.frame(metabolite_list)))
metabolite_df$Pathway <- row.names(metabolite_df)
colnames(metabolite_df) <- c('Metabolite','Pathway')


matrix <- as.data.frame(mSet$analSet$ora.mat)
matrix$Pathway <- row.names(matrix)

#combined <- cbind(big_data,kegg_data)
#row.names(combined) <- combined$KeggID
original <- read.csv('pathway_results.csv',check.names=F)

cbinded_matrix <- cbind(matrix,original)

merged <- merge(cbinded_matrix,metabolite_df,on='row.name')


output_name <- paste(args[1],'.pathway.csv')

output_name = gsub(".corrected.csv ", "", output_name, fixed = TRUE)

write.csv(merged,output_name)

file.remove('pathway_results.csv')
