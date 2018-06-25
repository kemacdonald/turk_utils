'''
CLI tool for bonusing Amazon Mechanical Turkers
'''
import json
import click
import boto3
# connect to turk
mturk = boto3.client('mturk')

# read in a list of Turk IDs for workers who
# have already been bonused
def get_bonused_workers(hit_id, n_max):
    bonused = []
    already_bonused = mturk.list_bonus_payments(HITId=hit_id, MaxResults = n_max)
    for worker in already_bonused['BonusPayments']:
        bonused.append(worker['WorkerId'])
    return bonused

# get list of completed assignments for a HIT
def get_completed_worker_info(hit_id, n_max):
    completed_dict = {}
    completed_assignments = mturk.list_assignments_for_hit(HITId=hit_id, AssignmentStatuses=['Submitted', 'Approved'], MaxResults=n_max)
    for assignment in completed_assignments['Assignments']:
      completed_dict[assignment['WorkerId']] = assignment['AssignmentId']
    return completed_dict

# send bonus to workers
def send_bonuses(workers_to_bonus, worker_info_dict, hit_id, bonus):
    payment = str(bonus)
    message = ("Thank you for participating in the Food Ordering Game! Here is your bonus.")
    for worker_id in workers_to_bonus:
      mturk.send_bonus(
        WorkerId=worker_id,
        BonusAmount=payment,
        AssignmentId=worker_info_dict[worker_id],
        Reason=message)

def display_success_msg(workers_to_bonus):
     click.secho('Bonuses were sent to %s workers' % len(workers_to_bonus),
       fg='green')

@click.command()
@click.option('--bonus', default=0, type=float, help='bonus amount (in cents)')
@click.option('--env', default='sandbox', help='mturk environment: sandbox or production')
@click.option('--hit_id', help='unique ID for the HIT you wish to bonus')

def bonus_worker(env, hit_id, bonus):
    if env == "production":
      endpoint_url = 'https://mturk-requester.us-east-1.amazonaws.com'
      env_string = "production"
      HIT = mturk.get_hit(HITId=hit_id)
      n_max = HIT['HIT']['MaxAssignments']
      completed_worker_dict = get_completed_worker_info(hit_id, n_max)
      completed_worker_ids = list(completed_worker_dict.keys())
      already_bonused = get_bonused_workers(hit_id, n_max)
      workers_to_bonus = list(set(completed_worker_ids).difference(set(already_bonused)))
      click.secho('%s Turkers have completed this HIT. %s Turkers need to be bonused.' % (len(completed_worker_ids), len(workers_to_bonus)),
        fg='green')
      total_cost = len(workers_to_bonus) * bonus
      click.secho('The bonus amount is $%s and will be sent to %s turkers. The total cost will be $%s' % (bonus, len(workers_to_bonus), total_cost),
        fg='green')

      if click.confirm('Do you want to send these bonuses?'):
         if total_cost == 0:
           click.secho('Bonus amount is 0, so no bonuses were sent.',
             fg='red')
         else:
            send_bonuses(workers_to_bonus, completed_worker_dict, hit_id, bonus)
            display_success_msg(workers_to_bonus)
      else:
         click.secho('You chose not to bonus at this time, no bonuses were sent',
            fg='red')
    else:
      endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
      env_string = "sandbox"
      click.secho('You are working in the sandbox, no bonuses were sent',
        fg='red')

if __name__ == "__main__":
    bonus_worker()
