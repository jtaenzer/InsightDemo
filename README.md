# InsightDemo

## Interpreter and dependencies
Environment: Windows 10

IDE: PyCharm CE

Interpreter used for testing: python 3.7.6

External dependencies: tensorflow, keras, keras-preprocessing, pandas, numpy, sklearn, matplotlib

```
python -m pip install tensorflow --upgrade
python -m pip install keras --upgrade
python -m pip install keras-preprocessing --upgrade
python -m pip install pandas --upgrade
python -m pip install numpy --upgrade
python -m pip install sklearn --upgrade
python -m pip install matplotlib --upgrade
```

## Usage

First open db_config.py and enter the relevant database information, e.g.:

```
host = "localhost"
user = "joe"
passwd = "password"
database = "insightdemo"

makedb = True
schedule = True
team_gamelog = True
```

Make histograms of variables of interest and correlation heatmaps with:

```
python make_plots.py
python make_plots_by_team.py
```

Train a NN on the variables of interest:

```
python training.py
```

Test the NN and plot its accuracy by year:

```
python testing.py
```