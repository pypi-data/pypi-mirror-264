//===- Transforms.h - ArmSME Dialect Transformation Entrypoints -*- C++ -*-===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//

#ifndef MLIR_DIALECT_ARMSME_TRANSFORMS_H
#define MLIR_DIALECT_ARMSME_TRANSFORMS_H

namespace mlir {

class LLVMConversionTarget;
class LLVMTypeConverter;
class RewritePatternSet;

namespace arm_sme {
void populateOuterProductFusionPatterns(RewritePatternSet &patterns);
} // namespace arm_sme

} // namespace mlir

#endif // MLIR_DIALECT_ARMSME_TRANSFORMS_H
