import numpy as np
from scipy.stats import gaussian_kde
import matplotlib.pyplot as mpl
    
"""Base Shannon Entropy function."""
def ShanEn(Sig, P_i=False, bw=None, Logx=2, Plotx=False):
    """ShanEn  estimates the Shannon entropy of a univariate data sequence with discrete probability distribution.
 
    .. code-block:: python
    
        Shan, Probs = ShanEn(Sig) 
        
    Returns the Shannon entropy  (``Shan``) and the corresponding probabilities (``Probs``)
    estimated from the data sequence (``Sig``) using a PDF estimation (histogram binning)
    method with the following the default parameters: 
    logarithm = base 2, histogram bin width (``bw``) = Scott's Rule
   
    .. code-block:: python
    
        Shan, Probs = ShanEn(Sig, P_i = True) 
        
    Returns the Shannon entropy (``Shan``) calculated from the vector 
    of probability values (``Sig``) with a *default* logarithm base == 2.
    **NOTE: If ``P_i==True``, the values of ``Sig`` must sum to 1.**
    
    .. code-block:: python
    
        Shan, Probs = ShanEn(Sig, bw = 0) 
        
    Returns the Shannon entropy (``Shan``) and the corresponding probabilities (``Probs``)
    estimated from the data sequence (``Sig``). When ``bw==0``, ``Sig`` values 
    are considered discrete, thus probabilites are derived from a probability
    mass function (PMF), and *not* using probability density estimation (histogram method). 
    Default parameters:   logarithm = base 2
    
    .. code-block:: python
    
        Shan, Probs = ShanEn(Sig, keyword = value) 
        
    Returns the Shannon entropy estimate (``Shan``) and the corresponding 
    probabilities (``Probs``) estimated from the data sequence (``Sig``) using
    the following specified keyword arguments:

        :P_i:   - If True, assumes ``Sig`` is vector of probability values that sum to 1  (default: False)
                    *Note: if ``P_i == True``, any value assigned to ``bw`` is ignored.*
        :bw:    - bin width, one of the following:
                    - None          uses Scott's rule to get histogram bin width (default)
                    - int/float     a positive value, specifies histogram bin width for PDF estimation.
                    - 0             assumes ``Sig`` is sequence of discrete random values.
        :Logx:  - Logarithm base, a positive scalar  (default: 2. For natural logarithm enter 0)
        :Plotx: - When ``Plotx == True``, returns plot of histogram with probability density (default: False)  
    
    :See also:
        ``DiffEn``, ``RenyEn``, ``TsalEn``, ``HartEn``, ``MinEn``
    
    :References:
        [1]  Claude E. Shannon, 
             "A Mathematical Theory of Communication"
             Bell System Technical Journal (1948)
             27 (3): 379–423 
             
        [2]  Claude E. Shannon,
             "A Mathematical Theory of Communication"
             Bell System Technical Journal (1948)
             27 (4): 623–656. 
             
    """
    
    Sig = np.squeeze(Sig)
    N = Sig.shape[0]     
    assert isinstance(P_i,bool), "P_i:  a Bool. If True, Sig is vector of probabilities that must sum to 1"
    if not P_i:
        assert N>10 and Sig.ndim == 1, "Sig:   must be a numpy vector (N>10)"  
    else:
        assert N>1  and Sig.ndim == 1 and np.round(Sig.sum(),8)==1, "Sig:   When P_i==True, Sig (N>1) is vector of probabilites that sum to 1"  
    assert (bw is None) or (isinstance(bw,(int,float)) and bw>=0), "bw:  a scalar value >= 0, or None (implements Scott's rule)"
    assert isinstance(Logx,(int,float)) and Logx>=0, "Logx:     must be a positive value"
    assert isinstance(Plotx,bool), "Plotx:  must be a Bool - True or False"
    if Logx == 0:  Logx = np.e
    if (Plotx==True or bw is not None) and P_i==True:
        print("\n**Note**: When P_i==True, Plotx and bw parameters are ignored!\n")

    if not P_i: Probs = GenEn(Sig, Methodx='D', bw=bw, Plotx=Plotx)       
    else: Probs = Sig
    
    Probs = Probs[Probs!=0]
    with np.errstate(divide='ignore', invalid='ignore'):    
        Shan = -np.sum(Probs*np.log(Probs)/np.log(Logx))
        return Shan, Probs


