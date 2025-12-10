# Uniprocessor Scheduling Practice Exercises

## How to Use This Practice Program

1. **Compile the program:**
   ```bash
   gcc scheduling_practice.c -o scheduling_practice
   ```

2. **Run the program:**
   ```bash
   ./scheduling_practice
   ```

## Practice Exercise Sets

### Exercise 1: Basic FCFS vs Round Robin
**Test Data:**
| Process | Arrival Time | Burst Time |
|---------|--------------|------------|
| P1      | 0            | 8          |
| P2      | 1            | 4          |
| P3      | 2            | 9          |
| P4      | 3            | 5          |

**Questions:**
1. Calculate average waiting time for FCFS
2. Calculate average waiting time for RR (quantum = 2)
3. Which algorithm performs better? Why?
4. What happens if you increase the quantum to 4?

**Expected FCFS Results:**
- P1: Completes at 8
- P2: Completes at 12
- P3: Completes at 21
- P4: Completes at 26

---

### Exercise 2: SPN vs SRT Comparison
**Test Data:**
| Process | Arrival Time | Burst Time |
|---------|--------------|------------|
| P1      | 0            | 7          |
| P2      | 2            | 4          |
| P3      | 4            | 1          |
| P4      | 5            | 4          |

**Questions:**
1. Which process runs first in SPN?
2. When does P3 execute in SRT? Does it preempt another process?
3. Compare average turnaround times
4. Which algorithm minimizes average waiting time?

**Key Concept:** SRT is preemptive, so P3 (shortest) should interrupt the running process when it arrives.

---

### Exercise 3: HRRN Aging Effect
**Test Data:**
| Process | Arrival Time | Burst Time |
|---------|--------------|------------|
| P1      | 0            | 10         |
| P2      | 0            | 1          |
| P3      | 0            | 2          |
| P4      | 0            | 3          |

**Questions:**
1. What is the execution order?
2. Calculate response ratio for each process at different time points
3. How does HRRN prevent starvation of long processes?
4. Compare with SPN - what's different?

**Hint:** Response Ratio = (Waiting Time + Burst Time) / Burst Time

---

### Exercise 4: Round Robin Quantum Effect
**Test Data:**
| Process | Arrival Time | Burst Time |
|---------|--------------|------------|
| P1      | 0            | 5          |
| P2      | 1            | 3          |
| P3      | 2            | 8          |
| P4      | 3            | 6          |

**Questions:**
1. Run with quantum = 1, 2, 4, and 8
2. How does quantum size affect context switches?
3. What quantum gives best average waiting time?
4. What happens when quantum ≥ longest burst time?

---

### Exercise 5: Feedback Scheduling
**Test Data:**
| Process | Arrival Time | Burst Time |
|---------|--------------|------------|
| P1      | 0            | 12         |
| P2      | 2            | 4          |
| P3      | 4            | 6          |

**Settings:** 3 queues, quantum = 2

**Questions:**
1. How many times does P1 get demoted?
2. Trace the priority levels of each process over time
3. How does feedback scheduling penalize long-running processes?
4. Compare with Round Robin using same quantum

---

### Exercise 6: Real-World Scenario
**Test Data (Mixed Workload):**
| Process | Arrival Time | Burst Time | Description    |
|---------|--------------|------------|----------------|
| P1      | 0            | 3          | Short task     |
| P2      | 1            | 15         | Long batch job |
| P3      | 2            | 2          | Quick query    |
| P4      | 3            | 8          | Medium task    |
| P5      | 4            | 1          | Interrupt      |

**Questions:**
1. Which algorithm gives best response time for short tasks (P1, P3, P5)?
2. Which algorithm is fairest overall?
3. Which would you use for an interactive system? Why?
4. Which for a batch processing system? Why?

---

### Exercise 7: Convoy Effect Demonstration
**Test Data:**
| Process | Arrival Time | Burst Time |
|---------|--------------|------------|
| P1      | 0            | 20         |
| P2      | 1            | 2          |
| P3      | 1            | 3          |
| P4      | 1            | 2          |

**Questions:**
1. What happens with FCFS? (Convoy effect)
2. How does SPN solve this problem?
3. How does Round Robin help?
4. Calculate the difference in average waiting time

---

### Exercise 8: Advanced Comparison
**Test Data:**
| Process | Arrival Time | Burst Time |
|---------|--------------|------------|
| P1      | 0            | 6          |
| P2      | 1            | 8          |
| P3      | 2            | 7          |
| P4      | 3            | 3          |
| P5      | 4            | 4          |
| P6      | 5            | 2          |

