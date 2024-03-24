/* Copyright 2022 The StableHLO Authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#ifndef STABLEHLO_TRANSFORMS_PASSES_H
#define STABLEHLO_TRANSFORMS_PASSES_H

#include <memory>

#include "mlir/Dialect/Func/IR/FuncOps.h"
#include "mlir/Dialect/Quant/QuantOps.h"
#include "mlir/Dialect/Shape/IR/Shape.h"
#include "mlir/IR/BuiltinOps.h"
#include "mlir/Pass/Pass.h"
#include "mlir/Support/LogicalResult.h"
#include "mlir/Transforms/DialectConversion.h"

namespace mlir {
namespace stablehlo {

#define GEN_PASS_DECL
#define GEN_PASS_REGISTRATION
#include "stablehlo/transforms/Passes.h.inc"

// Populates --stablehlo-canonicalize-dynamism patterns.
void populateStablehloCanonicalizeDynamismPatterns(RewritePatternSet *patterns,
                                                   MLIRContext *context);

// Populates --stablehlo-refine-shapes patterns.
void populateStablehloRefineShapesPatterns(RewritePatternSet *patterns,
                                           MLIRContext *context);

// Populates StableHLO ops to VHLO ops rewriting patterns.
void populateStablehloToVhloPatterns(RewritePatternSet *patterns,
                                     TypeConverter *converter,
                                     MLIRContext *context);

// Populates VHLO ops to StableHLO ops rewriting patterns.
void populateVhloToStablehloPatterns(RewritePatternSet *patterns,
                                     TypeConverter *converter,
                                     MLIRContext *context);

// Populates VHLO downgrade rewriting patterns.
void populateVhloToVersionPatterns(RewritePatternSet *patterns,
                                   TypeConverter *converter,
                                   MLIRContext *contexts);

/// Collection of rewrite patterns for lowering of CHLO ops to StableHLO and
/// Shape ops.
void populateChloToStablehloPatterns(MLIRContext *context,
                                     RewritePatternSet *patterns);

/// Collection of canonicalization patterns for StableHLO.
void populateStablehloCanonicalizationPatterns(MLIRContext *context,
                                               RewritePatternSet *patterns,
                                               PatternBenefit benefit = 1);

/// Collection of shape dialect to StableHLO patterns.
void populateShapeToStablehloPatterns(MLIRContext *context,
                                      RewritePatternSet *patterns);

//// Additional pass constructors ////

std::unique_ptr<OperationPass<ModuleOp>> createStablehloRefineArgumentsPass(
    TypeRange refinedTypes);

//// Pass pipelines ////

// StableHLO consumers can add this pipeline to convert portable artifacts to
// StableHLO programs. This pipeline will silently pass if programs are not
// portable artifacts.
//
// Uses vhlo-to-version and vhlo-legalize-to-stablehlo passes. Does not require
// an option to specify VHLO target version since it always converts VHLO to
// the current version in order to legalize to StableHLO.
void createStablehloDeserializePipeline(OpPassManager &pm);

// Adds `stablehlo-deserialize` pipeline as a registered pass pipeline
// for opt tools.
void registerPassPipelines();

}  // namespace stablehlo
}  // namespace mlir

#endif  // STABLEHLO_TRANSFORMS_PASSES_H
