# Anomaly Detection and Prediction (ADAP) Package

This is a simple example package. You can use
[GitHub-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.

| Anomaly type | Type code | Description | Example in the literature and/or alternative terminology | Importance ranking (with respect to time series visualization in this case study) | Potential end-user and application |
| --- | --- | --- | --- | --- | --- |
| Impossible values | A | Values 6666 are highly impossible in compressor sensor data and consider as out of range value of the sensors. | - | Important, but it can be deleted easily using simple rule | - |
| Constant values within the acceptable region for long time period | B | Constant values within the acceptable region for long time period (more than one day) |- | Important can be detected using rate of change | - |
| Large sudden spike | C | The spikes are larger than the surrounding data points but less than 6666. Example one or two values much higher than previous or next values | - | At any point in the time series, used 3 times standard deviation as threshold | -  |
| Drift | D | Gradual change in values in positive to zero | - | High priority (Emergency shutdown, ESD) | -  |
| Sudden zero | E | Value suddenly shifts in values in positive to zero | - | High priority (Emergency shutdown, ESD) | - |

**Table 1: Load current related anomaly types**

| Anomaly type | Type code | Description | Example in the literature and/or alternative terminology | Importance ranking (with respect to time series visualization in this case study) | Potential end-user and application |
| --- | --- | --- | --- | --- | --- |
| Impossible values | A | Values 6666 are highly impossible in compressor sensor data and consider as out of range value of the sensors. | - | Important, but it can be deleted easily using simple rule | - |
| Constant values within the acceptable region for long time period | B | Constant values within the acceptable region for long time period (more than one day) |- | Important can be detected using rate of change | - |
| Large sudden spike | C | The spikes are larger than the surrounding data points but less than 6666. Example one or two values much higher than previous or next values | - | At any point in the time series, used 3 times standard deviation as threshold | -  |
| Drift | D | Gradual change in values in positive to zero | - | High priority (Emergency shutdown, ESD) | -  |
| Sudden zero | E | Value suddenly shifts in values in positive to zero | - | High priority (Emergency shutdown, ESD) | - |
| Step up (sudden shift) | F | Increase the mean while keeping the variance constant | - | High priority (Emergency shutdown, ESD) | - |
| Step down (sudden shift) | G | Decrease the mean while keeping the variance constant | - | Normal, indicate motor flips from OFF to ON | - |

**Table 2: Suction pressure related anomaly types**

| Anomaly type | Type code | Description | Example in the literature and/or alternative terminology | Importance ranking (with respect to time series visualization in this case study) | Potential end-user and application |
| --- | --- | --- | --- | --- | --- |
| Impossible values | A | Values 6666 are highly impossible in compressor sensor data and consider as out of range value of the sensors. | - | Important, but it can be deleted easily using simple rule | - |
| Constant values within the acceptable region for long time period | B | Constant values within the acceptable region for long time period (more than one day) |- | Important can be detected using rate of change | - |
| Large sudden spike | C | The spikes are larger than the surrounding data points but less than 6666. Example one or two values much higher than previous or next values | - | At any point in the time series, used 3 times standard deviation as threshold | -  |
| Drift | D | Gradual change in values in positive to zero | - | High priority (Emergency shutdown, ESD) | -  |
| Sudden zero | E | Value suddenly shifts in values in positive to zero | - | High priority (Emergency shutdown, ESD) | - |
| Step up (sudden shift) | F | Increase the mean while keeping the variance constant | - | Normal, indicate motor flips from OFF to ON | - |
| Step down (sudden shift) | G | Decrease the mean while keeping the variance constant | - | High priority (Emergency shutdown, ESD) | - |

**Table 2: Discharge pressure related anomaly types**