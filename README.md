# ROR1-EGFR Coexpression & RNA-Protein-Dropout-Analyse

## Status (Stand: 12.09.2017)

## Offene Aufgabe: RNA-seq-Rohdaten-Download
Ziel: Korrelationsanalyse zwischen ROR1/EGFR-Koexpression und 1) EMT ()definiert durch MSigDB und 2) Brust-Krebs-Stamm-Zell Faktor (definiert durch Genset)
Offenes Ziel:
Mit Lee et al prüfen, ob ROR1 einen ungewöhnlich großen RNA-Protein-Dropout zeigt
(verglichen mit anderen Genen), unter Nutzung der Rohdaten von
NCBI BioProject **PRJNA1422844** (RNA-seq der TNBC-Patientenkohorte) sowie Proteome.

### Pipeline (Skripte in diesem Repo)
- 'Three-Proteome.ipynb' - holt Proteome Tabellen von drei Papern:
    -Kosok et al:Kosok M, Alli-Shaik A, Bay BH, Gunaratne J. 
        Comprehensive Proteomic Characterization Reveals Subclass-Specific Molecular Aberrations within Triple-negative Breast Cancer. iScience. 2020 Feb 21;23(2):100868. doi: 10.1016/j.isci.2020.100868. Epub 2020 Jan 28. PMID: 32058975; PMCID: PMC7015993.
    -Lee et al: Lee DK, Kim MH, Hwang Y, Kim SG, Ryu WJ, Kim GU, Yun HM, Park S, Lee JD, Han HJ, Kim GM, Kim KH, Park JB, Kim MJ, Koo JS, Kim JY, Park HS, Kim SI, Gee HY, Park S, Sohn J.
        Proteogenomic decoding of chemotherapy resistance in patients with triple-negative breast cancer. Genome Biol. 2026 Apr 14;27(1):125. doi: 10.1186/s13059-026-04053-7. PMID: 41975515; PMCID: PMC13077823.
    -Anurag et al: Anurag M, Jaehnig EJ, Krug K, Lei JT, Bergstrom EJ, Kim BJ, Vashist TD, Huynh AMT, Dou Y, Gou X, Huang C, Shi Z, Wen B, Korchina V, Gibbs RA, Muzny DM, Doddapaneni H, Dobrolecki LE, Rodriguez H, Robles AI, Hiltke T, Lewis MT, Nangia JR, Nemati Shafaee M, Li S, Hagemann IS, Hoog J, Lim B, Osborne CK, Mani DR, Gillette MA, Zhang B, Echeverria GV, Miles G, Rimawi MF, Carr SA, Ademuyiwa FO, Satpathy S, Ellis MJ.
        Proteogenomic Markers of Chemotherapy Resistance and Response in Triple-Negative Breast Cancer. Cancer Discov. 2022 Nov 2;12(11):2586-2605. doi: 10.1158/2159-8290.CD-22-0200. PMID: 36001024; PMCID: PMC9627136.

### Offene Analysen:
- `get_run_list.py` — holt Run-Accession-Liste von NCBI E-Utilities
- `download_ena.py` — lädt FASTQ-Dateien von ENA (schneller als NCBI/prefetch)
- `run_salmon.py` — quantifiziert mit Salmon gegen einen GENCODE-Transkript-Index

### Benötigte Setup-Schritte
1. conda-Environment: `conda create -n rnaseq -c bioconda -c conda-forge sra-tools salmon python=3.11 pandas`
2. `aria2c` separat via Homebrew: `brew install aria2`
3. GENCODE-Transkriptom herunterladen + Salmon-Index bauen (siehe Kommentare in `run_salmon.py`)
4. `sample_manifest.csv` liegt bereits im Repo (SRR-IDs + Sample-Namen)

## Datenablage
Rohdaten liegen im Repo unter data