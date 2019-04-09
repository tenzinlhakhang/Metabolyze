#!/usr/bin/env Rscript
#sink("/dev/null")


#repos='http://cran.us.r-project.org'
#list.of.packages <- c("pheatmap", "string")
#new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
#if(length(new.packages)) install.packages(new.packages)

library('pheatmap',quietly=TRUE,warn.conflicts = FALSE)

args = commandArgs(trailingOnly=TRUE)


# Generate Heatmap for each corrected comparison using different pvalue cutoffs
comparison <- args[1]
pvalue <- 0.05
param <- as.logical(toupper(args[3]))

#print(args[3])

heatmap <- function(comparison,pvalue,param){
  
  #Directory name 
  directory <- strsplit(comparison, "\\/")[[1]]
  comparison_name <- directory[3]
  directory <- directory[1]
  
  counts <-read.csv(comparison,check.names = F)
  # Two Way Comparison Heatmap
  counts <- counts[!(is.na(counts$ttest_pval) | counts$ttest_pval=="-"), ]
  #counts$ttest_pval <- as.numeric(levels(counts$ttest_pval))[counts$ttest_pval]
  counts <- counts[ which(counts$ttest_pval < 0.05), ]
  
  colnames(counts)[which(names(counts) == "RT.Start..min.")]  <- 'Delete'
  
  # remove std counts
  
  require(dplyr)
  
  
  
  ## Heatmap Color Annotations
  getwd()
  sampleTable <- read.csv('inputs/Groups.csv',header=T)
  sampleTable <- sampleTable %>% 
    filter(Group != "Blank")
  columns.interest <- c('id','Group')
  
  
  
  
  sampleTable <- sampleTable[,columns.interest]
  sampleTable <- as.data.frame(sampleTable)
  sampleTable$id   <- sampleTable$id
  #sampleTable$id <- gsub(".mzXML", "", paste(sampleTable$id))
  
  colnames(sampleTable)<- c('File','Condition')
  col_anno <- as.data.frame(sampleTable$Condition)
  names(col_anno) <- c('Condition')
  row.names(col_anno)<- sampleTable$File
  
  columns.interest <- c('Metabolite',row.names(col_anno))
  counts <- counts[, which(names(counts) %in% columns.interest)]
  head(counts)
  
  row.names(counts) <- counts$Metabolite
  counts$Metabolite <- NULL
  
  
  x=apply( counts, 1, sd ) 
  df =as.data.frame(x)
  df$gene = row.names(df)
  head(df)
  
  datasetnew <- df[df$x>0,]
  colnames(datasetnew) <- c('std','metabolite')
  
  counts$metabolite <- row.names(counts)
  merged <- merge(counts,datasetnew,on='metabolite')
  row.names(merged) <- merged$metabolite
  
  merged$metabolite <- NULL
  merged$std <- NULL
  
  
  title = paste(length(colnames(merged)), 'x' ,nrow(merged))
  title= gsub(" ", "", title, fixed = TRUE)
  
  
  # Set heatmap colors
  
  cell_colors = colorRampPalette(c("#043177", "#244B88", "#FAFAFA",
                                   "#C62E2E", "#BF0F0F"))(50)
  
  
  
  
  pdf_name = paste(directory,'/Heatmap/plot.heatmap.',as.character(pvalue),'.',
                   as.character(comparison_name),'.',title,'.pdf')
  pdf_name = gsub(" ", "", pdf_name, fixed = TRUE)
  pdf(pdf_name)
  

  
  pheatmap(as.matrix(merged), color = cell_colors,
           border_color = NA,show_rownames = param,fontsize = 6, 
           scale = "row", cluster_rows = T,
           main = title,annotation_col = col_anno, 
           cluster_cols = T, 
           fontsize_col = 10, width = 12, height = 8)
  

  garbage <- dev.off()
  metabolites_sig = row.names(merged)
  
  # Plot with all samples
  
  
  full_counts_path = paste(directory,'/Tables/Intensity.values.csv')
  full_counts_path = gsub(" ", "", full_counts_path, fixed = TRUE)
  full_counts = read.csv(full_counts_path,check.names=FALSE)
  
  library(dplyr,quietly=TRUE,warn.conflicts=FALSE)
  
  full_counts <- full_counts %>% filter(Metabolite %in% metabolites_sig)
  row.names(full_counts) <- full_counts$Metabolite
  full_counts$Metabolite <- NULL
  nrow(full_counts)
  if(length(colnames(full_counts)) == length(colnames(merged))){
    print ("Only Two Group Comparison")
  } else {
    
    
    # Remove metabolites where zero is found in 50% of all samples or greater
    # threshold = round(length(colnames(full_counts))/2)
    # full_counts = full_counts[apply(full_counts, 1, FUN = function(x){sum(x == 0)}) < threshold,]
    
    title_all = paste(length(colnames(full_counts)), 'x' ,nrow(full_counts))
    title_all = gsub(" ", "", title_all, fixed = TRUE)
    
    pdf_name_full = paste(directory,'/Heatmap/plot.heatmap.',as.character(pvalue),'.',
                          as.character(comparison_name),'.',title_all,'.pdf')
    pdf_name_full = gsub(" ", "", pdf_name_full, fixed = TRUE)
    pdf(pdf_name_full)
    # two group heatmap
    pheatmap(full_counts, color = cell_colors,
             border_color = NA,show_rownames = param,fontsize = 6, 
             scale = "row", cluster_rows = T,
             main = title_all,annotation_col = col_anno, 
             cluster_cols = T, 
             fontsize_col = 10, width = 12, height = 8)
    
    garbage <- dev.off()
    
    
  }
  
  
  
  
}


heatmap(comparison,pvalue,param)
