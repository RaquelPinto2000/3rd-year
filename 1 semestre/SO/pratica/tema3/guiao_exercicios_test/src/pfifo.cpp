#include <dbc.h>
#include <string.h>
#include "pfifo.h"

#include "thread.h"
//#include "process.h"

/* changes may be required to this function */
//DONE
void init_pfifo(PriorityFIFO* pfifo)
{
   require (pfifo != NULL, "NULL pointer to FIFO");   // a false value indicates a program error
   /*A função require() importa arquivos, porém, caso o mesmo não seja encontrado, será levantado uma exceção e a execução é finalizada. Essa é uma maneira de interrompermos a execução dos scripts caso alguma anomalia ocorra.*/
   
   //Initialize fifo's mutex -> nao esta dentro da zona critica pq primeiro temos que inicializar a flag do monitor e so depois e que podemos entrar
   pfifo->accessCR = PTHREAD_MUTEX_INITIALIZER;
   
   //Lock access to critical zone (fifo)
   mutex_lock(&pfifo->accessCR);

   memset(pfifo->array, 0, sizeof(pfifo->array)); 
   //Esta função retorna um ponteiro para a área da memória pfifo->array.
   pfifo->inp = pfifo->out = pfifo->cnt = 0;

   pfifo->fifoNotEmpty = PTHREAD_COND_INITIALIZER;
   pfifo->fifoNotFull = PTHREAD_COND_INITIALIZER;

   //Signal the fifo is not full for all waiting threads
   cond_broadcast(&pfifo->fifoNotFull); // estamos a inicializa-lo logo ele nao vai ser cheio

   //unlock acess to critical zone
   mutex_unlock(&pfifo->accessCR);

}

/* --------------------------------------- */

int empty_pfifo(PriorityFIFO* pfifo)
{
   require (pfifo != NULL, "NULL pointer to FIFO");   // a false value indicates a program error

   return pfifo->cnt == 0;
}

/* --------------------------------------- */

int full_pfifo(PriorityFIFO* pfifo)
{
   require (pfifo != NULL, "NULL pointer to FIFO");   // a false value indicates a program error

   return pfifo->cnt == FIFO_MAXSIZE;
}

/* --------------------------------------- */

/* changes may be required to this function */
//DONE
void insert_pfifo(PriorityFIFO* pfifo, uint32_t id, uint32_t priority) //INSERIR NO FIFO (push)
{
   require (pfifo != NULL, "NULL pointer to FIFO");   // a false value indicates a program error
   require (id <= MAX_ID, "invalid id");              // a false value indicates a program error
   require (priority > 0 && priority <= MAX_PRIORITY, "invalid priority value");  // a false value indicates a program error
   //require (!full_pfifo(pfifo), "full FIFO");         // in a shared fifo, it may not result from a program error!
   
   //lock acess to critical zone 
   mutex_lock(&pfifo->accessCR);
   //printf("[insert_pfifo] value=%d, priority=%d, pfifo->inp=%d, pfifo->out=%d\n", id, priority, pfifo->inp, pfifo->out);


   while(full_pfifo(pfifo)){ // ele vai esperar ate o fifo estar vazio e ate ter acesso
      cond_wait(&pfifo->fifoNotFull, &pfifo->accessCR);
   }

   uint32_t idx = pfifo->inp;
   uint32_t prev = (idx + FIFO_MAXSIZE - 1) % FIFO_MAXSIZE;
   while((idx != pfifo->out) && (pfifo->array[prev].priority > priority))
   {
      //printf("[insert_pfifo] idx=%d, prev=%d\n", idx, prev);
      pfifo->array[idx] = pfifo->array[prev];
      idx = prev;
      prev = (idx + FIFO_MAXSIZE - 1) % FIFO_MAXSIZE;
   }
   //printf("[insert_pfifo] idx=%d, prev=%d\n", idx, prev);
   pfifo->array[idx].id = id;
   pfifo->array[idx].priority = priority;
   pfifo->inp = (pfifo->inp + 1) % FIFO_MAXSIZE;
   pfifo->cnt++;
   //printf("[insert_pfifo] pfifo->inp=%d, pfifo->out=%d\n", pfifo->inp, pfifo->out);
   
   //Signal the fifo is not empty for all waiting threads
   cond_broadcast(&pfifo->fifoNotEmpty);
   //unlock acess to critical zone
   mutex_unlock(&pfifo->accessCR);
}

/* --------------------------------------- */

/* changes may be required to this function */
//DONE
uint32_t retrieve_pfifo(PriorityFIFO* pfifo) //RETIRAR DO FIFO (pop)
{
   require (pfifo != NULL, "NULL pointer to FIFO");   // a false value indicates a program error
   //require (!empty_pfifo(pfifo), "empty FIFO");       // in a shared fifo, it may not result from a program error!


   //Lock acess to critical zone -> entra na zona critica
   //mais a frente vao testar dentro do array por isso tem que entrar aqui
   mutex_lock(&pfifo->accessCR);

   while(empty_pfifo(pfifo)){ //ele tem que esperar ate que o fifo nao estar vazio e ate ter acesso
      cond_wait(&pfifo->fifoNotEmpty, &pfifo->accessCR);
   }

   check_valid_id(pfifo->array[pfifo->out].id);
   check_valid_priority(pfifo->array[pfifo->out].priority);

   uint32_t result = pfifo->array[pfifo->out].id;
   pfifo->array[pfifo->out].id = INVALID_ID;
   pfifo->array[pfifo->out].priority = INVALID_PRIORITY;
   pfifo->out = (pfifo->out + 1) % FIFO_MAXSIZE;
   pfifo->cnt--;

   // update priority of all remaing elements (increase priority by one)
   uint32_t idx = pfifo->out;
   for(uint32_t i = 1; i <= pfifo->cnt; i++)
   {
      if (pfifo->array[idx].priority > 1 && pfifo->array[idx].priority != INVALID_PRIORITY)
         pfifo->array[idx].priority--;
      idx = (idx + 1) % FIFO_MAXSIZE;
   }
   
   //Signal all waiting threads that fifo is notFull
   cond_broadcast(&pfifo->fifoNotFull);

   //Unlock acess to critical zone -> sai da zona critica
   mutex_unlock(&pfifo->accessCR);
   return result;
}

/* --------------------------------------- */

/* changes may be required to this function */
//DONE
void print_pfifo(PriorityFIFO* pfifo)
{
   require (pfifo != NULL, "NULL pointer to FIFO");   // a false value indicates a program error
   
   //Lock access to critical zone
   mutex_lock(&pfifo->accessCR);

   uint32_t idx = pfifo->out;
   for(uint32_t i = 1; i <= pfifo->cnt; i++)
   {
      check_valid_id(pfifo->array[pfifo->out].id);
      check_valid_priority(pfifo->array[pfifo->out].priority);
      printf("[%02d] value = %d, priority = %d\n", i, pfifo->array[idx].id, pfifo->array[idx].priority);
      idx = (idx + 1) % FIFO_MAXSIZE;
   }

   //Unlock access to critical zone
   mutex_unlock(&pfifo->accessCR);
}

