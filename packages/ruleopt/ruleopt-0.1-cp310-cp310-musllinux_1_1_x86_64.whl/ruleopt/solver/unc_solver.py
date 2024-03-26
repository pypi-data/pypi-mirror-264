import numpy as np
from scipy.sparse import csr_matrix
from ..utils import check_module_available
from .base import OptimizationSolver

TORCH_AVAILABLE = check_module_available("torch")


class _TorchSolverManager:
    _torch_solver_class = None

    @staticmethod
    def _initialize_torch_solver():

        from torch import ones, topk, relu, zeros_like, sum, matmul
        from torch.nn import Module, Parameter

        class _TorchSolver(Module):
            """
            A Solver module for constrained optimization problems using PyTorch.

            This module is designed to solve optimization problems with a specific structure,
            leveraging the PyTorch framework for gradient-based optimization. It uses parameters,
            constraints, and a penalty method to find a solution that minimizes the given
            objective function while satisfying the constraints.

            Attributes:
                max_rule (int): The maximum number of rules to be selected.
                ws (torch.nn.Parameter): Weights associated with each rule.
                gates (torch.nn.Parameter): Gate parameters to control rule selection.
                vs (torch.nn.Parameter): Slack variables for handling constraints.
                penalty (float): Penalty parameter for the objective function.
                a_hat (torch.Tensor): Coefficient matrix after processing.
                costs (torch.Tensor): Cost associated with each rule.
            """

            def __init__(self, m, penalty, costs, k, max_rule=None, sample_weight=None):
                """
                Initializes the Solver with given parameters and coefficients.

                Parameters:
                    m (int): Number of rules.
                    penalty (float): Penalty parameter for the cost in the objective function.
                    coefficients (object): An object containing the sparse matrix coefficients ('yvals', 'rows', 'cols'),
                                            and costs associated with each rule ('costs').
                    k (float): A scaling factor for the coefficients.
                    max_rule (int): The maximum number of rules to be selected.
                """
                super().__init__()
                self.max_rule = max_rule if max_rule is not None else float("inf")

                self.ws = Parameter(ones(m, requires_grad=True))

                self.sample_weight = sample_weight

                self.penalty = penalty

                self.costs = costs

                self.k = k

                self.m = m

            def forward(self, a_hat):
                """
                Defines the forward pass for the optimization problem.

                Performs the selection of rules based on the weighted gates, calculates the
                objective function, and applies penalties for constraint violations.

                Returns:
                    torch.Tensor: The total loss comprising the objective function and penalties for constraint violations.
                """
                if self.max_rule < self.m:
                    _, indices = topk(self.ws, self.max_rule, sorted=False)
                    selected_weights = zeros_like(self.ws)
                    selected_weights.index_fill_(0, indices, 1)
                    ws = relu(self.ws) * selected_weights
                else:
                    ws = relu(self.ws)

                objective_ws = self.penalty * sum(self.costs * ws)

                betas = ((self.k - 1.0) / self.k) * relu(
                    1 - matmul(a_hat, ws.unsqueeze(-1)).squeeze()
                )

                if self.sample_weight is not None:
                    betas = betas * self.sample_weight

                betas_penalty = sum(betas)

                total_loss = objective_ws + betas_penalty

                inspection_values = {
                    "betas": betas,
                    "ws": ws,
                }

                return total_loss, inspection_values

        return _TorchSolver

    @classmethod
    def get_torch_solver(cls, *args, **kwargs):
        if cls._torch_solver_class is None:
            cls._torch_solver_class = cls._initialize_torch_solver()
        return cls._torch_solver_class(*args, **kwargs)


