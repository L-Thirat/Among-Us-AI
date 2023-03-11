from utility import get_task_list, load_dict, in_meeting, isImpostor, is_urgent_task, isDead
import subprocess
import time

def generate_files():
    possible_tasks = load_dict().keys()
    for task in possible_tasks:
        with open(f"task-solvers\{task}.py", "w") as f:
            f.close()

# Runs the correct task solver file in a subprocess
# Note - the AI only goes to the upper location of sabotages
def solve_task(task_name=None, task_index=None) -> int:
    old_dead : bool = isDead()
    if task_name == "vote":
        p = subprocess.Popen(["python", f"task-solvers\\vote.py"])

    if isImpostor():
        time.sleep(1.5)
        p = subprocess.Popen(["python", f"task-solvers\Sabotage.py"])

        # Wait for process to finish
        while p.poll() is None:
            if in_meeting():
                p.kill()
                return 1
            time.sleep(1/30)

        time.sleep(3) # Fake doing stuff
        return 0
    
    if is_urgent_task() is not None:
        if task_name is not None and task_name != is_urgent_task()[0]:
            return 1

    if task_name is not None and task_name != ():
        p = subprocess.Popen(["python", f"task-solvers\{task_name}.py"])

        # Wait for process to finish
        while p.poll() is None:
            if in_meeting() or isDead() != old_dead:
                p.kill()
                return 1 if task_name != "Inspect Sample" else 2
            time.sleep(1/30)

        return 0
    
    print("Task not found")
    return -1