"""Base Differential Entropy function."""
def DiffEn(Sig, bw=None, Logx=2, Plotx=False):
    """DiffEn  estimates the differential entropy of a univariate data sequence with continuous probability distribution.
 
    .. code-block:: python
    
        Diff, Probs = DiffEn(Sig) 
        
    Returns the differential entropy (``Diff``) and the corresponding probabilities (``Probs``)
    estimated from the data sequence (``Sig``) using a continuous PDF estimation 
    method (Gaussian kernel density estimation - KDE) with the following the default parameters: 
    logarithm = base 2, KDE bandwidth (``bw``) = Silverman's Rule
    **Note: Probability values are obtained via numerical integration of the 
    kernel density estimated PDF between ``min(Sig)`` - ``max(Sig)`` in N intervals, 
    where N is the length of ``Sig``.**
           
    .. code-block:: python
    
        Diff, Probs = DiffEn(Sig, keyword = value) 
        
    Returns the differential entropy (``Diff``) and the corresponding 
    probabilities (``Probs``) estimated from the data sequence (``Sig``) using
    the following specified keyword arguments:

        :bw:    - kernel bandwidth, one of the following:
                    - None          uses Silverman's rule to get kernel bandwidth for Gaussian KDE method (default)
                    - int/float     a positive value > 0, specifies bandwidth for estimating Gaussian KDE.
        :Logx:  - Logarithm base, a positive scalar  (default: 2. For natural logarithm enter 0)
        :Plotx: - When ``Plotx == True``, returns plot of the PDF (default: False)  
    
    :See also:
        ``ShanEn``, ``RenyEn``, ``TsalEn``, ``HartEn``, ``MinEn``
    
    :References:
        [1] Thomas Cover, Thomas, Joy A. 
            "Elements of Information Theory"
            Wiley (1991)
        
        [2]  Claude E. Shannon, 
             "A Mathematical Theory of Communication"
             Bell System Technical Journal (1948)
             27 (3): 379–423 
             
        [3]  Claude E. Shannon,
             "A Mathematical Theory of Communication"
             Bell System Technical Journal (1948)
             27 (4): 623–656.              
    """    
 
    Sig = np.squeeze(Sig)
    N = Sig.shape[0]     
    if Logx == 0:  Logx = np.e
    assert N>10 and Sig.ndim == 1, "Sig:   must be a numpy vector (N>10)"  
    assert (bw is None) or (isinstance(bw,(int,float)) and bw>0), "bw:  a scalar value > 0"
    assert isinstance(Logx,(int,float)) and Logx>0, "Logx:     must be a positive value"
    assert isinstance(Plotx,bool), "Plotx:  must be a Bool - True or False"
    
    Probs = GenEn(Sig, Methodx='C', bw=bw, Plotx=Plotx)
    Probs = Probs[Probs!=0]
    with np.errstate(divide='ignore', invalid='ignore'):    
        Shan = -np.sum(Probs*np.log(Probs)/np.log(Logx))
        return Shan, Probs


