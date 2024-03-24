import mcnets.main as mc
from __deprecated import MCNeuralNetwork
import numpy as np

# SOUP requirements
from main import copy, r2d2, sig



# ==================== Models ==================== #

# SOUP Regressor (Sub-Ordinary Universal Polynomial)
## The SOUP models are good, but the np.clip should really
## be replaced with L2 and L1 penalties instead
class MCSoupRegressor:
    def __init__(self, coef_bounds = (-1, 1), use_tan=False, round_threshold=1e-5):
        # Desc
        """
        ## Sub-Ordinary Universal Polynomial

        Creates a large fittable funtion/""polynomial"" for every X feature given in .fit

        - coef_bounds
            - These are the min and max bounds that the coefficients (k_i) in f(x) can take.
              Feel free to experiment with various ranges, though (-1, 1) tends to work just fine.
        - use_tan
            - Three TAN(x) terms are included in f(x), but due to the asymptotic nature of TAN, they
              can actually hurt model preformance. So, this is disabled by default, but left as a
              setting to try anyways.
        - round_threshold
            - When adjusting the coefficients of the model, if a single coefficient's magnitude falls
              below this threshold, it is rounded to 0. This makes it easier for the model to completely
              remove terms from its various f(x) equations if it finds that is better.


        ## Technical Breakdown

        For each column of (Normalized!) data, generates a function of best fit of the form:

        f(x) = k0 + k1*(|x|**0.5) + k2*(x) + k3*(x**2) + k4*sin(x/3) + k5*sin(x) + k6*sin(3x) + 

               k7*cos(x/3) + k8*cos(x) + k9*cos(3x) + k10*tan(x/3) + k11*tan(x) + k12*tan(3x) + 

               k13*e**(x/3) + k14*e**(x) + k15*e**(3x) + k16*e**(-x/3) + k17*e**(-x) + k18*e**(-3x)

        There is an f(x) for every x feature. This means the net model is:

        F(x) = SUM[f_i(x)] for i=[0, 1, ..., (# of features - 1)]

        And no, I will not write it out more than that. You can see how large one f(x) alone is!

        TODO:
        - Add more function parts!
        - Function customization?
            - Add filter on which parts to ignore if any
        """

        # Unchanging attributes
        self.FUNCTION_LENGTH = 19
        self.USE_TAN = use_tan
        self.ROUND = round_threshold

        # Changable attributes
        self._coefs = 0
        self.coef_bounds = coef_bounds
        self.num_features = 0
        self.parameters = 0
        self.fitted = False

    ## coefs Handling ##
    @property
    def coefs(self):
        return self._coefs

    @coefs.setter
    def coefs(self, new_coefs):      
        self._coefs = new_coefs.copy()
        self._coefs[np.abs(self._coefs) < self.ROUND] = 0

    ## Model Functions ##
    def predict(self, X:np.ndarray, run_debug=False):
        """
        Calculates each ungodly f(x) described in the __init__ for each row in X.

        (Actually iterates over columns/features to speed things up)
        """

        # Verify the shape of X (and num_features)
        if run_debug:
            if len(X.shape) == 1 and self.num_features > 1:
                raise ValueError(f"Expected X array shape of ({len(X)}, {self.num_features}), got {X.shape}")
            elif len(X.shape) > 1 and X.shape[1] != self.num_features:
                raise ValueError(f"Expected X array shape of ({len(X)}, {self.num_features}), got {X.shape}")
            
        # Main function, per feature
        def f(x, col_index):
            """Yes this is f(x) from above. Rip readability *shrug*"""

            # Get function coefficients for this feature
            k = self.coefs[col_index].flatten()

            # Good lord
            return (k[0] + k[1]*(np.abs(x)**0.5) + k[2]*x + k[3]*(x**2) + k[4]*np.sin(x/3) + k[5]*np.sin(x) + k[6]*np.sin(3*x) + 
                    k[7]*np.cos(x/3) + k[8]*np.cos(x) + k[9]*np.cos(3*x) + self.USE_TAN*k[10]*np.tan(x/3) + self.USE_TAN*k[11]*np.tan(x) + self.USE_TAN*k[12]*np.tan(3*x) + 
                    k[13]*np.exp(x/3) + k[14]*np.exp(x) + k[15]*np.exp(3*x) + k[16]*np.exp(-x/3) + k[17]*np.exp(-x) + k[18]*np.exp(-3*x))
        
        # Calculate the sum described in INIT
        result = 0
        for col_index in range(self.num_features):
            result += f(X[:, col_index], col_index=col_index)

        return result

    def fit(self, X, Y, Ieta=100, Beta=25, Gamma=50, dropout=0.9, init_adj_max=2, verbose=True):
        """
        ## Function
        Adjusts the model's coefficients for N iterations. Returns the fitted model in-place.

        ## Inputs
        - X
            - The input data to make predictions with
        - Y
            - The data to test model outputs too
        - N
            - The number of iterations to run to attempt to improve the model
        - beta
            - Number of adjustments tested to the current best model, per iteration
        - gamma
            - Every gamma # of iterations, the scale of the adjustments made to the model
              coefficients are reduced by 1/2
        - dropout
            - (Approximately) The % of coefficients that are NOT adjusted per beta test. These are picked randomly.
            - Stay in school!
        - init_adj_max
            - The initial maximum amplitude that adjustments can make to an individual model coefficient.
              Having this much larger than the coefficient bounds makes finding improvements slower. Having
              this value be too small will cause not many meaningful adjustments to be made.
        - verbose
            - Whether or not an update of iteration # and current model score is printed (in one line) every
              10 iterations.
        """

        # Check if model initial fit complete
        if not self.fitted:
            # Generate the coefficients for each feature
            if len(X.shape) == 2:
                self.num_features = X.shape[1]
                self.coefs = np.random.rand(self.num_features, self.FUNCTION_LENGTH)
            elif len(X.shape) == 1:
                # Assume a singular feature
                self.num_features = 1
                self.coefs = np.random.rand(self.num_features, self.FUNCTION_LENGTH)
            else:
                raise ValueError(f"X Array Must be 1 or 2 Dimensional! Not {len(X.shape)}-Dimensional")
            
            # Confirm initial fit
            self.parameters = self.coefs.size
            self.fitted = True

        # Tweak params for N iterations
        score = r2d2(self.predict(X), Y)
        for itr in range(Ieta):
            add_mode = itr%2

            # Get dropout filter and apply it (discards changing drapout % num of coefficients)
            filt = np.random.rand(self.num_features, self.FUNCTION_LENGTH) > dropout

            # Get Tweak amplitude adjustment
            adjustments = []
            for _ in range(Beta):
                adjustments.append(filt * init_adj_max*(2**(-(itr) / Gamma)) * 2*(np.random.rand(self.num_features, self.FUNCTION_LENGTH) - 0.5))

            # Apply adjustment to test coeff array
            og_coefs = self.coefs.copy()
            test_scores = []
            for adj in adjustments:
                if add_mode:
                    self.coefs = np.clip(og_coefs+adj, self.coef_bounds[0], self.coef_bounds[1])
                else:
                    self.coefs = np.clip(og_coefs*adj, self.coef_bounds[0], self.coef_bounds[1])
                test_scores.append(self.score(X, Y))

            # Test new coef array score
            best_score = max(test_scores)
            if best_score > score:
                score = best_score

                best_adj = adjustments[test_scores.index(best_score)]

                if add_mode:
                    self.coefs = np.clip(og_coefs+best_adj, self.coef_bounds[0], self.coef_bounds[1])
                else:
                    self.coefs = np.clip(og_coefs*best_adj, self.coef_bounds[0], self.coef_bounds[1])

            else:
                self.coefs = og_coefs

            # Print status
            if verbose and (itr+1)%10 == 0:
                print(f"Iteration #{itr+1} | Score = {format(score, '.6f')}        ", end='\r')
        
        if verbose:
            print(f"Iteration #{itr+1} | Score = {format(score, '.6f')}        ")

    def score(self, X, Y, **kwargs):
        """
        Return the models R2 score to the given X and Y Data
        """
        return r2d2(self.predict(X), Y)

    def CopyNet(self):
        """
        Copy a model object to a new variable. Used in similar
        situations as NumPy's copy method to make an isolated net
        with the same values and properties as the parent net.
        """
        # Check that it is fitted
        if self.fitted == False:
            raise ValueError("Model is not yet fitted and therefore cannot be copied")

        return copy.deepcopy(self)

