# Examining the Use of Feature Flags in Open-Source with CI/CD Pipelines

## Overview
This repository will contain the code, datasets, and results of the collection + analysis
for my thesis project. The intent of the project is to provide a generalized implementation 
for the automatic detection and categorization of feature toggles (feature flags), construct a
dataset of valid open-source repositories using both feature toggles and CI/CD pipelines with deployments,
and perform analysis on the dataset through feature toggle categorization in order to achieve
meaningful correlations to [DORA metrics](https://dora.dev/guides/dora-metrics/) and observations related to the usage of feature toggles. 

## Revised Research Questions
- RQ1: How prevalent is the use of each feature toggle usage pattern in open-source software where CI/CD pipelines are present?
- RQ2: How does the presence of feature toggles correlate with the four key DORA metrics collected from open-source software?
- RQ3: Do certain feature toggle usage patterns have more significant impacts on the four key DORA metrics collected from open-source software?

## Dataset Collection Rules
The repositories must fulfill all of the following criteria:
1. Fully open-source code repositories.
2. Uses a CI/CD pipeline with public results.
3. Has deployments with public results.
4. Uses feature flags in the codebase.

Criteria 1 and 4 are currently fulfilled using the existing dataset from (Capture the Feature Flag:
Detecting Feature Flags in Open-Source)[https://dl.acm.org/doi/pdf/10.1145/3379597.3387463].

Criteria 2 and 3 are currently checked via the `check_for_workflows.py` script. As of 10/20/26, only GitHub Workflows and GitHub Deployments are being checked for.
