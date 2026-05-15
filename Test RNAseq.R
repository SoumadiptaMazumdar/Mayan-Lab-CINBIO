R.version.string
install.packages("BiocManager")
BiocManager::install(c(
"DESeq2",
"EnhancedVolcano",
"pheatmap",
"clusterProfiler",
"org.Hs.eg.db",
"msigdbr",
"apeglm"
))
library(DESeq2)
library(EnhancedVolcano)
library(pheatmap)
library(org.Hs.eg.db)
library(EnhancedVolcano)
install.packages("tidyverse")
library(tidyverse)
setwd("~/Downloads")
list.files()
counts <- read.csv("test_RNAseq_counts.csv", row.names = 1)
metadata <- read.csv("test_RNAseq_metadata.csv")
head(counts)
metadata
rownames(metadata) <- metadata$sample
counts <- counts[, rownames(metadata)]
metadata$condition <- factor(
metadata$condition,
levels = c("WT", "CX43")
)
dds <- DESeqDataSetFromMatrix(
countData = counts,
colData = metadata,
design = ~ condition
)
dds <- dds[rowSums(counts(dds)) > 10, ]
dds <- DESeq(dds)
res <- results(
dds,
contrast = c("condition", "CX43", "WT")
)
res <- as.data.frame(res)
res$gene <- rownames(res)
head(res)
EnhancedVolcano(
res,
lab = res$gene,
x = "log2FoldChange",
y = "padj",
title = "CX43 vs WT melanoma EV RNAseq",
pCutoff = 0.05,
FCcutoff = 1
)
vsd <- vst(dds, blind = FALSE)
vsd <- varianceStabilizingTransformation(dds, blind = FALSE)
plotPCA(vsd, intgroup = "condition")
lipid_genes <- c(
"FASN","ACACA","SCD","ELOVL6",
"FADS2","CPT1A","ACOX1",
"HMGCR","HMGCS1","SQLE",
"SREBF1","SREBF2",
"CHKA","PCYT1A","PLA2G4A",
"SPTLC1","CERS5","SGMS1",
"CD36","FABP5","ABCA1","PPARG"
)
lipid_genes_present <- intersect(lipid_genes, rownames(vsd))
mat <- assay(vsd)[lipid_genes_present, ]
mat <- mat - rowMeans(mat)
pheatmap(
mat,
annotation_col = metadata["condition"],
fontsize_row = 8,
main = "Lipid metabolism genes"
)
write.csv(
res_sorted,
"CX43_vs_WT_DEGs.csv",
row.names = FALSE
)
res_sorted <- res[order(res$padj), ]
head(res_sorted)
sig_genes <- subset(
res_sorted,
padj < 0.05
)
head(sig_genes)
lipid_res <- subset(
res_sorted,
gene %in% lipid_genes
)
lipid_res
write.csv(
lipid_res,
"lipid_metabolism_results.csv",
row.names = FALSE
)
write.csv(
res_sorted,
"CX43_vs_WT_full_DESeq2_results.csv",
row.names = FALSE
)
BiocManager::install(c(
"DOSE",
"enrichplot"
))
getwd()
list.files()
list.files(pattern = "\\.R$")
find ~ -name "*.R"

