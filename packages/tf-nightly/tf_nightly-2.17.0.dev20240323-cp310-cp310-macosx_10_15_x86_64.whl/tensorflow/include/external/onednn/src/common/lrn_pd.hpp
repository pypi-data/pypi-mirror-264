/*******************************************************************************
* Copyright 2016-2023 Intel Corporation
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*******************************************************************************/

#ifndef COMMON_LRN_PD_HPP
#define COMMON_LRN_PD_HPP

#include "oneapi/dnnl/dnnl.h"

#include "c_types_map.hpp"
#include "primitive_desc.hpp"

namespace dnnl {
namespace impl {

struct lrn_fwd_pd_t;

struct lrn_pd_t : public primitive_desc_t {
    static constexpr auto base_pkind = primitive_kind::lrn;

    const lrn_desc_t *desc() const { return &desc_; }
    const op_desc_t *op_desc() const override {
        return reinterpret_cast<const op_desc_t *>(this->desc());
    }

    status_t query(query_t what, int idx, void *result) const override {
        switch (what) {
            case query::prop_kind:
                *(prop_kind_t *)result = desc()->prop_kind;
                break;
            case query::alg_kind:
                *(alg_kind_t *)result = desc()->alg_kind;
                break;
            case query::alpha_f32: *(float *)result = desc()->lrn_alpha; break;
            case query::beta_f32: *(float *)result = desc()->lrn_beta; break;
            case query::local_size_s64:
                *(dim_t *)result = desc()->local_size;
                break;
            case query::k_f32: *(float *)result = desc()->lrn_k; break;
            default: return primitive_desc_t::query(what, idx, result);
        }
        return status::success;
    }

    /* common lrn aux functions */

    dim_t MB() const { return src_md()->dims[0]; }
    dim_t C() const { return src_md()->dims[1]; }
    dim_t D() const { return ndims() >= 5 ? src_md()->dims[ndims() - 3] : 1; }
    dim_t H() const { return ndims() >= 4 ? src_md()->dims[ndims() - 2] : 1; }
    dim_t W() const { return ndims() >= 3 ? src_md()->dims[ndims() - 1] : 1; }

    int ndims() const { return src_md()->ndims; }

    bool has_zero_dim_memory() const {
        return memory_desc_wrapper(desc_.src_desc).has_zero_dim();
    }

    bool is_fwd() const {
        return utils::one_of(desc_.prop_kind, prop_kind::forward_training,
                prop_kind::forward_inference);
    }

protected:
    lrn_desc_t desc_;
    const lrn_fwd_pd_t *hint_fwd_pd_;

    memory_desc_t src_md_;
    memory_desc_t ws_md_;

    lrn_pd_t(const lrn_desc_t *adesc, const primitive_attr_t *attr,
            const lrn_fwd_pd_t *hint_fwd_pd)
        : primitive_desc_t(attr, base_pkind)
        , desc_(*adesc)
        , hint_fwd_pd_(hint_fwd_pd)
        , src_md_(desc_.src_desc)
        , ws_md_() {}
};

struct lrn_fwd_pd_t : public lrn_pd_t {
    typedef lrn_fwd_pd_t base_class;
    typedef lrn_fwd_pd_t hint_class;

    arg_usage_t arg_usage(int arg) const override {
        if (arg == DNNL_ARG_SRC) return arg_usage_t::input;

        if (arg == DNNL_ARG_DST) return arg_usage_t::output;

        if (arg == DNNL_ARG_WORKSPACE && (!types::is_zero_md(workspace_md())))
            return arg_usage_t::output;

        return primitive_desc_t::arg_usage(arg);
    }

    const memory_desc_t *arg_md(
            int arg, bool user_input = false) const override {
        switch (arg) {
            case DNNL_ARG_SRC: return src_md(0);
            case DNNL_ARG_DST: return dst_md(0, user_input);
            default: return lrn_pd_t::arg_md(arg);
        }
    }

