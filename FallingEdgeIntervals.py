# FallingEdgeIntervals.py
# Saleae Logic 2 - Digital Measurement
# Fall-to-fall interval stats with selectable behavior when empty:
# - ZERO_IF_EMPTY = True  -> return 0.0 for time metrics
# - ZERO_IF_EMPTY = False -> OMIT time metrics entirely (UI shows N/A)

from math import sqrt
from saleae.range_measurements import DigitalMeasurer

class FallToFallMeasurer(DigitalMeasurer):
    supported_measurements = [
        "fallMin", "fallMax", "fallAvg", "fallStd",
        "fallIntervals", "fallCount"
    ]

    # True: 빈 측정(N<1)일 때 0.0을 반환(완전 숫자, 크래시 방지)
    # False: 빈 측정(N<1)일 때 해당 키 자체를 반환하지 않음(Logic UI가 N/A로 표기)
    ZERO_IF_EMPTY = False

    def __init__(self, requested_measurements):
        super().__init__(requested_measurements)
        self.requested = set(requested_measurements)
        self._initialized = False
        self._prev_state = None
        self._last_fall_time = None
        self._intervals_s = []   # list[float seconds]
        self._fall_count = 0     # number of falling edges (k)

    def process_data(self, data):
        """
        data yields (t, bitstate): first pair is starting sample, then transitions (bitstate is NEW state).
        """
        for t, bitstate in data:
            if not self._initialized:
                self._prev_state = bitstate
                self._initialized = True
                continue

            if bitstate != self._prev_state:
                # Falling edge when new state becomes LOW (False)
                if bitstate is False:
                    self._fall_count += 1
                    if self._last_fall_time is not None:
                        dt = t - self._last_fall_time
                        try:
                            delta_s = float(dt)
                        except Exception:
                            delta_s = dt
                        if isinstance(delta_s, (int, float)) and delta_s >= 0:
                            self._intervals_s.append(float(delta_s))
                    self._last_fall_time = t

                self._prev_state = bitstate

    def _emit_time_metrics(self, out, mn, mx, mean, std):
        if "fallMin" in self.requested: out["fallMin"] = float(mn)
        if "fallMax" in self.requested: out["fallMax"] = float(mx)
        if "fallAvg" in self.requested: out["fallAvg"] = float(mean)
        if "fallStd" in self.requested: out["fallStd"] = float(std)

    def _emit_empty_time_metrics(self, out):
        """
        N < 1일 때 동작:
        - ZERO_IF_EMPTY=True  -> 0.0 반환
        - ZERO_IF_EMPTY=False -> 아무 키도 넣지 않음 (UI가 N/A로 표시)
        """
        if self.ZERO_IF_EMPTY:
            if "fallMin" in self.requested: out["fallMin"] = 0.0
            if "fallMax" in self.requested: out["fallMax"] = 0.0
            if "fallAvg" in self.requested: out["fallAvg"] = 0.0
            if "fallStd" in self.requested: out["fallStd"] = 0.0
        # else: intentionally omit keys → N/A

    def measure(self):
        N = len(self._intervals_s)  # interval count (k-1, k = falling edges)
        out = {}

        # Always report counts
        if "fallIntervals" in self.requested:
            out["fallIntervals"] = int(N)
        if "fallCount" in self.requested:
            out["fallCount"] = int(self._fall_count)

        if N < 1:
            # 빈 측정 처리 (0 반환 or 키 생략)
            self._emit_empty_time_metrics(out)
            return out

        # N >= 1 → 정상 통계
        mn = min(self._intervals_s)
        mx = max(self._intervals_s)
        mean = sum(self._intervals_s) / N
        std = 0.0 if N == 1 else (sum((x - mean) ** 2 for x in self._intervals_s) / (N - 1)) ** 0.5
        self._emit_time_metrics(out, mn, mx, mean, std)
        return out
