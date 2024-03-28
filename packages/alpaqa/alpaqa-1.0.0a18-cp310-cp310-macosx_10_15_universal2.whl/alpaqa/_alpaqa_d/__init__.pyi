"""
Python interface to alpaqa's C++ implementation.
"""
from __future__ import annotations
import datetime
import typing
from . import float64
from . import longdouble
__all__ = ['ApproxKKT', 'ApproxKKT2', 'BasedOnCurvature', 'BasedOnExternalStepSize', 'Busy', 'Converged', 'EvalCounter', 'FPRNorm', 'FPRNorm2', 'Interrupted', 'Ipopt', 'LBFGSBpp', 'LBFGSStepsize', 'Lower', 'MaxIter', 'MaxTime', 'NoProgress', 'NotFinite', 'OCPEvalCounter', 'PANOCStopCrit', 'ProjGradNorm', 'ProjGradNorm2', 'ProjGradUnitNorm', 'ProjGradUnitNorm2', 'SolverStatus', 'Symmetry', 'Unsymmetric', 'Upper', 'build_time', 'commit_hash', 'float64', 'longdouble', 'not_implemented_error', 'with_casadi', 'with_casadi_ocp', 'with_external_casadi']
class EvalCounter:
    """
    C++ documentation: :cpp:class:`alpaqa::EvalCounter`
    
    """
    class EvalTimer:
        """
        C++ documentation: :cpp:class:`alpaqa::EvalCounter::EvalTimer`
        
        """
        f: datetime.timedelta
        f_g: datetime.timedelta
        f_grad_f: datetime.timedelta
        g: datetime.timedelta
        grad_L: datetime.timedelta
        grad_f: datetime.timedelta
        grad_f_grad_g_prod: datetime.timedelta
        grad_g_prod: datetime.timedelta
        grad_gi: datetime.timedelta
        grad_ψ: datetime.timedelta
        hess_L: datetime.timedelta
        hess_L_prod: datetime.timedelta
        hess_ψ: datetime.timedelta
        hess_ψ_prod: datetime.timedelta
        inactive_indices_res_lna: datetime.timedelta
        jac_g: datetime.timedelta
        proj_diff_g: datetime.timedelta
        proj_multipliers: datetime.timedelta
        prox_grad_step: datetime.timedelta
        ψ: datetime.timedelta
        ψ_grad_ψ: datetime.timedelta
        def __getstate__(self) -> tuple:
            ...
        def __setstate__(self, arg0: tuple) -> None:
            ...
    f: int
    f_g: int
    f_grad_f: int
    g: int
    grad_L: int
    grad_f: int
    grad_f_grad_g_prod: int
    grad_g_prod: int
    grad_gi: int
    grad_ψ: int
    hess_L: int
    hess_L_prod: int
    hess_ψ: int
    hess_ψ_prod: int
    inactive_indices_res_lna: int
    jac_g: int
    proj_diff_g: int
    proj_multipliers: int
    prox_grad_step: int
    time: EvalCounter.EvalTimer
    ψ: int
    ψ_grad_ψ: int
    def __getstate__(self) -> tuple:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
    def __str__(self) -> str:
        ...
class LBFGSStepsize:
    """
    C++ documentation: :cpp:enum:`alpaqa::LBFGSStepSize`
    
    Members:
    
      BasedOnExternalStepSize
    
      BasedOnCurvature
    """
    BasedOnCurvature: typing.ClassVar[LBFGSStepsize]  # value = <LBFGSStepsize.BasedOnCurvature: 1>
    BasedOnExternalStepSize: typing.ClassVar[LBFGSStepsize]  # value = <LBFGSStepsize.BasedOnExternalStepSize: 0>
    __members__: typing.ClassVar[dict[str, LBFGSStepsize]]  # value = {'BasedOnExternalStepSize': <LBFGSStepsize.BasedOnExternalStepSize: 0>, 'BasedOnCurvature': <LBFGSStepsize.BasedOnCurvature: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OCPEvalCounter:
    """
    C++ documentation: :cpp:class:`alpaqa::OCPEvalCounter`
    
    """
    class OCPEvalTimer:
        """
        C++ documentation: :cpp:class:`alpaqa::OCPEvalCounter::OCPEvalTimer`
        
        """
        add_Q: datetime.timedelta
        add_Q_N: datetime.timedelta
        add_R_masked: datetime.timedelta
        add_R_prod_masked: datetime.timedelta
        add_S_masked: datetime.timedelta
        add_S_prod_masked: datetime.timedelta
        add_gn_hess_constr: datetime.timedelta
        add_gn_hess_constr_N: datetime.timedelta
        constr: datetime.timedelta
        constr_N: datetime.timedelta
        f: datetime.timedelta
        grad_constr_prod: datetime.timedelta
        grad_constr_prod_N: datetime.timedelta
        grad_f_prod: datetime.timedelta
        h: datetime.timedelta
        h_N: datetime.timedelta
        jac_f: datetime.timedelta
        l: datetime.timedelta
        l_N: datetime.timedelta
        q_N: datetime.timedelta
        qr: datetime.timedelta
        def __getstate__(self) -> tuple:
            ...
        def __setstate__(self, arg0: tuple) -> None:
            ...
    add_Q: int
    add_Q_N: int
    add_R_masked: int
    add_R_prod_masked: int
    add_S_masked: int
    add_S_prod_masked: int
    add_gn_hess_constr: int
    add_gn_hess_constr_N: int
    constr: int
    constr_N: int
    f: int
    grad_constr_prod: int
    grad_constr_prod_N: int
    grad_f_prod: int
    h: int
    h_N: int
    jac_f: int
    l: int
    l_N: int
    q_N: int
    qr: int
    time: OCPEvalCounter.OCPEvalTimer
    def __getstate__(self) -> tuple:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
    def __str__(self) -> str:
        ...