"""Base Renyi (Q) Entropy function."""
def RenyEn(Sig, q=2, P_i=False, Methodx='C', bw=None, Logx=np.e, Plotx=False):
    """RenyEn  estimates the Renyi entropy (also known as Q-entropy, or Collision entropy when q =2) of a univariate data sequence.
 
    .. code-block:: python
    
        Renyi, Probs = RenyEn(Sig) 
        
    Returns the Renyi entropy (collision entropy) (``Renyi``) and the corresponding probabilities
    (``Probs``) estimated from the data sequence (``Sig``) using a continuous PDF 
    estimation  method (Gaussian kernel density estimation - KDE)
    with the following the default parameters: 
    q = 2, logarithm = natural, KDE bandwidth (``bw``) = Silverman's Rule
    **Note: Probability values are obtained via numerical integration of the 
    kernel density estimated PDF between ``min(Sig)`` - ``max(Sig)`` in N intervals, 
    where N is the length of ``Sig``. See EntropyHub Guide for more info.**
    
    .. code-block:: python
    
        Renyi, Probs = RenyEn(Sig, Methodx='D') 
              
    Returns the Renyi entropy (collision entropy) estimate (``Renyi``) and the 
    corresponding probabilities (``Probs``) estimated from the data sequence (``Sig``)
    using a *discrete* PDF estimation (histogram binning) method with the following the default parameters: 
    q = 2, logarithm = natural, histogram bin width (``bw``) = Scott's Rule
    
    .. code-block:: python
    
        Renyi, Probs = RenyEn(Sig, P_i = True) 
                  
    Returns the Renyi entropy (collision entropy) estimate (``Renyi``) calculated 
    from the vector of probability values (``Sig``) with the following default parameters:
    q = 2, logarithm base = natural.
    **NOTE: If ``P_i==True``, the values of ``Sig`` must sum to 1.**
    
    .. code-block:: python
        
        Renyi, Probs = RenyEn(Sig, keyword = value) 
    
    Returns the Renyi entropy estimate (``Renyi``) and the corresponding 
    probabilities (``Probs``) estimated from the data sequence (``Sig``) using
    the following specified keyword arguments:

        :q:     - the ``q`` parameter in Renyi entropy equation, must be > 1 (default = 2)
        :P_i:   - If True, assumes ``Sig`` is vector of probability values that sum to 1  (default: False)
                    When ``P_i==True``, ``Methodx`` and ``bw`` parameters are ignored.
        :Methodx:   - Method to obtain probabilities, one of the following: (default = 'C')
                        - 'D'   performs discrete PDF estimation using histogram binning
                        - 'C'   performs continuous PDF estimation using Gaussian kernel density estimation (KDE)
        :bw:    - histogram bin width / kernel bandwidth, one of the following:
                    - None          uses Silverman's rule to get kernel bandwidth when Methodx=='C' (default)
                                    uses Scott's rule to get histogram bin width when Methodx=='D'
                    - int/float     specifies kernel bandwidth, when Methodx=='C'
                                    specifies histogram bin width when Methodx=='D'
                    - 0             when Methodx='D', assumes ``Sig`` is discrete random variable 
        :Logx:  - Logarithm base, a positive scalar  (default: natural logarithm)
        :Plotx: - When ``Plotx == True``, returns plot of the PDF (default: False)  
    
    :See also:
        ``ShanEn``, ``DiffEn``, ``TsalEn``, ``HartEn``, ``MinEn``
    
    :References:
        [1]  Rényi, Alfréd 
             "On measures of information and entropy"
             Proceedings of the 4th Berkeley Symposium on Mathematics, Statistics and Probability (1960)
             pp. 547–561.

        [2] Thomas Cover, Thomas, Joy A. 
            "Elements of Information Theory"
            Wiley (1991)
                             
    """
        
    Sig = np.squeeze(Sig)
    N = Sig.shape[0]     
    if Logx == 0:  Logx = np.e
    assert isinstance(P_i,bool), "P_i:  a Bool. If True, Sig is vector of probabilities that must sum to 1"
    if not P_i:
        assert N>10 and Sig.ndim == 1, "Sig:   must be a numpy vector (N>10)"  
    else:
        assert N>1  and Sig.ndim == 1 and np.round(Sig.sum(),8)==1, "Sig:   When P_i==True, Sig (N>1) is vector of probabilites that sum to 1"      
    assert (bw is None) or (isinstance(bw,(int,float)) and bw>=0), "bw:  a scalar value > 0"
    assert isinstance(P_i,bool), "P_i:  a Bool. If True, Sig is vector of probabilities that must sum to 1"
    assert isinstance(Logx,(int,float)) and Logx>0, "Logx:     must be a positive value"
    assert isinstance(Plotx,bool), "Plotx:  must be a Bool - True or False"
    assert isinstance(q,int) and q>1, "q:  an integer > 1"
    assert Methodx.lower() in ['d', 'c'], """Methodx must be either:
        'D' - discrete probability estimation (histogram method + normalisation)
        'C' - continuous probability estimation (gaussian kernel density + integration)"""
        
    if P_i is False: Probs = GenEn(Sig, Methodx=Methodx, bw=bw, Plotx=Plotx)
    else: Probs = Sig
    
    Probs = Probs[Probs!=0]
    with np.errstate(divide='ignore', invalid='ignore'):
        Renyi = -(np.log(np.sum(Probs**q))/np.log(Logx))/(1-q)
        return Renyi, Probs

    
