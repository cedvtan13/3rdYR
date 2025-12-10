/*
  a simple example of a proxy server that uses fork() and socket programming
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sched.h>

int main() {
    int id = fork();

    if (id == 0){
      //child process
      printf("Hello from child process, ID# = %d\nRealPID = %d\n", id, getpid());
    }
    else {
      //parent process
      printf("Hello from parent process, ID# = %d\nRealPID = %d\n", id, getpid());
    }
    return 0;
}