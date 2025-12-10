# Disk Scheduling & I/O Management Practice Exercises

## How to Use This Practice Program

1. **Compile the program:**
   ```bash
   gcc disk_scheduling_practice.c -o disk_scheduling -lm
   ```

2. **Run the program:**
   ```bash
   ./disk_scheduling
   ```

## Practice Exercise Sets

---

## PART A: DISK SCHEDULING ALGORITHMS

### Exercise 1: Basic FIFO vs SSTF
**Test Data:**
- Initial head position: **50**
- Disk requests (track numbers): **82, 170, 43, 140, 24, 16, 190**

**Questions:**
1. Calculate total head movement for FIFO
2. Calculate total head movement for SSTF
3. Which algorithm is more efficient? By how much?
4. Draw the movement diagram for both

**Expected FIFO Answer:**
- Sequence: 50 → 82 → 170 → 43 → 140 → 24 → 16 → 190
- Movement: 32 + 88 + 127 + 97 + 116 + 8 + 174 = **642 tracks**

**Expected SSTF Answer:**
- Sequence: 50 → 43 → 24 → 16 → 82 → 140 → 170 → 190
- Movement: 7 + 19 + 8 + 66 + 58 + 30 + 20 = **208 tracks**
- SSTF is **67.6% more efficient**

---

### Exercise 2: SCAN Algorithm Understanding
**Test Data:**
- Initial head position: **53**
- Disk requests: **98, 183, 37, 122, 14, 124, 65, 67**
- Disk size: **0-199**
- Initial direction: **Moving toward 0 (left/inward)**

**Questions:**
1. What is the head movement sequence for SCAN?
2. Calculate total head movement
3. Why does SCAN service requests in this order?
4. What happens when the head reaches track 0?

**Expected Answer:**
- Sequence: 53 → 37 → 14 → 0 (reaches end) → 65 → 67 → 98 → 122 → 124 → 183
- Total movement: **236 tracks**
- Services all requests in current direction first, then reverses

---

### Exercise 3: C-SCAN vs SCAN Comparison
**Test Data:**
- Initial head position: **100**
- Disk requests: **50, 20, 80, 150, 175, 15, 90**
- Disk size: **0-199**

**Questions:**
1. Calculate head movement for SCAN (moving right)
2. Calculate head movement for C-SCAN
3. Which is more fair? Why?
4. When would you prefer C-SCAN over SCAN?

**Key Concept:**
- C-SCAN provides more uniform wait time by always scanning in one direction
- SCAN might favor middle tracks over edge tracks

---

### Exercise 4: SSTF Starvation Problem
**Test Data:**
- Initial head position: **100**
- Requests arriving in waves:
  - Wave 1: **95, 105** (arrive at t=0)
  - Wave 2: **98, 102** (arrive at t=5)
  - Wave 3: **99, 101** (arrive at t=10)
  - Wave 4: **30** (arrive at t=0, waiting!)

**Questions:**
1. In what order does SSTF service these requests?
2. When does request 30 finally get serviced?
3. How does this demonstrate the starvation problem?
4. Which algorithm would prevent this?

**Answer:**
- Track 30 keeps getting delayed by newer, closer requests
- SCAN or C-SCAN would prevent starvation

---

### Exercise 5: Algorithm Performance Analysis
**Test Data:**
- Initial head: **50**
- Requests: **10, 22, 20, 2, 40, 6, 38**
- Disk size: **0-49**

**Tasks:**
1. Run all 4 algorithms (FIFO, SSTF, SCAN, C-SCAN)
2. Create a comparison table:
   - Total head movement
   - Average seek distance
   - Best case scenario
   - Worst case scenario
3. Rank algorithms from most to least efficient for this scenario

---

## PART B: I/O BUFFERING

### Exercise 6: Single vs Double Buffer
**Test Data:**
| Request | Data Size (KB) | Arrival Time |
|---------|----------------|--------------|
| 1       | 100            | 0            |
| 2       | 50             | 2            |
| 3       | 75             | 4            |
| 4       | 100            | 6            |

