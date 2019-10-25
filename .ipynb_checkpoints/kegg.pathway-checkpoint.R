library(pathview)
metabolite.data <- data.frame(FC = sim.mol.data(mol.type = "cpd", nmol = 3000))
head(metabolite.data)

test <- read.csv('kegg.id.final.csv',check.names = F)
row.names(test) <- test$`Kegg ID`
test$`Kegg ID` <- NULL
colnames(test) <- 'FC'
metabolite.data <- test

organism <- "Homo sapiens"
matches <- unlist(sapply(1:ncol(korg), function(i) {
  agrep(organism, korg[, i])
}))
(kegg.code <- korg[matches, 1, drop = F])

library(KEGGREST)
pathways <- keggList("pathway", kegg.code)
head(pathways)


library(pathview)
map <- gsub("path:", "", names(pathways)[2])  # remove 'path:'
pv.out <- pathview(cpd.data = metabolite.data, gene.idtype = "KEGG", 
                   pathway.id = map, species = kegg.code, out.suffix = map, keys.align = "y", 
                   kegg.native = T, match.data = T, key.pos = "topright")
?pathview
plot.name <- paste(map, map, "png", sep = ".")

(pv.out)




