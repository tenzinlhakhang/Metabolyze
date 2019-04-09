setwd('/Users/TenzinLhakhang/Desktop/Projects/metabolyze/DME-results-12-Samples/Results/')


counts <- read.csv('Intensity.values.csv')
head(counts)
row.names(counts) <- counts$Metabolite
counts$Metabolite <- NULL

library('pheatmap')


colnames(counts) <- row.names(counts[1:12,])
pdf("test.pdf",width=23,height=6)
par(mfrow=c(2,3))
pheatmap(head(counts,n=1),cluster_rows = F,fontsize_row = 15,fontsize_col = 10,cluster_cols = F)
pheatmap(head(counts,n=1),cluster_rows = F,fontsize_row = 15,fontsize_col = 10,cluster_cols = F)
pheatmap(head(counts,n=1),cluster_rows = F,fontsize_row = 15,fontsize_col = 10,cluster_cols = F)




dev.off()
         
