

#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/wait.h>

char let = 'A';

/*
child must print modify the global variable let to 'Z' and print it
parent must print the variable let as it is.
the parent will wait till the child is done before it prints.
*/
int main(){
  pid_t pid = fork();

  if (pid == 0){
    char let = 'Z';
    printf("Letter is: %c\n", let);
  }
  else {
    wait(NULL);
    printf("Letter is: %c\n", let);
  }
  
  return 0;
}