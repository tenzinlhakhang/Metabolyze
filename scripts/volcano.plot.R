library('manhattanly',quietly=TRUE,warn.conflicts = FALSE)

args = commandArgs(trailingOnly=TRUE)

input_split <- strsplit(args[1], "\\/")[[1]]
# Create environment variables

directory <- input_split[1]

file_name <- input_split[3]

x <- args[1]
result <- read.csv(x,check.names = F)

colnames(result)[which(names(result) == "ttest_pval")] <- "P"
colnames(result)[which(names(result) == "Log2FoldChange")] <- "EFFECTSIZE"
result <- result[complete.cases(result), ]
#result$EFFECTSIZE <- log2(result$EFFECTSIZE)
volcano <- volcanoly(result, snp = "Metabolite", gene = "Formula",genomewideline = -log10(0.05),xlab = 'log2FC',ylab='-log10(p)')

setwd(directory)
setwd('Volcano')


title = paste(file_name,'.volcano.html')
title = gsub(" ", "", title, fixed = TRUE)
title = gsub(".csv", "", title, fixed = TRUE)

dir_to_remove = gsub(".html", "", title, fixed = TRUE)
dir_to_remove = paste(dir_to_remove,'_files')
dir_to_remove = gsub(" ", "", dir_to_remove, fixed = TRUE)



htmlwidgets::saveWidget(volcano,file = title,selfcontained=FALSE)
#unlink(dir_to_remove, recursive=TRUE)

setwd('..')
setwd('..')