# SOUP Classifier (Sub-Ordinary Universal Polynomial)
## The SOUP models are good, but the np.clip should really
## be replaced with L2 and L1 penalties instead
class MCSoupClassifier:
    def __init__(self, coef_bounds = (-1, 1), use_tan=False, round_threshold=1e-5):
        # Desc
        """
        ## Sub-Ordinary Universal Polynomial

        Creates a large fittable funtion/""polynomial"" for every X feature given in .fit

        - coef_bounds
            - These are the min and max bounds that the coefficients (k_i) in f(x) can take.
              Feel free to experiment with various ranges, though (-1, 1) tends to work just fine.
        - use_tan
            - Three TAN(x) terms are included in f(x), but due to the asymptotic nature of TAN, they
              can actually hurt model preformance. So, this is disabled by default, but left as a
              setting to try anyways.
        - round_threshold
            - When adjusting the coefficients of the model, if a single coefficient's magnitude falls
              below this threshold, it is rounded to 0. This makes it easier for the model to completely
              remove terms from its various f(x) equations if it finds that is better.


        ## Technical Breakdown

        For each column of (Normalized!) data, generates a function of best fit of the form:

        f(x) = k0 + k1*(|x|**0.5) + k2*(x) + k3*(x**2) + k4*sin(x/3) + k5*sin(x) + k6*sin(3x) + 

               k7*cos(x/3) + k8*cos(x) + k9*cos(3x) + k10*tan(x/3) + k11*tan(x) + k12*tan(3x) + 

               k13*e**(x/3) + k14*e**(x) + k15*e**(3x) + k16*e**(-x/3) + k17*e**(-x) + k18*e**(-3x)

        There is an f(x) for every x feature. This means the net model is:

        F(x) = SUM[f_i(x)] for i=[0, 1, ..., (# of features - 1)]

        And no, I will not write it out more than that. You can see how large one f(x) alone is!

        TODO:
        - Add more function parts!
        - Function customization?
            - Add filter on which parts to ignore if any
        """

        # Unchanging attributes
        self.FUNCTION_LENGTH = 19
        self.USE_TAN = use_tan
        self.ROUND = round_threshold

        # Changable attributes
        self._coefs = 0
        self.coef_bounds = coef_bounds
        self.num_features = 0
        self.parameters = 0
        self.fitted = False
        self.num_classes = None

    ## coefs Handling ##
    @property
    def coefs(self):
        return self._coefs

    @coefs.setter
    def coefs(self, new_coefs):      
        self._coefs = new_coefs.copy()
        self._coefs[np.abs(self._coefs) < self.ROUND] = 0

    ## Model Functions ##
    def predict(self, X:np.ndarray, run_debug=False):
        """
        Calculates each ungodly f(x) described in the __init__ for each row in X.

        (Actually iterates over columns/features to speed things up)
        """

        # Verify the shape of X (and num_features)
        if run_debug:
            if len(X.shape) == 1 and self.num_features > 1:
                raise ValueError(f"Expected X array shape of ({len(X)}, {self.num_features}), got {X.shape}")
            elif len(X.shape) > 1 and X.shape[1] != self.num_features:
                raise ValueError(f"Expected X array shape of ({len(X)}, {self.num_features}), got {X.shape}")
            
        # Main function, per feature
        def f(x, col_index):
            """Yes this is f(x) from above. Rip readability *shrug*"""

            # Get function coefficients for this feature
            k = self.coefs[col_index].flatten()

            # Good lord
            return (k[0] + k[1]*(np.abs(x)**0.5) + k[2]*x + k[3]*(x**2) + k[4]*np.sin(x/3) + k[5]*np.sin(x) + k[6]*np.sin(3*x) + 
                    k[7]*np.cos(x/3) + k[8]*np.cos(x) + k[9]*np.cos(3*x) + self.USE_TAN*k[10]*np.tan(x/3) + self.USE_TAN*k[11]*np.tan(x) + self.USE_TAN*k[12]*np.tan(3*x) + 
                    k[13]*np.exp(x/3) + k[14]*np.exp(x) + k[15]*np.exp(3*x) + k[16]*np.exp(-x/3) + k[17]*np.exp(-x) + k[18]*np.exp(-3*x))
        
        # Calculate the sum described in INIT
        result = 0
        for col_index in range(self.num_features):
            result += f(X[:, col_index], col_index=col_index)

        # Classifier Addition
        result = sig(result)

        return result

    def fit(self, X, Y, Ieta=100, Beta=25, Gamma=50, dropout=0.9, init_adj_max=2, verbose=True):
        """
        ## Function
        Adjusts the model's coefficients for N iterations. Returns the fitted model in-place.

        ## Inputs
        - X
            - The input data to make predictions with
        - Y
            - The data to test model outputs too
        - N
            - The number of iterations to run to attempt to improve the model
        - beta
            - Number of adjustments tested to the current best model, per iteration
        - gamma
            - Every gamma # of iterations, the scale of the adjustments made to the model
              coefficients are reduced by 1/2
        - dropout
            - (Approximately) The % of coefficients that are NOT adjusted per beta test. These are picked randomly.
            - Stay in school!
        - init_adj_max
            - The initial maximum amplitude that adjustments can make to an individual model coefficient.
              Having this much larger than the coefficient bounds makes finding improvements slower. Having
              this value be too small will cause not many meaningful adjustments to be made.
        - verbose
            - Whether or not an update of iteration # and current model score is printed (in one line) every
              10 iterations.
        """

        # Check if model initial fit complete
        if not self.fitted:
            # Generate the coefficients for each feature
            if len(X.shape) == 2:
                self.num_features = X.shape[1]
                self.coefs = np.random.rand(self.num_features, self.FUNCTION_LENGTH)
            elif len(X.shape) == 1:
                # Assume a singular feature
                self.num_features = 1
                self.coefs = np.random.rand(self.num_features, self.FUNCTION_LENGTH)
            else:
                raise ValueError(f"X Array Must be 1 or 2 Dimensional! Not {len(X.shape)}-Dimensional")
            
            # Get the number of classes to fit to
            self.num_classes = len(set(Y))

            # Confirm initial fit
            self.parameters = self.coefs.size
            self.fitted = True

        # Tweak params for N iterations
        score = r2d2(self.predict(X), Y)
        for itr in range(Ieta):
            add_mode = itr%2

            # Get dropout filter and apply it (discards changing drapout % num of coefficients)
            filt = np.random.rand(self.num_features, self.FUNCTION_LENGTH) > dropout

            # Get Tweak amplitude adjustment
            adjustments = []
            for _ in range(Beta):
                adjustments.append(filt * init_adj_max*(2**(-(itr) / Gamma)) * 2*(np.random.rand(self.num_features, self.FUNCTION_LENGTH) - 0.5))

            # Apply adjustment to test coeff array
            og_coefs = self.coefs.copy()
            test_scores = []
            for adj in adjustments:
                if add_mode:
                    self.coefs = np.clip(og_coefs+adj, self.coef_bounds[0], self.coef_bounds[1])
                else:
                    self.coefs = np.clip(og_coefs*adj, self.coef_bounds[0], self.coef_bounds[1])
                test_scores.append(self.score(X, Y))

            # Test new coef array score
            best_score = max(test_scores)
            if best_score > score:
                score = best_score

                best_adj = adjustments[test_scores.index(best_score)]

                if add_mode:
                    self.coefs = np.clip(og_coefs+best_adj, self.coef_bounds[0], self.coef_bounds[1])
                else:
                    self.coefs = np.clip(og_coefs*best_adj, self.coef_bounds[0], self.coef_bounds[1])

            else:
                self.coefs = og_coefs

            # Print status
            if verbose and (itr+1)%10 == 0:
                print(f"Iteration #{itr+1} | Score = {format(score, '.6f')}        ", end='\r')
        
        if verbose:
            print(f"Iteration #{itr+1} | Score = {format(score, '.6f')}        ")

    def score(self, X, Y, **kwargs):
        """
        Return the models R2 score to the given X and Y Data
        """
        return r2d2(self.predict(X), Y)

    def CopyNet(self):
        """
        Copy a model object to a new variable. Used in similar
        situations as NumPy's copy method to make an isolated net
        with the same values and properties as the parent net.
        """
        # Check that it is fitted
        if self.fitted == False:
            raise ValueError("Model is not yet fitted and therefore cannot be copied")

        return copy.deepcopy(self)

