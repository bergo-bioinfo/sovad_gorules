# Decision gorules for SoVaD

Decision rules, powed by [gorules](https://gorules.io/), to infer genomic alteration pathogenicity according to the SoVaD publication criterions:

Standardisation of pathogenicity classification for somatic alterations in solid tumours and haematologic malignancies.
Eur J Cancer. 2021 Dec:159:1-15. doi: 10.1016/j.ejca.2021.08.047. Epub 2021 Oct 23.
[PMID: 34700215](https://pubmed.ncbi.nlm.nih.gov/34700215/)

Related project with another implementation: [pathogen-decision-engine](https://github.com/bergo-bioinfo/pathogen-decision-engine)

# Quick start

## Requirements

- Python3
- zen-engine
- pytest (for testing)

### Installation

```bash
pip install zen-engine
```

## Usage

Use the [zen-engine](https://pypi.org/project/zen-engine/) python library to load the SoVaD rules and infer pathogenicity on your own criterions counts.

```python
import zen

# Load SoVaD gorules and create decision engine
with open("sovad_gorules.json") as f:
    content = f.read()
engine = zen.ZenEngine()
decision = engine.create_decision(content)

# Give your own SoVaD criterions counts by class
counts = {"PVS": 1, "PS": 1}

# Get the evaluation result
result = decision_engine.evaluate(counts)
evaluated_pathogenicity = result["result"]["pathogenicity"]

print(result)
# {'result': {'pathogenicity': 'Pathogenic'}, 'performance': '96.054µs'}

print(evaluated_pathogenicity)
# "Pathogenic"
```

# Decisions rules design

The decision rules have been generated with the online [editor](https://editor.gorules.io/) according to an [adaptation](#adapted-criterions)) of the table 3 from the publication and stored in the `sovad_gorules.json` file.

## Original criterions

Table 3 from the publication.

```
Pathogenicity classification based on the relative weight of the criteria.

Class 1—Benign         1 BA
                       >=2 BS
Class 2—Likely benign  1 BS + 1 BP
                       >=2 BP
Class 3—Unknown        Other criteria are unmet
 significance          Criteria for benign and
                       pathogenic are 
                       contradictory
Class 4—Likely         1 PVS + 1 PM
 pathogenic            1 PS + 1-2 PM
                       1 PS + >=2 PP
                       >=3 PM
                       2 PM + >=2 PP 
                       1 PM + >=4 PP 
Class 5—Pathogenic     1 PA
                       1 PVS + >=1 PS
                       1 PVS + >=2 PM/PP
                       >=2 PS
                       1 PS + >=3 PM
                       1 PS + 2 PM + >=2 PP 
                       1 PS + 1 PM + >=4 PP
```


## Adapted criterions

To fit all conditions inferences programatically, the table has been modified as following regarding the full list of criterions.

```
Pathogenicity classification based on the relative weight of the criteria.

Class 1—Benign         >=1 BA
                       >=2 BS
Class 2—Likely benign  1 BS + 1 BP
                       >=2 BP
Class 3—Unknown        Other criteria are unmet
 significance          Criteria for benign and
                       pathogenic are 
                       contradictory
Class 4—Likely         >=1 PVS + 1 PM
 pathogenic            1 PS + 1-2 PM
                       1 PS + >=2 PP
                       >=3 PM
                       >=2 PM + >=2 PP 
                       1 PM + >=4 PP 
Class 5—Pathogenic     >=1 PA
                       >=1 PVS + >=1 PS
                       >=1 PVS + >=2 PM/PP
                       >=2 PS
                       1 PS + >=3 PM
                       1 PS + 2 PM + >=2 PP 
                       1 PS + 1 PM + >=4 PP
```


## Diff

Differences between original and adapated tables above.

```diff
Pathogenicity classification based on the relative weight of the criteria.

- Class 1—Benign         1 BA
+ Class 1—Benign         >=1 BA
                       >=2 BS
Class 2—Likely benign  1 BS + 1 BP
                       >=2 BP
Class 3—Unknown        Other criteria are unmet
 significance          Criteria for benign and
                       pathogenic are 
                       contradictory
- Class 4—Likely         1 PVS + 1 PM
+ Class 4—Likely         >=1 PVS + 1 PM
 pathogenic            1 PS + 1-2 PM
                       1 PS + >=2 PP
                       >=3 PM
-                        2 PM + >=2 PP 
+                        >=2 PM + >=2 PP 
                       1 PM + >=4 PP 
- Class 5—Pathogenic     1 PA
+ Class 5—Pathogenic     >=1 PA
-                        1 PVS + >=1 PS
+                        >=1 PVS + >=1 PS
-                        1 PVS + >=2 PM/PP
+                        >=1 PVS + >=2 PM/PP
                       >=2 PS
                       1 PS + >=3 PM
                       1 PS + 2 PM + >=2 PP 
                       1 PS + 1 PM + >=4 PP
```

## SoVaD criterions list

| Class | Count | Criterions                                              |
|-------|-------|---------------------------------------------------------|
| BA    | 2     | BA1, BA2                                                |
| BP    | 11    | BP1, BP2, BP3, BP4, BP5, BP6, BP7, BP8, BP9, BP10, BP11 |
| BS    | 4     | BS1, BS3, BS5, BS6                                      |
| PA    | 2     | PA1, PA2                                                |
| PM    | 8     | PM1, PM2, PM3, PM4, PM5, PM7, PM8, PM9                  |
| PP    | 6     | PP2, PP3, PP4, PP5, PP6, PP7                            |
| PS    | 5     | PS1, PS3, PS5, PS6, PS7                                 |
| PVS   | 2     | PVS1, PVS2                                              |

# Tests

Run the following command from this directory to test SoVaD rules:

```bash
python3 -m pytest
```
