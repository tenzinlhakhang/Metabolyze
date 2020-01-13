import sys

PPM = float(sys.argv[2])
RT_DELTA = float(sys.argv[3])
MIN_SIGNAL = float(sys.argv[4])
MIN_RANGE  = float(sys.argv[5])
# 
# PPM = 20
# RT_DELTA = 0.5
# MIN_SIGNAL = 1000000.0
# MIN_RANGE = 1.1  # max-intensity in window must be >= MIN_RANGE * min_intensity

#
# Actual code begins here...
#

import os
import sys
import time
import bisect
import sqlite3

start_time = time.time()


outname = (os.environ['skeleton_input_name'])



batchmode = False
for arg in sys.argv:
    if arg in ("-b", "-B", "--batch"):
        batchmode = True

__version__ = "0.5"


#
# Based on: https://github.com/suzaku/plain_obj
#


def make_constructor(fields):
    assignments = '\n'.join([f'    self.{f} = {f}' for f in fields])
    parameter_lists = ', '.join(fields)
    source = 'def __init__(self, %s):\n%s' % (parameter_lists, assignments)
    namespace = {}
    exec(source, namespace)
    return namespace['__init__']


def make_lt(key_field):
    source = f"def __lt__(self, other):\n    return self.{key_field} < other.{key_field}"
    namespace = {}
    exec(source, namespace)
    return namespace['__lt__']


def sortable(type_name, field_names):
    if isinstance(field_names, str):
        # names separated by whitespace and/or commas
        field_names = field_names.replace(',', ' ').split()
    return type(
        type_name,
        (object,),
        {
            '__slots__': field_names,
            '__init__': make_constructor(field_names),
            '__lt__': make_lt(field_names[0])
        }
    )


ppm = PPM / 1000000.0

#
# Set up our cursor
#

MS1_DBNAME = sys.argv[1]
assert MS1_DBNAME.endswith(".sqlite3")

con = sqlite3.connect(MS1_DBNAME)
cur = con.cursor()

PEAK_SQL = """SELECT ms1_peaks.intensity, ms1_peaks.mz / 10000.0, ms1_peaks.rt / 60000.0, ms1_peaks.rawfile FROM ms1_peaks WHERE ms1_peaks.rawfile > 0 AND ms1_peaks.intensity > ? ORDER BY ms1_peaks.intensity DESC"""

print(f"Starting the mega-query...", file=sys.stderr)
start_query = time.time()
all_peaks = list(cur.execute(PEAK_SQL, (MIN_SIGNAL,)))
stop_query = time.time()

print(f"Finished mega-query in {stop_query-start_query:.2f} seconds.", file=sys.stderr)

print(f"The total number of peaks is: {len(all_peaks)}", file=sys.stderr)

print(f"Starting the peak processing...", file=sys.stderr)
start_process = time.time()

Slot = sortable("Slot", "mz rt file min max")
slots = []
rt_max = 0
for (intensity, mz, rt, rfile) in all_peaks:
    potential_slot = Slot(mz, rt, rfile, intensity, intensity)
    if rt > rt_max:
        rt_max = rt
    if mz > 0.0:
        lower = (1.0 - ppm) * mz
        upper = (1.0 + ppm) * mz
    else:
        lower = (1.0 + ppm) * mz
        upper = (1.0 - ppm) * mz
    potential_slot.mz = lower
    lower_index = bisect.bisect_left(slots, potential_slot)
    potential_slot.mz = upper
    upper_index = bisect.bisect_right(slots, potential_slot)
    potential_slot.mz = mz
    assigned = False
    if (lower_index != len(slots)) and (upper_index > 0):
        for offset in range(lower_index, upper_index):
            slot = slots[offset]
            if abs(slot.rt - rt) < RT_DELTA:
                assigned = True
                if slot.file == rfile and intensity < slot.min:
                    slot.min = intensity
    if not assigned:
        bisect.insort(slots, potential_slot)

stop_process = time.time()
print(f"Finished peak processing {len(all_peaks)} peaks into {len(slots)} potential features in {stop_process-start_process:.2f} seconds.", file=sys.stderr)

out = open(outname, 'w')
print("Metabolite\tFormula\tIon Type\tRT Start (min)\tRT End (min)\tm/z Tolerance (ppm)\tRT Tolerance (min)", file=out)
final_feature_counter = 0
for slot in slots:
    if slot.max / slot.min > MIN_RANGE:
        polarity = "+"
        rt_start = max(0, slot.rt - RT_DELTA)
        rt_stop = min(slot.rt + RT_DELTA, rt_max)
        mz_name = abs(slot.mz)
        if slot.mz < 0:
            polarity = "-"
        print(f"Feature_{polarity}_{mz_name:.4f}_{slot.rt:.1f}\t{slot.mz :.4f}\t\t{rt_start:.3f}\t{rt_stop:.3f}\t{PPM}\t{RT_DELTA}", file=out)
        final_feature_counter += 1
out.close()

stop_time = time.time()

#print(f"Ungrid processed {len(all_peaks)} peaks into {final_feature_counter} features in {stop_time - start_time :.2f} seconds.", file=sys.stderr)
#if not batchmode:
#    input("press Return key to exit...")
