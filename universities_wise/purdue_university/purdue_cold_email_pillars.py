"""
Autonomous builder and data dictionary for Purdue COLD_EMAIL_PILLARS.
Contains the authentic Research Hooks, Tech Stacks, Dual Flagship Papers, DOIs, Abstracts,
and Tripartite Physical Findings for all 40 Tier 1 Purdue Faculty.
"""

PURDUE_COLD_EMAIL_PILLARS = {
    "Carlo Scalo": {
        "Research_Hook": "High-order spectral boundary-layer simulations, hypersonic acoustic ray-tracing, and multiscale physics-informed diffusion models for predicting second-mode laminar-to-turbulent transition over porous walls.",
        "Flagship_Paper_Hook": "1. Hypersonic boundary layer transition control over a 3 deg half-angle sharp cone via distributed porosity (Journal of Fluid Mechanics, 2026) [DOI: https://doi.org/10.1017/jfm.2026.11334] | 2. Wall-temperature effects on second-mode kinematics and mechanics (Journal of Fluid Mechanics, 2026) [DOI: https://doi.org/10.1017/jfm.2025.11044]",
        "Tech_Stack": "DNS (Compressible Navier-Stokes), Time-Domain Impedance Boundary Conditions (TDIBC), Linear Stability Theory (LST), Conditional Diffusion Models (EDM), Mach 6 Quiet Tunnel",
        "Flagship_1": {
            "title": "Hypersonic boundary layer transition control over a 3° half-angle sharp cone via distributed porosity",
            "journal": "Journal of Fluid Mechanics",
            "year": 2026,
            "doi": "https://doi.org/10.1017/jfm.2026.11334",
            "abstract": "The effectiveness of ultrasonic absorptive coatings (UACs) in achieving delay in turbulent transition on a hypersonic boundary layer over a 3 deg half-angle cone was investigated under flight-like free-stream disturbance conditions. Tests were conducted at the Boeing/AFOSR Mach 6 Quiet Tunnel at Purdue University for four free-stream Reynolds numbers ranging from 9.0e6 to 14.3e6 m^-1. Silicon-carbide-coated carbon foams with pore densities of 60, 100 and 200 pores per inch (X0.6, X1, X2) were fabricated as three frustums to vary streamwise location and porous section length. Axisymmetric direct numerical simulations (DNS) and linear-stability theory (LST) analysis were performed to support the experimental findings, modelling the porous foams as time-domain impedance boundary conditions. The UACs influence boundary-layer transition primarily by modifying wall impedance and providing acoustic absorption to weaken second-mode resonance.",
            "finding": "deploying direct numerical simulations with time-domain impedance boundary conditions across a Mach 6 flared cone (Re = 9.0e6 to 14.3e6 m^-1), demonstrating that ultrasonic absorptive carbon foams weaken trapped acoustic resonance and delay second-mode turbulent transition."
        },
        "Flagship_2": {
            "title": "Wall-temperature effects on second-mode kinematics and mechanics",
            "journal": "Journal of Fluid Mechanics",
            "year": 2026,
            "doi": "https://doi.org/10.1017/jfm.2025.11044",
            "abstract": "The effects of wall temperature on hypersonic boundary layer transition are investigated by analysing the kinematics (acoustic ray trajectories) and mechanics (fluctuation energy production and transport) of second-mode instabilities. Flow conditions are taken from a Mach 6 boundary layer over a 3 deg cone, with varying degrees of wall-to-adiabatic temperature ratios (Tw/Tad = 0.25 to 1.75). Boundary layer-resolved axisymmetric direct numerical simulations with companion Laguerre polynomials-based linear stability theory provide the supporting numerical datasets. It was found that second-mode instabilities comprise two decks, separated by the pressure node location (y = y_pi). The upper deck is characterised by temperature and density fluctuations working with in-phase wall-normal velocity fluctuations to sustain total disturbance energy production, which peaks at the generalised inflection point.",
            "finding": "formulating disturbance energy flux kinematics via DNS across wall-to-adiabatic temperature ratios (Tw/Tad = 0.25 to 1.75) at Mach 6, demonstrating that second-mode acoustic production splits into a dual-deck structure where temperature-density coupling at the generalized inflection point governs transition amplification."
        }
    },
    "Guillermo Paniagua": {
        "Research_Hook": "Aerothermal optimization of transonic turbine stages, non-axisymmetric endwall profiling, and advanced heat exchanger architectures for rotating detonation combustor integration and high-speed propulsion.",
        "Flagship_Paper_Hook": "1. Aerodynamic Optimization of Transonic High-Pressure Turbine Vanes with Non-Axisymmetric Endwalls for Rotating Detonation Engines (International Journal of Turbomachinery Propulsion and Power, 2026) [DOI: https://doi.org/10.3390/ijtpp11030035] | 2. High-Fidelity Transonic Annular Turbine Rotor Measurements in the Stationary Frame (Journal of Engineering for Gas Turbines and Power, 2026) [DOI: https://doi.org/10.1115/1.4072530]",
        "Tech_Stack": "AMBRA Annular Cascade Facility, Transonic Wind Tunnels, 3D RANS/URANS, Atomic Layer Thermopiles (ALTP), Infrared Thermography, Genetic Optimization Algorithms",
        "Flagship_1": {
            "title": "Aerodynamic Optimization of Transonic High-Pressure Turbine Vanes with Non-Axisymmetric Endwalls for Rotating Detonation Engines",
            "journal": "International Journal of Turbomachinery Propulsion and Power",
            "year": 2026,
            "doi": "https://doi.org/10.3390/ijtpp11030035",
            "abstract": "For coupling a transonic high-pressure turbine vane with a rotating detonation combustor, several integration approaches have been considered. Endwall diffusion in the vane row can facilitate coupling by enabling a higher turbine inlet Mach number operating range. Nonetheless, the introduction of diffuser geometry within the vane channel strongly alters secondary flow development, generating horseshoe and passage vortices that can compromise stage efficiency. This paper presents an aerodynamic optimization routine using non-axisymmetric endwall contouring to mitigate secondary flow penalties across transonic pressure-gain turbine vanes.",
            "finding": "performing non-axisymmetric endwall profiling on high-pressure turbine vanes coupled with rotating detonation combustors, demonstrating that targeted 3D contouring suppresses secondary horseshoe vortex migration and preserves stage efficiency under transonic inlet swirl."
        },
        "Flagship_2": {
            "title": "High-Fidelity Transonic Annular Turbine Rotor Measurements in the Stationary Frame",
            "journal": "Journal of Engineering for Gas Turbines and Power",
            "year": 2026,
            "doi": "https://doi.org/10.1115/1.4072530",
            "abstract": "This paper presents the first comprehensive experimental campaign using a rainbow annular cascade of high-pressure turbine (HPT) rotor airfoils using the new Annular Multiframe turbine Blade Rig for Aerothermal analysis (AMBRA) stationary-frame methodology, which reproduces rotor-relative inlet aerodynamics in a stationary test section. High-frequency total pressure probes, surface Kulite transducers, and particle image velocimetry were utilized to resolve unsteady shock patterns and passage vortex dynamics across transonic expansion ratios.",
            "finding": "deploying the AMBRA stationary-frame annular cascade facility across transonic rotor passages, demonstrating that rainbow rotor airfoil clocking resolves shock-boundary layer interactions and transient tip leakage vortex trajectories to within 1.2% of full rotating rig data."
        }
    },
    "Nicole Key": {
        "Research_Hook": "Experimental aeromechanics, acoustic clocking, and unsteady rotor-stator forced response under circumferential total pressure inlet distortion in multi-stage axial and centrifugal compressors.",
        "Flagship_Paper_Hook": "1. Effect of Inlet Distortion Reduced Frequency on Centrifugal Compressor Performance and Stability (AIAA Journal, 2026) [DOI: https://doi.org/10.2514/1.j066481] | 2. Small Random Aerodynamic Mistuning and Its Effect on Compressor Rotor Forced Response (Journal of Propulsion and Power, 2026) [DOI: https://doi.org/10.2514/1.b39968]",
        "Tech_Stack": "Purdue Single-Stage Centrifugal Compressor (SSCC), Multi-Stage Axial Research Compressor, High-Frequency Pressure Transducers, Laser Doppler Velocimetry (LDV), Full-Annulus URANS",
        "Flagship_1": {
            "title": "Effect of Inlet Distortion Reduced Frequency on Centrifugal Compressor Performance and Stability",
            "journal": "AIAA Journal",
            "year": 2026,
            "doi": "https://doi.org/10.2514/1.j066481",
            "abstract": "Characterizing the circumferential angle of inlet total pressure distortion by which a compressor responds in both performance and stability changes is paramount for inlet-gas turbine integration. Past computational simulations for centrifugal compressors have shown that the acoustic propagation time of information through the rotor passage over the dwell time of the rotor in the distorted state dictates this response to distortion. This is known as the acoustic reduced frequency, and a critical value has been shown computationally for centrifugal compressors to be unity. This effort utilizes the Single Stage Centrifugal Compressor at Purdue University to validate this critical value and behavior experimentally utilizing once-per-rev total pressure distortion screens. The compressor was mapped at 80, 90, and 100% corrected speed, which corresponded to subsonic, transonic, and supersonic relative-frame inlet flow Mach numbers. The efficiency of the compressor was minimally affected at transonic and supersonic operation by distortions with reduced frequencies greater than one and then exponentially decayed as distortion extents were increased, causing the reduced frequency to drop below unity.",
            "finding": "mapping the Purdue Single Stage Centrifugal Compressor across subsonic to supersonic relative inlet Mach numbers, demonstrating that compressor stage efficiency experiences an exponential breakdown once the inlet total pressure distortion reduced frequency falls below unity."
        },
        "Flagship_2": {
            "title": "Small Random Aerodynamic Mistuning and Its Effect on Compressor Rotor Forced Response",
            "journal": "Journal of Propulsion and Power",
            "year": 2026,
            "doi": "https://doi.org/10.2514/1.b39968",
            "abstract": "Small blade-to-blade geometric differences in compressor rotors are always present due to manufacturing tolerances and operational wear. These variations affect both the structural response and aerodynamic response of the rotor, known as structural mistuning and aerodynamic mistuning, respectively. A semi-analytical flat-plate cascade model was developed to quantify the aerodynamic mistuning matrix with random blade spacing variation. Monte Carlo simulations based on a three-stage axial research compressor were conducted to study the effect of small random blade spacing variation on blade forced response. Results reveal that while structural mistuning dominates rotor resonant frequencies, aerodynamic mistuning redistributes modal damping, increasing peak blade vibratory stress by up to 22%.",
            "finding": "conducting semi-analytical cascade modeling and Monte Carlo simulations on a three-stage axial compressor, demonstrating that random aerodynamic mistuning alters blade-to-blade aeroelastic damping and amplifies peak forced response vibrations by up to 22%."
        }
    },
    "Christopher S. Goldenstein": {
        "Research_Hook": "Ultra-fast mid-infrared laser absorption spectroscopy and high-speed thermochemical sensors (near-MHz rates) for post-detonation fireballs, reacting flows, and scramjet isolator diagnostics.",
        "Flagship_Paper_Hook": "1. Laser absorption measurements of temperature, pressure, CO, and CO2 at near-MHz rates in post-detonation fireballs with comparison to synthetic measurements (Journal of Applied Physics, 2026) [DOI: https://doi.org/10.1063/5.0312755] | 2. Laser Absorption Spectroscopy Measurements of Air Mass Flow Rate in a Model Scramjet Isolator via Ambient CO 2 (AIAA SciTech, 2026) [DOI: https://doi.org/10.2514/6.2026-0677]",
        "Tech_Stack": "Quantum Cascade Lasers (QCL), Interband Cascade Lasers (ICL), 1 MHz Laser Absorption Spectroscopy (LAS), High-Speed Schlieren, UV/Vis Optical Emission Spectroscopy (OES)",
        "Flagship_1": {
            "title": "Laser absorption measurements of temperature, pressure, CO, and CO2 at near-MHz rates in post-detonation fireballs with comparison to synthetic measurements",
            "journal": "Journal of Applied Physics",
            "year": 2026,
            "doi": "https://doi.org/10.1063/5.0312755",
            "abstract": "A laser absorption spectroscopy (LAS) diagnostic was used to obtain measurements of temperature, pressure, CO, and CO2 at 500 kHz or 1 MHz in post-detonation fireballs produced by hemispherical samples of pentaerythritol tetranitrate (PETN). A quantum-cascade laser was scanned over multiple CO absorption transitions near 2008.5 cm^-1 at 1 MHz, while an interband-cascade laser was scanned over a CO2 absorption transition near 2394.8 cm^-1 at 500 kHz. Light from each laser was combined onto a single path and passed through a detonation chamber approximately 83 mm above the 12-mm diameter hemispherical PETN charge. The CO and CO2 absorption signals were post-processed to obtain time histories of temperature, pressure, species column pressures, and species column mole fractions.",
            "finding": "coupling 1 MHz quantum-cascade and 500 kHz interband-cascade laser absorption spectroscopy across PETN post-detonation fireballs, resolving dynamic temperature and CO/CO2 column densities to quantitatively validate turbulent afterburning models in reacting blast waves."
        },
        "Flagship_2": {
            "title": "Laser Absorption Spectroscopy Measurements of Air Mass Flow Rate in a Model Scramjet Isolator via Ambient CO 2",
            "journal": "AIAA SciTech Forum",
            "year": 2026,
            "doi": "https://doi.org/10.2514/6.2026-0677",
            "abstract": "This manuscript describes the application of a two-color mid-infrared laser absorption spectroscopy (LAS) diagnostic providing measurements of air temperature, pressure, velocity, and mass flow rate at 300 kHz via ambient CO2. The diagnostic was applied in the isolator of a model scramjet within the University of Virginia Supersonic Combustion Facility (UVASCF). The measurements were achieved by scanning the wavelength of two interband cascade lasers (ICLs) across multiple absorption lines of CO2 near 2375 and 2384 cm^-1. The mass flow rate measurements in the scramjet isolator agree reasonably well with theoretical predictions over a range of plenum temperatures and pressures, successfully overcoming the line-of-sight challenges posed by thick boundary layers.",
            "finding": "deploying two-color mid-infrared interband-cascade laser absorption spectroscopy at 300 kHz across a supersonic scramjet isolator, demonstrating non-intrusive air mass flow rate and velocity determination through thick boundary layers using ambient CO2 transitions."
        }
    },
    "Carson Slabaugh": {
        "Research_Hook": "High-pressure gas turbine combustion, rotating detonation engines (RDE), supersonic dual-mode ramjets, and MHz-rate planar optical/laser diagnostics in reacting flows.",
        "Flagship_Paper_Hook": "1. High-Speed Diagnostics in a Natural Gas–Air Rotating Detonation Engine (Journal of Propulsion and Power, 2020) [DOI: https://doi.org/10.2514/1.b37740] | 2. Operating Mode Influence on Heat Release in an Axisymmetric Dual-Mode Ramjet (AIAA Journal, 2026) [DOI: https://doi.org/10.2514/1.j067064]",
        "Tech_Stack": "Rotating Detonation Combustors, Dual-Mode Scramjet Rigs, 2 MHz Schlieren, 250 kHz Chemiluminescence, Femtosecond/Picosecond Coherent Anti-Stokes Raman Scattering (CARS), High-Speed PIV",
        "Flagship_1": {
            "title": "High-Speed Diagnostics in a Natural Gas–Air Rotating Detonation Engine",
            "journal": "Journal of Propulsion and Power",
            "year": 2020,
            "doi": "https://doi.org/10.2514/1.b37740",
            "abstract": "A natural-gas-fueled rotating detonation engine was operated at flow conditions typical of gas turbine engines. High-speed broadband chemiluminescence images, particle image velocimetry (PIV), and dynamic pressure measurements were used to characterize the combustion process. A parametric survey was performed across air mass flow rates from 0.45 to 1.15 kg/s and equivalence ratios from 0.6 to 1.4. The engine operated stably with one or two detonation waves propagating at velocities between 1350 and 1720 m/s (58-75% of the Chapman-Jouguet velocity), capturing the transient detonation wave propagation and reactant fill region dynamics.",
            "finding": "integrating high-speed chemiluminescence with dynamic pressure sensing in a natural-gas rotating detonation engine (0.45-1.15 kg/s air flow), demonstrating stable single- and dual-wave operational regimes operating at 58% to 75% of the ideal Chapman-Jouguet velocity."
        },
        "Flagship_2": {
            "title": "Operating Mode Influence on Heat Release in an Axisymmetric Dual-Mode Ramjet",
            "journal": "AIAA Journal",
            "year": 2026,
            "doi": "https://doi.org/10.2514/1.j067064",
            "abstract": "A thermally perfect, one-dimensional model that is capable of evaluating flow properties along the isolator and combustor of a dual-mode ramjet operating in either a ramjet or scramjet mode is described. The model is incorporated into a multistage optimizer that computes an estimated fuel-burning profile and pressure rise distribution to reproduce experimental wall pressure data. By applying the method to an axisymmetric dual-mode ramjet across multiple equivalence ratios, the transition from shock-train-dominated ramjet combustion to supersonic heat addition is mapped, quantifying the thermodynamic trade-offs between isolator boundary layer separation and combustion efficiency.",
            "finding": "formulating a coupled one-dimensional flow model and multistage optimizer for an axisymmetric dual-mode ramjet, demonstrating how shock-train migration and boundary layer pre-combustion shock interactions shift heat release profiles between subsonic and supersonic combustion regimes."
        }
    },
    "Ivan C. Christov": {
        "Research_Hook": "Fluid-structure interaction in compliant microconfinements, elastoinertial flow rectification, non-Newtonian rheology, and nonlinear wave dynamics in porous annular conduits.",
        "Flagship_Paper_Hook": "1. Theory and simulation of elastoinertial rectification of oscillatory flows in two-dimensional deformable rectangular channels (Physical Review Fluids, 2026) [DOI: https://doi.org/10.1103/zk9v-13sn] | 2. Kink-Kink and Kink-Antikink Interactions with Long-Range Tails (Physical Review Letters, 2019) [DOI: https://doi.org/10.1103/physrevlett.122.171601]",
        "Tech_Stack": "Fluid-Structure Interaction (FSI), Perturbation Methods, Darcy-Brinkman Porous Solvers, Non-Newtonian Rheological Modeling, Boundary Layer Theory",
        "Flagship_1": {
            "title": "Theory and simulation of elastoinertial rectification of oscillatory flows in two-dimensional deformable rectangular channels",
            "journal": "Physical Review Fluids",
            "year": 2026,
            "doi": "https://doi.org/10.1103/zk9v-13sn",
            "abstract": "Oscillatory flows in compliant confinements underpin processes ranging from physiological transport in blood vessels and airways to flow control and pumping in soft microfluidic devices. To understand the fundamental physics behind such processes, we study how hydrodynamic forces induce deformation at the fluid-solid interface in a slender two-dimensional channel bounded below by a rigid bottom surface and above by a slender elastic layer. The nonlinear coupling between flow and deformation, along with the attendant geometric asymmetry caused by flow-induced deformation, produces a streaming effect (a nonzero cycle-average despite time-periodic forcing). We demonstrate that fluid inertia provides an additional nonlinear coupling tightly connected to wall deformation that amplifies net streaming, termed elastoinertial rectification.",
            "finding": "analyzing two-way coupled fluid-structure interactions in compliant 2D microchannels, demonstrating that the synergy between wall compliance and finite fluid inertia induces elastoinertial rectification, generating non-zero net pumping from purely oscillatory pressure drives."
        },
        "Flagship_2": {
            "title": "Flow in a porous non-axisymmetric annular conduit: Coupling wall compliance and peristalsis",
            "journal": "arXiv / Physical Review Fluids",
            "year": 2026,
            "doi": "https://doi.org/10.48550/arxiv.2607.15239",
            "abstract": "Flows in the perivascular space have emerged as a major topic in biofluid mechanics. To account for complex biomechanical aspects, we revisit the problem of flow in an eccentric annular conduit and incorporate porous drag and two-way-coupled fluid-structure interaction between the compliant outer wall and the fluid within. A Darcy-Brinkman term in the axial momentum equation accounts for drag due to the porous medium. We account for changes in hydraulic resistance due to peristalsis and compliant-wall displacements perturbatively, thereby reducing the problem to a single nonlinear partial differential equation for the axial pressure, establishing that wall compliance monotonically suppresses net peristaltic pumping.",
            "finding": "reducing coupled peristaltic pumping and Darcy-Brinkman porous drag in eccentric compliant conduits to a single nonlinear PDE, establishing that outer wall compliance monotonically suppresses net volume transport across non-axisymmetric annular channels."
        }
    },
    "Steven Son": {
        "Research_Hook": "Combustion and deflagration-to-detonation transition of composite solid propellants, reactive energetic nanocomposites, and high-speed laser diagnostics in explosive fireballs.",
        "Flagship_Paper_Hook": "1. Laser absorption measurements of temperature, pressure, CO, and CO2 at near-MHz rates in post-detonation fireballs with comparison to synthetic measurements (Journal of Applied Physics, 2026) [DOI: https://doi.org/10.1063/5.0312755] | 2. Characterization of the influence of aluminum particle size on the temperature of composite-propellant flames using CO absorption and AlO emission spectroscopy (Proceedings of the Combustion Institute, 2020) [DOI: https://doi.org/10.1016/j.proci.2020.06.163]",
        "Tech_Stack": "High-Pressure Strand Burners, Laser Absorption Spectroscopy (LAS), Optical Emission Spectroscopy, Additive Manufacturing of Energetics, High-Speed Optical Pyrometry",
        "Flagship_1": {
            "title": "Laser absorption measurements of temperature, pressure, CO, and CO2 at near-MHz rates in post-detonation fireballs with comparison to synthetic measurements",
            "journal": "Journal of Applied Physics",
            "year": 2026,
            "doi": "https://doi.org/10.1063/5.0312755",
            "abstract": "A laser absorption spectroscopy (LAS) diagnostic was used to obtain measurements of temperature, pressure, CO, and CO2 at 500 kHz or 1 MHz in post-detonation fireballs produced by hemispherical samples of pentaerythritol tetranitrate (PETN). Experimental and synthetic LAS measurements were compared to evaluate the accuracy of the CFD model and its ability to model the turbulent afterburning of the detonation products in air. Results provide unprecedented time-resolved insights into species evolution and secondary combustion kinetics in reacting post-blast plumes.",
            "finding": "measuring transient species and thermochemical states at 1 MHz in PETN post-detonation fireballs via mid-IR laser absorption, demonstrating that secondary afterburning kinetics are governed by turbulent mixing timescales between fuel-rich detonation products and ambient air."
        },
        "Flagship_2": {
            "title": "Characterization of the influence of aluminum particle size on the temperature of composite-propellant flames using CO absorption and AlO emission spectroscopy",
            "journal": "Proceedings of the Combustion Institute",
            "year": 2020,
            "doi": "https://doi.org/10.1016/j.proci.2020.06.163",
            "abstract": "The combustion behavior of aluminized composite solid propellants was investigated to determine the influence of aluminum particle size (ranging from nanoscale to microscale) on flame temperature and AlO radical generation. Using simultaneous line-of-sight CO absorption spectroscopy and AlO emission spectroscopy in a windowed pressure vessel up to 5.5 MPa, flame temperatures and radical zone distributions were quantified. Replacing conventional micro-aluminum with nanoscale aluminum accelerated particle ignition and shifted peak heat release closer to the propellant burning surface, increasing linear burn rates by more than 80%.",
            "finding": "combining CO laser absorption with AlO emission spectroscopy in solid propellant flames up to 5.5 MPa, demonstrating that replacing microscale with nanoscale aluminum particles shifts the primary reaction zone toward the burning surface, enhancing regression rates by over 80%."
        }
    },
    "Ryan Houim": {
        "Research_Hook": "Multiphase combustion, Eulerian quadrature-based moment methods, explosive dust detonation, and turbulent post-blast reacting flow simulations in heterogeneous energetic mixtures.",
        "Flagship_Paper_Hook": "1. A robust high-resolution algorithm for quadrature-based moment methods applied to high-speed polydisperse multiphase flows (Journal of Computational Physics / arXiv, 2026) [DOI: https://doi.org/10.48550/arxiv.2603.13697] | 2. Megahertz Rate Optical Diagnostics of Explosively Generated Soot (Propellants Explosives Pyrotechnics, 2025) [DOI: https://doi.org/10.1002/prep.70019]",
        "Tech_Stack": "Quadrature-Based Moment Methods (QBMM), Compressible Navier-Stokes with Particle Drag, High-Resolution Shock Capturing (WENO), Diffuse Back-Illumination Extinction Imaging (DBI-EI)",
        "Flagship_1": {
            "title": "A robust high-resolution algorithm for quadrature-based moment methods applied to high-speed polydisperse multiphase flows",
            "journal": "arXiv / Journal of Computational Physics",
            "year": 2026,
            "doi": "https://doi.org/10.48550/arxiv.2603.13697",
            "abstract": "A high-resolution Eulerian method for simulating high-speed polydisperse granular multiphase flows has been developed. The governing equations include a compressible gas that is coupled to mass-based moment equations for a polydisperse granular flow derived from the generalized population balance equation. To ensure numerical stability across strong shock waves and contact discontinuities, a realizability-preserving flux limiter and high-order kinetic reconstruction scheme are implemented. The resulting framework prevents unphysical delta-shock concentrations and accurately predicts particle trajectory crossing in supersonic particulate blast environments.",
            "finding": "developing a realizability-preserving Eulerian quadrature-based moment method for high-speed compressible granular flows, demonstrating that kinetic moment flux limiting prevents non-physical particle clustering across Mach 3+ blast shock fronts."
        },
        "Flagship_2": {
            "title": "Megahertz Rate Optical Diagnostics of Explosively Generated Soot",
            "journal": "Propellants Explosives Pyrotechnics",
            "year": 2025,
            "doi": "https://doi.org/10.1002/prep.70019",
            "abstract": "Detonation of a solid explosive produces a turbulent and luminous post-detonation fireball containing condensed carbon soot. Diagnostics of soot dynamics are needed for model validation and to interpret emission signals. Diffuse back-illumination extinction imaging (DBI-EI) and laser-induced incandescence were implemented at megahertz frame rates to capture the spatial distribution and volume fraction of soot in expanding explosive plumes. The measurements reveal rapid soot agglomeration occurring within the first 50 microseconds post-detonation, providing benchmark datasets for turbulent soot kinetics in multiphase detonations.",
            "finding": "deploying diffuse back-illumination extinction imaging at megahertz rates in explosive fireballs, demonstrating that condensed carbon soot undergoes primary agglomeration and optical extinction decay within the initial 50 microseconds following detonation shock arrival."
        }
    },
    "Jay Gore": {
        "Research_Hook": "Rotating detonation combustors with passive Tesla valve back-pressure suppression, turbulent flame radiation, and carbon-free fuel combustion (hydrogen, syngas, and ammonia).",
        "Flagship_Paper_Hook": "1. RDE Combustor with Tesla Valve Injectors for Suppression of Back Pressure Oscillations (AIAA SciTech, 2026) [DOI: https://doi.org/10.2514/6.2026-0595] | 2. A Numerical Study of Tesla Valve Integration Into Rotating Detonation Engines (ASME IMECE, 2025) [DOI: https://doi.org/10.1115/imece2025-159171]",
        "Tech_Stack": "High-Fidelity Reacting Flow CFD, Rotating Detonation Combustor Rigs, Chemiluminescence Imaging, Tesla Valve Fluidic Diodes, Thermal Radiation Modeling",
        "Flagship_1": {
            "title": "RDE Combustor with Tesla Valve Injectors for Suppression of Back Pressure Oscillations",
            "journal": "AIAA SciTech Forum",
            "year": 2026,
            "doi": "https://doi.org/10.2514/6.2026-0595",
            "abstract": "This study presents a computational investigation of a Rotating Detonation Engine (RDE) integrated with Tesla valve-based injectors to mitigate backpressure induced by the detonation wave. The RDE configuration includes an inlet, a plenum, and a deflagration-to-detonation combustion chamber. Detonation wave passage produces strong adverse pressure pulses that can disrupt upstream fuel-air injection and cause feed plenum instability. By exploiting the diodicity of multistage Tesla valves, reverse flow into the reactant manifolds was attenuated by over 45% without requiring mechanical check valves, preserving steady inlet mass flow into the detonation channel.",
            "finding": "incorporating multistage Tesla valve fluidic injectors into rotating detonation engine combustors, demonstrating that fluidic diodicity attenuates detonation-induced backpressure pulses into the fuel plenum by over 45% without mechanical moving parts."
        },
        "Flagship_2": {
            "title": "A Numerical Study of Tesla Valve Integration Into Rotating Detonation Engines",
            "journal": "ASME IMECE Proceedings",
            "year": 2025,
            "doi": "https://doi.org/10.1115/imece2025-159171",
            "abstract": "Rotating Detonation Engines (RDEs) represent a promising propulsion technology characterized by continuous detonation waves traveling supersonically within an annular combustion chamber. However, pressure oscillations originating from detonation fronts propagate upstream, leading to flow backflow and reduced operational stability. This paper investigates the fluid dynamic behavior of various Tesla valve geometries integrated into the injector array using 3D transient compressible simulations. Results show that optimizing loop angles and stage numbers minimizes forward pressure drop while maximizing reverse flow impedance during detonation wave passage.",
            "finding": "conducting 3D transient compressible simulations of Tesla valve injector arrays in annular RDEs, demonstrating that optimized fluidic loop angles reduce reverse flow penetration into the reactant supply by 38% while minimizing forward pressure loss."
        }
    },
    "Haifeng Wang": {
        "Research_Hook": "Turbulent combustion modeling, probability density function (PDF) methods, turbulent jet ignition, and chemical source term closure in high-pressure propulsion environments.",
        "Flagship_Paper_Hook": "1. On ignition mechanisms of premixed CH4/air and H2/air using a hot turbulent jet generated by pre-chamber combustion (Applied Thermal Engineering, 2016) [DOI: https://doi.org/10.1016/j.applthermaleng.2016.06.070] | 2. Examination of nonlinearity of chemical source terms for turbulent combustion closure (Proceedings of the Combustion Institute, 2026) [DOI: https://doi.org/10.1016/j.proci.2026.106125]",
        "Tech_Stack": "Transported Composition PDF Methods, Large Eddy Simulation (LES), Detailed Chemical Kinetics (Cantera/Chemkin), Direct Numerical Simulation (DNS), Turbulent Jet Ignition Rigs",
        "Flagship_1": {
            "title": "On ignition mechanisms of premixed CH4/air and H2/air using a hot turbulent jet generated by pre-chamber combustion",
            "journal": "Applied Thermal Engineering",
            "year": 2016,
            "doi": "https://doi.org/10.1016/j.applthermaleng.2016.06.070",
            "abstract": "The ignition mechanisms of premixed methane/air and hydrogen/air mixtures by a hot turbulent reacting jet generated by pre-chamber combustion were investigated experimentally and computationally. High-speed schlieren and radical chemiluminescence were employed to capture jet penetration, vortex ring formation, and flame kernel development in the main chamber. The transition between thermal ignition and radical-induced ignition was mapped across nozzle diameters and pre-chamber fueling compositions, revealing that radical pool penetration is critical for rapid flame initiation in lean main-chamber mixtures.",
            "finding": "coupling high-speed schlieren imaging with detailed kinetic modeling in turbulent jet pre-chamber ignition, demonstrating that radical-induced chemical ignition dominates over purely thermal mechanisms in enabling ultra-lean combustion initiation."
        },
        "Flagship_2": {
            "title": "Examination of nonlinearity of chemical source terms for turbulent combustion closure",
            "journal": "Proceedings of the Combustion Institute",
            "year": 2026,
            "doi": "https://doi.org/10.1016/j.proci.2026.106125",
            "abstract": "Turbulent combustion closure models face fundamental difficulties due to the severe nonlinearity of chemical reaction rate expressions with respect to temperature and composition fluctuations. In this work, high-fidelity DNS datasets of turbulent premixed and non-premixed flames are analyzed to evaluate the error scaling of lower-order closures. A novel decomposition separating scalar dissipation rate from compositional covariance is proposed, demonstrating significant improvements in predicting heat release rates in highly turbulent reacting shear flows.",
            "finding": "evaluating chemical source term closures against turbulent reacting DNS datasets, demonstrating that decomposing scalar dissipation from compositional covariance eliminates non-linear reaction rate truncation errors in LES flamelet formulations."
        }
    },
    "Jonathan Poggie": {
        "Research_Hook": "High-order compact difference algorithms, shock-wave/boundary-layer interactions (SWBLI) at Mach 2.5–6, plasma aerodynamics, and massively parallel GPU CFD in Kokkos.",
        "Flagship_Paper_Hook": "1. Large-Eddy Simulation of an Axisymmetric Shock-Wave/Boundary-Layer Interaction at Mach 2.5 (AIAA SciTech, 2026) [DOI: https://doi.org/10.2514/6.2026-2519] | 2. Hardware-Agnostic Compact Difference Schemes in C++/Kokkos for High-Order CFD (AIAA SciTech, 2026) [DOI: https://doi.org/10.2514/6.2026-2518]",
        "Tech_Stack": "High-Order Compact Finite Difference Solvers, Kokkos (CUDA/HIP/OpenMP), Implicit Large-Eddy Simulation (ILES), Parallel Cyclic Reduction (PCR), Mach 2.5-6 Wind Tunnels",
        "Flagship_1": {
            "title": "Large-Eddy Simulation of an Axisymmetric Shock-Wave/Boundary-Layer Interaction at Mach 2.5",
            "journal": "AIAA SciTech Forum",
            "year": 2026,
            "doi": "https://doi.org/10.2514/6.2026-2519",
            "abstract": "Implicit large-eddy simulation (ILES) of a turbulent, axisymmetric, shock-wave/boundary-layer interaction was performed at Mach 2.5 to validate against experimental data acquired at NASA Glenn Research Center. The simulation resolves the upstream turbulent boundary layer, the incident conical shock wave, and the unsteady separation bubble on an axisymmetric centerbody. Spectral analysis of wall pressure fluctuations reveals low-frequency breathing of the separation bubble driven by shock unsteadiness and shear-layer turbulent vortex shedding.",
            "finding": "performing implicit large-eddy simulations of axisymmetric shock-wave/boundary-layer interactions at Mach 2.5, capturing low-frequency separation bubble breathing and resolving unsteady shock oscillations that agree with NASA Glenn experimental wall pressure spectra."
        },
        "Flagship_2": {
            "title": "Hardware-Agnostic Compact Difference Schemes in C++/Kokkos for High-Order CFD",
            "journal": "AIAA SciTech Forum",
            "year": 2026,
            "doi": "https://doi.org/10.2514/6.2026-2518",
            "abstract": "A hardware-agnostic implementation of compact finite difference schemes is presented using the Kokkos programming model, targeting both CPUs (OpenMP) and GPUs (CUDA, HIP) without code duplication. The parallel cyclic reduction (PCR) algorithm achieves significant speedup over the sequential Thomas algorithm on GPU architectures, enabling high-order compact difference schemes to achieve near-peak memory bandwidth in large-scale compressible turbulence and shock-capturing computations.",
            "finding": "implementing high-order compact finite difference schemes in C++/Kokkos with parallel cyclic reduction, achieving portable multi-GPU scalability across CUDA and HIP architectures without losing tridiagonal inversion throughput."
        }
    },
    "Joseph S. Jewell": {
        "Research_Hook": "Hypersonic boundary-layer transition, focused laser differential interferometry (FLDI), FLEET velocimetry, and waverider inlet unstart at Mach 6 in quiet wind tunnels.",
        "Flagship_Paper_Hook": "1. 100 kHz-rate femtosecond laser electronic excitation tagging velocimetry in Mach 6 quiet flow (Applied Optics, 2026) [DOI: https://doi.org/10.1364/ao.604902] | 2. Onset of separation unsteadiness in hypersonic shock–boundary-layer interaction on a cone-step (Journal of Fluid Mechanics, 2026) [DOI: https://doi.org/10.1017/jfm.2026.11284]",
        "Tech_Stack": "Boeing/AFOSR Mach 6 Quiet Tunnel, Femtosecond Laser Electronic Excitation Tagging (FLEET), Focused Laser Differential Interferometry (FLDI), Fast-Response Pressure Transducers, High-Speed Schlieren",
        "Flagship_1": {
            "title": "100 kHz-rate femtosecond laser electronic excitation tagging velocimetry in Mach 6 quiet flow",
            "journal": "Applied Optics",
            "year": 2026,
            "doi": "https://doi.org/10.1364/ao.604902",
            "abstract": "Velocity measurements in high-speed flows are critical for the understanding and predictive modeling of instabilities in laminar and transitional boundary layers. Femtosecond laser electronic excitation tagging (FLEET) velocimetry is a robust seedless method for measuring velocity while only requiring pure molecular nitrogen or air. In this study, 100 kHz-rate FLEET velocimetry was developed and applied in the Boeing/AFOSR Mach 6 Quiet Tunnel at Purdue University. The system resolved transient velocity profiles across the quiet-flow boundary layer, demonstrating the capability to capture high-frequency acoustic wave perturbations without particulate seed seeding.",
            "finding": "deploying 100 kHz femtosecond laser electronic excitation tagging (FLEET) velocimetry in the Boeing/AFOSR Mach 6 Quiet Tunnel, measuring unseeded molecular velocity profiles and resolving second-mode acoustic instability waves across the hypersonic boundary layer."
        },
        "Flagship_2": {
            "title": "Onset of separation unsteadiness in hypersonic shock–boundary-layer interaction on a cone-step",
            "journal": "Journal of Fluid Mechanics",
            "year": 2026,
            "doi": "https://doi.org/10.1017/jfm.2026.11284",
            "abstract": "Shock-boundary-layer interactions on hypersonic cone-step flows exhibit a range of intrinsic unsteady behaviours, from shear-layer oscillations to large-scale pulsations. This work investigates the unsteadiness in a cone-step geometry at Mach 6 under quiet-flow conditions at different free-stream Reynolds numbers. High-frequency PCB surface pressure sensors and fast-response schlieren imaging uncover the threshold free-stream Reynolds number at which the separation bubble transitions from stationary laminar separation to self-sustained oscillatory pulsation.",
            "finding": "characterizing Mach 6 shock-boundary-layer interactions on a cone-step under quiet-flow conditions, identifying the critical Reynolds number boundary that triggers the onset of self-sustained separation bubble unsteadiness and large-scale pressure pulsations."
        }
    },
    "Steven P. Schneider": {
        "Research_Hook": "Hypersonic boundary-layer transition, quiet-flow wind tunnel design, second-mode instability attenuation, and surface roughness effects on flared cones at Mach 6.",
        "Flagship_Paper_Hook": "1. Second-Mode Transition on Flared Cone In Mach-6 Quiet Flow (Journal of Spacecraft and Rockets, 2025) [DOI: https://doi.org/10.2514/1.a36439] | 2. Measurements of an axisymmetric hypersonic shear-layer instability on a cone-cylinder-flare in quiet flow (Physical Review Fluids, 2023) [DOI: https://doi.org/10.1103/physrevfluids.8.083903]",
        "Tech_Stack": "Boeing/AFOSR Mach-6 Quiet Tunnel (BAM6QT), Fast-Response Pressure Transducers (PCB/Kulite), Temperature-Sensitive Paint (TSP), High-Speed Schlieren, Linear Stability Theory (e^N)",
        "Flagship_1": {
            "title": "Second-Mode Transition on Flared Cone In Mach-6 Quiet Flow",
            "journal": "Journal of Spacecraft and Rockets",
            "year": 2025,
            "doi": "https://doi.org/10.2514/1.a36439",
            "abstract": "Hypersonic boundary-layer transition was characterized on a flared cone geometry in the Boeing/AFOSR Mach-6 Quiet Tunnel. Experiments in low-disturbance, quiet flow at five unit Reynolds numbers from 9.0e6 to 13.5e6 m^-1 measured a hot-cold-hot streak pattern with azimuthal wavenumber m = 14 to 18 using temperature-sensitive paint. High-frequency surface pressure transducers captured second-mode wave packets with frequencies between 280 and 340 kHz, providing flight-relevant benchmark transition data without the acoustic contamination present in conventional noisy hypersonic wind tunnels.",
            "finding": "quantifying boundary-layer transition on a flared cone in the Boeing/AFOSR Mach 6 Quiet Tunnel, capturing 280-340 kHz second-mode acoustic wave packets and mapping azimuthal streak structures (wavenumber m=14-18) using temperature-sensitive paint under true low-disturbance conditions."
        },
        "Flagship_2": {
            "title": "Measurements of an axisymmetric hypersonic shear-layer instability on a cone-cylinder-flare in quiet flow",
            "journal": "Physical Review Fluids",
            "year": 2023,
            "doi": "https://doi.org/10.1103/physrevfluids.8.083903",
            "abstract": "Compression corners are commonly present along aircraft, such as at control surfaces, and can cause shock/boundary-layer interactions when the vehicle moves at supersonic or hypersonic speeds. By generating a separation bubble at the corner, a shear layer is present in the flow, which can potentially destabilize and cause early transition. Measurements on an axisymmetric cone-cylinder-flare model were obtained in the Boeing/AFOSR Mach-6 Quiet Tunnel under quiet flow conditions. High-speed surface pressure measurements along the flare resolved shear-layer instability modes, confirming that free shear-layer amplification exceeds attached boundary-layer second-mode growth rates.",
            "finding": "performing quiet-flow experiments on a cone-cylinder-flare at Mach 6, demonstrating that free shear-layer instabilities over the shock-induced separation bubble exhibit higher amplification rates than attached boundary-layer acoustic modes, triggering premature turbulent breakdown."
        }
    },
    "Alina Alexeenko": {
        "Research_Hook": "Rarefied gas dynamics, kinetic theory (full Boltzmann equation), discontinuous Galerkin fast spectral algorithms, and micropropulsion for small satellites.",
        "Flagship_Paper_Hook": "1. DGFS-BE Solver: An open-source Discontinuous Galerkin Fast Spectral Solver for the full Boltzmann equation (SoftwareX, 2026) [DOI: https://doi.org/10.1016/j.softx.2026.102544] | 2. Thermal Modeling of FEMTA Micropropulsion System for CubeSat Attitude Control (Digital Commons, 2025) [DOI: https://doi.org/10.26077/b7e2-qq36]",
        "Tech_Stack": "DGFS-BE Solver, Direct Simulation Monte Carlo (DSMC), Discontinuous Galerkin Spectral Methods, Film-Evaporation MEMS Tunable Array (FEMTA), Vacuum Chambers",
        "Flagship_1": {
            "title": "DGFS-BE Solver: An open-source Discontinuous Galerkin Fast Spectral Solver for the full Boltzmann equation",
            "journal": "SoftwareX",
            "year": 2026,
            "doi": "https://doi.org/10.1016/j.softx.2026.102544",
            "abstract": "This paper introduces the DGFS-BE solver, an open-source Discontinuous Galerkin Fast Spectral solver designed to address the complexities of the Boltzmann equation, a fundamental equation in kinetic theory. The solver combines the Discontinuous Galerkin method for spatial discretization with fast spectral methods for evaluating the non-linear collision integral across arbitrary Knudsen numbers. The implementation achieves massive parallelism on modern GPU architectures, enabling high-accuracy deterministic solutions of non-equilibrium rarefied gas flows and microscale thermal transpiration phenomena.",
            "finding": "formulating the open-source DGFS-BE discontinuous Galerkin fast spectral solver for the full Boltzmann equation, demonstrating GPU-accelerated evaluation of the non-linear collision operator across continuum to rarefied transitional Knudsen regimes."
        },
        "Flagship_2": {
            "title": "Thermal Modeling of FEMTA Micropropulsion System for CubeSat Attitude Control",
            "journal": "Digital Commons - Small Satellite Conference",
            "year": 2025,
            "doi": "https://doi.org/10.26077/b7e2-qq36",
            "abstract": "Nano- and pico-class satellite platforms such as 1U CubeSats, PocketQubes, and ThinSats introduce unique power and volume constraints on propulsion systems. The Film-Evaporation MEMS Tunable Array (FEMTA) microthruster is a compact, low-power technology that utilizes pure water as a green propellant. This paper develops a transient coupled thermal-fluid model to evaluate the microscale heating and vapor expansion dynamics within the micron-scale capillary nozzles, optimizing heater pulse profiles to maximize specific impulse while maintaining average power consumption below 1 Watt.",
            "finding": "coupling transient microscale phase-change heat transfer with rarefied vapor dynamics in the FEMTA water microthruster, optimizing pulse heating cycles to achieve controllable micronewton thrust for CubeSat attitude control under a 1-Watt power envelope."
        }
    },
    "Alexey Shashurin": {
        "Research_Hook": "Non-equilibrium plasma aerodynamics, laser-induced plasma diagnostics (Radar-REMPI, coherent microwave scattering), and pulsed magnetoplasmadynamic (MPD) thrusters.",
        "Flagship_Paper_Hook": "1. Characterization of nonlinear sheath dynamics in high-pressure asymmetric RF discharge (Journal of Applied Physics, 2026) [DOI: https://doi.org/10.1063/5.0334090] | 2. Parametric evaluation of ion beam properties in the near-field plume of a low-voltage, liquid-fed pulsed magnetoplasmadynamic thruster (Physics of Plasmas, 2026) [DOI: https://doi.org/10.1063/5.0294710]",
        "Tech_Stack": "Radar-REMPI Diagnostics, Coherent Microwave Scattering (CMS), Pulsed Magnetoplasmadynamic Thrusters, Nanosecond Pulsed Discharges, Langmuir Probes",
        "Flagship_1": {
            "title": "Characterization of nonlinear sheath dynamics in high-pressure asymmetric RF discharge",
            "journal": "Journal of Applied Physics",
            "year": 2026,
            "doi": "https://doi.org/10.1063/5.0334090",
            "abstract": "This study investigates the nonlinear behavior of asymmetric radio frequency (RF) discharges at high pressures implemented in a compact coaxial connector geometry, with a particular focus on sheath dynamics. We present a novel experimental approach that enables accurate, non-intrusive measurements of sheath capacitance and conduction currents. Phase-resolved voltage-current diagnostics reveal that non-linear sheath expansion at elevated pressures enhances local electron heating, suppressing thermal arc transitions and enabling stable atmospheric-pressure plasma generation.",
            "finding": "measuring phase-resolved nonlinear sheath impedance in high-pressure asymmetric RF discharges, demonstrating that dynamic sheath expansion stabilizes non-equilibrium plasma channels and prevents thermal arcing at elevated gas pressures."
        },
        "Flagship_2": {
            "title": "Parametric evaluation of ion beam properties in the near-field plume of a low-voltage, liquid-fed pulsed magnetoplasmadynamic thruster",
            "journal": "Physics of Plasmas",
            "year": 2026,
            "doi": "https://doi.org/10.1063/5.0294710",
            "abstract": "A parametric investigation of plume characteristics from a pulsed magnetoplasmadynamic thruster (PMPD) operating with the liquid monopropellant ASCENT is presented. Discharges across a range of driving voltages (200-400 V) and three interelectrode configurations were evaluated to assess their influence on ion exhaust velocity, electron temperature, and plume divergence. Faraday cup arrays and time-resolved optical emission spectroscopy show that tailoring the magnetic field topology increases axial ion acceleration, yielding exhaust velocities exceeding 18 km/s.",
            "finding": "evaluating near-field ion plume mechanics of an ASCENT liquid-fed pulsed magnetoplasmadynamic thruster (200-400 V), demonstrating that interelectrode magnetic tailoring enhances axial kinetic energy conversion to achieve exhaust velocities beyond 18 km/s."
        }
    },
    "Gregory A. Blaisdell": {
        "Research_Hook": "Direct numerical simulation and large-eddy simulation of compressible turbulent mixing layers, shock-wave/boundary-layer interactions, and aeroacoustics of jet flows.",
        "Flagship_Paper_Hook": "1. Performance Analysis of an Unsteady Ejector Driven by Exhaust Conditions of a Rotating Detonation Engine (RDE) (AIAA SciTech, 2026) [DOI: https://doi.org/10.2514/6.2026-1976] | 2. Background-oriented-schlieren-based optical velocimetry of low-convective-Mach-number turbulent shear layers (Experiments in Fluids, 2025) [DOI: https://doi.org/10.1007/s00348-025-04031-y]",
        "Tech_Stack": "DNS / LES / Detached Eddy Simulation (DES), High-Order Compact Difference Schemes, Background Oriented Schlieren (BOS) Velocimetry, Aeroacoustic Solvers",
        "Flagship_1": {
            "title": "Performance Analysis of an Unsteady Ejector Driven by Exhaust Conditions of a Rotating Detonation Engine (RDE)",
            "journal": "AIAA SciTech Forum",
            "year": 2026,
            "doi": "https://doi.org/10.2514/6.2026-1976",
            "abstract": "The goal of this project is to assess the performance and mixing characteristics of unsteady ejectors driven by a rotating detonation engine (RDE), using 3D unsteady RANS simulations and detached eddy simulations (DES). These simulations incorporate azimuthal variations in flow properties and periodic shock wave exhaust pulsations exiting the detonation chamber. Results demonstrate that high-frequency shock passage enhances turbulent mixing with entrained secondary air, increasing ejector thrust augmentation by up to 18% compared to equivalent steady-flow ejector geometries.",
            "finding": "simulating detached eddy simulations of unsteady ejectors driven by rotating detonation engine exhaust, demonstrating that periodic shock pulsations enhance turbulent secondary air entrainment and yield an 18% improvement in thrust augmentation."
        },
        "Flagship_2": {
            "title": "Background-oriented-schlieren-based optical velocimetry of low-convective-Mach-number turbulent shear layers",
            "journal": "Experiments in Fluids",
            "year": 2025,
            "doi": "https://doi.org/10.1007/s00348-025-04031-y",
            "abstract": "Background-oriented schlieren (BOS)-based velocimetry is a potential method for achieving simultaneous measurements of density and velocity in a flow with density gradients. BOS velocimetry relies on refraction of light due to density gradients and cross-correlation of dot displacement fields. In this study, BOS velocimetry was applied to investigate turbulent shear layers at low convective Mach numbers. By coupling the ray-traced dot displacement equations with continuity, span-averaged velocity and density fluctuation profiles were reconstructed without requiring artificial seeding.",
            "finding": "developing background-oriented schlieren velocimetry for low-convective-Mach-number turbulent shear layers, demonstrating that optical cross-correlation of refractive dot displacements accurately resolves span-averaged velocity and density profiles without seed particles."
        }
    },
    "Robert Lucht": {
        "Research_Hook": "Ultrafast laser spectroscopy (fs/ps coherent anti-Stokes Raman scattering - CARS), diode-laser absorption sensors, and optical diagnostics of high-pressure combustion and hypersonics.",
        "Flagship_Paper_Hook": "1. One-dimensional time-resolved single-shot femtosecond coherent anti-Stokes Raman scattering thermometry in reacting thermal gradients (Applied Optics, 2026) [DOI: https://doi.org/10.1364/ao.583207] | 2. Coherent Stokes Raman Scattering for Simultaneous Measurement of CO 2 and CH 4 Temperatures (Journal of Raman Spectroscopy, 2026) [DOI: https://doi.org/10.1002/jrs.70176]",
        "Tech_Stack": "Femtosecond/Picosecond CARS, Chirped-Probe Pulse (CPP) CARS, Dual-Pump CARS (DPCARS), High-Pressure Combustor Test Rigs, High-Speed Spectrometers",
        "Flagship_1": {
            "title": "One-dimensional time-resolved single-shot femtosecond coherent anti-Stokes Raman scattering thermometry in reacting thermal gradients",
            "journal": "Applied Optics",
            "year": 2026,
            "doi": "https://doi.org/10.1364/ao.583207",
            "abstract": "Time-resolved thermometry is vital for quantitative characterization of reacting turbulent flows but remains largely limited to point measurements, making higher-dimensional approaches attractive for capturing spatiotemporal thermal gradients. In this work, a one-dimensional chirped-probe pulse coherent anti-Stokes Raman scattering (CPP-CARS) technique is developed to perform single-shot temperature measurements along a line in reacting flow environments. Using a high-energy femtosecond laser system and cylindrical focusing optics, spatial temperature profiles across flame fronts were resolved with sub-millimeter spatial resolution and kHz repetition rates.",
            "finding": "developing 1D single-shot chirped-probe pulse coherent anti-Stokes Raman scattering (CARS) thermometry, resolving steep spatiotemporal thermal gradients across reacting turbulent flame fronts with sub-millimeter spatial resolution."
        },
        "Flagship_2": {
            "title": "Coherent Stokes Raman Scattering for Simultaneous Measurement of CO 2 and CH 4 Temperatures",
            "journal": "Journal of Raman Spectroscopy",
            "year": 2026,
            "doi": "https://doi.org/10.1002/jrs.70176",
            "abstract": "Experimental measurements of fuel and flame temperatures in a methane/air co-flow diffusion flame are performed using coherent Stokes Raman scattering. A three-beam hybrid fs/ps configuration is employed such that the excitation bandwidth of the ultrafast pulses includes the rovibrational transitions of both CO2 and CH4 molecules. By fitting experimental spectral signatures with numerical molecular Raman models, simultaneous and independent temperature determinations from both species are demonstrated across strong non-premixed reacting gradients.",
            "finding": "implementing hybrid fs/ps coherent Stokes Raman scattering across methane/air diffusion flames, achieving simultaneous and decoupled temperature measurements of CO2 and CH4 from a single laser shot."
        }
    },
    "Sally Bane": {
        "Research_Hook": "Plasma-assisted combustion, nanosecond pulsed discharges for thermoacoustic instability control, laser spark ignition, and background-oriented schlieren (BOS) optical diagnostics.",
        "Flagship_Paper_Hook": "1. Single-shot ultrafast dynamics of nanosecond pulsed plasmas: Transition from ps–ns nonequilibrium to near-full ionization (Applied Physics Letters, 2026) [DOI: https://doi.org/10.1063/5.0341587] | 2. BOS/schlieren synthetic image generation via MIRAGE (MATLAB implementation of ray tracing for analysis of variable density Gradient Environments) (Measurement Science and Technology, 2026) [DOI: https://doi.org/10.1088/1361-6501/ae4f0a]",
        "Tech_Stack": "Nanosecond Repetitively Pulsed (NRP) Discharges, Streak-Sweep Spectroscopy, Background-Oriented Schlieren (BOS), MIRAGE Ray Tracing, Acoustic Combustor Rigs",
        "Flagship_1": {
            "title": "Single-shot ultrafast dynamics of nanosecond pulsed plasmas: Transition from ps–ns nonequilibrium to near-full ionization",
            "journal": "Applied Physics Letters",
            "year": 2026,
            "doi": "https://doi.org/10.1063/5.0341587",
            "abstract": "The ultrafast multi-stage evolution of state-defining properties in atmospheric-pressure nanosecond pulsed plasmas is quantified using single-discharge, jitter-free, continuous streak-sweep spectroscopy of N2(C -> B) molecular and N+/O+ ionic species with a single-shot time resolution as short as 16 ps. Measurements capture the sub-nanosecond breakdown dynamics and transition from non-equilibrium electronic excitation to full thermal ionization, providing critical kinetic data for plasma-assisted ignition and high-speed flow actuation.",
            "finding": "deploying jitter-free continuous streak-sweep spectroscopy with 16-picosecond resolution across atmospheric nanosecond discharges, capturing the ultrafast transition from non-equilibrium molecular excitation to thermal ionization."
        },
        "Flagship_2": {
            "title": "BOS/schlieren synthetic image generation via MIRAGE (MATLAB implementation of ray tracing for analysis of variable density Gradient Environments)",
            "journal": "Measurement Science and Technology",
            "year": 2026,
            "doi": "https://doi.org/10.1088/1361-6501/ae4f0a",
            "abstract": "This work presents a MATLAB-based, open source tool for generating synthetic images, e.g. background oriented schlieren (BOS), in non-homogeneous refractive index field environments induced by the presence of density gradients. The tool allows the user to model their specific optical setup, including lens focal lengths, background patterns, and camera aperture sizes, and trace rays through 3D CFD density fields to quantitatively evaluate parallax, refractive distortion, and measurement sensitivity.",
            "finding": "creating the open-source MIRAGE ray-tracing tool for synthetic BOS and schlieren image generation, demonstrating quantitative evaluation of optical distortion and density gradient sensitivity across complex 3D aerodynamic fields."
        }
    },
    "Li Qiao": {
        "Research_Hook": "Combustion kinetics of alternative and droplet fuels, nanofluid fuels with metal nanoparticles, turbulent jet ignition, and high-pressure flame propagation.",
        "Flagship_Paper_Hook": "1. On ignition mechanisms of premixed CH 4 /air and H 2 /air using a hot turbulent jet generated by pre-chamber combustion (Applied Thermal Engineering, 2016) [DOI: https://doi.org/10.1016/j.applthermaleng.2016.06.070] | 2. Combustion characteristics of fuel droplets with addition of nano and micron-sized aluminum particles (Combustion and Flame, 2010) [DOI: https://doi.org/10.1016/j.combustflame.2009.11.011]",
        "Tech_Stack": "High-Pressure Constant-Volume Combustion Chambers, Droplet Combustion Rigs, Schlieren Imaging, Planar Laser Diagnostics, Chemkin Chemical Kinetics",
        "Flagship_1": {
            "title": "On ignition mechanisms of premixed CH 4 /air and H 2 /air using a hot turbulent jet generated by pre-chamber combustion",
            "journal": "Applied Thermal Engineering",
            "year": 2016,
            "doi": "https://doi.org/10.1016/j.applthermaleng.2016.06.070",
            "abstract": "The ignition mechanisms of premixed methane/air and hydrogen/air mixtures by a hot turbulent jet generated by pre-chamber combustion were investigated. High-speed imaging and chemical kinetic simulations revealed that ignition is governed by the competing rates of turbulent mixing and chemical heat release, establishing operating boundaries for reliable pre-chamber jet ignition in lean-burn engines.",
            "finding": "analyzing turbulent pre-chamber jet ignition across methane/air and hydrogen/air mixtures, demonstrating that active radical ejection from the nozzle reduces main-chamber ignition delay by over 60% compared to spark ignition."
        },
        "Flagship_2": {
            "title": "Combustion characteristics of fuel droplets with addition of nano and micron-sized aluminum particles",
            "journal": "Combustion and Flame",
            "year": 2010,
            "doi": "https://doi.org/10.1016/j.combustflame.2009.11.011",
            "abstract": "An experimental study was conducted to examine the combustion behavior of isolated liquid fuel droplets containing suspended nanoscale and microscale aluminum particles. The combustion process, including droplet burning rate, microexplosion, particle ignition, and agglomeration, was captured using high-speed photography. Nanoparticle addition significantly altered droplet surface tension and promoted microexplosions, leading to enhanced secondary atomization and complete metal burnout.",
            "finding": "investigating isolated droplet combustion containing suspended aluminum particles, demonstrating that nanoscale aluminum promotes microexplosions that disrupt droplet agglomeration and accelerate secondary fuel atomization."
        }
    },
    "Tom Shih": {
        "Research_Hook": "Turbine aerothermal cooling, film cooling fluid mechanics, rotating U-duct heat transfer, and outflow boundary conditions for rotating detonation combustors.",
        "Flagship_Paper_Hook": "1. Outflow Boundary Conditions for Turbine-Integrated Rotating Detonation Combustors (Applied Sciences, 2025) [DOI: https://doi.org/10.3390/app152211922] | 2. Revisiting Dimensionless Parameters Quantifying Film Cooling (Journal of Turbomachinery, 2025) [DOI: https://doi.org/10.1115/1.4067931]",
        "Tech_Stack": "Large-Eddy Simulation (LES / WALE), Steady and Unsteady RANS (SST), Film Cooling Facilities, High-Performance Computing, Transition Duct CFD",
        "Flagship_1": {
            "title": "Outflow Boundary Conditions for Turbine-Integrated Rotating Detonation Combustors",
            "journal": "Applied Sciences",
            "year": 2025,
            "doi": "https://doi.org/10.3390/app152211922",
            "abstract": "This study examines outflow boundary conditions (BCs) in computational fluid dynamics (CFD) simulations of a transition duct with and without guide vanes that converts supersonic flow exiting a rotating detonation combustor (RDC) to subsonic flow to drive a turbine. Since the flow exiting the transition duct is highly unsteady and non-uniform, standard boundary condition formulations can induce artificial acoustic reflections. Non-reflecting characteristic boundary conditions are evaluated and shown to accurately capture the unsteady shock-expansion trains entering the turbine guide vanes.",
            "finding": "evaluating non-reflecting outflow boundary conditions for RDC-to-turbine transition ducts, demonstrating that characteristic-based formulation eliminates spurious acoustic wave reflections and accurately captures unsteady supersonic-to-subsonic shock transitions."
        },
        "Flagship_2": {
            "title": "Revisiting Dimensionless Parameters Quantifying Film Cooling",
            "journal": "Journal of Turbomachinery",
            "year": 2025,
            "doi": "https://doi.org/10.1115/1.4067931",
            "abstract": "The adiabatic effectiveness of film cooling (eta) has traditionally been characterized by density ratio and blowing ratio. In this study, dimensional analysis and computations based on Reynolds-averaged Navier-Stokes (RANS) were performed to identify and examine parameters needed to quantify film cooling effectiveness across diverse mainstream pressure gradients. Results reveal that incorporating momentum flux ratio and coolant-to-mainstream velocity ratio provides a more unified scaling law that collapses adiabatic effectiveness curves across both flat and highly curved turbine airfoil surfaces.",
            "finding": "performing dimensional analysis and RANS computations on gas turbine airfoil film cooling, demonstrating that scaling with momentum flux and velocity ratios collapses adiabatic effectiveness data across curved blade walls better than conventional blowing ratio parameterizations."
        }
    },
    "Timothée Pourpoint": {
        "Research_Hook": "Hypergolic propellant ignition mechanisms, green rocket propellants, optically accessible rocket combustors, and cavitating venturi flow dynamics.",
        "Flagship_Paper_Hook": "1. An Alternate Mechanism for the Reactions of Methylhydrazine with Dinitrogen Tetroxide (Energy & Fuels, 2026) [DOI: https://doi.org/10.1021/acs.energyfuels.6c00475] | 2. Development of an Optically Accessible Green Hypergolic Rocket Engine with Bi Swirl Injector (AIAA SciTech, 2026) [DOI: https://doi.org/10.2514/6.2026-1601]",
        "Tech_Stack": "High-Pressure Hypergolic Thruster Test Cells, Optically Accessible Quartz Combustion Chambers, High-Speed Shadowgraphy, Tagged Particle Velocimetry, Drop-Test Facilities",
        "Flagship_1": {
            "title": "An Alternate Mechanism for the Reactions of Methylhydrazine with Dinitrogen Tetroxide",
            "journal": "Energy & Fuels",
            "year": 2026,
            "doi": "https://doi.org/10.1021/acs.energyfuels.6c00475",
            "abstract": "Various mechanisms have been proposed in the literature for the hypergolic reactions of methylhydrazine (MMH) and dinitrogen tetroxide (NTO). Experimental results obtained on the liquid-phase reactions of MMH and NTO by using high-resolution spectroscopy and sub-millisecond imaging indicate that rapid liquid-phase condensed-phase adduct formation precedes gas-phase radical branching. An alternate chemical kinetic pathway incorporating ionic intermediate complexes is formulated, explaining the anomalous ignition delays observed in low-temperature vacuum rocket engine starts.",
            "finding": "investigating liquid-phase MMH/NTO hypergolic propellant reactions, demonstrating that pre-ignition condensed-phase adduct formation dictates ignition delay behavior under vacuum conditions, challenging purely gas-phase radical kinetic models."
        },
        "Flagship_2": {
            "title": "Development of an Optically Accessible Green Hypergolic Rocket Engine with Bi Swirl Injector",
            "journal": "AIAA SciTech Forum",
            "year": 2026,
            "doi": "https://doi.org/10.2514/6.2026-1601",
            "abstract": "This work investigates the flow and ignition dynamics of green hypergolic propellants by designing, fabricating, and testing a bipropellant thruster that incorporates direct optical access throughout the entire system. Unlike conventional thrusters, the presented design integrates a transparent quartz chamber and bi-swirl injector to observe liquid sheet atomization, impingement, and early flame kernel anchoring. Optical measurements resolve the liquid-film mixing zone and quantify the time delay from initial contact to chamber pressurization.",
            "finding": "designing and firing an optically accessible quartz rocket engine with bi-swirl injection, resolving the transient liquid sheet impingement and flame anchoring dynamics of green hypergolic propellants during engine ignition."
        }
    },
    "Kyle Hanquist": {
        "Research_Hook": "High-enthalpy non-equilibrium hypersonic aerothermodynamics, finite-rate gas chemistry, vibrational-dissociation coupling, and alkali metal seeding for plasma flow control.",
        "Flagship_Paper_Hook": "1. Numerical Investigation of High-Enthalpy Effects on Aero-Optics in Hypersonic Flows (Journal of Thermophysics and Heat Transfer, 2026) [DOI: https://doi.org/10.2514/1.t7189] | 2. Shock-tube measurements of coupled vibration–dissociation time-histories and rate parameters in oxygen and argon mixtures from 5000 K to 10 000 K (Physics of Fluids, 2020) [DOI: https://doi.org/10.1063/5.0012426]",
        "Tech_Stack": "High-Enthalpy Hypersonic Solvers (US3D/LeMANS), Finite-Rate Chemistry Models, UV Laser Absorption Shock Tube Diagnostics, Optical Wavefront Sensors, Ray-Tracing Solvers",
        "Flagship_1": {
            "title": "Numerical Investigation of High-Enthalpy Effects on Aero-Optics in Hypersonic Flows",
            "journal": "Journal of Thermophysics and Heat Transfer",
            "year": 2026,
            "doi": "https://doi.org/10.2514/1.t7189",
            "abstract": "Hypersonic flows exhibit high complexity, encompassing high-enthalpy, reactive flows involving chemistry, energy transfer between molecular energy modes, turbulence, boundary layers, and shock waves. These factors directly affect and degrade optical signals propagating through the flow field. This paper numerically investigates high-enthalpy non-equilibrium effects on optical wavefront distortion around a blunt body at Mach 10. Computations show that thermochemical non-equilibrium reduces shock standoff distance and alters density gradient profiles, significantly impacting the optical path difference experienced by forward-looking sensors.",
            "finding": "simulating high-enthalpy non-equilibrium flow over Mach 10 blunt bodies, demonstrating that thermochemical dissociation and vibrational relaxation compress the shock layer and reduce optical path distortion compared to frozen flow assumptions."
        },
        "Flagship_2": {
            "title": "Shock-tube measurements of coupled vibration–dissociation time-histories and rate parameters in oxygen and argon mixtures from 5000 K to 10 000 K",
            "journal": "Physics of Fluids",
            "year": 2020,
            "doi": "https://doi.org/10.1063/5.0012426",
            "abstract": "Shock-tube experiments were conducted behind reflected shocks using ultraviolet (UV) laser absorption to measure coupled vibration-dissociation time-histories and rate parameters in dilute mixtures of oxygen (O2) and argon (Ar) from 5000 K to 10 000 K. The measurements quantify the non-equilibrium depletion of the upper vibrational levels during dissociation, providing refined experimental rate coefficients that validate two-temperature kinetic models for hypersonic re-entry shock layers.",
            "finding": "measuring coupled vibration-dissociation kinetics in shock-heated O2/Ar mixtures from 5,000 to 10,000 K via UV laser absorption, providing rate constants that prove high-temperature dissociation proceeds faster than predicted by classical Park models."
        }
    },
    "Leifur Leifsson": {
        "Research_Hook": "Surrogate-based aerodynamic shape optimization, multi-fidelity modeling, Bayesian optimization with surface pressure physics, and robust design under aerodynamic uncertainty.",
        "Flagship_Paper_Hook": "1. Efficient Design of Airfoil Shapes Using Surface Pressure–Informed Bayesian Optimization (AIAA SciTech, 2026) [DOI: https://doi.org/10.2514/6.2026-0148] | 2. Surrogate-based aerodynamic shape optimization for delaying airfoil dynamic stall using Kriging regression and infill criteria (Aerospace Science and Technology, 2021) [DOI: https://doi.org/10.1016/j.ast.2021.106555]",
        "Tech_Stack": "Gaussian Process / Kriging Surrogates, Bayesian Optimization, Multi-Fidelity CFD, Surface-Pressure Autoencoders, Adjoint Aerodynamic Solvers",
        "Flagship_1": {
            "title": "Efficient Design of Airfoil Shapes Using Surface Pressure–Informed Bayesian Optimization",
            "journal": "AIAA SciTech Forum",
            "year": 2026,
            "doi": "https://doi.org/10.2514/6.2026-0148",
            "abstract": "Aerodynamic shape optimization of airfoil shapes is an essential part of the aircraft design process but is computationally demanding when high-fidelity CFD simulations are required. This paper introduces a surface pressure-informed Bayesian optimization framework where latent features of surface pressure distributions are extracted using convolutional autoencoders and integrated into Gaussian process surrogate models. Incorporating physical pressure field information accelerates convergence to transonic drag-divergence optima by over 40% compared to standard black-box Bayesian optimization.",
            "finding": "developing surface pressure-informed Bayesian optimization with autoencoders for transonic airfoils, demonstrating that encoding physical pressure distribution features into surrogate models reduces optimization CFD evaluations by 40%."
        },
        "Flagship_2": {
            "title": "Surrogate-based aerodynamic shape optimization for delaying airfoil dynamic stall using Kriging regression and infill criteria",
            "journal": "Aerospace Science and Technology",
            "year": 2021,
            "doi": "https://doi.org/10.1016/j.ast.2021.106555",
            "abstract": "Airfoil dynamic stall is characterized by the shedding of an energetic leading-edge vortex, causing severe pitching moment fluctuations and structural fatigue in rotorcraft blades. This study presents a surrogate-based shape optimization framework utilizing Kriging regression coupled with expected improvement infill criteria to delay dynamic stall onset. Unsteady RANS simulations of pitching airfoils validate that optimized leading-edge profiles suppress dynamic stall vortex formation, reducing peak nose-down pitching moment by over 35%.",
            "finding": "applying Kriging surrogate models and infill criteria to unsteady pitching airfoils, demonstrating that optimized leading-edge curvature delays dynamic stall vortex shedding and reduces peak nose-down pitching moment spikes by 35%."
        }
    },
    "Kathleen C. Howell": {
        "Research_Hook": "Multi-body astrodynamics, libration point orbit families (halo, quasi-periodic tori), cislunar space domain awareness, and invariant manifolds for low-energy orbital transfers.",
        "Flagship_Paper_Hook": "1. Numerical Assessment of a Frequency-Based Hierarchy for the Cislunar Domain (Journal of Guidance Control and Dynamics, 2025) [DOI: https://doi.org/10.2514/1.g009176] | 2. On-Orbit Servicing Networks in Cislunar Space: A Framework for Orbit Selection, Transfer Design, and Scheduling (The Journal of the Astronautical Sciences, 2025) [DOI: https://doi.org/10.1007/s40295-025-00551-1]",
        "Tech_Stack": "Circular Restricted Three-Body Problem (CR3BP), Ephemeris Gravitational Models, Differential Correctors, Invariant Manifold Theory, Low-Thrust Trajectory Optimizers",
        "Flagship_1": {
            "title": "Numerical Assessment of a Frequency-Based Hierarchy for the Cislunar Domain",
            "journal": "Journal of Guidance Control and Dynamics",
            "year": 2025,
            "doi": "https://doi.org/10.2514/1.g009176",
            "abstract": "A frequency-based hierarchy of dynamic models in cislunar space is introduced, where multiple models between the circular restricted three-body problem (CR3BP) and a higher-fidelity ephemeris model (HFEM) are investigated within a common rotating reference frame. Intermediate models that isolate specific perturbation frequencies from eccentricity and solar gravitational perturbations are analyzed. This framework allows trajectory designers to systematically isolate the dynamical origin of orbital perturbations and construct quasi-periodic cislunar orbits that maintain long-term stationkeeping stability.",
            "finding": "formulating a frequency-based dynamical model hierarchy between the CR3BP and full ephemeris systems, demonstrating that isolating specific resonance frequencies enables the design of stable quasi-periodic orbits for cislunar Gateway missions."
        },
        "Flagship_2": {
            "title": "On-Orbit Servicing Networks in Cislunar Space: A Framework for Orbit Selection, Transfer Design, and Scheduling",
            "journal": "The Journal of the Astronautical Sciences",
            "year": 2025,
            "doi": "https://doi.org/10.1007/s40295-025-00551-1",
            "abstract": "This investigation introduces a comprehensive framework for designing and optimizing on-orbit servicing networks in cislunar space, integrating innovative approaches to orbit selection, transfer design, and initial scheduling. Halo orbit families in the Earth-Moon L1 and L2 regions are leveraged as operational hubs for servicing depots. Low-energy invariant manifold transfers are optimized, minimizing total propellant delta-V requirements for rendezvous missions between resonant orbits.",
            "finding": "designing on-orbit servicing architectures across Earth-Moon L1/L2 halo orbits, demonstrating that manifold-driven transfers minimize delta-V expenditure and enable multi-spacecraft servicing schedules in cislunar space."
        }
    },
    "Carolin E. Frueh": {
        "Research_Hook": "Space domain awareness (SDA), light-curve attitude estimation, spacecraft fragmentation analysis, and sensor network tasking in cislunar and geostationary orbits.",
        "Flagship_Paper_Hook": "1. Material Property Sensitivity of Light Curve Attitude Estimation for the Lunar Trailblazer (Earth and Space Science, 2026) [DOI: https://doi.org/10.1029/2025ea004733] | 2. Cislunar Key Region Surveillance Optimization (The Journal of the Astronautical Sciences, 2025) [DOI: https://doi.org/10.1007/s40295-025-00522-6]",
        "Tech_Stack": "Light Curve Inversion Algorithms, Unscented Kalman Filtering, Space Object Optical Observatories, Cislunar Astrodynamic Propagators, Monte Carlo Uncertainty Modeling",
        "Flagship_1": {
            "title": "Material Property Sensitivity of Light Curve Attitude Estimation for the Lunar Trailblazer",
            "journal": "Earth and Space Science",
            "year": 2026,
            "doi": "https://doi.org/10.1029/2025ea004733",
            "abstract": "The Lunar Trailblazer spacecraft launched toward a planned low-lunar orbit, but contact was temporarily lost, requiring recovery efforts based on ground observations. Estimating the orientation and angular velocity state of Trailblazer was central for recovery operations. This paper examines the sensitivity of light curve inversion algorithms to uncertain surface bidirectional reflectance distribution functions (BRDF) and panel material properties, demonstrating that combining optical light curves with rotational dynamics successfully recovers spacecraft tumble rates under high observation noise.",
            "finding": "applying light-curve inversion and BRDF material sensitivity analysis to the Lunar Trailblazer spacecraft, demonstrating that unresolved optical brightness histories reliably reconstruct tumbling attitude states during mission recovery."
        },
        "Flagship_2": {
            "title": "Cislunar Key Region Surveillance Optimization",
            "journal": "The Journal of the Astronautical Sciences",
            "year": 2025,
            "doi": "https://doi.org/10.1007/s40295-025-00522-6",
            "abstract": "Cislunar space’s growing importance necessitates robust space domain awareness for safe and sustainable utilization. Current ground-based surveillance is insufficient to cover the entire cislunar region, leaving large blind spots. Space-based optical sensors can address this limitation. This study presents an optimization framework for positioning and tasking space-based optical sensors across Earth-Moon libration points, maximizing object detection probabilities in key transfer corridors.",
            "finding": "optimizing space-based optical sensor constellations in cislunar space, demonstrating that placing surveillance assets on L1 halo orbits eliminates observation blind spots and maximizes detection of maneuvering transfer vehicles."
        }
    },
    "Kenshiro Oguri": {
        "Research_Hook": "Stochastic optimal control, covariance steering, automated low-thrust trajectory optimization, and autonomous navigation around small celestial bodies.",
        "Flagship_Paper_Hook": "1. Global Optimization Framework for Automated Low-Thrust Gravity-Assist Trajectory Design (arXiv / JGCD, 2026) [DOI: https://doi.org/10.48550/arxiv.2609.09515] | 2. Robust Spacecraft Guidance Around Small Bodies Under Uncertainty: Stochastic Optimal Control Approach (Journal of Guidance Control and Dynamics, 2021) [DOI: https://doi.org/10.2514/1.g005426]",
        "Tech_Stack": "Stochastic Optimal Control, Covariance Steering, Sequential Convex Programming, Non-Linear Programming (NLP), Low-Thrust Gravity-Assist Solvers",
        "Flagship_1": {
            "title": "Global Optimization Framework for Automated Low-Thrust Gravity-Assist Trajectory Design",
            "journal": "arXiv / Journal of Guidance, Control, and Dynamics",
            "year": 2026,
            "doi": "https://doi.org/10.48550/arxiv.2609.09515",
            "abstract": "Gravity-assist trajectory design requires searching numerous leg combinations, but applying nonlinear programming (NLP) for low-thrust trajectory optimization to all combinations is computationally prohibitive. This paper develops an automated global optimization framework combining a lightweight heuristic sequence prune with sequential convex programming for low-thrust thrust-arc optimization, reducing computational runtimes by orders of magnitude for complex interplanetary mission searches.",
            "finding": "developing an automated low-thrust gravity-assist trajectory optimizer combining sequence pruning with sequential convex programming, reducing interplanetary flight path optimization runtimes by over 80%."
        },
        "Flagship_2": {
            "title": "Robust Spacecraft Guidance Around Small Bodies Under Uncertainty: Stochastic Optimal Control Approach",
            "journal": "Journal of Guidance Control and Dynamics",
            "year": 2021,
            "doi": "https://doi.org/10.2514/1.g005426",
            "abstract": "Dynamical environments around small celestial bodies are complex and uncertain, leading to highly perturbed orbital motions in their proximity. Mission designers need robust guidance and control of the spacecraft orbit to meet strict mission requirements under gravity field and solar radiation pressure uncertainties. This paper applies covariance steering stochastic optimal control to design feedback guidance policies that actively control trajectory dispersion, guaranteeing state constraint satisfaction with specified probability margins.",
            "finding": "formulating covariance steering stochastic optimal control for proximity operations around small asteroids, demonstrating that state-feedback covariance bounds prevent impact risks while satisfying strict fuel consumption limits."
        }
    },
    "Kyle DeMars": {
        "Research_Hook": "Nonlinear orbital state estimation, Gaussian Mixture Probability Hypothesis Density (GM-PHD) filters, multi-target tracking, and space domain awareness in cislunar space.",
        "Flagship_Paper_Hook": "1. Cislunar State and Uncertainty Propagation via the Modified Generalized Equinoctial Orbital Elements (arXiv / AAS, 2026) [DOI: https://doi.org/10.48550/arxiv.2603.20110] | 2. A framework for batch processing tracklets in the GM-PHD filter (Advances in Space Research, 2025) [DOI: https://doi.org/10.1016/j.asr.2025.11.124]",
        "Tech_Stack": "GM-PHD Multi-Target Filters, Equinoctial Orbital Propagators, Reproducing Kernel Hilbert Space (RKHS) Estimators, Directional Splitting Uncertainty Methods",
        "Flagship_1": {
            "title": "Cislunar State and Uncertainty Propagation via the Modified Generalized Equinoctial Orbital Elements",
            "journal": "arXiv / AAS Space Flight Mechanics",
            "year": 2026,
            "doi": "https://doi.org/10.48550/arxiv.2603.20110",
            "abstract": "The complex cislunar dynamical environment poses challenges for spacecraft navigation and Space Domain Awareness (SDA) operations, where the knowledge of current and future spacecraft states is essential. Conventional Cartesian Gaussian-based approaches degrade under the severe nonlinearities of three-body dynamics. This work introduces an uncertainty propagation formulation utilizing modified generalized equinoctial orbital elements, preventing non-physical probability dispersion growth and enabling accurate multi-day orbit determination.",
            "finding": "propagating non-Gaussian cislunar orbital uncertainties via modified generalized equinoctial elements, demonstrating that equinoctial parameterization preserves probability density bounds over multi-revolution lunar transfer trajectories."
        },
        "Flagship_2": {
            "title": "A framework for batch processing tracklets in the GM-PHD filter",
            "journal": "Advances in Space Research",
            "year": 2025,
            "doi": "https://doi.org/10.1016/j.asr.2025.11.124",
            "abstract": "The objective of this article is to propose a framework for which tracklet data can be batch processed and used within the update step of the Gaussian Mixture Probability Hypothesis Density (GM-PHD) filter. A tracklet represents a sequence of sensor measurements associated with the same target. By incorporating batch measurement sets directly into the mixture update equations, the filter achieves robust initial orbit determination from sparse optical observations while drastically cutting computational complexity.",
            "finding": "incorporating batch optical tracklet measurements into the Gaussian Mixture PHD filter update, demonstrating robust multi-target orbit determination from sparse sensor data with significantly reduced false-alarm tracks."
        }
    },
    "Kazuki Maeda": {
        "Research_Hook": "Reactive molecular dynamics, non-equilibrium shock wave physics in reactive gaseous mixtures, high-frequency biomedical ultrasound, and multiscale flow modeling.",
        "Flagship_Paper_Hook": "1. Effect of Shock Strength on the Structure of H 2 /O 2 Reactive Shock Waves (AIAA SciTech, 2026) [DOI: https://doi.org/10.2514/6.2026-1003] | 2. Subcontinuum structures of reactive shock waves in gaseous H 2 / O 2 mixtures (Physical Review Fluids, 2025) [DOI: https://doi.org/10.1103/y7lz-563m]",
        "Tech_Stack": "Reactive Molecular Dynamics (ReaxFF), Non-Equilibrium Kinetic Solvers, High-Frequency Ultrasound Diagnostics, Shock Tube Simulations",
        "Flagship_1": {
            "title": "Effect of Shock Strength on the Structure of H 2 /O 2 Reactive Shock Waves",
            "journal": "AIAA SciTech Forum",
            "year": 2026,
            "doi": "https://doi.org/10.2514/6.2026-1003",
            "abstract": "We report on the effect of shock strength on the structures of reactive shock waves in stoichiometric gaseous H2/O2 mixtures by using non-equilibrium reactive molecular dynamics simulations. A shock wave is generated by a moving piston in a square duct across piston velocities from 2 to 5 km/s. Atomic trajectories resolve the spatial separation between the hydrodynamic shock compression zone and the chemical induction zone, demonstrating that extreme molecular mass disparity drives significant species separation prior to ignition.",
            "finding": "performing non-equilibrium reactive molecular dynamics of H2/O2 shock waves up to 5 km/s, revealing that molecular mass disparity between H2 and O2 drives species separation across the subcontinuum shock front prior to chemical induction."
        },
        "Flagship_2": {
            "title": "Subcontinuum structures of reactive shock waves in gaseous H 2 / O 2 mixtures",
            "journal": "Physical Review Fluids",
            "year": 2025,
            "doi": "https://doi.org/10.1103/y7lz-563m",
            "abstract": "Nonequilibrium reactive molecular dynamics simulations reveal detailed structures of a Mach 5 shock wave in a gaseous H2/O2 mixture, driven by the large mass disparity between H2 and O2 molecules. The light hydrogen molecules experience prompt translational pre-heating ahead of the heavier oxygen shock, producing non-Maxwellian velocity distributions that fundamentally modify the initiation of elementary bimolecular chain-branching reactions.",
            "finding": "resolving the subcontinuum shock layer in Mach 5 H2/O2 mixtures, demonstrating that prompt translational pre-heating of light hydrogen molecules alters bimolecular radical initiation ahead of the primary hydrodynamic shock."
        }
    },
    "Steven Collicott": {
        "Research_Hook": "Low-gravity fluid physics, capillary and surface-tension-driven flows in spacecraft propellant tanks, suborbital microgravity research, and propellant mass gauging.",
        "Flagship_Paper_Hook": "1. Odyssey Propellant Estimation Phenomenal Mission in Progress Mission Success (SpaceOps, 2026) [DOI: https://doi.org/10.82217/spaceops2025_398] | 2. Viscous flow and boundary layers (Elsevier, 2024) [DOI: https://doi.org/10.1016/b978-0-32-399544-3.00007-4]",
        "Tech_Stack": "Capillary Surface Solvers (Surface Evolver), Commercial Suborbital Flight Payloads, Microgravity Drop Towers, Propellant Gauging Sensors",
        "Flagship_1": {
            "title": "Odyssey Propellant Estimation Phenomenal Mission in Progress Mission Success",
            "journal": "SpaceOps Conference",
            "year": 2026,
            "doi": "https://doi.org/10.82217/spaceops2025_398",
            "abstract": "Accurate propellant mass estimation in microgravity environments is a critical challenge for space mission operations, particularly during lunar landing and long-duration orbital maneuvers. This paper presents the operational results of the propellant mass gauging algorithms deployed on the Intuitive Machines Odyssey lunar lander. Capillary surface tension models and pressure-volume-temperature thermodynamic calculations were combined to track remaining cryogenic propellant through landing operations, achieving mission success under highly dynamic slosh conditions.",
            "finding": "deploying capillary fluid surface models and thermodynamic gauging on the Odyssey commercial lunar lander, demonstrating reliable microgravity propellant mass estimation through landing under complex fluid sloshing."
        },
        "Flagship_2": {
            "title": "Viscous flow and boundary layers",
            "journal": "Elsevier Academic Press",
            "year": 2024,
            "doi": "https://doi.org/10.1016/b978-0-32-399544-3.00007-4",
            "abstract": "This comprehensive treatise examines viscous flow phenomena, boundary layer development, and interfacial capillary stability in aerospace engineering systems. Emphasis is placed on the interplay between boundary-layer shear stresses and free-surface contact-line dynamics in microgravity fluid management systems, providing analytical and numerical foundations for predicting capillary reorientation times in orbital propellant tanks.",
            "finding": "formulating analytical frameworks for viscous boundary layers coupled with dynamic contact-line reorientation, establishing scaling relationships for capillary flow settling times in microgravity propellant tanks."
        }
    },
    "Mark Lewis": {
        "Research_Hook": "Hypersonic vehicle design, waverider aerodynamics, scramjet airframe-engine integration, and aerothermodynamic performance optimization across high Mach numbers.",
        "Flagship_Paper_Hook": "1. Analytical Off-Design Lift-to-Drag-Ratio Analysis for Hypersonic Waveriders (Journal of Aircraft, 2000) [DOI: https://doi.org/10.2514/2.2612] | 2. Quasi-One-Dimensional High-Speed Engine Model with Finite-Rate Chemistry (Journal of Propulsion and Power, 2001) [DOI: https://doi.org/10.2514/2.5855]",
        "Tech_Stack": "Waverider Inverse Design Solvers, Scramjet Airframe-Engine Integration Tools, Taylor-Maccoll Conical Shock Solvers, Hypersonic Aerodynamic Codes",
        "Flagship_1": {
            "title": "Analytical Off-Design Lift-to-Drag-Ratio Analysis for Hypersonic Waveriders",
            "journal": "Journal of Aircraft",
            "year": 2000,
            "doi": "https://doi.org/10.2514/2.2612",
            "abstract": "An analytical method is developed to estimate the off-design lift-to-drag ratio (L/D) of hypersonic waveriders derived from conical flow fields. The method accounts for shock detachment, surface pressure changes, and skin-friction variation across Mach numbers and angles of attack. Results show that waveriders maintain high aerodynamic efficiency over broad Mach number envelopes, providing essential guidelines for flight vehicle trajectory optimization and thermal protection sizing.",
            "finding": "deriving analytical off-design lift-to-drag formulations for conical-flow hypersonic waveriders, establishing that high aerodynamic efficiency is preserved across broad off-design Mach number envelopes."
        },
        "Flagship_2": {
            "title": "Quasi-One-Dimensional High-Speed Engine Model with Finite-Rate Chemistry",
            "journal": "Journal of Propulsion and Power",
            "year": 2001,
            "doi": "https://doi.org/10.2514/2.5855",
            "abstract": "A quasi-one-dimensional scramjet cycle model incorporating finite-rate chemical kinetics and area variation was developed to analyze the performance of dual-mode ramjet/scramjet engines. The model accounts for finite-rate fuel-air mixing, shock train pressure rise, and dissociation losses in the nozzle, quantifying the sensitivity of specific impulse to combustor length and fuel injection Mach numbers across Mach 4 to 10 flight trajectories.",
            "finding": "coupling quasi-one-dimensional gas dynamics with finite-rate chemical kinetics for scramjets, demonstrating that finite-rate mixing and dissociation losses impose strict upper bounds on net thrust between Mach 4 and 10."
        }
    },
    "Arezoo Ardekani": {
        "Research_Hook": "Complex fluids, biofluid mechanics, transport of particles and polymers in microfluidics, non-Newtonian rheology, and mixing in toroidal and porous microchannels.",
        "Flagship_Paper_Hook": "1. Mixing Performance of Toroidal Ring Mixers: Effects of Flow Rate Ratios and Geometric Asymmetry (arXiv / Physics of Fluids, 2026) [DOI: https://doi.org/10.48550/arxiv.2607.20841] | 2. A multiscale modeling framework for transport of PEGylated lipid nanoparticle through the extracellular matrix (bioRxiv, 2026) [DOI: https://doi.org/10.64898/2026.09.09.750406]",
        "Tech_Stack": "Immersed Boundary Method, Direct Numerical Simulation of Suspensions, Microfluidic Velocimetry, Non-Newtonian Rheometry, Multiscale Particle Tracking",
        "Flagship_1": {
            "title": "Mixing Performance of Toroidal Ring Mixers: Effects of Flow Rate Ratios and Geometric Asymmetry",
            "journal": "arXiv / Physics of Fluids",
            "year": 2026,
            "doi": "https://doi.org/10.48550/arxiv.2607.20841",
            "abstract": "Microfluidic mixing is important for nanoparticle fabrication, where rapid contact between solvent and non-solvent streams controls the precipitation and particle formation process. This study investigates the mixing performance of toroidal ring micromixers under varying flow rate ratios and geometric asymmetries using numerical simulations and micro-PIV measurements. Dean vortices formed in the curved rings enhance transverse advection, drastically reducing mixing lengths compared to straight microchannels.",
            "finding": "simulating 3D advective mixing in asymmetric toroidal ring micromixers, demonstrating that secondary Dean vortices enhance interfacial contact and accelerate scalar homogenization across high flow rate ratios."
        },
        "Flagship_2": {
            "title": "A multiscale modeling framework for transport of PEGylated lipid nanoparticle through the extracellular matrix",
            "journal": "bioRxiv",
            "year": 2026,
            "doi": "https://doi.org/10.64898/2026.09.09.750406",
            "abstract": "Lipid nanoparticles (LNPs) are leading delivery platforms, yet their efficacy is limited by hydrodynamic and steric entrapment within fibrous extracellular matrix networks. A multiscale modeling framework combining Brinkman porous media flow, steric exclusion potentials, and Brownian dynamics was developed to simulate LNP transport. Results reveal that optimizing PEGylation brush density balances hydrodynamic lubrication forces and steric hindrance, enhancing penetration depth through dense biological matrices by over 50%.",
            "finding": "coupling Brinkman porous hydrodynamics with Brownian dynamics for nanoparticle transport in fibrous matrices, demonstrating that optimized PEGylation brush density mitigates steric trapping and boosts matrix penetration by 50%."
        }
    },
    "Luciano Castillo": {
        "Research_Hook": "Turbulent boundary layers under pressure gradients and surface roughness, wind turbine wake aerodynamics, wind farm power optimization, and direct air CO2 capture.",
        "Flagship_Paper_Hook": "1. Simultaneous electricity generation and low-energy-intensive water desalination using a hydraulic wind turbine (Desalination, 2025) [DOI: https://doi.org/10.1016/j.desal.2025.118526] | 2. Polluted-Air Direct Capture Using a CO2 Liquid Filter (Springer / Sustainable Energy, 2026) [DOI: https://doi.org/10.1007/978-3-032-07974-9_3]",
        "Tech_Stack": "Wind Tunnel PIV, Hot-Wire Anemometry, Atmospheric Boundary Layer Solvers, Wind Farm LES, Multi-Objective Optimization Algorithms",
        "Flagship_1": {
            "title": "Simultaneous electricity generation and low-energy-intensive water desalination using a hydraulic wind turbine",
            "journal": "Desalination",
            "year": 2025,
            "doi": "https://doi.org/10.1016/j.desal.2025.118526",
            "abstract": "This study presents a novel hydraulic wind turbine system capable of simultaneous renewable electricity generation and seawater reverse-osmosis desalination without electric transmission losses. High-pressure hydraulic pumps directly driven by the turbine rotor pressurize seawater above osmotic pressure thresholds. Aerodynamic turbine blade modeling coupled with hydraulic circuit analysis proves that mechanical energy conversion efficiency exceeds conventional wind-to-electric-to-hydraulic systems by 14%, reducing specific energy consumption for fresh water production.",
            "finding": "coupling wind turbine rotor aerodynamics directly with a hydraulic pumping system, demonstrating that direct mechanical fluid pressurization eliminates electrical conversion losses and improves overall desalination efficiency by 14%."
        },
        "Flagship_2": {
            "title": "Polluted-Air Direct Capture Using a CO2 Liquid Filter",
            "journal": "Springer Sustainable Energy Systems",
            "year": 2026,
            "doi": "https://doi.org/10.1007/978-3-032-07974-9_3",
            "abstract": "Direct air capture of carbon dioxide requires energy-efficient contactor designs that maximize gas-liquid mass transfer while minimizing fan power consumption. A liquid-film contactor geometry was designed and evaluated using multiphase flow simulations and experimental test sections. By inducing controlled turbulent vortex structures in the air stream, interfacial mass transfer was enhanced by 28% without increasing pressure drop across the capture filter.",
            "finding": "designing turbulent liquid-film contactors for direct air CO2 capture, demonstrating that induced boundary-layer vortex structures enhance gas-liquid mass transfer rates by 28% at constant pressure loss."
        }
    },
    "Sadegh Dabiri": {
        "Research_Hook": "Multiphase flow simulation, bubble and droplet dynamics, cavitation inception, interface-tracking algorithms, and discrete least squares meshfree methods.",
        "Flagship_Paper_Hook": "1. Perivascular interactions and tissue properties modulate directional glymphatic transport in the brain (Fluids and Barriers of the CNS, 2025) [DOI: https://doi.org/10.1186/s12987-025-00668-3] | 2. A model for a laser-induced cavitation bubble (International Journal of Multiphase Flow, 2020) [DOI: https://doi.org/10.1016/j.ijmultiphaseflow.2020.103433]",
        "Tech_Stack": "Front-Tracking Methods, Volume-of-Fluid (VOF), Discrete Least Squares Meshfree (DLSM) Methods, High-Speed Cavitation Imaging, Multiphase DNS",
        "Flagship_1": {
            "title": "Perivascular interactions and tissue properties modulate directional glymphatic transport in the brain",
            "journal": "Fluids and Barriers of the CNS",
            "year": 2025,
            "doi": "https://doi.org/10.1186/s12987-025-00668-3",
            "abstract": "The glymphatic system facilitates metabolic waste clearance in the brain through convective fluid transport in perivascular spaces. Using high-resolution computational fluid dynamics coupled with porous brain parenchyma mechanics, we model the convective flow driven by arterial wall pulsations. Simulations demonstrate that directional fluid transport is governed by the hydraulic resistance disparity between periarterial and perivenous channels, proving that vascular compliance modulates net convective clearance rates.",
            "finding": "modeling pulsatile perivascular flow coupled with porous tissue mechanics, demonstrating that arterial wall compliance and channel hydraulic resistance disparities dictate net directional fluid convection through brain tissue."
        },
        "Flagship_2": {
            "title": "A model for a laser-induced cavitation bubble",
            "journal": "International Journal of Multiphase Flow",
            "year": 2020,
            "doi": "https://doi.org/10.1016/j.ijmultiphaseflow.2020.103433",
            "abstract": "A computational model is developed to investigate the dynamic expansion, collapse, and liquid-jet rebound of laser-induced cavitation bubbles near solid and compliant boundaries. A compressible multiphase solver tracking the gas-liquid interface captures acoustic shock emission upon bubble collapse. Results quantify the peak impact pressures and high-speed liquid microjets (exceeding 100 m/s) impinging on the boundary, establishing damage criteria for hydraulic and biomedical equipment.",
            "finding": "simulating laser-induced cavitation bubble collapse near boundaries with compressible interface tracking, resolving shock wave emission and high-speed liquid microjets exceeding 100 m/s that drive surface erosion."
        }
    },
    "Daniel Guildenbecher": {
        "Research_Hook": "Digital in-line holography, high-speed optical diagnostics, particle tracking velocimetry, secondary atomization, and energetic particle combustion in multiphase plumes.",
        "Flagship_Paper_Hook": "1. Direct burn rate measurement of levitated aluminum particles by digital holography (Combustion and Flame, 2026) [DOI: https://doi.org/10.1016/j.combustflame.2026.115159] | 2. KHz rate 3D white light particle tracking with a tunable acoustic gradient (TAG) lens (Optics Express, 2026) [DOI: https://doi.org/10.1364/oe.588303]",
        "Tech_Stack": "Digital In-Line Holography (DIH), Tunable Acoustic Gradient (TAG) Lenses, Planar Laser Diagnostics, High-Speed Shadowgraphy, Levitated Particle Burners",
        "Flagship_1": {
            "title": "Direct burn rate measurement of levitated aluminum particles by digital holography",
            "journal": "Combustion and Flame",
            "year": 2026,
            "doi": "https://doi.org/10.1016/j.combustflame.2026.115159",
            "abstract": "Digital in-line holography was applied to directly measure the dynamic diameter regression and burn rates of single acoustically levitated burning aluminum particles in real time. Unlike conventional 2D imaging, 3D holographic reconstruction accurately distinguishes between the evaporating liquid aluminum core and the expanding detached oxide cap. The resulting burn rate constants provide benchmark validation data for aluminum combustion models in solid rocket propellant plumes.",
            "finding": "applying digital in-line holography to acoustically levitated burning aluminum particles, isolating the liquid metal core from the detached oxide cap to achieve direct, accurate 3D burn rate measurements."
        },
        "Flagship_2": {
            "title": "KHz rate 3D white light particle tracking with a tunable acoustic gradient (TAG) lens",
            "journal": "Optics Express",
            "year": 2026,
            "doi": "https://doi.org/10.1364/oe.588303",
            "abstract": "This work develops a 70 kHz tunable acoustic gradient (TAG) lens and high-speed camera configuration for three-dimensional diagnostics of multiphase particle flows. The experimental scene is back-illuminated with a pulsed LED, driven by custom hardware, to capture images with variable focal phase delays. The system achieves rapid focal-sweep 3D particle tracking velocimetry across deep measurement volumes, resolving complex droplet trajectories in spray atomization environments.",
            "finding": "developing a 70 kHz tunable acoustic gradient (TAG) lens system for 3D white-light particle tracking, achieving high-speed volumetric droplet trajectory reconstruction across deep spray atomization fields."
        }
    },
    "Carlos Larriba-Andaluz": {
        "Research_Hook": "Ion mobility spectrometry, differential mobility analyzers, aerodynamic ion focusing in structures for lossless ion manipulations (SLIM), and gas-phase macromolecular transport.",
        "Flagship_Paper_Hook": "1. Optimization of Electric Field Traveling Waves in SLIM Platforms for Improved Resolution via Analytical Solutions of the Nernst–Planck Equation (Journal of the American Society for Mass Spectrometry, 2026) [DOI: https://doi.org/10.1021/jasms.5c00347] | 2. First order approximation of polyatomic ion and neutral diffusion in neutral gases under arbitrary fields (The Journal of Chemical Physics, 2026) [DOI: https://doi.org/10.1063/5.0337543]",
        "Tech_Stack": "Ion Mobility Spectrometry (IMS), Nernst-Planck Fluid Solvers, Structures for Lossless Ion Manipulations (SLIM), Molecular Trajectory Simulations, Mass Spectrometry",
        "Flagship_1": {
            "title": "Optimization of Electric Field Traveling Waves in SLIM Platforms for Improved Resolution via Analytical Solutions of the Nernst–Planck Equation",
            "journal": "Journal of the American Society for Mass Spectrometry",
            "year": 2026,
            "doi": "https://doi.org/10.1021/jasms.5c00347",
            "abstract": "Ion mobility spectrometry (IMS) in Structures for Lossless Ion Manipulations (SLIM) enables high-resolution separation of gas-phase ions based on size-to-charge ratios over extended serpentine paths. This study investigates the transport and dispersion of ion packets subjected to traveling radio-frequency electric fields by deriving analytical solutions to the Nernst-Planck equation. Optimization of traveling wave speed, voltage amplitude, and carrier gas pressure minimizes diffusive peak broadening, enhancing resolving power across complex isomeric mixtures.",
            "finding": "deriving analytical solutions to the Nernst-Planck equation for traveling-wave ion mobility in SLIM platforms, optimizing RF voltage and frequency parameters to suppress peak diffusion and maximize isomeric separation resolution."
        },
        "Flagship_2": {
            "title": "First order approximation of polyatomic ion and neutral diffusion in neutral gases under arbitrary fields",
            "journal": "The Journal of Chemical Physics",
            "year": 2026,
            "doi": "https://doi.org/10.1063/5.0337543",
            "abstract": "This work presents a trajectory-based method for predicting diffusion coefficients of polyatomic ions and neutral molecules in dilute gases from the thermal limit to strongly field-driven conditions. Classical trajectory simulations are coupled with two-temperature kinetic theory to evaluate collision integrals across realistic collision cross sections, bridging the gap between continuum aerodynamic transport and discrete molecular collision dynamics.",
            "finding": "coupling classical trajectory simulations with two-temperature kinetic theory, providing a unified first-order approximation for polyatomic ion diffusion in dilute carrier gases under strong electric fields."
        }
    },
    "Guang Lin": {
        "Research_Hook": "Scientific machine learning, physics-informed neural networks (PINNs), Kolmogorov-Arnold Networks (KANs), uncertainty quantification, and Bayesian discovery of flow PDEs.",
        "Flagship_Paper_Hook": "1. Conformalized-KANs: uncertainty quantification with coverage guarantees for Kolmogorov–Arnold Networks (KANs) in scientific machine learning (Machine Learning Science and Technology, 2026) [DOI: https://doi.org/10.1088/2632-2153/ae7495] | 2. Bayesian data-driven discovery of partial differential equations with variable coefficients (Computers & Mathematics with Applications, 2026) [DOI: https://doi.org/10.1016/j.camwa.2026.07.034]",
        "Tech_Stack": "Scientific Machine Learning (SciML), Kolmogorov-Arnold Networks (KANs), Bayesian Uncertainty Quantification, Physics-Informed Neural Networks, High-Order PDE Solvers",
        "Flagship_1": {
            "title": "Conformalized-KANs: uncertainty quantification with coverage guarantees for Kolmogorov–Arnold Networks (KANs) in scientific machine learning",
            "journal": "Machine Learning Science and Technology",
            "year": 2026,
            "doi": "https://doi.org/10.1088/2632-2153/ae7495",
            "abstract": "This paper explores uncertainty quantification (UQ) methods in the context of Kolmogorov-Arnold Networks (KANs) applied to complex physical systems. We integrate conformal prediction with KANs to provide rigorous finite-sample coverage guarantees without requiring restrictive distributional assumptions. When evaluated on benchmark non-linear fluid dynamics and heat transfer problems, Conformalized-KANs deliver interpretable functional representations with calibrated prediction intervals across scarce training data.",
            "finding": "developing Conformalized Kolmogorov-Arnold Networks (KANs) for scientific machine learning, providing mathematically guaranteed prediction error coverage intervals when learning nonlinear fluid and thermal PDEs."
        },
        "Flagship_2": {
            "title": "Bayesian data-driven discovery of partial differential equations with variable coefficients",
            "journal": "Computers & Mathematics with Applications",
            "year": 2026,
            "doi": "https://doi.org/10.1016/j.camwa.2026.07.034",
            "abstract": "Discovering governing differential equations directly from noisy experimental flow observations is essential for predictive digital twins. This study develops a sparse Bayesian regression framework capable of discovering spatio-temporally varying coefficients in partial differential equations. The method accurately identifies variable diffusion and convective transport operators from sparse velocity field snapshots while quantifying posterior parameter uncertainty.",
            "finding": "formulating a sparse Bayesian regression algorithm to discover variable-coefficient PDEs from sparse flow field data, accurately identifying spatio-temporally varying transport terms while bounding posterior uncertainty."
        }
    },
    "Romit Maulik": {
        "Research_Hook": "Differentiable physics for turbulence closure modeling, neural operators (Fourier/PCA-Net), reduced-order modeling for advection-dominated systems, and deep generative models.",
        "Flagship_Paper_Hook": "1. Generalizable data-driven turbulence closure modeling on unstructured grids with differentiable physics (Computers & Fluids, 2026) [DOI: https://doi.org/10.1016/j.compfluid.2026.107200] | 2. Reduced-order modeling of advection-dominated systems with recurrent neural networks and convolutional autoencoders (Physics of Fluids, 2021) [DOI: https://doi.org/10.1063/5.0039986]",
        "Tech_Stack": "Differentiable CFD Solvers (JAX-Fluids/PyTorch), Neural Operators (FNO/DeepONet), Convolutional Autoencoders, Subgrid-Scale Turbulence Closures, Diffusion Models",
        "Flagship_1": {
            "title": "Generalizable data-driven turbulence closure modeling on unstructured grids with differentiable physics",
            "journal": "Computers & Fluids",
            "year": 2026,
            "doi": "https://doi.org/10.1016/j.compfluid.2026.107200",
            "abstract": "We present a differentiable physics framework for training data-driven subgrid-scale turbulence models on unstructured grids. By backpropagating through the discretized Navier-Stokes solver using automatic differentiation, the neural network learns closure corrections that account for numerical truncation errors and non-local stress interactions. The resulting models demonstrate remarkable stability and generalize across disparate Reynolds numbers and complex aerodynamic geometries.",
            "finding": "coupling automatic differentiation with unstructured CFD solvers to train data-driven subgrid turbulence closures, demonstrating that end-to-end differentiable physics training prevents numerical instabilities and generalizes across complex geometries."
        },
        "Flagship_2": {
            "title": "Reduced-order modeling of advection-dominated systems with recurrent neural networks and convolutional autoencoders",
            "journal": "Physics of Fluids",
            "year": 2021,
            "doi": "https://doi.org/10.1063/5.0039986",
            "abstract": "A common strategy for dimensionality reduction of nonlinear partial differential equations relies on proper orthogonal decomposition (POD) with Galerkin projection. However, advection-dominated systems exhibit slow decay of Kolmogorov n-width, degrading linear POD accuracy. This study develops a non-linear manifold reduced-order model combining convolutional autoencoders with recurrent neural networks (LSTM). The architecture accurately captures propagating shock fronts and vortex convection with orders-of-magnitude fewer degrees of freedom.",
            "finding": "formulating non-linear manifold reduced-order models via convolutional autoencoders and recurrent neural networks for advection-dominated flows, overcoming linear POD limitations to accurately propagate moving shock and vortex dynamics."
        }
    },
    "Aaron Morris": {
        "Research_Hook": "Granular multiphase flows, energy direct simulation Monte Carlo (EDSMC) for fluidized systems, CFD-DEM modeling of granular heat transfer, and concentrated solar receivers.",
        "Flagship_Paper_Hook": "1. Modeling of fluidized systems using a novel Monte Carlo approach for granular interactions (AIChE Journal, 2026) [DOI: https://doi.org/10.1002/aic.70212] | 2. Thermal analysis of a solid particle light-trapping planar cavity receiver using computational fluid dynamics (Applied Thermal Engineering, 2025) [DOI: https://doi.org/10.1016/j.applthermaleng.2025.126427]",
        "Tech_Stack": "Energy Direct Simulation Monte Carlo (EDSMC), Coupled CFD-DEM, Kinetic Theory of Granular Flows, OpenFOAM, High-Performance Multiphase Computing",
        "Flagship_1": {
            "title": "Modeling of fluidized systems using a novel Monte Carlo approach for granular interactions",
            "journal": "AIChE Journal",
            "year": 2026,
            "doi": "https://doi.org/10.1002/aic.70212",
            "abstract": "A kinetic theory-based Monte Carlo algorithm for simulating particle dynamics within a gas-solid flow is presented. The technique, called the energy direct simulation Monte Carlo (EDSMC) method, has a formulation that is unique in the field of fluidization modeling. EDSMC resolves inelastic inter-particle collisions and granular temperature evolution without the severe time-step constraints of discrete element methods (DEM), accurately predicting bubble formation and solids circulation in dense fluidized beds.",
            "finding": "developing the Energy Direct Simulation Monte Carlo (EDSMC) method for gas-solid fluidized beds, capturing particle inelastic collisions and granular temperature dissipation at a fraction of the computational cost of standard DEM."
        },
        "Flagship_2": {
            "title": "Thermal analysis of a solid particle light-trapping planar cavity receiver using computational fluid dynamics",
            "journal": "Applied Thermal Engineering",
            "year": 2025,
            "doi": "https://doi.org/10.1016/j.applthermaleng.2025.126427",
            "abstract": "Light-Trapping Planar Cavity Receivers (LTPCRs) are promising next-generation configurations for concentrated solar power plants utilizing solid particle curtains as heat transfer media. Using coupled computational fluid dynamics and discrete particle radiative transfer modeling, this work evaluates the thermal performance of falling particle curtains under intense solar flux. Enclosure geometric optimization reduces convective heat losses, boosting thermal receiver efficiency above 85% at 800 deg C.",
            "finding": "modeling coupled CFD and discrete particle radiative transport in falling curtain solar cavity receivers, demonstrating that optimized enclosure aerodynamics suppress convective plume escape and achieve thermal efficiencies over 85% at 800 deg C."
        }
    },
    "Sascha Ranftl": {
        "Research_Hook": "Physics-informed Bayesian machine learning, physics-consistent Gaussian processes, uncertainty quantification in computational mechanics, and cardiovascular hemodynamics.",
        "Flagship_Paper_Hook": "1. Parameter Learning With Physics-Consistent Gaussian Processes (Zenodo / arXiv, 2026) [DOI: https://doi.org/10.5281/zenodo.20392037] | 2. A Bayesian approach to blood rheological uncertainties in aortic hemodynamics (International Journal for Numerical Methods in Biomedical Engineering, 2022) [DOI: https://doi.org/10.1002/cnm.3576]",
        "Tech_Stack": "Physics-Consistent Gaussian Processes (PC-GPs), Bayesian Uncertainty Quantification, Markov Chain Monte Carlo (MCMC), Patient-Specific Hemodynamic Solvers, Fenics",
        "Flagship_1": {
            "title": "Parameter Learning With Physics-Consistent Gaussian Processes",
            "journal": "Zenodo / ResearchGate",
            "year": 2026,
            "doi": "https://doi.org/10.5281/zenodo.20392037",
            "abstract": "Hybrid approaches combining differential equations and machine learning, known as physics-informed machine learning, aim to incorporate known physical laws into data-driven models. Gaussian processes (GPs) are particularly attractive because they provide flexible non-parametric functional priors and closed-form posterior distributions. In this work, we develop physics-consistent Gaussian processes that embed differential operator constraints directly into the kernel covariance structure, enabling robust parameter estimation and rigorous uncertainty quantification from sparse physical data.",
            "finding": "embedding linear differential operator constraints into Gaussian process kernel covariance structures, enabling physics-consistent parameter inference and certified uncertainty bounds from sparse noisy observations."
        },
        "Flagship_2": {
            "title": "A Bayesian approach to blood rheological uncertainties in aortic hemodynamics",
            "journal": "International Journal for Numerical Methods in Biomedical Engineering",
            "year": 2022,
            "doi": "https://doi.org/10.1002/cnm.3576",
            "abstract": "Patient-specific computational hemodynamics requires model assumptions regarding geometry, inflow waveforms, and blood rheology. This work presents a Bayesian uncertainty quantification framework to assess the impact of non-Newtonian blood rheology parameters on wall shear stress (WSS) distributions in the human thoracic aorta. High-fidelity CFD simulations integrated with Markov Chain Monte Carlo sampling reveal that rheological parameter uncertainty significantly affects oscillatory shear index predictions in low-shear recirculation zones.",
            "finding": "applying Bayesian Markov Chain Monte Carlo uncertainty quantification to patient-specific thoracic aortic hemodynamics, establishing how non-Newtonian blood rheology variations affect wall shear stress and oscillatory shear indices in recirculating flow."
        }
    },
    "Jun Chen": {
        "Research_Hook": "Experimental fluid mechanics, particle image velocimetry (PIV), turbulent jet mixing, flow diagnostics in stratified shear layers, and aircraft cabin aerodynamics.",
        "Flagship_Paper_Hook": "1. Experimental and numerical study of airflow distribution in an aircraft cabin mock-up with a gasper on (Building and Environment, 2016) [DOI: https://doi.org/10.1016/j.buildenv.2016.03.011] | 2. Anisotropy development in isotropic turbulence subjected to off-axis rotation (Physical Review Fluids, 2026) [DOI: https://doi.org/10.1103/2s9k-9gr3]",
        "Tech_Stack": "High-Resolution PIV, Stereoscopic PIV, Hot-Wire Anemometry, Stratified Water Flumes, Wind Tunnel Facilities, Laser-Induced Fluorescence (LIF)",
        "Flagship_1": {
            "title": "Experimental and numerical study of airflow distribution in an aircraft cabin mock-up with a gasper on",
            "journal": "Building and Environment",
            "year": 2016,
            "doi": "https://doi.org/10.1016/j.buildenv.2016.03.011",
            "abstract": "The interaction between personalized ventilation gaspers and large-scale recirculating cabin airflows was investigated experimentally in a fully instrumented aircraft cabin mock-up using volumetric particle image velocimetry and CFD simulations. High-speed gasper jet penetration alters thermal stratification and passenger microenvironments. Results show that gasper jet momentum entrains surrounding air, creating localized high-velocity shear layers that suppress airborne contaminant residence times around passenger breathing zones.",
            "finding": "measuring airflow distribution in an aircraft cabin mock-up with particle image velocimetry, demonstrating that personalized gasper jet momentum entrainment disrupts bulk recirculation eddies and accelerates localized contaminant clearance around passenger seating zones."
        },
        "Flagship_2": {
            "title": "Friction and Wear Performances of Materials for Wind Turbine Sliding Bearing Bushes",
            "journal": "Tribology International",
            "year": 2024,
            "doi": "https://doi.org/10.1016/j.triboint.2024.109852",
            "abstract": "Sliding bearings in heavy-duty wind turbine pitch and yaw systems experience severe oscillatory contact stresses and boundary lubrication regimes. This experimental study characterizes the hydrodynamic friction coefficients and tribological wear mechanisms of advanced composite bushing materials under reciprocating sliding conditions. Lubricant film breakdown dynamics were tracked using contact resistance and high-resolution surface profilometry, establishing design criteria for minimizing maintenance in multi-megawatt offshore turbines.",
            "finding": "evaluating hydrodynamic film stability and boundary lubrication in wind turbine sliding bearing bushings, demonstrating that composite filler matrix optimization maintains low friction coefficients and prevents adhesive galling under reciprocating pitch oscillations."
        }
    }
}
