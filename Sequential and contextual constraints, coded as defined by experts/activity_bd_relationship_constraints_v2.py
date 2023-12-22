def generate_constraints(eventLog, threshold):
    # Initialize data structures
    freqDict = {}
    constraints = []

    # Part 1: Populate frequency dictionary
    for event in eventLog:
        activity = event[1][0]
        BD = retrieveBD(activity)

        if activity not in freqDict:
            freqDict[activity] = {}

        for element in BD:
            if element not in freqDict[activity]:
                freqDict[activity][element] = 1
            else:
                freqDict[activity][element] += 1

    # Part 2: Generate constraints
    for activity in freqDict:
        highOccList = []

        for element, frequency in freqDict[activity].items():
            occRate = frequency / totalInstances(activity)

            if occRate > threshold:
                highOccList.append(element)

        constraint = f"{activity}ALWAYSWITH{highOccList}"
        constraints.append(constraint)

    return constraints

# Example usage
eventLog = [...]  # Replace with your event log data
threshold = 0.5  # Replace with your desired threshold

result_constraints = generate_constraints(eventLog, threshold)
print(result_constraints)
