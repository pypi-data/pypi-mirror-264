import numpy as np
import pandas as pd
from scipy.optimize import least_squares, root
from typing import Union, Optional, Type, List

from ..components import Component
from ..actmodels import ActModel
from ..utils.spacing import spacing
from ..utils.lle_scanner import estimate_lle_from_gmix


class LLE:
    def __init__(self,
                 actmodel: Union[ActModel, Type[ActModel]],
                 mixture: Optional[List[Component]] = None) -> None:
        self.actmodel = actmodel
        self.mixture = mixture
        self._validate_arguments()

    def fobj_binodal(self, x1, T):
        # Equilibrium: Isoactivity criterion (aL1 - aL2 = 0)
        x = np.array([x1, 1-x1])
        activity = self.actmodel.activity(T, x)
        equilibrium = np.diff(activity, axis=1)
        return equilibrium.ravel() # reshape from (2,1) --> (2,)

    def fobj_spinodal(self, x1):
        T = 0
        x = np.array([x1, 1-x1])
        return self.actmodel.thermofac(T, x)

    def binodal(self, T, x0=None, solver='least_squares'):
        if x0 is None:
            x0 = [0.1, 0.999]    # 1_N2_Ethan

        if solver == 'least_squares':
            kwargs = dict(bounds=(0,1), ftol=1e-15, xtol=1e-15)
            res = least_squares(self.fobj_binodal, x0, args=(T,), **kwargs)
            # print(res.nfev)
            return res.x, res.nfev
        else:
            kwargs = dict(method='krylov', options={'maxiter': 5})
            res = root(self.fobj_binodal, x0, args=(T,), **kwargs)
            # print(res.nit)
            return res.x, 30

    def spinodal(self, x0=None):
        if x0 is None:
            x0 = self.binodal()
        return least_squares(self.fobj_spinodal, x0).x

# =============================================================================
# TODO: (1) Add some "approx_initial_values" function based on gmix
# TODO: (2) Overall improve this code to match the SLE code
# =============================================================================
    def approx_init_x0(self, T):
        x1 = spacing(0,1,51,'poly',n=3)
        gmix = self.actmodel.gmix(T, x1)
        xL, xR, yL, yR = estimate_lle_from_gmix(x1, gmix, rough=True)
        return xL, xR

    def solve_lle(self, T, x0, solver='least_squares', info=True):
        binodal_x, nfev = self.binodal(T, x0, solver)
        binodal_w = self.actmodel._convert(binodal_x)
        formatted_w_binodal = [f"wL{i+1}={value:.4f}" for i, value in enumerate(binodal_w)]
        formatted_x_binodal = [f"xL{i+1}={value:.6f}" for i, value in enumerate(binodal_x)]
        msg = ('LLE: ', f"{T=:.2f}", *formatted_w_binodal, *formatted_x_binodal)
        if info:
            print(*msg)
            return binodal_x, binodal_w, nfev
        return binodal_x, binodal_w, nfev, msg

    def miscibility(self, T, x0=None, max_gap=0.1, max_T=500, dT=25, exponent=2):
        """ Calculate miscibility """
        print()
        print("Calculating LLE...")
        res = []

        if x0 is None:
            print("...searching for suitable initial value...")
            x0 = self.approx_init_x0(T)
        binodal_x, binodal_w, nfev, msg = self.solve_lle(T, x0, info=False)

        # Check if initial guess is reasonalble - otherwise increase T
        while binodal_x[0] < x0[0] and T <= max_T:
            print('LLE: ', f"{T=:.2f}", "...no feasbible initial value found.")
            T += 10  # Increase T by 10
            x0 = self.approx_init_x0(T)
            binodal_x, binodal_w, nfev, msg = self.solve_lle(T, x0, info=False)
        print("Suitable initial value found! Proceed with calculating LLE...")
        print(*msg)
        gap = np.diff(binodal_w)[0]
        res.append((T, *binodal_w, *binodal_x))

        while gap > max_gap and T <= max_T:
            solver = 'least_squares' if nfev <= 30 else 'root'
            solver = 'least_squares'
            # print(solver)
            T += dT * gap**exponent
            x0 = binodal_x
            binodal_x, binodal_w, nfev = self.solve_lle(T, x0, solver)
            gap = np.diff(binodal_w)[0]
            res.append((T, *binodal_w, *binodal_x))

        columns = ['T', 'wL1', 'wL2', 'xL1', 'xL2']
        res = pd.DataFrame(res, columns=columns)
        return res

# =============================================================================
# AUXILLIARY FUNCTIONS
# =============================================================================
    def _validate_arguments(self):
        """Validate the arguments for the LLE class."""
        # TODO: Insert case where both actmodel and mixture are provided (check if acmodel.mixture == mixture, if not raise warning)
        if isinstance(self.actmodel, ActModel):
            # If actmodel is an instance of ActModel
            self.mixture: List[Component] = self.mixture or self.actmodel.mixture
        elif isinstance(self.actmodel, type) and issubclass(self.actmodel, ActModel):
            # If actmodel is a class (subclass of ActModel)
            if self.mixture is None:
                raise ValueError("Please provide a valid mixture:Mixture.")
            self.actmodel: ActModel = self.actmodel(self.mixture)
        else:
            # If actmodel is neither an instance nor a subclass of ActModel
            err = "'actmodel' must be an instance or a subclass of 'ActModel'"
            raise ValueError(err)
