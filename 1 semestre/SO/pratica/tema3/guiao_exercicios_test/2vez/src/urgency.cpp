/**
 * @file
 *
 * \brief A hospital pediatric urgency with a Manchester triage system.
 */

#include  <stdio.h>
#include  <stdlib.h>
#include  <string.h>
#include  <libgen.h>
#include  <unistd.h>
#include  <sys/wait.h>
#include  <sys/types.h>
#include  <thread.h>
#include  <math.h>
#include  <stdint.h>
#include  <signal.h>
#include  <utils.h>
#include  "settings.h"
#include  "pfifo.h"

#include "thread.h"
//#include "process.h"

#include <iostream>

#define USAGE "Synopsis: %s [options]\n" \
   "\t----------+-------------------------------------------\n" \
   "\t  Option  |          Description                      \n" \
   "\t----------+-------------------------------------------\n" \
   "\t -p num   | number of patients (dfl: 4)               \n" \
   "\t -n num   | number of nurses (dfl: 1)                 \n" \
   "\t -d num   | number of doctors (dfl: 1)                \n" \
   "\t -h       | this help                                 \n" \
   "\t----------+-------------------------------------------\n"

/**
 * \brief Patient data structure
 */
typedef struct
{
   char name[MAX_NAME+1];
   int done; // 0: waiting for consultation; 1: consultation finished
} Patient;

typedef struct
{
    int num_patients;
    Patient all_patients[MAX_PATIENTS];
    PriorityFIFO triage_queue;
    PriorityFIFO doctor_queue;
    pthread_t* patient; //entidade patient
    pthread_t* npatient;// numero de pacientes
    pthread_t* nurse; //entidade nurse
    pthread_t* doctor; //entidade doctor
} HospitalData;

HospitalData * hd = NULL;

/**
 *  \brief patient verification test
 */
#define check_valid_patient(id) do { check_valid_id(id); check_valid_name(hd->all_patients[id].name); } while(0)

int random_manchester_triage_priority();
void new_patient(Patient* patient); // initializes a new patient
void random_wait();

void* patientThread(void* args);
void* nurseThread(void* args);
void* doctorThread(void* args);


/* ************************************************* */

/* changes may be required to this function */
void init_simulation(uint32_t np,uint32_t nN,uint32_t nd)
{
   printf("Initializing simulation\n");
   hd = (HospitalData*)mem_alloc(sizeof(HospitalData)); // mem_alloc is a malloc with NULL pointer verification
   memset(hd, 0, sizeof(HospitalData));
   hd->num_patients = np;
   init_pfifo(&hd->triage_queue);
   init_pfifo(&hd->doctor_queue);

   hd->patient = new pthread_t[np];
   hd->npatient = new pthread_t[np];
   hd->nurse = new pthread_t[nN];
   hd->doctor = new pthread_t[nd];

   printf("Launching %d patient threads\n", np);
   for(uint32_t i=0;i<np;i++){ //i = numero de pacientes por cada fila
      printf("\033[1;33mPatient %d launched\n\033[0m", i);
      hd->npatient[i] = i;
      thread_create(&hd->patient[i],NULL,patientThread,&hd->npatient[i]);
   }
   printf("Launching %d nurses threads\n", np);
   for(uint32_t i=0;i<nN;i++){
      printf("\033[1;33mNurse %d launched\n\033[0m", i);
      hd->nurse[i]=i;
      thread_create(&hd->nurse[i],NULL,nurseThread,NULL);
   }
   printf("Launching %d doctor threads\n", np);
   for (uint32_t i=0; i<nd; i++){
      printf("\033[1;33mDoctor %d launched\n\033[0m",i);
      hd->doctor[i]=i;
      thread_create(&hd->doctor[i],NULL,doctorThread,NULL);
   }
   /* Waiting for all patient threads to finish -> inexistencia de mais pacientes */ 
   for(uint32_t i = 0 ; i<np;i++){
      pthread_join(hd->patient[i],NULL);
      printf("Patient thread %d is terminated\n",i);
   }
}

/* ************************************************* */

void nurse_iteration()
{
   printf("\e[34;01mNurse: get next patient\e[0m\n");
   uint32_t patient = retrieve_pfifo(&hd->triage_queue);
   check_valid_patient(patient);
   printf("\e[34;01mNurse: evaluate patient %u priority\e[0m\n", patient);
   uint32_t priority = random_manchester_triage_priority();
   printf("\e[34;01mNurse: add patient %u with priority %u to doctor queue\e[0m\n", patient, priority);
   insert_pfifo(&hd->doctor_queue, patient, priority);
}

/* ************************************************* */

void doctor_iteration()
{
   printf("\e[32;01mDoctor: get next patient\e[0m\n");
   uint32_t patient = retrieve_pfifo(&hd->doctor_queue);
   check_valid_patient(patient);
   printf("\e[32;01mDoctor: treat patient %u\e[0m\n", patient);
   random_wait();
   printf("\e[32;01mDoctor: patient %u treated\e[0m\n", patient);
   hd->all_patients[patient].done = 1;
}

/* ************************************************* */