**Tasks:**
1. Run ALL algorithms (use option 7)
2. Create a comparison table of:
   - Average Turnaround Time
   - Average Waiting Time
   - Average Response Time
3. Rank algorithms from best to worst for each metric
4. Identify which algorithm would be best for:
   - Time-sharing system
   - Batch processing
   - Real-time system (minimize response time)

---

## Key Concepts to Remember

### 1. FCFS (First-Come-First-Served)
- **Type:** Non-preemptive
- **Pros:** Simple, fair in order of arrival
- **Cons:** Convoy effect, poor for short jobs
- **Best for:** Batch systems with similar job lengths

### 2. Round Robin
- **Type:** Preemptive
- **Pros:** Fair, good response time
- **Cons:** High context switching overhead
- **Best for:** Time-sharing systems
- **Quantum selection:** 
  - Too small → too many context switches
  - Too large → approaches FCFS

### 3. SPN (Shortest Process Next)
- **Type:** Non-preemptive
- **Pros:** Minimizes average waiting time
- **Cons:** Can starve long processes, requires burst time knowledge
- **Best for:** When you know process durations

### 4. SRT (Shortest Remaining Time)
- **Type:** Preemptive version of SPN
- **Pros:** Optimal average waiting time
- **Cons:** More context switches, starvation risk
- **Best for:** Environments where short jobs should complete quickly

### 5. HRRN (Highest Response Ratio Next)
- **Type:** Non-preemptive
- **Pros:** Prevents starvation using aging
- **Cons:** Requires burst time calculation
- **Formula:** Response Ratio = (Waiting + Burst) / Burst
- **Best for:** Mix of short and long jobs

### 6. Feedback Scheduling
- **Type:** Preemptive, multi-level
- **Pros:** Adapts to process behavior, favors I/O-bound
- **Cons:** Complex, needs tuning
- **Best for:** General-purpose systems

---

## Exam-Style Questions

### Calculation Problems
1. Given processes with arrivals [0,2,4,6] and bursts [8,4,9,5], calculate:
   - Gantt chart for FCFS
   - Average waiting time
   - Average turnaround time

2. For RR with quantum=3, draw the Gantt chart and calculate metrics

3. Calculate response ratios for HRRN at time t=10

### Conceptual Questions
1. Explain the convoy effect. Which algorithm suffers from it?
2. Why is SRT optimal for minimizing average waiting time?
3. How does feedback scheduling prevent starvation?
4. What are the trade-offs in selecting a time quantum for Round Robin?
5. Compare preemptive vs non-preemptive scheduling

### Analysis Questions
1. A system has 70% I/O-bound and 30% CPU-bound processes. Which algorithm is best?
2. Why might FCFS be preferred despite poor average waiting time?
3. How does aging work in HRRN to prevent starvation?

---

## Tips for Your Exam

1. **Always show your work:**
   - Draw Gantt charts
   - Show calculations for each metric
   - Label clearly

2. **Remember formulas:**
   - Turnaround Time = Completion - Arrival
   - Waiting Time = Turnaround - Burst
   - Response Time = First_Run - Arrival
   - Response Ratio = (Waiting + Burst) / Burst

3. **Check for edge cases:**
   - Processes arriving at different times
   - CPU idle time
   - Process starvation

4. **Practice tracing:**
   - Use this program to verify your manual calculations
   - Compare your answers with program output

5. **Understand trade-offs:**
   - No algorithm is best for everything
   - Know when to use each algorithm

---

## Challenge Exercises

### Challenge 1: Custom Scenario
Create your own test case with 8 processes that demonstrates:
- Convoy effect in FCFS
- Starvation in SPN
- Fair scheduling in RR

### Challenge 2: Manual Calculation Race
1. Get a friend to give you random test data
2. Calculate FCFS, SPN, and RR manually
3. Verify with the program
4. Time yourself - try to get faster!

### Challenge 3: Algorithm Selection
For each scenario, choose the best algorithm and explain why:
1. Web server handling user requests
2. Scientific computing cluster
3. Operating system task scheduler
4. Print queue manager
5. Real-time embedded system

---

## Good Luck with Your Practice! 🚀

Remember: Understanding *why* each algorithm behaves the way it does is more important than just memorizing the steps!