"""Base Tsallis Entropy function."""
def TsalEn(Sig, q=2, P_i=False, Methodx='C', bw=None, Logx=np.e, Plotx=False):
    """TsalEn  estimates the Tsallis entropy of a univariate data sequence.
 
    .. code-block:: python
    
        Tsallis, Probs = TsalEn(Sig) 
        
    Returns the Tsallis entropy (``Tsallis``) and the corresponding probabilities
    (``Probs``) estimated from the data sequence (``Sig``) using a continuous 
    PDF approximation method (Gaussian kernel density estimation - KDE)
    with the following the default parameters: 
    q = 2, logarithm = natural, KDE bandwidth (``bw``) = Silverman's Rule
    **Note: Probability values are obtained via numerical integration of the 
    kernel density estimated PDF between ``min(Sig)`` - ``max(Sig)`` in N intervals, 
    where N is the length of ``Sig``. See EntropyHub Guide for more info.**
    
    .. code-block:: python
    
        Tsallis, Probs = TsalEn(Sig, Methodx='D') 
              
    Returns the Tsallis entropy (``Tsallis``) and the corresponding probabilities 
    (``Probs``) estimated from the data sequence (``Sig``) using a discrete PDF 
    approximation (histogram binning) method with the following the default parameters: 
    q = 2, logarithm = natural, histogram bin width (``bw``) = Scott's Rule
    
    .. code-block:: python
    
        Tsallis, Probs = TsalEn(Sig, P_i = True) 
                  
    Returns the Tsallis entropy estimate (``Tsallis``) calculated 
    from the vector of probability values (``Sig``) with the following default parameters:
    q = 2, logarithm base = natural.
    **NOTE: If ``P_i==True``, the values of ``Sig`` must sum to 1.**
    
    .. code-block:: python
        
        Tsallis, Probs = TsalEn(Sig, keyword = value) 
    
    Returns the Tsallis entropy estimate (``Tsallis``) and the corresponding 
    probabilities (``Probs``) estimated from the data sequence (``Sig``) using
    the following specified keyword arguments:

        :q:     - the ``q`` parameter in Tsallis entropy equation, must be > 1 (default = 2)
        :P_i:   - If True, assumes ``Sig`` is vector of probability values that sum to 1  (default: False)
        :Methodx:   - Method to obtain probabilities, one of the following: (default = 'C')
                        - 'D'   performs discrete PDF estimation using histogram binning
                        - 'C'   performs continuous PDF estimation using Gaussian kernel density estimation (KDE) and numerical integration
        :bw:    - histogram bin width / kernel bandwidth, one of the following:
                    - None          uses Silverman's rule to get kernel bandwidth when Methodx=='C' (default)
                                    uses Scott's rule to get histogram bin width when Methodx=='D'
                    - int/float     specifies kernel bandwidth, when Methodx=='C'
                                    specifies histogram bin width when Methodx=='D'
                    - 0             when Methodx='D', assumes ``Sig`` is discrete random variable 
        :Logx:  - Logarithm base, a positive scalar  (default: natural logarithm)
        :Plotx: - When ``Plotx == True``, returns plot of the PDF (default: False)  
    
    :See also:
        ``RenyEn``, ``ShanEn``, ``DiffEn``, ``HartEn``, ``MinEn``
    
    :References:
        [1] Constantino Tsallis, 
            "Possible generalization of Boltzmann-Gibbs statistics"
            Journal of Statistical Physics
            52 (1988); 1–2: 479–487.
                             
    """    
    
    Sig = np.squeeze(Sig)
    N = Sig.shape[0]     
    if Logx == 0:  Logx = np.e
    assert isinstance(P_i,bool), "P_i:  a Bool. If True, Sig is vector of probabilities that must sum to 1"
    if not P_i:
        assert N>10 and Sig.ndim == 1, "Sig:   must be a numpy vector (N>10)"  
    else:
        assert N>1  and Sig.ndim == 1 and Sig.sum()==1, "Sig:   When P_i==True, Sig (N>1) is vector of probabilites that sum to 1"  
    assert (bw is None) or (isinstance(bw,(int,float)) and bw>=0), "bw:  a scalar value > 0"
    assert isinstance(Logx,(int,float)) and Logx>0, "Logx:     must be a positive value"
    assert isinstance(Plotx,bool), "Plotx:  must be a Bool - True or False"
    assert isinstance(q,int) and q>1, "q:  an integer > 1"
    assert Methodx.lower() in ['d', 'c'], """Methodx must be either:
        'D' - discrete probability estimation (histogram method)
        'C' - continuous probability estimation (gaussian kernel density + integration)"""
    
    if P_i is False: Probs = GenEn(Sig, Methodx=Methodx, bw=bw, Plotx=Plotx)
    else: Probs = Sig
    
    Probs = Probs[Probs!=0]
    with np.errstate(divide='ignore', invalid='ignore'):    
        Tsallis = (1 - np.sum(Probs**q))/(q-1) 
        return Tsallis, Probs


