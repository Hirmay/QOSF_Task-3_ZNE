# QOSF_Task-3_ZNE
This is the submission repo for the screening **Task 3 (ZNE)** for QOSF mentorship program

1. Description:
    * Zero-noise extrapolation (ZNE) is a noise mitigation technique. It works by intentionally     scaling the noise of a quantum circuit to then extrapolate the zero-noise limit of an observable of interest. In this task, you will build a simple ZNE function from scratch:
      1) Build a simple noise model with depolarizing noise
      2) Create different circuits to test your noise models and choose the observable to measure
      3) Apply the unitary folding method.
      4) Apply the extrapolation method to get the zero-noise limit. Different extrapolation methods achieve different results, such as Linear, polynomial, and exponential.
      5) Compare mitigated and unmitigated results
      6) Bonus: Run your ZNE function in real quantum hardware through the IBM Quantum Service
2. Resources:
    * MITIQ
    * https://arxiv.org/pdf/2402.15879.pdf (5.1.2)
    * https://github.com/RamAIbot/QOSF_errormitigation
