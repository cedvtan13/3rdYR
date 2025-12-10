/*
 * Disk Scheduling and I/O Management Practice
 * Chapter 11 - Operating Systems Concepts
 * 
 * This program implements:
 * 1. Disk Scheduling Algorithms (FIFO, SSTF, SCAN, C-SCAN)
 * 2. I/O Buffering Simulation (Single, Double, Circular)
 * 3. RAID Concepts and Calculations
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>

#define MAX_REQUESTS 50
#define MAX_TRACKS 200
#define MAX_BUFFER_SIZE 10

// Disk request structure
typedef struct {
    int track_number;
    int arrival_order;
} DiskRequest;

// I/O Request structure for buffering
typedef struct {
    int request_id;
    int data_size;
    double arrival_time;
    double completion_time;
} IORequest;

// Function prototypes - Disk Scheduling
void fifo_disk(int requests[], int n, int initial_head);
void sstf_disk(int requests[], int n, int initial_head);
void scan_disk(int requests[], int n, int initial_head, int disk_size, int direction);
void cscan_disk(int requests[], int n, int initial_head, int disk_size);

// Function prototypes - I/O Buffering
void single_buffer_simulation(IORequest requests[], int n, int buffer_size);
void double_buffer_simulation(IORequest requests[], int n, int buffer_size);
void circular_buffer_simulation(IORequest requests[], int n, int buffer_size, int num_buffers);

// Function prototypes - RAID
void raid_calculator();

// Utility functions
void print_disk_schedule(int sequence[], int n, int total_head_movement);
int calculate_total_movement(int sequence[], int n);
void copy_requests(int dest[], int src[], int n);
int abs_diff(int a, int b);

int main() {
    int choice, n, initial_head, disk_size, direction;
    int requests[MAX_REQUESTS];
    IORequest io_requests[MAX_REQUESTS];
    
    printf("=================================================\n");
    printf("   DISK SCHEDULING & I/O MANAGEMENT PRACTICE\n");
    printf("=================================================\n\n");
    
    do {
        printf("\n=================================================\n");
        printf("                 MAIN MENU\n");
        printf("=================================================\n");
        printf("DISK SCHEDULING ALGORITHMS:\n");
        printf("1. FIFO (First-In-First-Out)\n");
        printf("2. SSTF (Shortest Seek Time First)\n");
        printf("3. SCAN (Elevator Algorithm)\n");
        printf("4. C-SCAN (Circular SCAN)\n");
        printf("5. Compare All Disk Scheduling Algorithms\n");
        printf("\nI/O BUFFERING:\n");
        printf("6. Single Buffer Simulation\n");
        printf("7. Double Buffer Simulation\n");
        printf("8. Circular Buffer Simulation\n");
        printf("\nRAID:\n");
        printf("9. RAID Calculator & Information\n");
        printf("\n0. Exit\n");
        printf("=================================================\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);
        
        switch(choice) {
            case 1:
            case 2:
            case 3:
            case 4:
            case 5:
                // Input disk requests
                printf("\nEnter number of disk requests (max %d): ", MAX_REQUESTS);
                scanf("%d", &n);
                
                if (n <= 0 || n > MAX_REQUESTS) {
                    printf("Invalid number of requests!\n");
                    break;
                }
                
                printf("Enter initial head position: ");
                scanf("%d", &initial_head);
                
                printf("Enter disk requests (track numbers):\n");
                for (int i = 0; i < n; i++) {
                    printf("  Request %d: ", i + 1);
                    scanf("%d", &requests[i]);
                }
                
                if (choice == 3 || choice == 4 || choice == 5) {
                    printf("Enter disk size (max track number): ");
                    scanf("%d", &disk_size);
                }
                
                if (choice == 3) {
                    printf("Enter initial direction (0=left/inward, 1=right/outward): ");
                    scanf("%d", &direction);
                }
                
                // Execute chosen algorithm
                if (choice == 1) {
                    printf("\n--- FIFO DISK SCHEDULING ---\n");
                    fifo_disk(requests, n, initial_head);
                } else if (choice == 2) {
                    printf("\n--- SSTF DISK SCHEDULING ---\n");
                    sstf_disk(requests, n, initial_head);
                } else if (choice == 3) {
                    printf("\n--- SCAN DISK SCHEDULING ---\n");
                    scan_disk(requests, n, initial_head, disk_size, direction);
                } else if (choice == 4) {
                    printf("\n--- C-SCAN DISK SCHEDULING ---\n");
                    cscan_disk(requests, n, initial_head, disk_size);
                } else if (choice == 5) {
                    printf("\n========== DISK SCHEDULING COMPARISON ==========\n");
                    
                    printf("\n--- FIFO ---\n");
                    fifo_disk(requests, n, initial_head);
                    
                    printf("\n--- SSTF ---\n");
                    sstf_disk(requests, n, initial_head);
                    
                    printf("\n--- SCAN (moving right) ---\n");
                    scan_disk(requests, n, initial_head, disk_size, 1);
                    
                    printf("\n--- C-SCAN ---\n");
                    cscan_disk(requests, n, initial_head, disk_size);
                }
                break;
                
            case 6:
            case 7:
            case 8:
                printf("\nEnter number of I/O requests: ");
                scanf("%d", &n);
                
                if (n <= 0 || n > MAX_REQUESTS) {
                    printf("Invalid number of requests!\n");
                    break;
                }
                
                printf("Enter I/O requests:\n");
                for (int i = 0; i < n; i++) {
                    io_requests[i].request_id = i + 1;
                    printf("  Request %d - Data size (KB): ", i + 1);
                    scanf("%d", &io_requests[i].data_size);
                    printf("  Request %d - Arrival time: ", i + 1);
                    scanf("%lf", &io_requests[i].arrival_time);
                }
                
                int buffer_size;
                printf("Enter buffer size (KB): ");
                scanf("%d", &buffer_size);
                
                if (choice == 6) {
                    printf("\n--- SINGLE BUFFER SIMULATION ---\n");
                    single_buffer_simulation(io_requests, n, buffer_size);
                } else if (choice == 7) {
                    printf("\n--- DOUBLE BUFFER SIMULATION ---\n");
                    double_buffer_simulation(io_requests, n, buffer_size);
                } else if (choice == 8) {
                    int num_buffers;
                    printf("Enter number of circular buffers: ");
                    scanf("%d", &num_buffers);
                    printf("\n--- CIRCULAR BUFFER SIMULATION ---\n");
                    circular_buffer_simulation(io_requests, n, buffer_size, num_buffers);
                }
                break;
                
            case 9:
                raid_calculator();
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

// Utility function: absolute difference
int abs_diff(int a, int b) {
    return abs(a - b);
}

// Copy requests array
void copy_requests(int dest[], int src[], int n) {
    for (int i = 0; i < n; i++) {
        dest[i] = src[i];
    }
}

// Calculate total head movement
int calculate_total_movement(int sequence[], int n) {
    int total = 0;
    for (int i = 0; i < n - 1; i++) {
        total += abs_diff(sequence[i], sequence[i + 1]);
    }
    return total;
}

// Print disk scheduling results
void print_disk_schedule(int sequence[], int n, int total_head_movement) {
    printf("\nDisk Head Movement Sequence:\n");
    printf("Track: ");
    for (int i = 0; i < n; i++) {
        printf("%d", sequence[i]);
        if (i < n - 1) printf(" -> ");
    }
    printf("\n\nSeek Sequence:\n");
    for (int i = 0; i < n - 1; i++) {
        int movement = abs_diff(sequence[i], sequence[i + 1]);
        printf("  %d to %d: %d tracks\n", sequence[i], sequence[i + 1], movement);
    }
    printf("\n----------------------------------------\n");
    printf("Total Head Movement: %d tracks\n", total_head_movement);
    printf("Average Seek Length: %.2f tracks\n", (double)total_head_movement / (n - 1));
    printf("----------------------------------------\n");
}

// 1. FIFO (First-In-First-Out) Disk Scheduling
void fifo_disk(int requests[], int n, int initial_head) {
    int sequence[MAX_REQUESTS + 1];
    sequence[0] = initial_head;
    
    // Simply process requests in order of arrival
    for (int i = 0; i < n; i++) {
        sequence[i + 1] = requests[i];
    }
    
    int total_movement = calculate_total_movement(sequence, n + 1);
    print_disk_schedule(sequence, n + 1, total_movement);
}

// 2. SSTF (Shortest Seek Time First) Disk Scheduling
void sstf_disk(int requests[], int n, int initial_head) {
    int sequence[MAX_REQUESTS + 1];
    bool serviced[MAX_REQUESTS] = {false};
    int current_head = initial_head;
    sequence[0] = initial_head;
    
    // Service requests in order of shortest seek time
    for (int count = 0; count < n; count++) {
        int min_seek = 999999;
        int min_index = -1;
        
        // Find closest unserviced request
        for (int i = 0; i < n; i++) {
            if (!serviced[i]) {
                int seek_distance = abs_diff(current_head, requests[i]);
                if (seek_distance < min_seek) {
                    min_seek = seek_distance;
                    min_index = i;
                }
            }
        }
        
        // Service the closest request
        serviced[min_index] = true;
        current_head = requests[min_index];
        sequence[count + 1] = current_head;
    }
    
    int total_movement = calculate_total_movement(sequence, n + 1);
    print_disk_schedule(sequence, n + 1, total_movement);
}

// 3. SCAN (Elevator) Disk Scheduling
void scan_disk(int requests[], int n, int initial_head, int disk_size, int direction) {
    int sequence[MAX_REQUESTS + 3];
    int seq_index = 0;
    bool serviced[MAX_REQUESTS] = {false};
    int current_head = initial_head;
    sequence[seq_index++] = initial_head;
    
    // If moving right (outward)
    if (direction == 1) {
        // Service all requests from current position to end
        while (1) {
            int next_request = -1;
            int min_distance = 999999;
            
            // Find next request in the right direction
            for (int i = 0; i < n; i++) {
                if (!serviced[i] && requests[i] >= current_head) {
                    int distance = requests[i] - current_head;
                    if (distance < min_distance) {
                        min_distance = distance;
                        next_request = i;
                    }
                }
            }
            
            if (next_request == -1) break;
            
            serviced[next_request] = true;
            current_head = requests[next_request];
            sequence[seq_index++] = current_head;
        }
        
        // If head needs to go to the end (if there were requests beyond)
        bool has_right_requests = false;
        for (int i = 0; i < n; i++) {
            if (requests[i] > initial_head) {
                has_right_requests = true;
                break;
            }
        }
        
        // Now reverse and service remaining requests
        while (1) {
            int next_request = -1;
            int min_distance = 999999;
            
            for (int i = 0; i < n; i++) {
                if (!serviced[i]) {
                    int distance = current_head - requests[i];
                    if (distance > 0 && distance < min_distance) {
                        min_distance = distance;
                        next_request = i;
                    }
                }
            }
            
            if (next_request == -1) break;
            
            serviced[next_request] = true;
            current_head = requests[next_request];
            sequence[seq_index++] = current_head;
        }
    } else {
        // Moving left (inward) - service requests from current to 0, then reverse
        while (1) {
            int next_request = -1;
            int min_distance = 999999;
            
            for (int i = 0; i < n; i++) {
                if (!serviced[i] && requests[i] <= current_head) {
                    int distance = current_head - requests[i];
                    if (distance < min_distance) {
                        min_distance = distance;
                        next_request = i;
                    }
                }
            }
            
            if (next_request == -1) break;
            
            serviced[next_request] = true;
            current_head = requests[next_request];
            sequence[seq_index++] = current_head;
        }
        
        // Now reverse and service remaining requests
        while (1) {
            int next_request = -1;
            int min_distance = 999999;
            
            for (int i = 0; i < n; i++) {
                if (!serviced[i]) {
                    int distance = requests[i] - current_head;
                    if (distance > 0 && distance < min_distance) {
                        min_distance = distance;
                        next_request = i;
                    }
                }
            }
            
            if (next_request == -1) break;
            
            serviced[next_request] = true;
            current_head = requests[next_request];
            sequence[seq_index++] = current_head;
        }
    }
    
    int total_movement = calculate_total_movement(sequence, seq_index);
    print_disk_schedule(sequence, seq_index, total_movement);
}

// 4. C-SCAN (Circular SCAN) Disk Scheduling
void cscan_disk(int requests[], int n, int initial_head, int disk_size) {
    int sequence[MAX_REQUESTS + 3];
    int seq_index = 0;
    bool serviced[MAX_REQUESTS] = {false};
    int current_head = initial_head;
    sequence[seq_index++] = initial_head;
    
    // Service all requests from current position to end (moving right)
    while (1) {
        int next_request = -1;
        int min_distance = 999999;
        
        for (int i = 0; i < n; i++) {
            if (!serviced[i] && requests[i] >= current_head) {
                int distance = requests[i] - current_head;
                if (distance < min_distance) {
                    min_distance = distance;
                    next_request = i;
                }
            }
        }
        
        if (next_request == -1) break;
        
        serviced[next_request] = true;
        current_head = requests[next_request];
        sequence[seq_index++] = current_head;
    }
    
    // Jump to beginning (track 0) and continue
    bool has_left_requests = false;
    for (int i = 0; i < n; i++) {
        if (!serviced[i]) {
            has_left_requests = true;
            break;
        }
    }
    
    if (has_left_requests) {
        // Move to end then to beginning
        if (current_head != disk_size - 1) {
            sequence[seq_index++] = disk_size - 1;
            current_head = disk_size - 1;
        }
        sequence[seq_index++] = 0;
        current_head = 0;
        
        // Service remaining requests from beginning
        while (1) {
            int next_request = -1;
            int min_distance = 999999;
            
            for (int i = 0; i < n; i++) {
                if (!serviced[i] && requests[i] >= current_head) {
                    int distance = requests[i] - current_head;
                    if (distance < min_distance) {
                        min_distance = distance;
                        next_request = i;
                    }
                }
            }
            
            if (next_request == -1) break;
            
            serviced[next_request] = true;
            current_head = requests[next_request];
            sequence[seq_index++] = current_head;
        }
    }
    
    int total_movement = calculate_total_movement(sequence, seq_index);
    print_disk_schedule(sequence, seq_index, total_movement);
}

// I/O BUFFERING SIMULATIONS

// Single Buffer Simulation
void single_buffer_simulation(IORequest requests[], int n, int buffer_size) {
    printf("\nSingle Buffer Simulation:\n");
    printf("Buffer Size: %d KB\n\n", buffer_size);
    
    double current_time = 0;
    double total_waiting_time = 0;
    
    printf("%-10s %-12s %-15s %-15s %-15s\n", 
           "Request", "Data Size", "Arrival", "Start Time", "Completion");
    printf("--------------------------------------------------------------------\n");
    
    for (int i = 0; i < n; i++) {
        // Request must wait if it arrives before buffer is free
        double start_time = (current_time > requests[i].arrival_time) ? 
                           current_time : requests[i].arrival_time;
        
        // Transfer time based on data size and buffer size
        double transfer_time = (double)requests[i].data_size / buffer_size;
        double completion_time = start_time + transfer_time;
        
        requests[i].completion_time = completion_time;
        total_waiting_time += (start_time - requests[i].arrival_time);
        
        printf("%-10d %-12d %-15.2f %-15.2f %-15.2f\n",
               requests[i].request_id,
               requests[i].data_size,
               requests[i].arrival_time,
               start_time,
               completion_time);
        
        current_time = completion_time;
    }
    
    printf("\n----------------------------------------\n");
    printf("Average Waiting Time: %.2f time units\n", total_waiting_time / n);
    printf("Total Completion Time: %.2f time units\n", current_time);
    printf("----------------------------------------\n");
}

// Double Buffer Simulation
void double_buffer_simulation(IORequest requests[], int n, int buffer_size) {
    printf("\nDouble Buffer Simulation:\n");
    printf("Buffer Size: %d KB (x2 buffers)\n\n", buffer_size);
    
    double buffer1_free_time = 0;
    double buffer2_free_time = 0;
    double total_waiting_time = 0;
    
    printf("%-10s %-12s %-15s %-15s %-15s %-15s\n", 
           "Request", "Data Size", "Arrival", "Buffer Used", "Start Time", "Completion");
    printf("---------------------------------------------------------------------------------\n");
    
    for (int i = 0; i < n; i++) {
        // Choose the buffer that becomes free first
        int buffer_used;
        double start_time;
        
        if (buffer1_free_time <= buffer2_free_time) {
            buffer_used = 1;
            start_time = (buffer1_free_time > requests[i].arrival_time) ? 
                        buffer1_free_time : requests[i].arrival_time;
            double transfer_time = (double)requests[i].data_size / buffer_size;
            double completion_time = start_time + transfer_time;
            buffer1_free_time = completion_time;
            requests[i].completion_time = completion_time;
        } else {
            buffer_used = 2;
            start_time = (buffer2_free_time > requests[i].arrival_time) ? 
                        buffer2_free_time : requests[i].arrival_time;
            double transfer_time = (double)requests[i].data_size / buffer_size;
            double completion_time = start_time + transfer_time;
            buffer2_free_time = completion_time;
            requests[i].completion_time = completion_time;
        }
        
        total_waiting_time += (start_time - requests[i].arrival_time);
        
        printf("%-10d %-12d %-15.2f %-15d %-15.2f %-15.2f\n",
               requests[i].request_id,
               requests[i].data_size,
               requests[i].arrival_time,
               buffer_used,
               start_time,
               requests[i].completion_time);
    }
    
    printf("\n----------------------------------------\n");
    printf("Average Waiting Time: %.2f time units\n", total_waiting_time / n);
    printf("Total Completion Time: %.2f time units\n", 
           (buffer1_free_time > buffer2_free_time) ? buffer1_free_time : buffer2_free_time);
    printf("----------------------------------------\n");
}

// Circular Buffer Simulation
void circular_buffer_simulation(IORequest requests[], int n, int buffer_size, int num_buffers) {
    printf("\nCircular Buffer Simulation:\n");
    printf("Buffer Size: %d KB (x%d buffers)\n\n", buffer_size, num_buffers);
    
    double buffer_free_time[MAX_BUFFER_SIZE] = {0};
    double total_waiting_time = 0;
    
    printf("%-10s %-12s %-15s %-15s %-15s %-15s\n", 
           "Request", "Data Size", "Arrival", "Buffer Used", "Start Time", "Completion");
    printf("---------------------------------------------------------------------------------\n");
    
    for (int i = 0; i < n; i++) {
        // Find the buffer that becomes free first
        int selected_buffer = 0;
        double min_free_time = buffer_free_time[0];
        
        for (int j = 1; j < num_buffers; j++) {
            if (buffer_free_time[j] < min_free_time) {
                min_free_time = buffer_free_time[j];
                selected_buffer = j;
            }
        }
        
        double start_time = (buffer_free_time[selected_buffer] > requests[i].arrival_time) ? 
                           buffer_free_time[selected_buffer] : requests[i].arrival_time;
        double transfer_time = (double)requests[i].data_size / buffer_size;
        double completion_time = start_time + transfer_time;
        
        buffer_free_time[selected_buffer] = completion_time;
        requests[i].completion_time = completion_time;
        total_waiting_time += (start_time - requests[i].arrival_time);
        
        printf("%-10d %-12d %-15.2f %-15d %-15.2f %-15.2f\n",
               requests[i].request_id,
               requests[i].data_size,
               requests[i].arrival_time,
               selected_buffer + 1,
               start_time,
               completion_time);
    }
    
    // Find max completion time
    double max_completion = buffer_free_time[0];
    for (int i = 1; i < num_buffers; i++) {
        if (buffer_free_time[i] > max_completion) {
            max_completion = buffer_free_time[i];
        }
    }
    
    printf("\n----------------------------------------\n");
    printf("Average Waiting Time: %.2f time units\n", total_waiting_time / n);
    printf("Total Completion Time: %.2f time units\n", max_completion);
    printf("----------------------------------------\n");
}

// RAID Calculator and Information
void raid_calculator() {
    int raid_choice;
    
    printf("\n=================================================\n");
    printf("              RAID INFORMATION\n");
    printf("=================================================\n\n");
    
    printf("RAID Levels:\n");
    printf("1. RAID 0 (Striping) - High performance, no redundancy\n");
    printf("2. RAID 1 (Mirroring) - Full redundancy, 50%% capacity\n");
    printf("3. RAID 5 (Distributed Parity) - Good balance\n");
    printf("4. RAID 6 (Dual Parity) - High redundancy\n");
    printf("5. RAID Comparison\n");
    printf("0. Back to main menu\n");
    printf("\nEnter choice: ");
    scanf("%d", &raid_choice);
    
    if (raid_choice == 0) return;
    
    int num_disks;
    double disk_capacity;
    
    if (raid_choice >= 1 && raid_choice <= 4) {
        printf("\nEnter number of disks: ");
        scanf("%d", &num_disks);
        printf("Enter capacity of each disk (GB): ");
        scanf("%lf", &disk_capacity);
    }
    
    printf("\n");
    
    switch(raid_choice) {
        case 1:
            printf("--- RAID 0 (STRIPING) ---\n");
            printf("Total Raw Capacity: %.2f GB\n", num_disks * disk_capacity);
            printf("Usable Capacity: %.2f GB\n", num_disks * disk_capacity);
            printf("Capacity Efficiency: 100%%\n");
            printf("Fault Tolerance: None (any disk failure = data loss)\n");
            printf("Min Disks Required: 2\n");
            printf("Performance: Excellent (parallel reads/writes)\n");
            printf("Best For: High-performance applications (video editing)\n");
            break;
            
        case 2:
            printf("--- RAID 1 (MIRRORING) ---\n");
            printf("Total Raw Capacity: %.2f GB\n", num_disks * disk_capacity);
            printf("Usable Capacity: %.2f GB\n", disk_capacity);
            printf("Capacity Efficiency: %.2f%%\n", (1.0 / num_disks) * 100);
            printf("Fault Tolerance: Can survive %d disk failure(s)\n", num_disks - 1);
            printf("Min Disks Required: 2\n");
            printf("Performance: Good reads, normal writes\n");
            printf("Best For: High reliability (critical data)\n");
            break;
            
        case 3:
            if (num_disks < 3) {
                printf("RAID 5 requires at least 3 disks!\n");
            } else {
                printf("--- RAID 5 (DISTRIBUTED PARITY) ---\n");
                printf("Total Raw Capacity: %.2f GB\n", num_disks * disk_capacity);
                printf("Usable Capacity: %.2f GB\n", (num_disks - 1) * disk_capacity);
                printf("Capacity Efficiency: %.2f%%\n", ((num_disks - 1.0) / num_disks) * 100);
                printf("Parity Overhead: %.2f GB (1 disk)\n", disk_capacity);
                printf("Fault Tolerance: 1 disk failure\n");
                printf("Min Disks Required: 3\n");
                printf("Performance: Good balance\n");
                printf("Best For: General purpose (file servers)\n");
            }
            break;
            
        case 4:
            if (num_disks < 4) {
                printf("RAID 6 requires at least 4 disks!\n");
            } else {
                printf("--- RAID 6 (DUAL PARITY) ---\n");
                printf("Total Raw Capacity: %.2f GB\n", num_disks * disk_capacity);
                printf("Usable Capacity: %.2f GB\n", (num_disks - 2) * disk_capacity);
                printf("Capacity Efficiency: %.2f%%\n", ((num_disks - 2.0) / num_disks) * 100);
                printf("Parity Overhead: %.2f GB (2 disks)\n", 2 * disk_capacity);
                printf("Fault Tolerance: 2 simultaneous disk failures\n");
                printf("Min Disks Required: 4\n");
                printf("Performance: Good reads, slower writes\n");
                printf("Best For: Critical applications (databases)\n");
            }
            break;
            
        case 5:
            printf("--- RAID COMPARISON TABLE ---\n\n");
            printf("%-10s %-15s %-20s %-25s %-15s\n", 
                   "RAID", "Min Disks", "Capacity", "Fault Tolerance", "Performance");
            printf("-----------------------------------------------------------------------------------\n");
            printf("%-10s %-15s %-20s %-25s %-15s\n", 
                   "RAID 0", "2", "100%", "None", "Excellent");
            printf("%-10s %-15s %-20s %-25s %-15s\n", 
                   "RAID 1", "2", "50% (n disks)", "n-1 failures", "Good");
            printf("%-10s %-15s %-20s %-25s %-15s\n", 
                   "RAID 5", "3", "(n-1)/n", "1 failure", "Good");
            printf("%-10s %-15s %-20s %-25s %-15s\n", 
                   "RAID 6", "4", "(n-2)/n", "2 failures", "Moderate");
            printf("\n");
            break;
            
        default:
            printf("Invalid choice!\n");
    }
}