# ReNN (Recursive NN)
## Recursive nature doesn't help much, but its training algorithm
## is what enabled the new incredible accuracy of the current Neural Network
class ReNN:
    def __init__(self, input_size:int, output_size:int, units_counter=5, units_thinker=100, 
                 counter_af=mc.sig, thinker_in_af=mc.relu, thinker_rep_af=mc.lin, max_iter=500, 
                 learning_rate_init=0.1, learning_rate_mode=['constant', 'dynamic', 'blocks'],
                 gamma=0.01, n_iter_no_change=10, verbose=1):
        # Data size
        self.in_size = input_size
        self.out_size = output_size

        # Weights/Biases for counter NN
        self.W_cin = np.random.rand(self.in_size, units_counter) - 0.5
        self.W_cout = np.random.rand(units_counter, self.out_size) - 0.5
        self.B_c = np.random.rand(units_counter) - 0.5

        # Weights/Biases for thinker NN
        self.W_tin = np.random.rand(self.in_size, units_thinker) - 0.5
        self.W_trep = np.random.rand(units_thinker, units_thinker) - 0.5
        self.W_tout = np.random.rand(units_thinker, self.out_size) - 0.5
        self.B_t = np.random.rand(units_thinker) - 0.5

        # Activation functions
        self.cAF1 = counter_af
        self.tAF1 = thinker_in_af
        self.tAF2 = thinker_rep_af

        # Misc params
        self.max_iter = max_iter
        self.learning_rate = learning_rate_init
        self.learning_mode = 'dynamic' if type(learning_rate_mode) == list else learning_rate_mode
        self.gamma = gamma
        self.n_iter_lim = n_iter_no_change
        self.verbose = verbose

        # Sneaky settings
        self.max_reps = 10
        self.min_reps = 0

    def _calculate_counter(self, xi):
        if self.W_cin.size == 0:
            return 0

        # Matrix calculation for counter
        out = self.cAF1(np.dot(xi, self.W_cin)) + self.B_c
        out = np.dot(out, self.W_cout)[0]

        try:
            while True:
                out = out[0]
        except:
            return out
    
    def _calculate_thinker(self, xi:np.ndarray, repeats:int):
        # Initial calculation
        out = self.tAF1(np.dot(xi, self.W_tin)) + self.B_t

        # If repeats requested in middle layer, do them
        for _ in range(repeats):
            out = self.tAF2(np.dot(out, self.W_trep)) + self.B_t

        # Final matrix calculation
        return np.dot(out, self.W_tout).tolist()

    def predict(self, X, report_counts=False):
        # Recording counter
        if report_counts:
            counts = []

        # Calculation per data point
        if self.W_cin.size > 0:
            out = []
            for xi in X:
                # Get counter's num of repeats
                num_reps = round(np.clip(self._calculate_counter(xi), self.min_reps, self.max_reps))

                if report_counts:
                    counts.append(num_reps)

                # Get thinker's calculations
                out += list(self._calculate_thinker(xi, num_reps))
        
        else:
            # Initial calculation
            out = self.tAF1(np.dot(X, self.W_tin)) + self.B_t

            # Final matrix calculation
            out = np.dot(out, self.W_tout)

        # Reshape out array
        out = np.array(out)
        if self.out_size > 1:
            out = out.reshape((len(X), self.out_size))
        else:
            out = out.flatten()
        if report_counts:
            return counts
        return out
    
    def _get_error(self, X, Y):
        return -np.mean(np.abs(self.predict(X) - Y))
    
    def _get_weights_biases(self):
        weights = [
            self.W_cin.copy(),
            self.W_cout.copy(),
            self.W_tin.copy(),
            self.W_trep.copy(),
            self.W_tout.copy(),
            self.B_c.copy(),
            self.B_t.copy(),
        ]
        return weights
    
    def _set_weights_biases(self, new_weights:'list[np.ndarray]'):
        self.W_cin  = new_weights[0].copy()
        self.W_cout = new_weights[1].copy()
        self.W_tin  = new_weights[2].copy()
        self.W_trep = new_weights[3].copy()
        self.W_tout = new_weights[4].copy()
        self.B_c = new_weights[5].copy()
        self.B_t = new_weights[6].copy()
    
    def _test_new_random(self, X:np.ndarray, Y:np.ndarray, current_error, amplitude):
        # Weight set to modify and test
        og_weights = self._get_weights_biases()
        weights = self._get_weights_biases()
        error = current_error

        # Modify a weight, test score, keep if better
        for i in range(len(weights)):
            # Modify the weight
            weights[i] += 2*amplitude*(np.random.random(weights[i].shape) - 0.5)

            # Apply to model and test
            self._set_weights_biases(weights)
            test_e = self._get_error(X, Y)

            # Behavior if worse
            if test_e < current_error:
                weights[i] = og_weights[i].copy()
                self._set_weights_biases(weights)

            # Behvaior if better
            else:
                error = test_e

        return error
    
    def _get_learning_rate(self, i, last_i_improved, current_rate):
        if self.learning_mode == 'dynamic':
            return self.learning_rate * 2**(-i * self.gamma)
        elif self.learning_mode == 'blocks':
            if i-last_i_improved >= self.n_iter_lim:
                return current_rate / 2
            else:
                return current_rate
        else:
            return current_rate
    
    def fit(self, X, Y):
        # Get currents stuff
        history = []
        current_error = self._get_error(X, Y)
        last_i_improved = 0
        learning_rate = self.learning_rate

        # Iterations for improvement
        for i in range(self.max_iter):
            # Update learning rate
            learning_rate = self._get_learning_rate(i, last_i_improved=last_i_improved, current_rate=learning_rate)
            if i-last_i_improved >= self.n_iter_lim:
                last_i_improved = i

            # Test improvement
            error = self._test_new_random(X, Y, current_error, amplitude=learning_rate)
            if error > current_error:
                current_error = error
                last_i_improved = i

            history.append(current_error)

            # Printout
            if self.verbose == 2:
                print(f"Round: {i+1}/{self.max_iter} | Error: {abs(current_error):.6f} | Learning Rate: {learning_rate:.2e}")
            if self.verbose == 1:
                print(f"Round: {i+1}/{self.max_iter} | Error: {abs(current_error):.6f} | Learning Rate: {learning_rate:.2e}      ", end='\r')
        
        # Final printout
        if self.verbose == 1:
            print(f"Round: {i+1}/{self.max_iter} | Error: {abs(current_error):.6f} | Learning Rate: {learning_rate:.2e}  ")

        return history