class UNCSolver(OptimizationSolver):
    """
    A gradient descent solver for optimization problems, leveraging PyTorch for gradient-based optimization.

    This solver iteratively updates parameters to minimize an objective function, applying penalties
    for constraint violations. It utilizes a gradient descent approach with early stopping based on
    a patience parameter to prevent overfitting.
    """

    def __new__(cls, *args, **kwargs):
        if not TORCH_AVAILABLE:
            raise ImportError(
                "PyTorch is required for this class but is not installed.",
                "Please install it with 'pip install pytorch'",
            )
        instance = super(UNCSolver, cls).__new__(cls)
        return instance

    def __init__(
        self,
        penalty: float = 2.0,
        lr: float = 0.01,
        weight_decay: float = 0.1,
        max_rule: int | None = None,
        patience: int = 100,
        device: str = "cpu",
        use_sparse: bool = False,
    ) -> None:
        """
        Parameters
        ----------
        penalty : float, default=2.0
            Penalty parameter for the cost in the objective function.
        lr : float, default=0.01
            Learning rate for the Adam optimizer.
        weight_decay : float, default=0.01
            Weight decay (L2 penalty) for the optimizer.
        max_rule : int or None, default=None
            Maximum number of rules to be selected. If None, no limit is applied.
        patience : int, default=100
            Number of iterations to wait for an improvement before stopping the optimization.
        device : {"cuda", "cpu"}, default="cpu"
            The device on which to perform computations.
        use_sparse : bool, default=False
            Determines whether to use a sparse matrix representation for the optimization
            problem. Using sparse matrices can significantly reduce memory usage and improve
            performance for large-scale problems with many zeros in the data.
        """
        self.penalty = penalty
        self.lr = lr
        self.weight_decay = weight_decay
        self.max_rule = max_rule
        self.patience = patience
        self.device = device
        self.use_sparse = use_sparse
        super().__init__()
        super()._check_params()

    def __call__(self, coefficients, k, sample_weight=None, *args, **kwargs):
        """
        Executes the heuristic optimization process on given problem coefficients.

        Parameters
        ----------
        coefficients : object
            An object containing the sparse matrix coefficients ('yvals', 'rows', 'cols'),
            and costs associated with each rule ('costs').
        k : float
            A scaling factor for the coefficients.
        ws0 : array-like, optional
            Initial weights for the optimization process. If provided, should have the same
            length as the number of rules. Otherwise, weights are initialized to ones.

        Returns
        -------
        ws : numpy.ndarray
            The optimized weights for each rule after the optimization process.
        betas : numpy.ndarray
            The betas values indicating constraint violations for the optimized solution.
        """
        ### LAZY IMPORT
        from torch import tensor, sparse_csr_tensor, from_numpy, float32
        from torch.optim import Adam
        from torch.optim.lr_scheduler import ReduceLROnPlateau

        a_hat = csr_matrix(
            (
                coefficients.yvals,
                (coefficients.rows, coefficients.cols),
            ),
            dtype=np.float64,
        ) * ((k - 1.0) / k)

        if not self.use_sparse:
            a_hat = tensor(a_hat.toarray(), dtype=float32, device=self.device)

        else:
            a_hat = sparse_csr_tensor(
                from_numpy(a_hat.indptr),
                from_numpy(a_hat.indices),
                from_numpy(a_hat.data),
                dtype=float32,
                device=self.device,
            )

        if sample_weight is not None:
            sample_weight = tensor(sample_weight, dtype=float32)

        costs = tensor(coefficients.costs, dtype=float32, device=self.device)

        m = a_hat.shape[1]

        solver = _TorchSolverManager.get_torch_solver(
            m=m,
            k=k,
            penalty=self.penalty,
            costs=costs,
            max_rule=self.max_rule,
            sample_weight=sample_weight,
        ).to(self.device)

        optimizer = Adam(
            solver.parameters(), lr=self.lr, weight_decay=self.weight_decay
        )
        scheduler = ReduceLROnPlateau(
            optimizer, "min", factor=0.1, patience=self.patience // 4
        )

        best_loss = float("inf")
        counter = 0

        ws = None
        betas = None

        while True:
            optimizer.zero_grad()
            loss, inspection_values = solver(a_hat)
            loss.backward()
            optimizer.step()

            scheduler.step(loss)

            if loss.item() < best_loss:
                best_loss = loss.item()
                ws = inspection_values.get("ws").detach().cpu().numpy()
                betas = inspection_values.get("betas").detach().cpu().numpy()
                counter = 0
            else:
                counter += 1
                if counter > self.patience:
                    break

        return ws, np.where(betas <= 1.0e-4, 0, betas)