class PANOCStopCrit:
    """
    C++ documentation: :cpp:enum:`alpaqa::PANOCStopCrit`
    
    Members:
    
      ApproxKKT
    
      ApproxKKT2
    
      ProjGradNorm
    
      ProjGradNorm2
    
      ProjGradUnitNorm
    
      ProjGradUnitNorm2
    
      FPRNorm
    
      FPRNorm2
    
      Ipopt
    
      LBFGSBpp
    """
    ApproxKKT: typing.ClassVar[PANOCStopCrit]  # value = <PANOCStopCrit.ApproxKKT: 0>
    ApproxKKT2: typing.ClassVar[PANOCStopCrit]  # value = <PANOCStopCrit.ApproxKKT2: 1>
    FPRNorm: typing.ClassVar[PANOCStopCrit]  # value = <PANOCStopCrit.FPRNorm: 6>
    FPRNorm2: typing.ClassVar[PANOCStopCrit]  # value = <PANOCStopCrit.FPRNorm2: 7>
    Ipopt: typing.ClassVar[PANOCStopCrit]  # value = <PANOCStopCrit.Ipopt: 8>
    LBFGSBpp: typing.ClassVar[PANOCStopCrit]  # value = <PANOCStopCrit.LBFGSBpp: 9>
    ProjGradNorm: typing.ClassVar[PANOCStopCrit]  # value = <PANOCStopCrit.ProjGradNorm: 2>
    ProjGradNorm2: typing.ClassVar[PANOCStopCrit]  # value = <PANOCStopCrit.ProjGradNorm2: 3>
    ProjGradUnitNorm: typing.ClassVar[PANOCStopCrit]  # value = <PANOCStopCrit.ProjGradUnitNorm: 4>
    ProjGradUnitNorm2: typing.ClassVar[PANOCStopCrit]  # value = <PANOCStopCrit.ProjGradUnitNorm2: 5>
    __members__: typing.ClassVar[dict[str, PANOCStopCrit]]  # value = {'ApproxKKT': <PANOCStopCrit.ApproxKKT: 0>, 'ApproxKKT2': <PANOCStopCrit.ApproxKKT2: 1>, 'ProjGradNorm': <PANOCStopCrit.ProjGradNorm: 2>, 'ProjGradNorm2': <PANOCStopCrit.ProjGradNorm2: 3>, 'ProjGradUnitNorm': <PANOCStopCrit.ProjGradUnitNorm: 4>, 'ProjGradUnitNorm2': <PANOCStopCrit.ProjGradUnitNorm2: 5>, 'FPRNorm': <PANOCStopCrit.FPRNorm: 6>, 'FPRNorm2': <PANOCStopCrit.FPRNorm2: 7>, 'Ipopt': <PANOCStopCrit.Ipopt: 8>, 'LBFGSBpp': <PANOCStopCrit.LBFGSBpp: 9>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class SolverStatus:
    """
    C++ documentation: :cpp:enum:`alpaqa::SolverStatus`
    
    Members:
    
      Busy : In progress.
    
      Converged : Converged and reached given tolerance
    
      MaxTime : Maximum allowed execution time exceeded
    
      MaxIter : Maximum number of iterations exceeded
    
      NotFinite : Intermediate results were infinite or NaN
    
      NoProgress : No progress was made in the last iteration
    
      Interrupted : Solver was interrupted by the user
    """
    Busy: typing.ClassVar[SolverStatus]  # value = <SolverStatus.Busy: 0>
    Converged: typing.ClassVar[SolverStatus]  # value = <SolverStatus.Converged: 1>
    Interrupted: typing.ClassVar[SolverStatus]  # value = <SolverStatus.Interrupted: 6>
    MaxIter: typing.ClassVar[SolverStatus]  # value = <SolverStatus.MaxIter: 3>
    MaxTime: typing.ClassVar[SolverStatus]  # value = <SolverStatus.MaxTime: 2>
    NoProgress: typing.ClassVar[SolverStatus]  # value = <SolverStatus.NoProgress: 5>
    NotFinite: typing.ClassVar[SolverStatus]  # value = <SolverStatus.NotFinite: 4>
    __members__: typing.ClassVar[dict[str, SolverStatus]]  # value = {'Busy': <SolverStatus.Busy: 0>, 'Converged': <SolverStatus.Converged: 1>, 'MaxTime': <SolverStatus.MaxTime: 2>, 'MaxIter': <SolverStatus.MaxIter: 3>, 'NotFinite': <SolverStatus.NotFinite: 4>, 'NoProgress': <SolverStatus.NoProgress: 5>, 'Interrupted': <SolverStatus.Interrupted: 6>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __ge__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __gt__(self, other: typing.Any) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __le__(self, other: typing.Any) -> bool:
        ...
    def __lt__(self, other: typing.Any) -> bool:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Symmetry:
    """
    C++ documentation: :cpp:enum:`alpaqa::sparsity::Symmetry`
    
    Members:
    
      Unsymmetric
    
      Upper
    
      Lower
    """
    Lower: typing.ClassVar[Symmetry]  # value = <Symmetry.Lower: 2>
    Unsymmetric: typing.ClassVar[Symmetry]  # value = <Symmetry.Unsymmetric: 0>
    Upper: typing.ClassVar[Symmetry]  # value = <Symmetry.Upper: 1>
    __members__: typing.ClassVar[dict[str, Symmetry]]  # value = {'Unsymmetric': <Symmetry.Unsymmetric: 0>, 'Upper': <Symmetry.Upper: 1>, 'Lower': <Symmetry.Lower: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class not_implemented_error(NotImplementedError):
    pass
