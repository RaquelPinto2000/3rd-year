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
   
   //inicializar a variavel de acesso
   pfifo->accessCR = PTHREAD_MUTEX_INITIALIZER;
   mutex_lock(&pfifo->accessCR); //entra na zona restrita
 
   memset(pfifo->array, 0, sizeof(pfifo->array));
   pfifo->inp = pfifo->out = pfifo->cnt = 0;
   
   //inicializar as variaveis de controlo do fifo
   pfifo->fifoNotFull = PTHREAD_COND_INITIALIZER;
   pfifo->fifoNotEmpty = PTHREAD_COND_INITIALIZER;

   // Sinaliza todos os threads em espera que fifo não está cheio -> se eu acabo de o criar e pq nao esta cheio - esta vazio
   cond_broadcast(&pfifo->fifoNotFull);
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
void insert_pfifo(PriorityFIFO* pfifo, uint32_t id, uint32_t priority)
{
   require (pfifo != NULL, "NULL pointer to FIFO");   // a false value indicates a program error
   require (id <= MAX_ID, "invalid id");              // a false value indicates a program error
   require (priority > 0 && priority <= MAX_PRIORITY, "invalid priority value");  // a false value indicates a program error
   // require (!full_pfifo(pfifo), "full FIFO");         // in a shared fifo, it may not result from a program error!
		
   //printf("[insert_pfifo] value=%d, priority=%d, pfifo->inp=%d, pfifo->out=%d\n", id, priority, pfifo->inp, pfifo->out);
   mutex_lock(&pfifo->accessCR);

   while(full_pfifo(pfifo)){
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

   // Sinaliza todos os threads em espera que fifo não está vazio -> se eu acrescento um quer dizer que no final nao esta vazio
   cond_broadcast(&pfifo->fifoNotEmpty);

   mutex_unlock(&pfifo->accessCR);
   //printf("[insert_pfifo] pfifo->inp=%d, pfifo->out=%d\n", pfifo->inp, pfifo->out);
}

/* --------------------------------------- */

/* changes may be required to this function */
//DONE
uint32_t retrieve_pfifo(PriorityFIFO* pfifo)
{
   require (pfifo != NULL, "NULL pointer to FIFO");   // a false value indicates a program error
   //require (!empty_pfifo(pfifo), "empty FIFO");       // in a shared fifo, it may not result from a program error!
   mutex_lock(&pfifo->accessCR);

   while(empty_pfifo(pfifo)){
      cond_wait(&pfifo->fifoNotEmpty,&pfifo->accessCR);
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

   // Sinaliza todos os threads em espera que fifo não está cheio -> se eu retiro quer dizer que no final nao esta cheio
   cond_broadcast(&pfifo->fifoNotFull);

   mutex_unlock(&pfifo->accessCR);

   return result;
}

/* --------------------------------------- */

/* changes may be required to this function */
void print_pfifo(PriorityFIFO* pfifo)
{
   require (pfifo != NULL, "NULL pointer to FIFO");   // a false value indicates a program error

   mutex_lock(&pfifo->accessCR);
   uint32_t idx = pfifo->out;
   for(uint32_t i = 1; i <= pfifo->cnt; i++)
   {
      check_valid_id(pfifo->array[pfifo->out].id);
      check_valid_priority(pfifo->array[pfifo->out].priority);
      printf("[%02d] value = %d, priority = %d\n", i, pfifo->array[idx].id, pfifo->array[idx].priority);
      idx = (idx + 1) % FIFO_MAXSIZE;
   }
      
   mutex_unlock(&pfifo->accessCR);
}

