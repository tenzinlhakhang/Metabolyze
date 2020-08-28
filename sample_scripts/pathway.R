suppressMessages(library('MetaboAnalystR',quietly = TRUE))
suppressMessages(library('filesstrings',quietly = TRUE))
args = commandArgs(trailingOnly=TRUE)
suppressMessages(library('pathview'))
suppressMessages(library('tidyr'))
suppressMessages(library('dplyr'))


setwd(args[1])

output_path = args[2]
files <- list.files(pattern = "\\corrected.csv")

comparison_full <- read.csv(files[1])

full_tmp.vec <- comparison_full$Metabolite

# Create mSetObj for storing objects created during your analysis
full_mSet<-InitDataObjects("conc", "pathora", FALSE)

# Set up mSetObj with the list of compounds
full_mSet<-Setup.MapData(full_mSet, full_tmp.vec);

# Cross reference list of compounds against libraries (hmdb, pubchem, chebi, kegg, metlin)
full_mSet<-CrossReferencing(full_mSet, "name");

full_mSet<-CreateMappingResultTable(full_mSet);

#mSet<-GetCandidateList(mSet);

# Select the pathway library, ranging from mammals to prokaryotes
full_mSet<-SetKEGG.PathLib(full_mSet, "hsa",lib.version='current')

# Set the metabolite filter
full_mSet<-SetMetabolomeFilter(full_mSet, F);

# kegg_compounds <- print.data.frame(data.frame(full_mSet$dataSet$map.table), 
#                                    quote=FALSE)
kegg_compounds <- as.data.frame(full_mSet$dataSet$map.table)
colnames(kegg_compounds)[2] <- 'Metabolite'


kegg_compounds <- kegg_compounds[!(is.na(kegg_compounds$KEGG) | kegg_compounds$KEGG==""), ]
kegg_compounds <- kegg_compounds[!duplicated(kegg_compounds$KEGG),]

### get kegg pathway name from hsa id


#test <- keggGet(c("hsa00785"))
#test[[1]]$PATHWAY_MAP


perform_pathways <- function(file){
  
  comparison_full <- read.csv(file)
  comparison <- comparison_full[ which(comparison_full$ttest_pval < 0.05), ]
  
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
  mSet<-SetKEGG.PathLib(mSet, "hsa",lib.version='current')
  
  # Set the metabolite filter
  mSet<-SetMetabolomeFilter(mSet, F);
  
  # Calculate the over representation analysis score, here we selected to use the hypergeometric test (alternative is Fisher's exact test)
  # A results table "pathway_results.csv" will be created and found within your working directory
  mSet<-CalculateOraScore(mSet, "rbc", "hyperg")
  
  mSet_compounds <- mSet$analSet$ora.mat
  # subset significant pathways
  
  pathway_df <- as.data.frame(mSet_compounds)
  colnames(pathway_df)[6] <- 'HolmAdjusted'
  sig_pathways <- row.names(pathway_df[ which(pathway_df$'HolmAdjusted' < 0.05), ])
  
  
  
  # Convert Full List of Metabolites to corresponding Kegg IDS

  
  
  #get compound names



  merged <- merge(comparison_full,kegg_compounds,on='Metabolite')
  merged <- subset(merged,Log2FoldChange!=0)
  
  library('dplyr')
  pathway_input <- merged %>%
  select(KEGG, Log2FoldChange)

  row.names(pathway_input) <- pathway_input$KEGG
  pathway_input$KEGG <- NULL


  colnames(pathway_input) <- c('FC')

  output_name <- paste(file,'.pathway.csv')
  
  output_name = gsub(".corrected.csv ", "", output_name, fixed = TRUE)
  
  plot_kegg <- function(hsa){
  	pv.out <- pathview(cpd.data = pathway_input, gene.idtype = "KEGG", 
					   pathway.id = hsa, species = 'hsa', out.suffix = 'kegg', keys.align = "y", 
					   kegg.native = T, match.data = T, key.pos = "topright",low = list(gene = "green", cpd = "blue"), mid =
					     list(gene = "gray", cpd = "gray"), high = list(gene = "yellow", cpd ="red"))
	kegg_plot_name <- paste(hsa,'.kegg.png')
  	kegg_plot_name = gsub(" ", "", kegg_plot_name, fixed = TRUE)
    kegg_plot_final_name = paste(file,'.',kegg_plot_name)
    file.rename(kegg_plot_name,kegg_plot_final_name )
  	file.move(kegg_plot_final_name,output_path)
  	file.remove(paste(hsa,'.xml',sep = ""))
  	file.remove(paste(hsa,'.png',sep = ""))

  }

  lapply(sig_pathways,plot_kegg)
  file.rename('pathway_results.csv',output_name )
  file.move(output_name,output_path)
  

  }

}


message(" ========== Performing Pathway Analysis ========== ")

bar <- function(x) tryCatch(perform_pathways(x), error = function(e) e)

lapply(files,bar)

file.remove('hsa.rda')
file.remove('syn_nms.rds')
file.remove('name_map.csv')
file.remove('compound_db.rds')

message(" ========== Pipeline Finished ========== ")


