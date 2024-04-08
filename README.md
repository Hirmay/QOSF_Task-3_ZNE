# QOSF_Task-3_ZNE
This is an implementation of Zero Noise Extrapolation as part of the task-3 of the Quantum Open Source Metorship program. The code repository is divided into two parts. Firslty, the `utils.py` is about the actual implementation of the task mentioned containing classes and functions required for application. Secondly, the `QOSF_ZNE.ipynb` contains my understanding about the topic, possible extensions of the idea, some insight about the implementation, and applying the implemented method. 

1. Description:
    * Zero-noise extrapolation (ZNE) is a noise mitigation technique. It works by intentionally     scaling the noise of a quantum circuit to then extrapolate the zero-noise limit of an observable of interest. In this task, you will build a simple ZNE function from scratch:
      1) Build a simple noise model with depolarizing noise
      2) Create different circuits to test your noise models and choose the observable to measure
      3) Apply the unitary folding method.
      4) Apply the extrapolation method to get the zero-noise limit. Different extrapolation methods achieve different results, such as Linear, polynomial, and exponential.
      5) Compare mitigated and unmitigated results
      6) Bonus: Run your ZNE function in real quantum hardware through the IBM Quantum Service
2. Resources:
   1. [Review of ZNE and improvements](https://arxiv.org/abs/2005.10921)
   
   2. [Mitiq](https://mitiq.readthedocs.io/en/stable/guide/zne-5-theory.html)
   
   3. [Original ZNE paper](https://arxiv.org/abs/1611.09301) 