**Buffer size: 50 KB/s transfer rate**

**Questions:**
1. Calculate completion times with single buffer
2. Calculate completion times with double buffer
3. What is the average waiting time for each?
4. When is double buffering most beneficial?

**Expected Single Buffer:**
- R1: 0→2, R2: 2→3, R3: 3→4.5, R4: 4.5→6.5
- Total time: 6.5 units

**Expected Double Buffer:**
- Both buffers can work in parallel
- Reduced waiting time

---

### Exercise 7: Circular Buffer Advantage
**Test Data:**
- 8 I/O requests arriving rapidly
- Buffer size: 25 KB
- Data sizes: All 50 KB each
- Compare: Single (1 buffer) vs Double (2 buffers) vs Circular (4 buffers)

**Questions:**
1. Which configuration completes fastest?
2. Calculate throughput (requests/time) for each
3. What's the optimal number of buffers?
4. When do additional buffers stop helping?

---

### Exercise 8: Buffer Overflow Scenario
**Scenario:**
- You have a real-time data acquisition system
- Data arrives at 100 KB/s
- Processing speed: 80 KB/s
- Buffer size: 500 KB

**Questions:**
1. How long before buffer overflow?
2. How many buffers needed to prevent overflow?
3. What buffering strategy would you use?
4. Calculate minimum buffer size for 10 seconds of safety margin

---

## PART C: RAID CONCEPTS

### Exercise 9: RAID Capacity Calculations
**Scenario:** You have 6 disks, each 1 TB capacity

**Calculate for each RAID level:**
1. **RAID 0:**
   - Total capacity?
   - Usable capacity?
   - Fault tolerance?

2. **RAID 1:**
   - Usable capacity?
   - Capacity efficiency %?
   - How many disk failures can it survive?

3. **RAID 5:**
   - Usable capacity?
   - Parity overhead?
   - Capacity efficiency %?

4. **RAID 6:**
   - Usable capacity?
   - Parity overhead?
   - Capacity efficiency %?

**Answers:**
- RAID 0: 6 TB usable, 100%, no fault tolerance
- RAID 1: 1 TB usable, 16.7%, survives 5 failures
- RAID 5: 5 TB usable, 1 TB parity, 83.3%, survives 1 failure
- RAID 6: 4 TB usable, 2 TB parity, 66.7%, survives 2 failures

---

### Exercise 10: RAID Selection Decision
**Scenarios - Choose the best RAID level:**

1. **Video editing workstation**
   - Needs: Maximum speed for large files
   - Budget: Good, but not unlimited
   - Answer: ? Why?

2. **Financial database server**
   - Needs: Maximum reliability, no data loss
   - Speed: Important but secondary
   - Answer: ? Why?

3. **Web server farm**
   - Needs: Balance of speed and reliability
   - Many random reads/writes
   - Answer: ? Why?

4. **Backup storage**
   - Needs: Maximum capacity
   - Can tolerate some risk
   - Budget: Limited
   - Answer: ? Why?

**Expected Answers:**
1. RAID 0 (speed) or RAID 5 (balance)
2. RAID 1 or RAID 6 (reliability)
3. RAID 5 (good balance)
4. RAID 0 or single disks (capacity priority)

---

### Exercise 11: RAID Rebuild Scenario
**Scenario:**
- RAID 5 array with 5 disks (each 2 TB)
- One disk fails
- Rebuild rate: 100 MB/s

**Questions:**
1. How much data needs to be rebuilt?
2. How long will the rebuild take? (Show calculation)
3. What happens if another disk fails during rebuild?
4. Would RAID 6 be safer? Why?

**Calculation:**
- Data per disk: 2 TB = 2,000,000 MB
- Time = 2,000,000 MB ÷ 100 MB/s = 20,000 seconds ≈ **5.5 hours**
- During rebuild, array is vulnerable
- RAID 6 would survive second failure

