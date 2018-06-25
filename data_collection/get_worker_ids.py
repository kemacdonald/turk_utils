'''
Short script for getting worker ids for AMT HIT
'''
import json
import boto3

mturk = boto3.client('mturk')
hit_id = "3OQQD2WO8JDQ6SGEMICFBPQL7MLI3O"
hit_id_batch1 = "3I7SHAD35N3U3U7S99DXGZ9ITXQM7C"

# get list of completed assignments for a HIT
def get_completed_worker_info(hit_id, n_max):
    completed_dict = {}
    completed_assignments = mturk.list_assignments_for_hit(HITId=hit_id, AssignmentStatuses=['Submitted', 'Approved'], MaxResults=n_max)
    for assignment in completed_assignments['Assignments']:
      completed_dict[assignment['WorkerId']] = assignment['AssignmentId']
    return completed_dict

d = get_completed_worker_info(hit_id, 80)
d_batch1 = get_completed_worker_info(hit_id_batch1, 80)

d.update(d_batch1)

with open('../turk_worker_ids.json', 'w') as outfile:
    json.dump(d, outfile)
