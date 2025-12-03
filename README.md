# CPARPythonToolbox

Code for parsing and prepossing raw subject data files from the standard Aalborg Cuff Pressure Algometry Protocol into a csv file for further analysis in Excel, Python, SPPS, or similar.

The protocol consists of the following tests:

1. `T01`: Stimulus Response Curve for Dominant Leg [PDT, PTT, PTL]
2. `T02`: Temporal summation (1s/1s, 10 stimuli) [VAS Ratings for each stimulus]
3. `T03`: Stimulus Response Curve for Non-dominant Leg [cPDT, cPTT, cPTL]
4. `T04`: Conditioned Pain Modulation for Dominant Leg (Conditioned by the non-dominant leg) [cpmPDT, cpm PTT, cpmPTL]

To use the script modify the path in the `analysis.py` script to point to where you have your `*.subx` raw data files:

```python
folder = Path(r"[Path to files]")

subjectFiles = list(folder.glob("*.subx"))   # or "*.txt", "*.json", "*.csv", etc.
```

and run the analysis.py script. This requires that you have Numpy and Pandas installed.

Running this script will create a `statistics.csv` file with the collected statistics from the data set.

This files does not exist in the repository (has been added to the ignore list) as uploading this sort of data to Github could quickly escalate into a GDPR violation.

**Consequently, never use this toolbox directly from a cloned repository as the risk of a GDPR violation is to big with this approach**