"""Base Min-entropy function"""
def MinEn(Sig, P_i=False, bw=None, Logx=np.e, Plotx=False):
    """MinEn estimates the minimum entropy of a univariate data sequence.
    
    .. code-block:: python
    
        MinE, Probs = MinEn(Sig) 
        
    Returns the min-entropy (``MinE``) and  the corresponding probabilities 
    (``Probs``) estimated from the data sequence (``Sig``) using a discrete
    PDF approximation (histogram binning) method with the following the default parameters: 
    logarithm = natural, histogram bin width (``bw``) = Scott's Rule
        
    .. code-block:: python
    
        MinE, Probs = MinEn(Sig, P_i = True) 
                  
    Returns the Min-entropy (``MinE``) calculated from the vector of probability
    values (``Sig``) with the following default parameters: logarithm base = natural.
    **NOTE: If ``P_i==True``, the values of ``Sig`` must sum to 1.**
    
    .. code-block:: python
        
        MinE, Probs = MinEn(Sig, keyword = value) 
    
    Returns the Min-entropy (``MinE``) and the corresponding 
    probabilities (``Probs``) estimated from the data sequence (``Sig``) using
    the following specified keyword arguments:
    
        :P_i:   - If True, assumes ``Sig`` is vector of probability values that sum to 1  (default: False)
        :bw:    - bin width, one of the following:
                    - None          uses Scott's rule to get histogram bin width (default)
                    - int/float     a positive value, specifies histogram bin width for PDF estimation.
                    - 0             assumes ``Sig`` is sequence of discrete random values.
        :Logx:  - Logarithm base, a positive scalar  (default: natural logarithm)
        :Plotx: - When ``Plotx == True``, returns plot of the PDF (default: False)  
    
    :See also:
        ``RenyEn``, ``ShanEn``, ``DiffEn``, ``HartEn``, ``TsalEn``
    
    :References:
        [1]  Robert Konig, Renato Renner and Christian Schaffner,
            "The operational meaning of min-and max-entropy." 
            IEEE Transactions on Information theory 
            55.9 (2009): 4337-4347.
                             
    """        
    
    Sig = np.squeeze(Sig)
    N = Sig.shape[0]     
    if Logx == 0:  Logx = np.e
    assert isinstance(P_i,bool), "P_i:  a Bool. If True, Sig is vector of probabilities that must sum to 1"
    if not P_i:
        assert N>10 and Sig.ndim == 1, "Sig:   must be a numpy vector (N>10)"  
    else:
        assert N>1  and Sig.ndim == 1 and Sig.sum()==1, "Sig:   When P_i==True, Sig (N>1) is vector of probabilites that sum to 1"  
    assert (bw is None) or (isinstance(bw,(int,float)) and bw>=0), "bw:  a scalar value > 0"
    assert isinstance(Logx,(int,float)) and Logx>0, "Logx:     must be a positive value"
    assert isinstance(Plotx,bool), "Plotx:  must be a Bool - True or False"
        
    if P_i is False: Probs = GenEn(Sig, Methodx='D', bw=bw, Plotx=Plotx)
    else: Probs = Sig
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.log(1/Probs.max())/np.log(Logx), Probs
       
    
"""Base Hartley (Max-) Entropy function"""
def HartEn(Sig, Logx = np.e): 
    """HartEn  estimates the Hartley entropy (or Max-entropy) of a univariate data sequence.
    
    .. code-block:: python
    
        Hart = HartEn(Sig) 
        
    Returns the Hartley entropy (``Hart``) of the data sequence
    (``Sig``) using a natural logarithm (default)
        
    .. code-block:: python
        
        Hart = HartEn(Sig, Logx = value) 
        
    Returns the Hartley entropy (``Hart``) of the data sequence
    (``Sig``) using the ``Logx``keyword argument:
    
        :Logx:  - Logarithm base, a positive scalar  (default: natural logarithm)
    
    :See also:
        ``MinEn``, ``RenyEn``, ``ShanEn``, ``DiffEn``,  ``TsalEn``
    
    :References:
        [1]  Robert Konig, Renato Renner and Christian Schaffner,
            "The operational meaning of min-and max-entropy." 
            IEEE Transactions on Information theory 
            55.9 (2009): 4337-4347.
                             
    """      
       
    Sig = np.squeeze(Sig)
    N = Sig.shape[0]     
    if Logx == 0:  Logx = np.e
    return np.log(N)/np.log(Logx)
    

