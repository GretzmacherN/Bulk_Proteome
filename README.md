# ROR1-EGFR Coexpression & RNA-Protein-Dropout-Analyse

## Status (Stand: [Datum einfügen])
Übergabe an [Name des Kollegen] wegen technischer Probleme beim RNA-seq-Download.

## Was funktioniert bereits
- R-Analyse-Pipeline (Notebook: `[Notebookname].ipynb`) für drei Proteomik-Datensätze:
  1. TNBC-Patientenkohorte (Genome Biology Paper, Table S2)
  2. Kosok et al. 2020 (iScience) Zelllinien-Panel (`mmc2.xlsx`)
  3. Anurag et al. CPTAC/NTN-Datensatz (`cd-22-0200_table_s3...xlsx`)
- Für alle drei: ROR1/EGFR-Coexpression, Z-Score-Normalisierung, Pair-Scores,
  EMT-Score (Hallmark) und BCSC-associated protein composite berechnet.
- Finale 3x3-Panel-Figur mit Pearson-R/p-Wert pro Panel (via `ggpubr::stat_cor()`).

## Offene Aufgabe: RNA-seq-Rohdaten-Download
Ziel: Prüfen, ob ROR1 einen ungewöhnlich großen RNA-Protein-Dropout zeigt
(verglichen mit anderen Genen), unter Nutzung der Rohdaten von
NCBI BioProject **PRJNA1422844** (RNA-seq der TNBC-Patientenkohorte).

### Pipeline (Skripte in diesem Repo)
- `get_run_list.py` — holt Run-Accession-Liste von NCBI E-Utilities
- `download_ena.py` — lädt FASTQ-Dateien von ENA (schneller als NCBI/prefetch)
- `run_salmon.py` — quantifiziert mit Salmon gegen einen GENCODE-Transkript-Index

### Bekannte Probleme / letzter Stand
- `aria2c` via conda führte zu einem Dependency-Konflikt mit `sra-tools`
  (libxml2-Versionskonflikt) → Lösung: `aria2c` separat via Homebrew installieren,
  NICHT im selben conda-Environment.
- Einige Downloads waren nach Tool-Wechsel (`curl` → `aria2c`) korrupt
  (`gzip -t` schlug fehl) — vermutlich Reste von abgebrochenen `curl`-Versuchen.
  Fix: betroffene Dateien löschen, Skript erneut laufen lassen
  (überspringt bereits erfolgreiche Samples automatisch).
- Noch zu verifizieren: alle Sample-Downloads vollständig & intakt
  (`gzip -t rnaseq_work/*.fastq.gz` sollte für ALLE Dateien fehlerfrei laufen).
- Salmon-Quantifizierung wurde noch nicht gestartet (wartet auf vollständigen Download).
- Transkript→Gen-Mapping für ROR1 (ENST-ID) muss noch verifiziert werden
  (aktuell nur Platzhalter im Code, siehe `build_matrix.py`).

### Benötigte Setup-Schritte für den Kollegen
1. conda-Environment: `conda create -n rnaseq -c bioconda -c conda-forge sra-tools salmon python=3.11 pandas`
2. `aria2c` separat via Homebrew: `brew install aria2`
3. GENCODE-Transkriptom herunterladen + Salmon-Index bauen (siehe Kommentare in `run_salmon.py`)
4. `sample_manifest.csv` liegt bereits im Repo (SRR-IDs + Sample-Namen)

## Datenablage
Rohdaten (FASTQ, Salmon-Ergebnisse, Excel-Supplementary-Tabellen) liegen NICHT
in diesem Repo (siehe `.gitignore`) — [hier ergänzen: wo genau, z.B. Pfad auf
gemeinsamer Festplatte/Cloud-Speicher, den der Kollege bekommt].