void patient_goto_urgency(int id)
{
   new_patient(&hd->all_patients[id]);
   check_valid_name(hd->all_patients[id].name);
   printf("\e[30;01mPatient %s (number %u): get to hospital\e[0m\n", hd->all_patients[id].name, id);
   insert_pfifo(&hd->triage_queue, id, 1); // all elements in triage queue with the same priority!
}

/* changes may be required to this function */
//DONE
void patient_wait_end_of_consultation(int id) // falta por quando e que uma consulta acaba
{
   check_valid_name(hd->all_patients[id].name);
   while(hd->all_patients[id].done==0){//enquanto estiver a decorrer a consulta ele tem que esperar pelo final para esse paciente acabar -> faz isto para todos
 	   random_wait();
   }
   printf("\e[30;01mPatient %s (number %u): health problems treated\e[0m\n", hd->all_patients[id].name, id);
}

/* changes are required to this function */
//DONE
void patient_life(int id)
{
   patient_goto_urgency(id);
   //nurse_iteration();  // to be deleted in concurrent version
   //doctor_iteration(); // to be deleted in concurrent version
   patient_wait_end_of_consultation(id);
   memset(&(hd->all_patients[id]), 0, sizeof(Patient)); // patient finished
}

/* ************************************************* */
//ciclos de vida
//onde vai comecar a correr a thread
//um paciente sai do hospital depois da consulta
void* patientThread(void* args){ //o args = n de pacientes
	uint32_t * np = (uint32_t *) args; //numero de pacientes
	patient_life(*np);
	return NULL;
}

// enfermeiro e doutor sao como se fossem servidores -> ciclos infinitos
// so nao sao ciclos infinitos quando se sabe exatamente quando acaba como os pacientes acabam quando ja nao tiver ninguem a espera(fifo vazio)
// um enfermeiro so leva o paciente ao medico e volta ao estado inicial (fica sempre no hospital a fazer a mesma coisa)  
// assim como o medico. atende um paciente e depois atende outro e outro
void* nurseThread(void* args){
	while(true){
		nurse_iteration();
	}
}

void* doctorThread(void* args){
	while(true){
		doctor_iteration();
	}
}

/* ************************************************* */

int main(int argc, char *argv[])
{
   uint32_t npatients = 4;  ///< number of patients
   uint32_t nnurses = 1;    ///< number of triage nurses
   uint32_t ndoctors = 1;   ///< number of doctors

   /* command line processing */
   int option;
   while ((option = getopt(argc, argv, "p:n:d:h")) != -1)
   {
      switch (option)
      {
         case 'p':
            npatients = atoi(optarg);
            if (npatients < 1 || npatients > MAX_PATIENTS)
            {
               fprintf(stderr, "Invalid number of patients!\n");
               return EXIT_FAILURE;
            }
            break;
         case 'n':
            nnurses = atoi(optarg);
            if (nnurses < 1)
            {
               fprintf(stderr, "Invalid number of nurses!\n");
               return EXIT_FAILURE;
            }
            break;
         case 'd':
            ndoctors = atoi(optarg);
            if (ndoctors < 1)
            {
               fprintf(stderr, "Invalid number of doctors!\n");
               return EXIT_FAILURE;
            }
            break;
         case 'h':
            printf(USAGE, basename(argv[0]));
            return EXIT_SUCCESS;
         default:
            fprintf(stderr, "Non valid option!\n");
            fprintf(stderr, USAGE, basename(argv[0]));
            return EXIT_FAILURE;
      }
   }

   /* start random generator */
   srand(getpid());

   /* init simulation */
   init_simulation(npatients,nnurses,ndoctors);

   /* dummy code to show a very simple sequential behavior */
   for(uint32_t i = 0; i < npatients; i++)
   {
      printf("\n");
      random_wait(); // random wait for patience creation
      patient_life(i);
   }

   return EXIT_SUCCESS;
}


/* YOU MAY IGNORE THE FOLLOWING CODE */

int random_manchester_triage_priority()
{
   int result;
   int perc = (int)(100*(double)rand()/((double)RAND_MAX)); // in [0;100]
   if (perc < 10)
      result = RED;
   else if (perc < 30)
      result = ORANGE;
   else if (perc < 50)
      result = YELLOW;
   else if (perc < 75)
      result = GREEN;
   else
      result = BLUE;
   return result;
}

static char **names = (char *[]) {"Ana", "Miguel", "Luis", "Joao", "Artur", "Maria", "Luisa", "Mario", "Augusto", "Antonio", "Jose", "Alice", "Almerindo", "Gustavo", "Paulo", "Paula", NULL};

char* random_name()
{
   static int names_len = 0;
   if (names_len == 0)
   {
      for(names_len = 0; names[names_len] != NULL; names_len++)
         ;
   }

   return names[(int)(names_len*(double)rand()/((double)RAND_MAX+1))];
}

void new_patient(Patient* patient)
{
   strcpy(patient->name, random_name());
   patient->done = 0;
}

void random_wait()
{
   usleep((useconds_t)(MAX_WAIT*(double)rand()/(double)RAND_MAX));
}

