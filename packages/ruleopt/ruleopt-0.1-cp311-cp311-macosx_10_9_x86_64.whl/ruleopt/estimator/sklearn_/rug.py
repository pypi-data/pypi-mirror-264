from __future__ import annotations
import warnings

import numpy as np
from numpy.typing import ArrayLike
from sklearn.tree import DecisionTreeClassifier

from .base_sklearn import _RUGSKLEARN
from ...rule_cost import Gini
from ...utils import check_inputs


class RUGClassifier(_RUGSKLEARN):
    """
    RUGClassifier iteratively generates and refines rules by partitioning the feature space,
    aiming for a blend of interpretability and accuracy in classification tasks.
    """

    def __init__(
        self,
        solver,
        *,
        rule_cost=Gini(),
        max_rmp_calls=20,
        tree_parameters=None,
        class_weight: dict | str | None = None,
        threshold: float = 1.0e-6,
        random_state: int | None = None,
    ):
        """
        Parameters
        ----------
        solver : OptimizationSolver
            An instance of either ORToolsSolver or UNCSolver. The solver is responsible for
            optimizing the rule set based on the cost function and constraints.
        rule_cost : RuleCost or int, default=Gini()
            Defines the cost of rules, either as a specific calculation method (RuleCost instance)
            or a fixed cost
        max_rmp_calls : int, default=20
            Maximum number of Restricted Master Problem iterations allowed during fitting.
        tree_parameters : dict or None, default=None
            Parameters for the sklearn.DecisionTreeClassifier. Excludes 'random_state'.
            Example: {'max_depth': 10, 'min_samples_split': 2}
        class_weight: dict, "balanced" or None, default=None
            A dictionary mapping class labels to their respective weights, the string "balanced"
            to automatically adjust weights inversely proportional to class frequencies,
            or None for no weights. Used to adjust the model in favor of certain classes.
        threshold : float, default=1.0e-6
            The minimum weight threshold for including a rule in the final model
        random_state : int or None, default=None
            Seed for the random number generator to ensure reproducible results.
            Defaults to None.
        """

        if hasattr(solver, "max_rule"):
            if getattr(solver, "max_rule") is not None:
                warnings.warn(
                    "The 'max_rule' attribute is available only for RUX classifiers. "
                    "It has been automatically set to 'None' for the current solver."
                )
                solver.max_rule = None

        super().__init__(
            threshold=threshold,
            random_state=random_state,
            solver=solver,
            rule_cost=rule_cost,
            class_weight=class_weight,
        )
        self._validate_parameters(max_rmp_calls, tree_parameters)
        self.max_rmp_calls = int(max_rmp_calls)
        self.tree_parameters = {} if tree_parameters is None else tree_parameters

    def _pspdt(
        self,
        x: np.ndarray,
        y: np.ndarray,
        vec_y: np.ndarray,
        fit_tree: DecisionTreeClassifier,
        treeno: int,
        betas: np.ndarray,
    ) -> bool:
        """
        Performs Pricing SubProblem for Decision Trees (PSPDT) in the column generation process.

        Parameters
        ----------
        x : np.ndarray
            Feature matrix of the training data.
        y : np.ndarray
            Target vector of the training data.
        vec_y : np.ndarray
            Preprocessed target vector, adjusted for optimization.
        fit_tree : DecisionTreeClassifier
            Decision tree fitted on data reweighted according to dual variables.
        treeno : int
            Identifier for the current tree in the iterative process.
        betas : np.ndarray
            Dual variables from the latest LP solution.

        Returns
        -------
        bool
            Indicates whether a new rule that improves the objective function was found.
        """
        no_improvement = True

        n, col = x.shape[0], np.max(self.coefficients_.cols) + 1

        # Apply the decision tree to the feature matrix
        y_rules = fit_tree.apply(x)

        for leafno in np.unique(y_rules):
            # Get the samples that fall into this leaf
            covers = np.where(y_rules == leafno)[0]
            leaf_y_vals = y[covers]  # y values of the samples in the leaf

            # Get the unique labels in the leaf and their counts
            unique_labels = np.arange(self.k_, dtype=np.intp)
            counts = np.zeros(self.k_, dtype=np.intp)
            unique_labels_, counts_ = np.unique(leaf_y_vals, return_counts=True)
            for i, j in enumerate(unique_labels_):
                unique_labels[j] = unique_labels_[i]
                counts[j] = counts_[i]

            # Identify the majority class in the leaf
            label = unique_labels_[np.argmax(counts_)]  # majority class in the leaf

            # Create a vector for this label
            label_vector = np.full((self.k_,), -1 / (self.k_ - 1))
            label_vector[label] = 1

            # Calculate the y values for the optimization problem
            fill_ahat = np.dot(vec_y[covers, :], label_vector)

            # Prepare to check the reduced cost
            aijhat = np.zeros(n)
            aijhat[covers] = fill_ahat

            cost = self._get_rule_cost(
                temp_rule=self._get_rule(fit_tree, leafno),
                covers=covers,
                counts=counts,
                y=y,
            )

            # Calculate the reduced cost
            red_cost = np.dot(
                np.multiply(((self.k_ - 1.0) / self.k_), aijhat), betas
            ) - (cost * self.solver.penalty)

            # If the reduced cost is positive, update the coefficients
            if red_cost > 0:  # only columns with proper reduced costs are added
                covers_fill = np.full((covers.shape[0],), fill_ahat, dtype=np.intp)
                covers_col = np.full((covers.shape[0],), col, dtype=np.intp)
                self.coefficients_.rows = np.concatenate(
                    (self.coefficients_.rows, covers)
                )
                self.coefficients_.cols = np.concatenate(
                    (self.coefficients_.cols, covers_col)
                )
                self.coefficients_.yvals = np.concatenate(
                    (self.coefficients_.yvals, covers_fill)
                )
                self.coefficients_.costs = np.concatenate(
                    (self.coefficients_.costs, [cost])
                )

                # Calculate the distribution of the samples in the leaf across the classes
                sdist = np.zeros(self.k_, dtype=np.intp)
                sdist[unique_labels] = counts
                self.rule_info_[col] = (treeno, leafno, label, sdist)
                col += 1
                no_improvement = False

        # Return whether there was any improvement
        return no_improvement

    def _fit_decision_tree(
        self, x: np.ndarray, y: np.ndarray, sample_weight: np.ndarray
    ) -> DecisionTreeClassifier:
        """
        Fits a decision tree to the data, taking into account sample weights.

        Parameters
        ----------
        x : np.ndarray
            Feature matrix of the training data.
        y : np.ndarray
            Target vector of the training data.
        sample_weight : np.ndarray
            Array of weights for the samples, influencing the fitting process of the decision tree.

        Returns
        -------
        DecisionTreeClassifier
            A decision tree classifier fitted to the weighted data.
        """
        if (
            self.tree_parameters.get("class_weight") is not None
            and sample_weight is not None
        ):
            self.tree_parameters.pop("class_weight")
        # Initialize a DecisionTreeClassifier with specified parameters
        dt = DecisionTreeClassifier(
            random_state=self._rng.integers(
                np.iinfo(np.int16).max
            ),  # Ensuring a large integer for random_state
            **self.tree_parameters,
        )

        # Fit the decision tree to the data
        return dt.fit(x, y, sample_weight=sample_weight)

    def _fill_ahat(
        self,
        x: np.ndarray,
        y: np.ndarray,
        vec_y: np.ndarray,
        fit_tree_: DecisionTreeClassifier = None,
        treeno_: int = None,
    ):
        """
        Updates the optimization problem's coefficients based on the rules from a decision tree.

        Parameters
        ----------
        x : np.ndarray
            Feature matrix of the training data.
        y : np.ndarray
            Target vector of the training data.
        vec_y : np.ndarray
            Preprocessed target vector, adjusted for optimization.
        fit_tree : DecisionTreeClassifier, optional
            A decision tree from which to extract rules. If not provided, the method will
            use existing trees.
        treeno : int, optional
            Identifier for the decision tree within an ensemble or sequence of generated trees.
        """
        # Initialize coefficients for the next batch.
        self.coefficients_.cleanup()

        # If there are existing rules, process them to fill the coefficient matrix
        if len(self.rule_info_) > 0:
            for col, (treeno, leafno, label, _) in self.rule_info_.items():
                # Retrieve the decision tree corresponding to the current rule
                fit_tree = self.decision_trees_[treeno]

                # Apply the decision tree to the feature matrix to get the leaf indices
                # for each sample
                y_rules = fit_tree.apply(x)

                # Identify the samples that fall into the current leaf
                covers = np.where(y_rules == leafno)[0]
                leaf_y_vals = y[covers]

                # Compute the unique labels in the leaf and their counts
                unique_labels, counts = np.unique(leaf_y_vals, return_counts=True)

                # Determine the majority class label in the leaf
                label = unique_labels[np.argmax(counts)]

                # Create a vector representation of this label
                label_vector = np.full((self.k_,), -1 / (self.k_ - 1))
                label_vector[label] = 1

                fill_ahat = np.dot(vec_y[covers, :], label_vector)

                self.coefficients_.rows = np.concatenate(
                    (self.coefficients_.rows, covers)
                )
                self.coefficients_.cols = np.concatenate(
                    (self.coefficients_.cols, [col] * covers.shape[0])
                )
                self.coefficients_.yvals = np.concatenate(
                    (self.coefficients_.yvals, np.full(covers.shape[0], fill_ahat))
                )

                cost = self._get_rule_cost(
                    temp_rule=self._get_rule(fit_tree, leafno),
                    covers=covers,
                    counts=counts,
                    y=y,
                )

                self.coefficients_.costs = np.concatenate(
                    (self.coefficients_.costs, [cost])
                )

        # If a specific decision tree is provided, update the coefficient matrix based on this tree
        if fit_tree_:
            self._get_matrix(x, y, vec_y, fit_tree_, treeno_)

    def fit(self, x: ArrayLike, y: ArrayLike, sample_weight: ArrayLike | None = None):
        """
        Fits the RUGClassifier model to the training data using a column generation approach.

        Parameters
        ----------
        x : array-like of shape (n_samples, n_features)
            The training input samples. Internally, it will be converted to dtype=np.float32.
        y : array-like of shape (n_samples,) or (n_samples, n_outputs)
            The target values (class labels) as integers
        sample_weight : array-like of shape (n_samples,), default=None
            Sample weights. If None, then samples are equally weighted.

        Returns
        -------
        self : RUGClassifier
            The fitted model.
        """
        x, y = check_inputs(x, y)
        if self._is_fitted:
            self._cleanup()

        treeno = 0
        fit_tree = self._fit_decision_tree(x, y, sample_weight=None)
        self.decision_trees_[treeno] = fit_tree

        self._get_class_infos(y)
        vec_y = self._preprocess(y)
        self._get_matrix(x, y, vec_y, fit_tree, treeno)

        sample_weight = self._get_sample_wight(sample_weight, self.class_weight, y)

        ws, betas = self.solver(
            coefficients=self.coefficients_, k=self.k_, sample_weight=sample_weight
        )

        # Column generation
        for _ in range(self.max_rmp_calls):
            if np.all(betas == 0):
                break

            treeno += 1
            fit_tree = self._fit_decision_tree(x, y, sample_weight=betas)
            self.decision_trees_[treeno] = fit_tree

            no_improvement = self._pspdt(x, y, vec_y, fit_tree, treeno, betas)

            if no_improvement:
                break

            ws, betas = self.solver(
                coefficients=self.coefficients_,
                k=self.k_,
                ws0=ws.copy(),
                sample_weight=sample_weight,
            )

        self._fill_rules(ws)
        self._is_fitted = True

        return self

    def _validate_parameters(self, max_rmp_calls: int, tree_parameters: dict | None):
        # max_rmp_calls için tip ve değer kontrolü
        if not isinstance(max_rmp_calls, (float, int)):
            raise TypeError("max_rmp_calls must be an integer.")

        if max_rmp_calls < 0:
            raise ValueError("max_rmp_calls must be a non-negative integer.")

        if tree_parameters is None:
            pass

        else:
            if isinstance(tree_parameters, dict):
                if "random_state" in tree_parameters:
                    warnings.warn(
                        "random_state parameter in tree_parameters non_used. ",
                        "Use random_state parameter in class parameters.",
                    )
                    tree_parameters.pop("random_state", None)

                expected_keys = {
                    "criterion",
                    "splitter",
                    "max_depth",
                    "min_samples_split",
                    "min_samples_leaf",
                    "min_weight_fraction_leaf",
                    "max_features",
                    "random_state",
                    "max_leaf_nodes",
                    "min_impurity_decrease",
                    "class_weight",
                    "ccp_alpha",
                    "monotonic_cst",
                }

                extra_keys = set(tree_parameters.keys()) - expected_keys

                if extra_keys:
                    raise ValueError(f"Unexpected parameter keys: {extra_keys}")

            else:
                raise TypeError("tree_parameters must be a dictionary or None.")
