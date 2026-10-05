# Clinical dMRI Corticospinal Tract (CST) Probabilistic Tractography Pipeline

[![dMRI CST Pipeline CI](https://github.com/Leonam0706/dti-cst-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/Leonam0706/dti-cst-pipeline/actions)
[![GitHub release](https://img.shields.io/github/v/release/Leonam0706/dti-cst-pipeline)](https://github.com/Leonam0706/dti-cst-pipeline/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)

An automated, end-to-end production-grade pipeline for diffusion MRI (dMRI) preprocessing, Bayesian probabilistic tractography (`bedpostx` / `probtrackx2`), microstructural along-tract profiling (FA & MD), and clinical Quality Assurance (QA) reporting.

---

## 📌 Executive Summary

The **Corticospinal Tract (CST)** is the primary motor pathway in the human brain. Microstructural alterations along the CST (measured via Fractional Anisotropy and Mean Diffusivity) serve as vital biomarkers in stroke recovery, neuro-oncology surgical planning, and motor neuron disease.

This pipeline automates the complete analytical workflow from raw NIfTI DICOM conversions to clinical reporting, ensuring 100% execution reproducibility via Docker, automated unit testing with `pytest`, and Continuous Integration via GitHub Actions.

---

## 🏗️ Pipeline Architecture

```text
  [ Raw dMRI (.nii.gz) + bvals/bvecs ]
                   │
                   ▼
  [ 1. Visual QA & Data Verification ] ───► scripts/00_verify_data.sh
                   │
                   ▼
  [ 2. Brain Extraction (BET) ]       ───► scripts/02_brain_extraction.sh
                   │
                   ▼
  [ 3. Eddy Current & Motion Correction] ──► scripts/03_eddy_correction.sh
                   │
                   ▼
  [ 4. DTI Tensor Fitting (dtifit) ]   ───► scripts/04_dtifit.sh
                   │
                   ▼
  [ 5. Fiber Orientation Estimation ]  ───► scripts/06_bedpostx_prep.sh
                   │
                   ▼
  [ 6. Seed/Target ROI Definition ]    ───► scripts/09_define_cst_rois.py
                   │
                   ▼
  [ 7. Probabilistic Tractography ]    ───► scripts/10_run_probtrackx.sh
                   │
                   ▼
  [ 8. Microstructural Quantification ] ──► scripts/12_profile_cst.py
                   │
                   ▼
  [ 9. Interactive Dashboard & QA ]   ───► app.py & CLINICAL_QA_REPORT.md
