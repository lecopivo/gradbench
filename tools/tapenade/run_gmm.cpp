#include "TapenadeGMM.h"
#include "adbench/main.h"
#include "adbench/shared/GMMData.h"

int main(int argc, char* argv[]) {
  return generic_main<GMMInput,
                      TapenadeGMM,
                      read_GMMInput_json,
                      write_GMMOutput_objective_json,
                      write_GMMOutput_jacobian_json>(argc, argv);
}
