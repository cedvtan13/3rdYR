/*
 * Uniprocessor Scheduling Algorithms Practice
 * Chapter 9 - Operating Systems Concepts
 * 
 * This program implements various CPU scheduling algorithms:
 * 1. First-Come-First-Served (FCFS)
 * 2. Round Robin (RR)
 * 3. Shortest Process Next (SPN)
 * 4. Shortest Remaining Time (SRT)
 * 5. Highest Response Ratio Next (HRRN)
 * 6. Feedback Scheduling
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>

#define MAX_PROCESSES 20
#define MAX_QUEUES 4

// Process structure
typedef struct {
    int pid;              // Process ID
    int arrival_time;     // Arrival time
    int burst_time;       // CPU burst time
    int remaining_time;   // Remaining burst time
    int completion_time;  // Completion time
    int turnaround_time;  // Turnaround time
    int waiting_time;     // Waiting time
    int response_time;    // Response time
    int priority;         // Priority level (for feedback)
    bool started;         // Has process started execution
} Process;

// Function prototypes
void initialize_processes(Process processes[], int n);
void copy_processes(Process dest[], Process src[], int n);
void print_results(Process processes[], int n, const char* algorithm);
void calculate_metrics(Process processes[], int n);

// Scheduling algorithm prototypes
void fcfs(Process processes[], int n);
void round_robin(Process processes[], int n, int quantum);
void spn(Process processes[], int n);
void srt(Process processes[], int n);
void hrrn(Process processes[], int n);
void feedback(Process processes[], int n, int num_queues, int quantum);

// Utility functions
void swap_processes(Process *a, Process *b);
int find_next_arrival(Process processes[], int n, int current_time);

int main() {
    int choice, n, quantum, num_queues;
    Process original[MAX_PROCESSES];
    Process temp[MAX_PROCESSES];
    
    printf("=================================================\n");
    printf("   UNIPROCESSOR SCHEDULING ALGORITHMS PRACTICE\n");
    printf("=================================================\n\n");
    
    // Input number of processes
    printf("Enter number of processes (max %d): ", MAX_PROCESSES);
    scanf("%d", &n);
    
    if (n <= 0 || n > MAX_PROCESSES) {
        printf("Invalid number of processes!\n");
        return 1;
    }
    
    // Input process details
    printf("\nEnter process details:\n");
    for (int i = 0; i < n; i++) {
        original[i].pid = i + 1;
        printf("\nProcess %d:\n", i + 1);
        printf("  Arrival Time: ");
        scanf("%d", &original[i].arrival_time);
        printf("  Burst Time: ");
        scanf("%d", &original[i].burst_time);
        original[i].remaining_time = original[i].burst_time;
        original[i].started = false;
        original[i].priority = 0;
    }
    
    do {
        printf("\n=================================================\n");
        printf("           SCHEDULING ALGORITHM MENU\n");
        printf("=================================================\n");
        printf("1. First-Come-First-Served (FCFS)\n");
        printf("2. Round Robin (RR)\n");
        printf("3. Shortest Process Next (SPN)\n");
        printf("4. Shortest Remaining Time (SRT)\n");
        printf("5. Highest Response Ratio Next (HRRN)\n");
        printf("6. Feedback Scheduling\n");
        printf("7. Run All Algorithms (Comparison)\n");
        printf("0. Exit\n");
        printf("=================================================\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);
        
        copy_processes(temp, original, n);
        
        switch(choice) {
            case 1:
                printf("\n--- FIRST-COME-FIRST-SERVED (FCFS) ---\n");
                fcfs(temp, n);
                print_results(temp, n, "FCFS");
                break;
                
            case 2:
                printf("\nEnter time quantum: ");
                scanf("%d", &quantum);
                printf("\n--- ROUND ROBIN (Quantum = %d) ---\n", quantum);
                round_robin(temp, n, quantum);
                print_results(temp, n, "Round Robin");
                break;
                
            case 3:
                printf("\n--- SHORTEST PROCESS NEXT (SPN) ---\n");
                spn(temp, n);
                print_results(temp, n, "SPN");
                break;
                
            case 4:
                printf("\n--- SHORTEST REMAINING TIME (SRT) ---\n");
                srt(temp, n);
                print_results(temp, n, "SRT");
                break;
                
            case 5:
                printf("\n--- HIGHEST RESPONSE RATIO NEXT (HRRN) ---\n");
                hrrn(temp, n);
                print_results(temp, n, "HRRN");
                break;
                
            case 6:
                printf("\nEnter number of queues (2-%d): ", MAX_QUEUES);
                scanf("%d", &num_queues);
                printf("Enter time quantum: ");
                scanf("%d", &quantum);
                printf("\n--- FEEDBACK SCHEDULING ---\n");
                feedback(temp, n, num_queues, quantum);
                print_results(temp, n, "Feedback");
                break;
                
            case 7:
                printf("\n========== ALGORITHM COMPARISON ==========\n");
                
                copy_processes(temp, original, n);
                fcfs(temp, n);
                print_results(temp, n, "FCFS");
                
                copy_processes(temp, original, n);
                round_robin(temp, n, 2);
                print_results(temp, n, "Round Robin (q=2)");
                
                copy_processes(temp, original, n);
                spn(temp, n);
                print_results(temp, n, "SPN");
                
                copy_processes(temp, original, n);
                srt(temp, n);
                print_results(temp, n, "SRT");
                
                copy_processes(temp, original, n);
                hrrn(temp, n);
                print_results(temp, n, "HRRN");
                
                break;
                
            case 0:
                printf("\nExiting program. Good luck with your practice!\n");
                break;
                
            default:
                printf("\nInvalid choice! Please try again.\n");
        }
    } while (choice != 0);
    
    return 0;
}

// Copy processes from source to destination
void copy_processes(Process dest[], Process src[], int n) {
    for (int i = 0; i < n; i++) {
        dest[i] = src[i];
    }
}

// Swap two processes
void swap_processes(Process *a, Process *b) {
    Process temp = *a;
    *a = *b;
    *b = temp;
}

// 1. FIRST-COME-FIRST-SERVED (FCFS)
void fcfs(Process processes[], int n) {
    // Sort by arrival time
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (processes[j].arrival_time > processes[j + 1].arrival_time) {
                swap_processes(&processes[j], &processes[j + 1]);
            }
        }
    }
    
    int current_time = 0;
    
    for (int i = 0; i < n; i++) {
        // If CPU is idle, jump to next process arrival
        if (current_time < processes[i].arrival_time) {
            current_time = processes[i].arrival_time;
        }
        
        // Response time (first time process gets CPU)
        processes[i].response_time = current_time - processes[i].arrival_time;
        
        // Execute process
        current_time += processes[i].burst_time;
        
        // Completion time
        processes[i].completion_time = current_time;
        
        // Turnaround time = Completion - Arrival
        processes[i].turnaround_time = processes[i].completion_time - processes[i].arrival_time;
        
        // Waiting time = Turnaround - Burst
        processes[i].waiting_time = processes[i].turnaround_time - processes[i].burst_time;
    }
}

// 2. ROUND ROBIN (RR)
void round_robin(Process processes[], int n, int quantum) {
    int current_time = 0;
    int completed = 0;
    int queue[MAX_PROCESSES];
    int front = 0, rear = 0;
    bool in_queue[MAX_PROCESSES] = {false};
    
    // Find first process to arrive
    int min_arrival = processes[0].arrival_time;
    for (int i = 1; i < n; i++) {
        if (processes[i].arrival_time < min_arrival) {
            min_arrival = processes[i].arrival_time;
        }
    }
    current_time = min_arrival;
    
    // Add all processes that have arrived at time 0
    for (int i = 0; i < n; i++) {
        if (processes[i].arrival_time <= current_time) {
            queue[rear++] = i;
            in_queue[i] = true;
        }
    }
    
    while (completed < n) {
        if (front == rear) {
            // Queue is empty, jump to next arrival
            int next_arrival = INT_MAX;
            for (int i = 0; i < n; i++) {
                if (processes[i].remaining_time > 0 && processes[i].arrival_time > current_time) {
                    if (processes[i].arrival_time < next_arrival) {
                        next_arrival = processes[i].arrival_time;
                    }
                }
            }
            if (next_arrival != INT_MAX) {
                current_time = next_arrival;
                for (int i = 0; i < n; i++) {
                    if (processes[i].arrival_time <= current_time && 
                        processes[i].remaining_time > 0 && !in_queue[i]) {
                        queue[rear++] = i;
                        in_queue[i] = true;
                    }
                }
            }
            continue;
        }
        
        int idx = queue[front++];
        in_queue[idx] = false;
        
        // Record response time on first execution
        if (!processes[idx].started) {
            processes[idx].response_time = current_time - processes[idx].arrival_time;
            processes[idx].started = true;
        }
        
        // Execute for quantum or remaining time, whichever is smaller
        int exec_time = (processes[idx].remaining_time < quantum) ? 
                        processes[idx].remaining_time : quantum;
        
        processes[idx].remaining_time -= exec_time;
        current_time += exec_time;
        
        // Check for new arrivals during execution
        for (int i = 0; i < n; i++) {
            if (processes[i].arrival_time <= current_time && 
                processes[i].remaining_time > 0 && !in_queue[i] && i != idx) {
                queue[rear++] = i;
                in_queue[i] = true;
            }
        }
        
        // If process is complete
        if (processes[idx].remaining_time == 0) {
            processes[idx].completion_time = current_time;
            processes[idx].turnaround_time = processes[idx].completion_time - processes[idx].arrival_time;
            processes[idx].waiting_time = processes[idx].turnaround_time - processes[idx].burst_time;
            completed++;
        } else {
            // Add back to queue if not finished
            queue[rear++] = idx;
            in_queue[idx] = true;
        }
    }
}

// 3. SHORTEST PROCESS NEXT (SPN) - Non-preemptive
void spn(Process processes[], int n) {
    int current_time = 0;
    int completed = 0;
    bool is_completed[MAX_PROCESSES] = {false};
    
    while (completed < n) {
        int shortest_idx = -1;
        int shortest_burst = INT_MAX;
        
        // Find process with shortest burst time that has arrived
        for (int i = 0; i < n; i++) {
            if (!is_completed[i] && processes[i].arrival_time <= current_time) {
                if (processes[i].burst_time < shortest_burst) {
                    shortest_burst = processes[i].burst_time;
                    shortest_idx = i;
                }
            }
        }
        
        if (shortest_idx == -1) {
            // No process available, jump to next arrival
            int next_arrival = INT_MAX;
            for (int i = 0; i < n; i++) {
                if (!is_completed[i] && processes[i].arrival_time > current_time) {
                    if (processes[i].arrival_time < next_arrival) {
                        next_arrival = processes[i].arrival_time;
                    }
                }
            }
            current_time = next_arrival;
            continue;
        }
        
        // Execute the shortest process
        processes[shortest_idx].response_time = current_time - processes[shortest_idx].arrival_time;
        current_time += processes[shortest_idx].burst_time;
        processes[shortest_idx].completion_time = current_time;
        processes[shortest_idx].turnaround_time = 
            processes[shortest_idx].completion_time - processes[shortest_idx].arrival_time;
        processes[shortest_idx].waiting_time = 
            processes[shortest_idx].turnaround_time - processes[shortest_idx].burst_time;
        
        is_completed[shortest_idx] = true;
        completed++;
    }
}

// 4. SHORTEST REMAINING TIME (SRT) - Preemptive SPN
void srt(Process processes[], int n) {
    int current_time = 0;
    int completed = 0;
    int prev_process = -1;
    
    while (completed < n) {
        int shortest_idx = -1;
        int shortest_remaining = INT_MAX;
        
        // Find process with shortest remaining time
        for (int i = 0; i < n; i++) {
            if (processes[i].arrival_time <= current_time && processes[i].remaining_time > 0) {
                if (processes[i].remaining_time < shortest_remaining) {
                    shortest_remaining = processes[i].remaining_time;
                    shortest_idx = i;
                }
            }
        }
        
        if (shortest_idx == -1) {
            // No process available, jump to next arrival
            int next_arrival = INT_MAX;
            for (int i = 0; i < n; i++) {
                if (processes[i].remaining_time > 0 && processes[i].arrival_time > current_time) {
                    if (processes[i].arrival_time < next_arrival) {
                        next_arrival = processes[i].arrival_time;
                    }
                }
            }
            current_time = next_arrival;
            continue;
        }
        
        // Record response time when process first starts
        if (!processes[shortest_idx].started) {
            processes[shortest_idx].response_time = current_time - processes[shortest_idx].arrival_time;
            processes[shortest_idx].started = true;
        }
        
        // Execute for 1 time unit
        processes[shortest_idx].remaining_time--;
        current_time++;
        
        // Check if process completed
        if (processes[shortest_idx].remaining_time == 0) {
            processes[shortest_idx].completion_time = current_time;
            processes[shortest_idx].turnaround_time = 
                processes[shortest_idx].completion_time - processes[shortest_idx].arrival_time;
            processes[shortest_idx].waiting_time = 
                processes[shortest_idx].turnaround_time - processes[shortest_idx].burst_time;
            completed++;
        }
    }
}

// 5. HIGHEST RESPONSE RATIO NEXT (HRRN)
void hrrn(Process processes[], int n) {
    int current_time = 0;
    int completed = 0;
    bool is_completed[MAX_PROCESSES] = {false};
    
    while (completed < n) {
        int selected_idx = -1;
        double highest_ratio = -1;
        
        // Calculate response ratio for all waiting processes
        // Response Ratio = (Waiting Time + Burst Time) / Burst Time
        for (int i = 0; i < n; i++) {
            if (!is_completed[i] && processes[i].arrival_time <= current_time) {
                int waiting = current_time - processes[i].arrival_time;
                double ratio = (double)(waiting + processes[i].burst_time) / processes[i].burst_time;
                
                if (ratio > highest_ratio) {
                    highest_ratio = ratio;
                    selected_idx = i;
                }
            }
        }
        
        if (selected_idx == -1) {
            // No process available, jump to next arrival
            int next_arrival = INT_MAX;
            for (int i = 0; i < n; i++) {
                if (!is_completed[i] && processes[i].arrival_time > current_time) {
                    if (processes[i].arrival_time < next_arrival) {
                        next_arrival = processes[i].arrival_time;
                    }
                }
            }
            current_time = next_arrival;
            continue;
        }
        
        // Execute selected process
        processes[selected_idx].response_time = current_time - processes[selected_idx].arrival_time;
        current_time += processes[selected_idx].burst_time;
        processes[selected_idx].completion_time = current_time;
        processes[selected_idx].turnaround_time = 
            processes[selected_idx].completion_time - processes[selected_idx].arrival_time;
        processes[selected_idx].waiting_time = 
            processes[selected_idx].turnaround_time - processes[selected_idx].burst_time;
        
        is_completed[selected_idx] = true;
        completed++;
    }
}

// 6. FEEDBACK SCHEDULING (Multi-level feedback queue)
void feedback(Process processes[], int n, int num_queues, int quantum) {
    int current_time = 0;
    int completed = 0;
    
    // Initialize process priorities (queue levels)
    for (int i = 0; i < n; i++) {
        processes[i].priority = 0; // Start at highest priority queue
    }
    
    while (completed < n) {
        int selected_idx = -1;
        int highest_priority = num_queues;
        
        // Find highest priority process that has arrived and not completed
        for (int i = 0; i < n; i++) {
            if (processes[i].arrival_time <= current_time && processes[i].remaining_time > 0) {
                if (processes[i].priority < highest_priority) {
                    highest_priority = processes[i].priority;
                    selected_idx = i;
                } else if (processes[i].priority == highest_priority && selected_idx != -1) {
                    // FCFS within same priority
                    if (processes[i].arrival_time < processes[selected_idx].arrival_time) {
                        selected_idx = i;
                    }
                }
            }
        }
        
        if (selected_idx == -1) {
            // No process available, jump to next arrival
            int next_arrival = INT_MAX;
            for (int i = 0; i < n; i++) {
                if (processes[i].remaining_time > 0 && processes[i].arrival_time > current_time) {
                    if (processes[i].arrival_time < next_arrival) {
                        next_arrival = processes[i].arrival_time;
                    }
                }
            }
            current_time = next_arrival;
            continue;
        }
        
        // Record response time
        if (!processes[selected_idx].started) {
            processes[selected_idx].response_time = current_time - processes[selected_idx].arrival_time;
            processes[selected_idx].started = true;
        }
        
        // Execute for quantum or remaining time
        int exec_time = (processes[selected_idx].remaining_time < quantum) ? 
                        processes[selected_idx].remaining_time : quantum;
        
        processes[selected_idx].remaining_time -= exec_time;
        current_time += exec_time;
        
        // If process completed
        if (processes[selected_idx].remaining_time == 0) {
            processes[selected_idx].completion_time = current_time;
            processes[selected_idx].turnaround_time = 
                processes[selected_idx].completion_time - processes[selected_idx].arrival_time;
            processes[selected_idx].waiting_time = 
                processes[selected_idx].turnaround_time - processes[selected_idx].burst_time;
            completed++;
        } else {
            // Demote to lower priority queue (penalty for long jobs)
            if (processes[selected_idx].priority < num_queues - 1) {
                processes[selected_idx].priority++;
            }
        }
    }
}

// Print results and calculate average metrics
void print_results(Process processes[], int n, const char* algorithm) {
    printf("\n%-10s %-10s %-10s %-15s %-15s %-15s %-15s\n", 
           "PID", "Arrival", "Burst", "Completion", "Turnaround", "Waiting", "Response");
    printf("------------------------------------------------------------------------------------\n");
    
    double avg_turnaround = 0, avg_waiting = 0, avg_response = 0;
    
    for (int i = 0; i < n; i++) {
        printf("P%-9d %-10d %-10d %-15d %-15d %-15d %-15d\n",
               processes[i].pid,
               processes[i].arrival_time,
               processes[i].burst_time,
               processes[i].completion_time,
               processes[i].turnaround_time,
               processes[i].waiting_time,
               processes[i].response_time);
        
        avg_turnaround += processes[i].turnaround_time;
        avg_waiting += processes[i].waiting_time;
        avg_response += processes[i].response_time;
    }
    
    avg_turnaround /= n;
    avg_waiting /= n;
    avg_response /= n;
    
    printf("------------------------------------------------------------------------------------\n");
    printf("Average Turnaround Time: %.2f\n", avg_turnaround);
    printf("Average Waiting Time: %.2f\n", avg_waiting);
    printf("Average Response Time: %.2f\n", avg_response);
    printf("\n");
}