# Linear Regressor ALternate
## Works much better with non-normalized data
class LinearRegression:
    def __init__(self):
        """
        Monte Carlo Linear Regressor
        """

        self.weights = None
        self.constant = None
        self.fitted = False

    def predict(self, x):
        # Get predictions
        if self.fitted:
            return x@self.weights + self.constant
        else:
            raise ValueError("Model is not yet fitted!")

    def score(self, x, y):
        if self.fitted:
            return mc.r2d2(self.predict(x), y)
        else:
            raise ValueError("Model is not yet fitted!")
    
    def fit(self, x, y, Ieta=2, Beta=300, Gamma=1000, verbose=True, **kwargs):
        # Initial fit
        if not self.fitted:
            # X (input) size
            if len(x.shape) > 1:
                in_size = x.shape[1]
            else:
                in_size = 1

            # Y (output) size
            if len(y.shape) > 1:
                out_size = y.shape[1]
            else:
                out_size = 1

            # Initial weights
            self.weights = np.random.rand(in_size, out_size) - 0.5
            self.constant = np.random.rand() - 0.5
                
            # self.weights = np.ones((in_size, out_size))
            # self.constant = 0

        # Printout
        sym_done = "="
        sym_todo = "-"
        str_len  = 40

        # Improve
        Gamma = 0.67*Ieta if not Gamma else Gamma
        for it in range(Ieta):
            # Progress bar
            # print(f"Score = {round(self.score(x, y), 6)} | <{sym_done*int(round(str_len*(it+1)/Ieta))}{sym_todo*(str_len-int(round(str_len*(it+1)/Ieta)))}>             ", end='\r')

            # Tweak amplitude
            # A = 2 ** ((-(it) / Gamma))
            # A = 100 * ((Ieta-it) / Ieta)
            # A = 10 ** (-(it/Ieta) + 1)
            # A = 3 * ((it + 1) / Ieta)
            # A = (1 - np.exp(it - Ieta)) * (1 - (it/Ieta))
            A = 2**(-it / Gamma)

            for b in range(Beta):
                if verbose:
                    print(f"Score = {round(self.score(x, y), 6)} | <{sym_done*int(round(str_len*(it*Beta + b)/(Ieta*Beta)))}{sym_todo*(str_len-int(round(str_len*(it*Beta + b)/(Ieta*Beta))))}>             ", end='\r')

                ## Adjust weights
                # Save initial value/score
                w_initial = self.weights.copy()
                s_initial = self.score(x, y)

                # Adjust value and retest
                adj = np.random.normal(0, A, size=self.weights.shape)

                # Test Multiply mode
                self.weights = w_initial * adj
                s_after_mult = self.score(x, y)

                # Test Add mode
                self.weights = w_initial + adj
                s_after_add = self.score(x, y)

                # Check for improvement
                if s_after_mult > s_initial or s_after_add > s_initial:
                    if s_after_mult > s_after_add:
                        self.weights = w_initial * adj
                        best = s_after_mult
                    else:
                        # In this case, add mode is better, but that was most recent
                        # change and is currently applied so no action required
                        best = s_after_add
                        pass
                else:
                    # All options sucked, reset to last weights
                    self.weights = w_initial.copy()
                    best = s_initial

                ## Adjust constant
                # Save initial value/score
                k_initial = self.constant
                s_initial = best

                # Adjust value and retest
                adj = np.random.normal(0, A)
                self.constant *= adj if adj != 0 else 1
                s_after = self.score(x, y)

                # Check for improvement
                if s_after < s_initial:
                    self.constant = k_initial

        # Final printout
        if verbose:
            print(f"Score = {round(self.score(x, y), 6)} | <{sym_done*str_len}>     ")