    const memory_desc_t *src_md(
            int index = 0, bool user_input = false) const override {
        if (index == 0) return user_input ? &desc()->src_desc : &src_md_;
        return &glob_zero_md;
    }
    const memory_desc_t *dst_md(
            int index = 0, bool user_input = false) const override {
        if (index == 0) return user_input ? &desc()->dst_desc : &dst_md_;
        return &glob_zero_md;
    }
    const memory_desc_t *workspace_md(int index = 0) const override {
        return index == 0 && !types::is_zero_md(&ws_md_) ? &ws_md_
                                                         : &glob_zero_md;
    }

    int n_inputs() const override { return 1; }
    int n_outputs() const override {
        return 1 + (!types::is_zero_md(workspace_md()));
    }

protected:
    memory_desc_t dst_md_;

    lrn_fwd_pd_t(const lrn_desc_t *adesc, const primitive_attr_t *attr,
            const lrn_fwd_pd_t *hint_fwd_pd)
        : lrn_pd_t(adesc, attr, hint_fwd_pd), dst_md_(desc_.dst_desc) {}

    bool set_default_formats_common() {
        return IMPLICATION(dst_md_.format_kind == format_kind::any,
                memory_desc_init_by_md_and_dt(
                        dst_md_, src_md_, dst_md_.data_type)
                        == status::success);
    }
};

struct lrn_bwd_pd_t : public lrn_pd_t {
    typedef lrn_bwd_pd_t base_class;
    typedef lrn_fwd_pd_t hint_class;

    arg_usage_t arg_usage(int arg) const override {
        if (utils::one_of(arg, DNNL_ARG_SRC, DNNL_ARG_DIFF_DST))
            return arg_usage_t::input;

        if (arg == DNNL_ARG_DIFF_SRC) return arg_usage_t::output;

        if (arg == DNNL_ARG_WORKSPACE && (!types::is_zero_md(workspace_md())))
            return arg_usage_t::input;

        return primitive_desc_t::arg_usage(arg);
    }

    const memory_desc_t *arg_md(
            int arg, bool user_input = false) const override {
        switch (arg) {
            case DNNL_ARG_SRC: return src_md(0);
            case DNNL_ARG_DIFF_DST: return diff_dst_md(0, user_input);
            case DNNL_ARG_DIFF_SRC: return diff_src_md(0);
            default: return lrn_pd_t::arg_md(arg);
        }
    }

    const memory_desc_t *src_md(
            int index = 0, bool user_input = false) const override {
        if (index == 0) return user_input ? &desc()->src_desc : &src_md_;
        return &glob_zero_md;
    }
    const memory_desc_t *diff_dst_md(
            int index = 0, bool user_input = false) const override {
        if (index == 0)
            return user_input ? &desc()->diff_dst_desc : &diff_dst_md_;
        return &glob_zero_md;
    }
    const memory_desc_t *diff_src_md(
            int index = 0, bool user_input = false) const override {
        if (index == 0)
            return user_input ? &desc()->diff_src_desc : &diff_src_md_;
        return &glob_zero_md;
    }
    const memory_desc_t *workspace_md(int index = 0) const override {
        return index == 0 && !types::is_zero_md(&ws_md_) ? &ws_md_
                                                         : &glob_zero_md;
    }

    int n_inputs() const override {
        return 2 + (!types::is_zero_md(workspace_md()));
    }
    int n_outputs() const override { return 1; }

protected:
    memory_desc_t diff_src_md_;
    memory_desc_t diff_dst_md_;

    lrn_bwd_pd_t(const lrn_desc_t *adesc, const primitive_attr_t *attr,
            const lrn_fwd_pd_t *hint_fwd_pd)
        : lrn_pd_t(adesc, attr, hint_fwd_pd)
        , diff_src_md_(desc_.diff_src_desc)
        , diff_dst_md_(desc_.diff_dst_desc) {}

    bool set_default_formats_common() {
        return IMPLICATION(diff_dst_md_.format_kind == format_kind::any,
                       memory_desc_init_by_md_and_dt(
                               diff_dst_md_, src_md_, diff_dst_md_.data_type)
                               == status::success)
                && IMPLICATION(diff_src_md_.format_kind == format_kind::any,
                        memory_desc_init_by_md_and_dt(
                                diff_src_md_, src_md_, diff_src_md_.data_type)
                                == status::success);
    }
};

} // namespace impl
} // namespace dnnl

#endif

// vim: et ts=4 sw=4 cindent cino+=l0,\:4,N-s
