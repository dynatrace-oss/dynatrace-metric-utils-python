#  Copyright 2021 Dynatrace LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import unittest

import pytest
from dynatrace.metric.utils._normalize import Normalize

normalizer = Normalize()

cases_metric_keys = [
    ("valid base case", "basecase", "basecase"),
    ("valid base case", "just.a.normal.key", "just.a.normal.key"),
    ("valid leading underscore", "_case", "_case"),
    ("valid underscore", "case_case", "case_case"),
    ("valid number", "case1", "case1"),
    ("invalid leading number", "1case", "case"),
    ("valid leading uppercase", "Case", "Case"),
    ("valid all uppercase", "CASE", "CASE"),
    ("valid intermittent uppercase", "someCase", "someCase"),
    ("valid multiple sections", "prefix.case", "prefix.case"),
    ("valid multiple sections upper", "This.Is.Valid", "This.Is.Valid"),
    ("invalid multiple sections leading number", "0a.b", "a.b"),
    ("valid multiple section leading underscore", "_a.b", "_a.b"),
    ("valid leading number second section", "a.0", "a.0"),
    ("valid leading number second section 2", "a.0.c", "a.0.c"),
    ("valid leading number second section 3", "a.0b.c", "a.0b.c"),
    ("invalid leading hyphen", "-dim", "dim"),
    ("valid trailing hyphen", "dim-", "dim-"),
    ("valid trailing hyphens", "dim---", "dim---"),
    ("invalid empty", "", ""),
    ("invalid only number", "000", ""),
    ("invalid key first section only number", "0.section", ""),
    ("invalid leading character", "~key", "key"),
    ("invalid leading characters", "~0#key", "key"),
    ("invalid intermittent character", "some~key", "some_key"),
    ("invalid intermittent characters", "some#~äkey", "some_key"),
    ("invalid two consecutive dots", "a..b", "a.b"),
    ("invalid five consecutive dots", "a.....b", "a.b"),
    ("invalid just a dot", ".", ""),
    ("invalid leading dot", ".a", ""),
    ("invalid trailing dot", "a.", "a"),
    ("invalid enclosing dots", ".a.", ""),
    ("valid consecutive leading underscores", "___a", "___a"),
    ("valid consecutive trailing underscores", "a___", "a___"),
    ("invalid delete trailing invalid chars", "a$%@", "a"),
    ("invalid delete trailing invalid chars groups", "a.b$%@.c", "a.b.c"),
    ("valid consecutive enclosed underscores", "a___b", "a___b"),
    ("invalid mixture dots underscores", "._._._a_._._.", ""),
    ("valid mixture dots underscores 2", "_._._.a_._", "_._._.a_._"),
    ("invalid empty section", "an..empty.section", "an.empty.section"),
    ("invalid characters", "a,,,b  c=d\\e\\ =,f", "a_b_c_d_e_f"),
    ("invalid characters long",
     "a!b\"c#d$e%f&g'h(i)j*k+l,m-n.o/p:q;r<s=t>u?v@w[x]y\\z^0 1_2;3{4|5}6~7",
     "a_b_c_d_e_f_g_h_i_j_k_l_m-n.o_p_q_r_s_t_u_v_w_x_y_z_0_1_2_3_4_5_6_7"),
    ("invalid trailing characters", "a.b.+", "a.b"),
    ("valid combined test", "metric.key-number-1.001",
     "metric.key-number-1.001"),
    ("valid example 1", "MyMetric", "MyMetric"),
    ("invalid example 1", "0MyMetric", "MyMetric"),
    ("invalid example 2", "mÄtric", "m_tric"),
    ("invalid example 3", "metriÄ", "metri"),
    ("invalid example 4", "Ätric", "tric"),
    ("invalid example 5", "meträääääÖÖÖc", "metr_c"),
    ("invalid truncate key too long", "a" * 270, "a" * 250),
]


@pytest.mark.parametrize("msg,inp,exp", cases_metric_keys,
                         ids=[x[0] for x in cases_metric_keys])
def test_parametrized_normalize_metric_key(msg, inp, exp):
    assert normalizer.normalize_metric_key(inp) == exp