ApproxKKT: PANOCStopCrit  # value = <PANOCStopCrit.ApproxKKT: 0>
ApproxKKT2: PANOCStopCrit  # value = <PANOCStopCrit.ApproxKKT2: 1>
BasedOnCurvature: LBFGSStepsize  # value = <LBFGSStepsize.BasedOnCurvature: 1>
BasedOnExternalStepSize: LBFGSStepsize  # value = <LBFGSStepsize.BasedOnExternalStepSize: 0>
Busy: SolverStatus  # value = <SolverStatus.Busy: 0>
Converged: SolverStatus  # value = <SolverStatus.Converged: 1>
FPRNorm: PANOCStopCrit  # value = <PANOCStopCrit.FPRNorm: 6>
FPRNorm2: PANOCStopCrit  # value = <PANOCStopCrit.FPRNorm2: 7>
Interrupted: SolverStatus  # value = <SolverStatus.Interrupted: 6>
Ipopt: PANOCStopCrit  # value = <PANOCStopCrit.Ipopt: 8>
LBFGSBpp: PANOCStopCrit  # value = <PANOCStopCrit.LBFGSBpp: 9>
Lower: Symmetry  # value = <Symmetry.Lower: 2>
MaxIter: SolverStatus  # value = <SolverStatus.MaxIter: 3>
MaxTime: SolverStatus  # value = <SolverStatus.MaxTime: 2>
NoProgress: SolverStatus  # value = <SolverStatus.NoProgress: 5>
NotFinite: SolverStatus  # value = <SolverStatus.NotFinite: 4>
ProjGradNorm: PANOCStopCrit  # value = <PANOCStopCrit.ProjGradNorm: 2>
ProjGradNorm2: PANOCStopCrit  # value = <PANOCStopCrit.ProjGradNorm2: 3>
ProjGradUnitNorm: PANOCStopCrit  # value = <PANOCStopCrit.ProjGradUnitNorm: 4>
ProjGradUnitNorm2: PANOCStopCrit  # value = <PANOCStopCrit.ProjGradUnitNorm2: 5>
Unsymmetric: Symmetry  # value = <Symmetry.Unsymmetric: 0>
Upper: Symmetry  # value = <Symmetry.Upper: 1>
__version__: str = '1.0.0a18'
build_time: str = '2024-03-27T15:48:28Z'
commit_hash: str = '2906af43b75d5d0d13bc95e1f7bab2934be3a481'
with_casadi: bool = True
with_casadi_ocp: bool = False
with_external_casadi: bool = True