def GenEn(Sig, Methodx="C", bw=None, Plotx=False):
            
    if Methodx.lower() == 'd':        
        if bw==0:
            by, P_i = np.unique(Sig, return_counts=True)
            bx = np.arange(len(P_i))
        else:
            if bw is None: 
                # Q1 = np.percentile(Sig, 25, interpolation = 'midpoint') 
                # Q2 = np.percentile(Sig, 75, interpolation = 'midpoint') 
                # bw = 2*(Q2-Q1)/np.cbrt(len(Sig)) 
                P_i, bx = np.histogram(Sig,'scott')
            else:
                P_i, bx = np.histogram(Sig,bins=np.arange(min(Sig),max(Sig)+bw,bw))
        
    elif Methodx.lower() == 'c':
        if bw is None:  bw = "silverman"
        elif bw==0: raise Exception("When Methodx=='C', bw must be > 0")
        kernel = gaussian_kde(Sig, bw_method=bw)
        Lx = np.linspace(min(Sig),max(Sig),20)  #len(Sig)+1)
        P_i = np.array([kernel.integrate_box_1d(Lx[k],Lx[k+1]) for k in range(len(Lx)-1)])
    
    P_i = P_i/np.sum(P_i)    
        
    if Plotx==True:
        fig, ax = mpl.subplots()
        c1 = (88/255, 163/255, 177/255)
        c2 = (7/255, 54/255, 66/255)
        
        if Methodx.lower()=='d':   
            if bw==0:
                mpl.bar(bx, P_i, width= 1, color=c1)
                mpl.bar(bx, P_i, width=.9, color=c2)
                ax.set_xticks(bx,by)
                ax.set_title("Normalised Data Histogram", fontsize=15,fontweight='bold')
            else:
                mpl.hist(Sig, bx, density=True, color=c1)
                mpl.hist(Sig, bx, density=True, color=c2, rwidth=.9)
                ax.set_title("Normalised Data Histogram\n(Bin Width = "+str(np.round(np.diff(bx)[0],3))+")", 
                         fontsize=15,fontweight='bold')
                ax.set_xticks(np.round(bx,3))

            ax.set_xlabel("Sequence values",fontsize=12,fontweight='bold',color=c2)
            ax.set_ylabel("Relative Frequency",fontsize=12,fontweight='bold',color=c2)
        else:
            mpl.plot(Lx, kernel.pdf(Lx), color=c1, linewidth=5)
            mpl.fill(np.hstack((Lx[0],Lx,Lx[-1])), np.hstack((0,kernel.pdf(Lx),0)), color=c2)
            ax.set_title("Kernel Density Estimate (PDF) \n(Integration Interval = "
                         + str(np.round(np.diff(Lx)[0],3)) + ")", fontsize=15,fontweight='bold')
            ax.set_xlabel("Sequence values",fontsize=12,fontweight='bold',color=c2)
            ax.set_ylabel("Probability Density",fontsize=12,fontweight='bold',color=c2)   
    
    return P_i



# def Differx(Sig, m, Logx=2):
    
#     N = len(Sig)
    
#     kernel = gaussian_kde(Sig, bw_method='silverman')
#     Lx = np.linspace(min(Sig),max(Sig),N)  #len(Sig)+1)
# #    P_i = np.array([kernel.integrate_box_1d(Lx[k],Lx[k+1]) for k in range(len(Lx)-1)])
#     P_i = np.cumsum(kernel.pdf(Lx))
    

#     x = np.hstack((np.ones(m-1)*P_i[0], P_i, np.ones(m-1)*P_i[-1]))
#     # x[:m] = Sig[0]
#     # x[-m:] = Sig[-1]
    
#     Temp = (x[m:] - x[:-m])*N/(2*m)
    
#     Hmn = np.sum(np.log(Temp)/np.log(Logx))/N
    
#     return Hmn
    
    
    
def ddd(Sig):
    kernel = gaussian_kde(Sig, bw_method='silverman')
    P_i = -np.mean(np.log(kernel.pdf(Sig)))


    

"""
    Copyright 2024 Matthew W. Flood, EntropyHub
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
     http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
    
    For Terms of Use see https://github.com/MattWillFlood/EntropyHub
"""    