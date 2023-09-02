import json
import matplotlib.pyplot as plt
from datetime import datetime

# Load and parse JSON data with explicit encoding specification
with open('jira_data.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Initialize dictionaries to store status, assignee, and date information
status_dict = {}
assignee_dict = {}

# Extract relevant information and organize it
for change in data['values']:
    created = change['created']
    date = datetime.strptime(created, '%Y-%m-%dT%H:%M:%S.%f%z')
    
    # Extract status and assignee changes
    for item in change.get('items', []):
        if item['field'] == 'status':
            key = data['self'].split('/')[-3]
            status = item.get('toString')
            if status is not None and isinstance(status, str):
                status_dict.setdefault(key, []).append((date, status))
        
        if item['field'] == 'assignee':
            key = data['self'].split('/')[-3]
            assignee = item.get('toString', 'Unassigned')
            if assignee is not None and isinstance(assignee, str):
                assignee_dict.setdefault(key, []).append((date, assignee))

# Create a figure for the combined chart
fig, ax = plt.subplots(figsize=(10, 6))

# Plot both status and assignee changes
for key, status_changes in status_dict.items():
    dates, statuses = zip(*status_changes)
    ax.plot(dates, statuses, label=f'{key} Status', marker='o')

for key, assignee_changes in assignee_dict.items():
    dates, assignees = zip(*assignee_changes)
    ax.plot(dates, assignees, label=f'{key} Assignee', marker='x')

# Annotate the toString values on the chart
for key, status_changes in status_dict.items():
    for date, status in status_changes:
        ax.annotate(status, (date, status), textcoords="offset points", xytext=(0,10), ha='center')

# Annotate the assignee names with staggered y-coordinates
for key, assignee_changes in assignee_dict.items():
    stagger = 0
    for date, assignee in assignee_changes:
        ax.annotate(assignee, (date, assignee), textcoords="offset points", xytext=(0,stagger), ha='center')
        stagger -= 10  # Adjust the stagger value as needed to control the vertical spacing
        ax.axvline(x=date, color='gray', linestyle='--', alpha=0.5)  # Plot vertical line for the date

ax.set_xlabel('Date')
ax.set_ylabel('Status / Assignee')
ax.set_title('Issue Status and Assignee Changes')
# ax.legend()  # Commented out legend creation
ax.yaxis.set_visible(False)  # Hide y-axis
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
