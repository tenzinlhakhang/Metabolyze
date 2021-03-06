

# increase output width
options(width = 120)
# print warnings as they occur
options(warn = 1)
# java heap size
options(java.parameters = "-Xmx8G")

# relevent arguments


args = commandArgs(trailingOnly=TRUE)


counts_table_file <- 'Intensity.detected.values.csv'
groups_table_file <- 'Groups.csv'

library('glue')


message(" ========== import inputs ========== ")

# import counts table
counts_table = read.csv(counts_table_file,check.names = F,row.names = 1)

message("input counts table gene num:      ", nrow(counts_table))
message("input counts table sample num:    ", ncol(counts_table))
message("input counts table sample names:  ", toString(colnames(counts_table)))
message("")

# import groups table
groups_table = read.csv(file = groups_table_file, header = TRUE, row.names = 1, colClasses = "factor")
message("sample groups table sample num:   ", nrow(groups_table))
message("sample groups table sample names: ", toString(rownames(groups_table)))
message("sample groups table group names:  ", toString(colnames(groups_table)))
message("")

# check that all samples from the groups table are found in the counts table
diff_samples = setdiff(rownames(groups_table), colnames(counts_table))
if (length(diff_samples)) stop("some samples not in counts table: ", toString(diff_samples))

# subset to samples in groups table (also sets samples to be in the same order)
counts_table = counts_table[, rownames(groups_table)]
message("subset counts table gene num:     ", nrow(counts_table))
message("subset counts table sample num:   ", ncol(counts_table))
message("")

# group info (use the first column for grouped comparisons)
group_name = colnames(groups_table)[1]
patient_name = colnames(groups_table)[2]

message("group name: ", group_name)
message("covariate name: ",patient_name)

group_levels = levels(groups_table[, group_name])
patient_levels = levels(groups_table[,patient_name])
message("group levels: ", toString(group_levels))
message("patient levels: ", toString(patient_levels))


message("")

# design formula
design_formula = formula(glue("~{patient_name} + {group_name}"))
if (length(group_levels) == 1) { design_formula = formula("~ 1") }
message("design formula: ", design_formula)

message(" ========== normalize ========== ")

library('DESeq2')
# import raw counts and create DESeq object

counts_table_rounded <- round(counts_table)
# since v1.16 (11/2016), betaPrior is set to FALSE and shrunken LFCs are obtained afterwards using lfcShrink
dds = DESeqDataSetFromMatrix(countData = counts_table_rounded, colData = groups_table, design = design_formula)
dds = DESeq(dds, betaPrior = TRUE, parallel = FALSE)


resultsNames(dds)
library('stringr')

comparison_level_top = levels(groups_table$Group)[1]
comparison_top = paste('Group',levels(groups_table$Group)[1])
comparison_top = str_replace_all(string=comparison_level_top, pattern=" ", repl="")

comparison_level_base = levels(groups_table$Group)[2]
comparison_top = paste('Group',levels(groups_table$Group)[2])
comparison_base = str_replace_all(string=comparison_level_base, pattern=" ", repl="")

resultsNames(dds)

results_1<- results(dds, contrast=list(comparison_top,comparison_base))
results_2 <- results(dds, contrast=list(comparison_base,comparison_top))


results_directory = paste('Adjusted-','DME-results-',nrow(groups_table),'-Samples')
results_directory <- str_replace_all(string=results_directory, pattern=" ", repl="")


result_1_outname = paste(results_directory,'/','Adjusted.',comparison_level_top,'_vs_',comparison_level_base,'.csv')
result_1_outname = str_replace_all(string=result_1_outname, pattern=" ", repl="")

result_2_outname = paste(results_directory,'/','Adjusted.',comparison_level_base,'_vs_',comparison_level_top,'.csv')
result_2_outname = str_replace_all(string=result_2_outname, pattern=" ", repl="")


write.csv(results_1,result_1_outname)
write.csv(results_2,result_2_outname)




