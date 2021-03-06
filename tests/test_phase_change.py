# -*- coding: utf-8 -*-
'''Chemical Engineering Design Library (ChEDL). Utilities for process modeling.
Copyright (C) 2016, Caleb Bell <Caleb.Andrew.Bell@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''

import pytest

from fluids.numerics import assert_close, assert_close1d
from thermo.phase_change import *
from chemicals.miscdata import CRC_inorganic_data, CRC_organic_data
from chemicals.identifiers import check_CAS

from thermo.phase_change import COOLPROP, VDI_PPDS, CLAPEYRON, LIU, ALIBAKHSHI, MORGAN_KOBAYASHI, VELASCO, PITZER, RIEDEL, SIVARAMAN_MAGEE_KOBAYASHI, CHEN, CRC_HVAP_TB, DIPPR_PERRY_8E, VETERE, CRC_HVAP_298, VDI_TABULAR, GHARAGHEIZI_HVAP_298

@pytest.mark.meta_T_dept
def test_EnthalpyVaporization():
    EtOH = EnthalpyVaporization(Tb=351.39, Tc=514.0, Pc=6137000.0, omega=0.635, similarity_variable=0.1954, Psat=7872.2, Zg=0.9633, Zl=0.0024, CASRN='64-17-5')

    EtOH.method = COOLPROP
    assert_close(EtOH.T_dependent_property(305), 42062.9371631488)
    EtOH.method = VDI_PPDS
    assert_close(EtOH.T_dependent_property(305), 42099.23631527565)
    EtOH.method = CLAPEYRON
    assert_close(EtOH.T_dependent_property(305), 39904.512005771176)
    EtOH.method = LIU
    assert_close(EtOH.T_dependent_property(305), 40315.087291316195)
    EtOH.method = ALIBAKHSHI
    assert_close(EtOH.T_dependent_property(305), 39244.0137575973)
    EtOH.method = MORGAN_KOBAYASHI
    assert_close(EtOH.T_dependent_property(305), 42182.87752489718)
    EtOH.method = VELASCO
    assert_close(EtOH.T_dependent_property(305), 43056.23753606326)
    EtOH.method = PITZER
    assert_close(EtOH.T_dependent_property(305), 41716.88048400951)
    EtOH.method = RIEDEL
    assert_close(EtOH.T_dependent_property(305), 44258.89496024996)
    EtOH.method = SIVARAMAN_MAGEE_KOBAYASHI
    assert_close(EtOH.T_dependent_property(305), 42279.09568184713)
    EtOH.method = CHEN
    assert_close(EtOH.T_dependent_property(305), 42951.50714053451)
    EtOH.method = CRC_HVAP_TB
    assert_close(EtOH.T_dependent_property(305), 42423.58947282491)
    EtOH.method = DIPPR_PERRY_8E
    assert_close(EtOH.T_dependent_property(305), 42115.102057622214)
    EtOH.method = VETERE
    assert_close(EtOH.T_dependent_property(305), 41382.22039928848)
    EtOH.method = CRC_HVAP_298
    assert_close(EtOH.T_dependent_property(305), 41804.5417918726)
    EtOH.method = VDI_TABULAR
    assert_close(EtOH.T_dependent_property(305), 42119.6665416816)
    EtOH.method = GHARAGHEIZI_HVAP_298
    assert_close(EtOH.T_dependent_property(305), 41686.00339359697)


    EtOH.extrapolation = None
    for i in EtOH.all_methods:
        EtOH.method = i
        assert EtOH.T_dependent_property(5000) is None


    assert EnthalpyVaporization.from_JSON(EtOH.as_JSON()) == EtOH

    EtOH = EnthalpyVaporization(CASRN='64-17-5', Tc=514.0)
    Hvap_calc = []
    for i in ['GHARAGHEIZI_HVAP_298', 'CRC_HVAP_298', 'VDI_TABULAR', 'COOLPROP']:
        EtOH.method = i
        Hvap_calc.append(EtOH.T_dependent_property(310.0))
    Hvap_exp = [41304.19234346344, 41421.6450231131, 41857.962450207546, 41796.56243049473]
    assert_close1d(Hvap_calc, Hvap_exp)

    # Test Clapeyron, without Zl
    EtOH = EnthalpyVaporization(Tb=351.39, Tc=514.0, Pc=6137000.0, omega=0.635, similarity_variable=0.1954, Psat=7872.2, Zg=0.9633, CASRN='64-17-5')
    assert_close(EtOH.calculate(298.15, 'CLAPEYRON'), 37864.70507798813)

    EtOH = EnthalpyVaporization(Tb=351.39, Pc=6137000.0, omega=0.635, similarity_variable=0.1954, Psat=7872.2, Zg=0.9633, CASRN='64-17-5')
    assert EtOH.test_method_validity(351.39, 'CRC_HVAP_TB')
    assert not EtOH.test_method_validity(351.39+10, 'CRC_HVAP_TB')
    assert not EtOH.test_method_validity(351.39, 'CRC_HVAP_298')


    Ts = [200, 250, 300, 400, 450]
    props = [46461.62768429649, 44543.08561867195, 42320.381894706225, 34627.726535926406, 27634.46144486471]
    EtOH.add_tabular_data(Ts=Ts, properties=props, name='CPdata')
    EtOH.forced = True
    assert_close(43499.47575887933, EtOH.T_dependent_property(275), rtol=1E-4)

    EtOH.tabular_extrapolation_permitted = False
    assert None == EtOH.T_dependent_property(5000)

    with pytest.raises(Exception):
        EtOH.test_method_validity('BADMETHOD', 300)

    assert EnthalpyVaporization.from_JSON(EtOH.as_JSON()) == EtOH


@pytest.mark.meta_T_dept
def test_EnthalpyVaporization_Watson_extrapolation():
    from thermo.phase_change import COOLPROP
    obj = EnthalpyVaporization(CASRN='7732-18-5', Tb=373.124, Tc=647.14, Pc=22048320.0, omega=0.344,
                         similarity_variable=0.16652530518537598, Psat=3167, Zl=1.0, Zg=0.96,
                         extrapolation='Watson')
    obj.method == COOLPROP
    assert 0 == obj(obj.Tc)
    assert_close(obj(1e-5), 54787.16649491286, rtol=1e-4)

    assert_close(obj.solve_property(5e4), 146.3404577534453)
    assert_close(obj.solve_property(1), 647.1399999389462)
    assert_close(obj.solve_property(1e-20), 647.13999999983)
    assert EnthalpyVaporization.from_JSON(obj.as_JSON()) == obj