---

## PART D: INTEGRATED SCENARIOS

### Exercise 12: Complete System Design
**Scenario:** Design storage for a hospital database system

**Requirements:**
- 10 TB total data
- Must survive 2 disk failures
- 24/7 availability critical
- Moderate budget

**Tasks:**
1. Choose RAID level
2. Calculate number and size of disks needed
3. Justify your choice
4. What disk scheduling algorithm would you use?
5. How many I/O buffers would you configure?

---

### Exercise 13: Performance Optimization
**Given:**
- Database with random access patterns
- 1000 requests/second
- Disk with 200 tracks
- Current algorithm: FIFO
- Average seek time: 10ms

**Questions:**
1. What's the throughput with FIFO?
2. Estimate improvement with SSTF
3. Would SCAN be better? Why or why not?
4. What's the best algorithm for random access?

---

## Key Formulas & Concepts

### Disk Scheduling Metrics
```
Total Head Movement = Σ|position[i+1] - position[i]|
Average Seek Length = Total Movement / Number of Requests
Throughput = Number of Requests / Total Time
```

### I/O Buffering
```
Transfer Time = Data Size / Transfer Rate
Waiting Time = Start Time - Arrival Time
Turnaround Time = Completion Time - Arrival Time
```

### RAID Calculations
```
RAID 0 Capacity = n × disk_size
RAID 1 Capacity = disk_size (for n disks)
RAID 5 Capacity = (n-1) × disk_size
RAID 6 Capacity = (n-2) × disk_size
Efficiency % = (Usable / Total) × 100
```

---

## Quick Reference: Algorithm Characteristics

### Disk Scheduling
| Algorithm | Type | Fairness | Efficiency | Starvation Risk |
|-----------|------|----------|------------|-----------------|
| **FIFO** | Simple | Fair | Low | No |
| **SSTF** | Greedy | Unfair | High | Yes |
| **SCAN** | Elevator | Fair | Good | No |
| **C-SCAN** | Circular | Very Fair | Good | No |

### I/O Organization
| Type | CPU Wait | Efficiency | Complexity |
|------|----------|------------|------------|
| **Programmed I/O** | Yes | Low | Simple |
| **Interrupt-Driven** | No | Medium | Moderate |
| **DMA** | No | High | Complex |

### RAID Levels
| RAID | Redundancy | Capacity | Speed | Cost |
|------|------------|----------|-------|------|
| **0** | None | 100% | Fastest | Low |
| **1** | Full | 50% | Fast reads | High |
| **5** | Parity | (n-1)/n | Balanced | Medium |
| **6** | Dual parity | (n-2)/n | Good | Medium-High |

---

## Exam Tips

### Disk Scheduling Calculations
1. **Always track current head position**
2. **Draw the movement diagram** - visual helps prevent mistakes
3. **Count movements, not positions**
4. **Remember SCAN/C-SCAN go to the edge**

### Common Mistakes to Avoid
- ❌ Forgetting to include initial head position in sequence
- ❌ Calculating positions instead of distances
- ❌ Not considering disk boundaries (0 and max)
- ❌ Mixing up SCAN and C-SCAN behavior

### Quick Checks
✓ Does SSTF always pick the closest request?  
✓ Does SCAN reverse direction at the end?  
✓ Does C-SCAN wrap around without servicing?  
✓ Is RAID 5 efficiency always (n-1)/n?

---

## Practice Strategy

1. **Start with Exercise 1-2** - Master basic calculations
2. **Do Exercise 3-5** - Understand algorithm differences
3. **Work through I/O exercises 6-8** - Learn buffering concepts
4. **Complete RAID exercises 9-11** - Master capacity calculations
5. **Challenge yourself with 12-13** - Integrated scenarios

**Pro tip:** Use the program to verify your manual calculations. This builds confidence and catches errors!

---

## Good Luck! 🎯

Remember: Understanding **why** an algorithm behaves a certain way is more valuable than just memorizing steps!
