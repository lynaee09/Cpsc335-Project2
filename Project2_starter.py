def time_to_minutes(t):
    hours, minutes = map(int, t.split(':'))
    return hours * 60 + minutes

def minutes_to_time(m):
    return f"{m // 60}:{m % 60:02d}"

def merge_intervals(intervals):
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for curr in intervals[1:]:
        last = merged[-1]
        if curr[0] <= last[1]:
            last[1] = max(last[1], curr[1])
        else:
            merged.append(curr)
    return merged

def invert_intervals(busy, start, end):
    free = []
    if not busy:
        return [[start, end]]
    if busy[0][0] > start:
        free.append([start, busy[0][0]])
    for i in range(len(busy) - 1):
        free.append([busy[i][1], busy[i+1][0]])
    if busy[-1][1] < end:
        free.append([busy[-1][1], end])
    return free

def intersect_intervals(list1, list2):
    result = []
    i = j = 0
    while i < len(list1) and j < len(list2):
        start = max(list1[i][0], list2[j][0])
        end = min(list1[i][1], list2[j][1])
        if start < end:
            result.append([start, end])
        if list1[i][1] <= list2[j][1]:
            i += 1
        else:
            j += 1
    return result

def is_within_lunch_hours(start, end):
    lunch_start = time_to_minutes('12:00')
    lunch_end = time_to_minutes('14:00')
    return start < lunch_end and end > lunch_start

def find_available_slots(schedules, working_periods, duration):
    free_times = []
    for i in range(len(schedules)):
        busy = [[time_to_minutes(t[0]), time_to_minutes(t[1])] for t in schedules[i]]
        working_start = time_to_minutes(working_periods[i][0])
        working_end = time_to_minutes(working_periods[i][1])
        # Add working period boundaries to busy intervals
        busy.append([0, working_start])
        busy.append([working_end, 24 * 60])
        busy = merge_intervals(busy)
        free = invert_intervals(busy, working_start, working_end)
        free_times.append(free)
    # Intersect the free times of all people
    common_free = free_times[0]
    for i in range(1, len(free_times)):
        common_free = intersect_intervals(common_free, free_times[i])
    # Filter intervals by duration and exclude lunch hours
    meeting_slots = []
    for interval in common_free:
        if interval[1] - interval[0] >= duration:
            if not is_within_lunch_hours(interval[0], interval[1]):
                meeting_slots.append([minutes_to_time(interval[0]), minutes_to_time(interval[1])])
    return meeting_slots

if __name__ == "__main__":
    # Read input from Input.txt
    with open('Input.txt', 'r') as file:
        lines = [line.strip() for line in file if line.strip()]
    schedules = []
    working_periods = []
    duration = None
    i = 0
    while i < len(lines):
        if lines[i].startswith('Enter person') and '_Schedule' in lines[i]:
            schedule = eval(lines[i].split('=')[1].strip())
            schedules.append(schedule)
            i += 1
            if i < len(lines) and 'DailyAct' in lines[i]:
                working_period = eval(lines[i].split('=')[1].strip())
                working_periods.append(working_period)
            else:
                print("Error: Missing working period for a person.")
                exit(1)
        elif 'Enter duration_of_meeting' in lines[i]:
            duration = int(lines[i].split('=')[1].strip())
            i += 1
        else:
            i += 1
    if duration is None:
        print("Error: Missing duration of the meeting.")
        exit(1)
    # Find available slots
    available_slots = find_available_slots(schedules, working_periods, duration)
    # Write output to Output.txt
    with open('Output.txt', 'w') as file:
        file.write(str(available_slots))
    # Print the result to the terminal
    print("Available meeting slots:")
    for slot in available_slots:
        print(f"{slot[0]} - {slot[1]}")
