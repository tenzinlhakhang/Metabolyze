#!/usr/bin/env Rscript
sink("/dev/null")


#repos='http://cran.us.r-project.org'
#list.of.packages <- c("pheatmap", "string")
#new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
#if(length(new.packages)) install.packages(new.packages)

suppressMessages(library('pheatmap',quietly=TRUE,warn.conflicts = FALSE))

args = commandArgs(trailingOnly=TRUE)


# directory <- strsplit(directory, "\\/")[[1]]
# directory <- directory[1]

directory <- strsplit(args, "\\/")[[1]]
directory <- directory[1]


full_counts <- read.csv((args[1]),check.names=FALSE)
row.names(full_counts) <- full_counts$Metabolite
full_counts$Metabolite <- NULL

std=apply( full_counts, 1, sd ) 
df =as.data.frame(std)
df$gene = row.names(df)
head(df)

datasetnew <- df[df$std>0,]
colnames(datasetnew) <- c('std','metabolite')

full_counts$metabolite <- row.names(full_counts)
merged <- merge(full_counts,datasetnew,on='metabolite')
row.names(merged) <- merged$metabolite

merged$metabolite <- NULL
merged$std <- NULL

head(merged)

nrow(merged)
#idx <- which(apply(full_counts[,-1], 1, function(x) all(x == 0)) == T)
#ull_counts <- full_counts[-idx,]

cell_colors = colorRampPalette(c("#043177", "#244B88", "#FAFAFA",
                                 "#C62E2E", "#BF0F0F"))(50)


# color annotations
sampleTable <- read.csv('inputs/Groups.csv',header=T)

sampleTable <- sampleTable[which(sampleTable$Group != 'Blank'),]

subset_color <- sampleTable[!duplicated(sampleTable[c("Group","Color")]),]

columns.interest <- c('id','Group')
sampleTable <- sampleTable[,columns.interest]
sampleTable <- as.data.frame(sampleTable)
sampleTable$id   <- sampleTable$id
#sampleTable$id <- gsub(".mzXML", "", paste(sampleTable$id))

colnames(sampleTable)<- c('File','Condition')
col_anno <- as.data.frame(sampleTable$Condition)
names(col_anno) <- c('Condition')
row.names(col_anno)<- sampleTable$File


Color <- as.character(subset_color$Color)
names(Color) <- as.character(subset_color$Group)
ann_color <- list(Color)
names(ann_color) <- 'Condition'

title = paste(length(colnames(merged)), 'x' ,nrow(merged))
title= gsub(" ", "", title, fixed = TRUE)

title.string <- as.character(args[2])
pdf_name = paste(directory,'/Heatmap/plot.heatmap.expressed.metabolite.',title.string, '.',title,'.pdf')
pdf_name = gsub(" ", "", pdf_name, fixed = TRUE)
pdf(pdf_name)
if (nrow(merged) > 200){row_name_toggle <- FALSE} else { row_name_toggle <- FALSE}
pheatmap(as.matrix(merged), color = cell_colors,
         border_color = NA,show_rownames=row_name_toggle,fontsize = 6, 
         scale = "row", cluster_rows = T,annotation_colors = ann_color,
         main = title,annotation_col = col_anno, 
         cluster_cols = T, 
         fontsize_col = 10, width = 12, height = 8)

garbage <- dev.off()

