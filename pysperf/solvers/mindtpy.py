from pyomo.environ import SolverFactory

from pysperf.config import get_base_gams_options_list
from pysperf import _JobResult, options
from pysperf.solver_library_tools import register_solve_function


@register_solve_function(
    name="MindtPy-OA",
    milp="cplex", nlp="ipopth"
)
def OA(pyomo_model):
    job_result = _JobResult()
    pyomo_results = SolverFactory('gdpopt').solve(
        pyomo_model,
        strategy='OA',
        tee=True,
        mip_solver='gams',
        mip_solver_args=dict(solver='cplex', add_options=get_base_gams_options_list()),
        nlp_solver='gams',
        nlp_solver_args=dict(solver='ipopth', add_options=get_base_gams_options_list()),
        iterlim=300,
        time_limit=options.time_limit
    )
    job_result.solver_run_time = pyomo_results.solver.timing.total
    job_result.pyomo_solver_status = pyomo_results.solver.status
    job_result.iterations = pyomo_results.solver.iterations
    job_result.termination_condition = pyomo_results.solver.termination_condition
    job_result.LB = pyomo_results.problem.lower_bound
    job_result.UB = pyomo_results.problem.upper_bound
    return job_result