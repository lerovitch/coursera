#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int main() {

    /* Enter your code here. Read input from STDIN. Print output to STDOUT */    
  int bytes_read = 0;
  size_t nbytes;
  char *my_string;

  /* These 2 lines are the heart of the program. */
  bytes_read = getline (&my_string, &nbytes, stdin);

  do {
      if (nbytes != 0) {
          printf("%s", my_string);
      }
      bytes_read = getline(&my_string, &nbytes, stdin);

  } while (bytes_read != -1);

  return 0;
}
