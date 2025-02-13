// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

// https://github.com/microsoft/ADBench/blob/38cb7931303a830c3700ca36ba9520868327ac87/src/cpp/modules/finite/FiniteGMM.h

#pragma once

#include "adbench/shared/ITest.h"
#include "adbench/shared/GMMData.h"
#include "finite.h"

class FiniteGMM : public ITest<GMMInput, GMMOutput> {
  FiniteDifferencesEngine<double> engine;

public:
  FiniteGMM(GMMInput&);

  void calculate_objective() override;
  void calculate_jacobian() override;
};