# ==================== Functions ==================== #
def dataSelect(X, Y, count:int):
    """
    **** Experimental training data selection method ****

    **** Only useable when X and Y are 1D ****

    Returns shortened x, y data arrays with (count) # of data points/rows

    Automatically thins a database by selecting "important" data points more often than
    "non-important data points". This probability comes from the local 2nd derivative
    magnitude that are around a data point.

    X:
        - Input x array

    Y:
        - Input y array

    count:
        - Number of data points to select from the main X/Y arrays
    """

    # Input error catching
    if np.size(X, 0) < 2:
        raise ValueError("There should be at least 2 data points/rows in the X array!")
    if np.size(X, 0) != np.size(Y, 0):
        raise ValueError(f"The # of entries in X ({np.size(X, 0)}) shpuld match Y ({np.size(Y, 0)})")

    # Make numerical derivative data
    Xlength = np.size(X, 0)
    d2X = []
    
    # Get 2nd Derivative
    for row in range(1, Xlength-1):
        dydx1 = (Y[row] - Y[row-1]) / X[row] - X[row-1]
        dydx2 = (Y[row+1] - Y[row]) / X[row+1] - X[row]
        D2 = (dydx2 - dydx1) / (X[row+1] - X[row-1])
        d2X.append(D2)
    d2X = [d2X[0]] + d2X + [d2X[-1]]

    # Shape into array
    d2X = np.array(d2X).reshape(Xlength)

    # Make relative weights of each data point from 2nd derivative magnitudes
    d2X = np.abs(d2X)
    d2X /= np.sum(d2X)

    # delet this
    # if givepp:
    #     return d2X

    # Randomly select indicies taking into account their weight
    indicies = [*range(Xlength)]
    selection = np.random.choice(indicies, size=count, replace=False, p=d2X)
    selection = np.sort(selection)

    # Get the data for the small arrays
    x = []
    y = []
    for idx in selection:
        x.append(X[idx])
        y.append(Y[idx])

    # Shape the lists into array data
    if len(X.shape) == 2:
        x = np.array(x).reshape(count, np.size(X, 1))
    else:
        x = np.array(x).reshape(count)
    if len(Y.shape) == 2:
        y = np.array(y).reshape(count, np.size(Y, 1))
    else:
        y = np.array(y).reshape(count)

    return x, y