# QOSF_Task-3_ZNE
This is an implementation of Zero Noise Extrapolation as part of Task 3 of the Quantum Open Source Mentorship program. The code repository is divided into two parts. Firstly, `utils.py` contains the actual implementation of the mentioned task, the `DepolarizingNoiseModel` class and functions required for the application. It provides two ways to scale noise levels: through a dummy method to increase gate error rate and through unitary folding, which includes both circuit and gate level folding. Additionally, `apply_folding_method` is used for applying unitary folding (circuit and gate) to any arbitrary Qiskit circuit. Lastly, the class includes five extrapolation methods (linear, quadratic, polynomial, exponential, power), and it even supports execution on a quantum computer.

Secondly, `QOSF_ZNE.ipynb` contains my understanding of the topic, possible extensions of the idea, insights about the implementation, and the application of the implemented method.

1. Description:
    * In this task, I will build a simple ZNE function from scratch:
      1) Build a simple noise model with depolarizing noise
      2) Create different circuits to test your noise models and choose the observable to measure
      3) Apply the unitary folding method.
      4) Apply the extrapolation method to get the zero-noise limit. Different extrapolation methods achieve different results, such as Linear, quadratic, polynomial, power, and exponential.
      5) Compare mitigated and unmitigated results
      6) Bonus: Run your ZNE function in real quantum hardware through the IBM Quantum Service (class enables this, but couldn't run because of long waiting time)


2. Results:

   ![Screenshot from 2024-04-09 00-33-24](https://github.com/Hirmay/QOSF_Task-3_ZNE/assets/56473003/81e6e6bf-8c84-47e3-88cf-0b2679251292)

   ![Screenshot from 2024-04-09 00-33-42](https://github.com/Hirmay/QOSF_Task-3_ZNE/assets/56473003/3abe1518-fa89-42a8-b5bb-e94e45d1ebfa)
   
   ![Screenshot from 2024-05-05 22-31-39](https://github.com/Hirmay/QOSF_Task-3_ZNE/assets/56473003/eea5c985-2b13-4356-8487-0ae7513c1424)


4. References:
   1. [Review of ZNE and improvements](https://arxiv.org/abs/2005.10921)
   
   2. [Mitiq](https://mitiq.readthedocs.io/en/stable/guide/zne-5-theory.html)

   3. [Original ZNE paper](https://arxiv.org/abs/1611.09301) 
   
