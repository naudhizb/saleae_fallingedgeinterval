# Falling Edge Interval Stats (Logic 2 Digital Measurement)

Compute statistics of **intervals between consecutive falling edges** in a selected time range.

- **Metrics:** `min`, `max`, `avg`, `stdev` of fall→fall intervals  
- **Counts:** number of **falling edges** and **intervals** in the selection  
- **Display:** compact names with **subscripts** (e.g., `Fall<sub>min</sub>`)  
- **Units:** time reported in **seconds** internally; Logic 2 **auto-scales** at display time (**ns / µs / ms / s**)  
- **Empty selection behavior:** configurable via `ZERO_IF_EMPTY` (see below)

---

## Installation

1. Open **Logic 2** → **Extensions** sidebar.
2. Click **“+” → Create an Extension** and choose **Digital Measurement**.
3. Replace the generated files with the ones from this project:
   - `extension.json`
   - `FallingEdgeIntervals.py`
   - `README.md` (this file)
4. Or use **“Load from Disk”** and select the plugin folder.

---

## Usage

1. Capture or open a recording, select a **digital** channel.
2. **Drag to select** a time region.
3. Add a measurement and choose **“Falling Edge Interval Stats → FallToFallStats.”**
4. The panel shows:
   - `Fall<sub>min</sub>`, `Fall<sub>max</sub>`, `Fall<sub>avg</sub>`, `Fall<sub>stdev</sub>` (time metrics)
   - `N<sub>interval</sub>` (number of intervals)
   - `N<sub>falling</sub>` (number of falling edges)

> Intervals are computed only at **LOW transitions** (HIGH→LOW).  
> If k falling edges are detected, there are **N = max(k−1, 0)** intervals.

---

## Metrics

| Key             | Panel name   | Notation               | Units | Description |
|-----------------|--------------|------------------------|-------|-------------|
| `fallMin`       | `Fall_min`   | `Fall<sub>min</sub>`   | `s`   | Minimum fall→fall interval within the selection. |
| `fallMax`       | `Fall_max`   | `Fall<sub>max</sub>`   | `s`   | Maximum fall→fall interval within the selection. |
| `fallAvg`       | `Fall_avg`   | `Fall<sub>avg</sub>`   | `s`   | Arithmetic mean of fall→fall intervals. |
| `fallStd`       | `Fall_stdev` | `Fall<sub>stdev</sub>` | `s`   | Sample standard deviation of intervals (N−1). |
| `fallIntervals` | `N_interval` | `N<sub>interval</sub>` | —     | Number of intervals (computed pairs), i.e., `max(N_falling−1, 0)`. |
| `fallCount`     | `N_falling`  | `N<sub>falling</sub>`  | —     | Number of falling edges detected in the selection. |

**Notes**

- Time metrics use `units: "s"` in `extension.json`; Logic 2 will **auto-scale** the display to `ns/µs/ms/s` depending on value magnitude.
- Subscripts are rendered via HTML `<sub>` in the `notation` field.
