#include <stdlib.h>
#include <chrono>
#include <iomanip>
#include <iostream>
#include <vector>
#include "problem/heuristic.h"

Heuristic::Heuristic(double runtime_limit, bool validation) :
  validation_(validation),
  start_time_(std::chrono::steady_clock::now()),
  best_(0.0),
  runtime_limit_(runtime_limit) {}

double Heuristic::Runtime() {
  auto curr_time = std::chrono::steady_clock::now();
  double secs =
    std::chrono::duration<double, std::milli>(curr_time-start_time_).count()/1000;
    
  return secs;
}

std::string Heuristic::History() {
  std::stringstream out_str;
  out_str << std::setprecision(15) << "[";
  for (int i = 0; i < past_solution_values_.size(); i++) {
    if (i > 0) out_str << ";";
    out_str << past_solution_values_[i] << ":" << past_solution_times_[i];
  }
  out_str << "]";
  return out_str.str();
}
