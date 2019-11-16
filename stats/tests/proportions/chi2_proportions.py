import sys
import scipy
import numpy as np
from scipy.stats import chi2_contingency


def chi2Proportions(count,nobs):
    """
    A wrapper for the chi2 testing proportions based upon the chi-square test

    Args:
        count (:obj `list` of :obj`int` or a single `int`):  the number of successes in nobs trials. If this is 
        array_like, then the assumption is that this represents the number of successes 
        for each independent sample 


        nobs (:obj `list` of :obj`int` or a single `int`):  The number of trials or observations, with the same length as count. 

    Returns: 
        chi2  (:obj `float`): The test statistic.

        p (:obj `float`): The p-value of the test

        dof (int) : Degrees of freedom

        expected (:obj `list`): list same shape as observed. The expected frequencies, based on the marginal sums of the table


    References: 
    [1] "scipy.stats.chi2_contingency" https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2_contingency.html
    [2] "statsmodels.stats.proportion.proportions_chisquare"  https://www.statsmodels.org/dev/generated/statsmodels.stats.proportion.proportions_chisquare.html
    [3]	(1, 2) “Contingency table”, https://en.wikipedia.org/wiki/Contingency_table
    [4]	(1, 2) “Pearson’s chi-squared test”, https://en.wikipedia.org/wiki/Pearson%27s_chi-squared_test
    [5]	(1, 2) Cressie, N. and Read, T. R. C., “Multinomial Goodness-of-Fit Tests”, J. Royal Stat. Soc. Series B, Vol. 46, No. 3 (1984), pp. 440-464.
    
    Sample use: 
        input: 
        [10,10,20] - number of successes in trial 
        [20,20,20] - number of trials 
        chi2Proportions([10,10,20], [20,20,20])
        
        output: 
        (2.7777777777777777,
        0.24935220877729619,
        2,
        array([[ 12.,  12.,  16.],
            [ 18.,  18.,  24.]]))
    """
    
    obs = np.array([count, nobs])
    print(obs)
    try: 
        return chi2_contingency(obs, correction=False) 

    except Exception as e:
        print("Exception: {}, returning int max array".format(e)) 
        int_max  = sys.maxsize
        return [int_max, int_max,int_max,int_max]
    
              


if __name__ == "__main__":
    print(chi2Proportions([10,10,20], [20,20,20]))
