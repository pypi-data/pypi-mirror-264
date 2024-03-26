# NeuralPDE: Modelling Dynamical Systems from Data

This is the repository containing themodels for the __NeuralPDE: Modelling Dynamical Systems from Data__ paper (accepted at KI 2022)

Many physical processes such as weather phenomena or fluid mechanics are governed by partial differential equations (PDEs). Modelling such dynamical systems using Neural Networks is an active research field. However, current methods are still very limited, as they do not exploit the knowledge about the dynamical nature of the system, require extensive prior knowledge about the governing equations or are limited to linear or first-order equations. In this work we make the observation that the Method of Lines used to solve PDEs can be represented using convolutions which makes convolutional neural networks (CNNs) the natural choice to parametrize arbitrary PDE dynamics. We combine this parametrization with differentiable ODE solvers to form the NeuralPDE Model, which explicitly takes into account the fact that the data is governed by differential equations. We show in several experiments on toy and real-world data that our model consistently outperforms state-of-the-art models used to learn dynamical systems. 


## License

The source code is licensed under the [MIT license](LICENSE).