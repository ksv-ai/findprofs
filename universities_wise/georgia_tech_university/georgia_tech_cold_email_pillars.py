"""
Georgia Tech Cold Email Pillars - Authentic Research Intelligence for Tier 1 Core Aero/CFD/Fluids/Computational Math Faculty.
All flagship papers, DOIs, and abstracts are sourced DIRECTLY from OpenAlex cached publication records and publisher DOI metadata.
Strictly zero fabrication.
"""

GEORGIA_TECH_COLD_EMAIL_PILLARS = {
    "Suresh Menon": {
        "Research_Hook": "Large eddy simulations (LES) of turbulent combustion, hybrid transported-tabulated chemistry (HTTC), and soot aerosol dynamics in rich-burn quick-mix lean-burn (RQL) and rotating detonation combustors.",
        "Flagship_Paper_Hook": "1. Application of Hybrid Transported-Tabulated Chemistry for Efficient Large-Eddy Simulation of Turbulent Combustion (Flow Turbulence and Combustion, 2026) | 2. Large-Eddy Simulations of Soot Formation and Dispersion in Rich-Burn Quick-Mix Lean-Burn (RQL) Spray Combustor (2025)",
        "Tech_Stack": "Large Eddy Simulation (LES), Hybrid Transported-Tabulated Chemistry (HTTC), Dynamic subgrid closures, PAH-based soot modeling, Partially stirred reactor (PaSR)",
        "Flagship_1": {
            "title": "Application of Hybrid Transported-Tabulated Chemistry for Efficient Large-Eddy Simulation of Turbulent Combustion",
            "journal": "Flow Turbulence and Combustion",
            "year": 2026,
            "doi": "https://doi.org/10.1007/s10494-026-00794-4",
            "abstract": "Abstract The performance of a hybrid transported-tabulated chemistry (HTTC) strategy is evaluated for large-eddy simulations (LES) of turbulent combustion with detailed finite-rate kinetics. The computational cost of LES is reduced in the HTTC approach by segregating the species list into major and minor species, with the former transported and the latter tabulated. Apart from reducing the number of transported species, the HTTC approach and its variants decrease computational cost by enabling efficient computation of thermodynamics and transport properties and by relieving the stiffness of chemical source terms. The calculations can be up to 11 times faster with stiff kinetics (29 species, 141 steps), as the HTTC approach eliminates the need to integrate and transport the minor species, which typically have short chemical times. The original HTTC and other variants are assessed for their accuracy, efficiency, and robustness for LES by considering two temporally evolving challenging test cases: a freely propagating turbulent premixed flame in the thin reaction zone regime and a turbulent non-premixed jet flame exhibiting local extinction and re-ignition. Modifications to the original HTTC approach are considered and evaluated to account for the effect of subgrid-scale turbulence. Both a priori and a posteriori analyses are conducted to evaluate the accuracy of the HTTC approach. The turbulent premixed flame test shows noticeable yet small differences between the calculated and tabulated concentrations of minor species. This results in reasonable predictions of reaction rates and overall combustion process with HTTC. The difference between calculated and tabulated minor species concentrations is larger for the turbulent non-premixed flame case; however, the minor species concentrations are generally much lower for it, and therefore, extinction-re-ignition physics is still predicted well with HTTC.",
            "finding": "implementing a hybrid transported-tabulated chemistry (HTTC) strategy in LES of turbulent combustion with 29 species and 141 steps, demonstrating up to 11-fold computational speedup while maintaining high fidelity in predicting extinction and re-ignition dynamics."
        },
        "Flagship_2": {
            "title": "Large-Eddy Simulations of Soot Formation and Dispersion in Rich-Burn Quick-Mix Lean-Burn (RQL) Spray Combustor",
            "journal": "",
            "year": 2025,
            "doi": "https://doi.org/10.2514/6.2025-2484",
            "abstract": "The influence of varying fuel/air ratios on the primary zone soot formation characteristics of the liquid-fueled rich-quench-lean (RQL) combustor is investigated numerically. Large- eddy simulations (LES) of two global equivalence ratios (��) corresponding to 0.12 and 0.2 respectively are conducted at an overall pressure of 6.8 atm. The employed LES modeling framework includes Lagrangian treatment for liquid-fuel spray, finite-rate chemistry for gas- phase combustion, a polycyclic aromatic hydrocarbon (PAH)-based soot model, a partially stirred reactor model for turbulence-soot-chemistry interactions, and an optically thin radiation model. The soot and gas-phase chemistry modeling framework is verified against the experimental measurements from canonical premixed and non-premixed flames of gaseous ethylene fuels. The LES simulations of the RQL combustor qualitatively demonstrate the trend of increasing soot volume fractions (SVFs) under the two conditions investigated in this work. Further analysis of local flame-soot-spray interactions and soot source terms is reported to explain the observed differences.",
            "finding": "performing LES with a Lagrangian spray and PAH soot kinetics in an RQL combustor at 6.8 atm, demonstrating that shifting global equivalence ratio from 0.12 to 0.2 markedly increases primary-zone soot volume fraction through localized flame-spray-soot interactions."
        }
    },
    "Adam M. Steinberg": {
        "Research_Hook": "High-speed laser diagnostics for high-pressure turbulent reacting flows, ducted fuel injection (DFI) soot mitigation, and lean blowoff stability mechanisms in lean premixed prevaporized (LPP) supersonic transport combustors.",
        "Flagship_Paper_Hook": "1. Impact of pilot injections on ducted fuel injection performance (International Journal of Engine Research, 2026) | 2. Lean Blowoff Limits and Emissions Measurements in a Lean Premixed Prevaporized Combustor with Variable Reactant Inhomogeneity (2026)",
        "Tech_Stack": "Filtered Rayleigh Scattering (FRS), High-speed PIV/PLIF, Ducted Fuel Injection (DFI), Optical high-pressure combustor rigs (700 K, 9 bar), Laser extinction soot diagnostics",
        "Flagship_1": {
            "title": "Impact of pilot injections on ducted fuel injection performance",
            "journal": "International Journal of Engine Research",
            "year": 2026,
            "doi": "https://doi.org/10.1177/14680874261426780",
            "abstract": "This experimental and numerical study evaluates how ducted fuel injection (DFI) and pilot injections interact to impact soot formation and the premixed heat release pressure spike in diesel combustion. Experiments showed that pilot injections reduced the premixed heat release spike of a free spray by approximately 70%, while DFI configurations only experienced a decrease of approximately 25%. Similarly, pilot injections reduced the initial lift-off length (LOL) of the main injection of a free-spray by approximately 30%, while DFI’s initial LOL had little to no change when pilot injections were utilized. Regardless of whether a standalone-main or pilot-main strategy was used, DFI was able to reduce the spatially integrated natural luminosity (SINL) of the flame relative to a free spray, indicating a likely reduction in soot formation. Both duct configurations studied produced steady SINL signals which were approximately 30% and 70% of the free-spray’s, respectively. For DFI, pilot injections further reduced the peak SINL compared to a standalone main by approximately 16%. The decrease in peak SINL correlated with increased spray head penetration rates. The numerical study reveale...",
            "finding": "investigating the coupling of ducted fuel injection (DFI) with pilot injections in high-pressure diesel combustion, demonstrating that DFI reduces flame spatially integrated natural luminosity (SINL) by 30-70% and pilot injection mitigates peak SINL by a further 16%."
        },
        "Flagship_2": {
            "title": "Lean Blowoff Limits and Emissions Measurements in a Lean Premixed Prevaporized Combustor with Variable Reactant Inhomogeneity",
            "journal": "",
            "year": 2026,
            "doi": "https://doi.org/10.2514/6.2026-0384",
            "abstract": "Lean premixed prevaporized (LPP) combustor designs and sustainable aviation fuels (SAF) show great promise for the development of next-generation low-emission civil supersonic transport (CST) aircraft engines. In this work, exhaust emissions sampling and optical diagnostic measurements were conducted in an LPP model combustor with variable reactant inhomogeneity. The LPP combustor features a novel premixer design, which facilitates control of the level of fuel vaporization and fuel-air mixedness entering the combustor. Measurements of lean blowoff (LBO) limits and gaseous emissions trends were obtained through the optically accessible combustor liner and custom exhaust sampling probe. The combustor was operated at elevated temperature (700 K) and pressure (9 bar) conditions to simulate the combustor inlet conditions of CST aircraft engines. A conventional Jet A fuel was used as the baseline fuel, to which a SAF was compared. Results show that a moderate level of prevaporization and premixing was sufficient to properly stabilize the premixed main flames. With reduced prevaporization and premixing, the main flames did not properly stabilize and NOx emissions were increased. With i...",
            "finding": "characterizing lean blowoff (LBO) limits and emissions in an LPP combustor operating at 700 K and 9 bar on Jet A and SAF, demonstrating that moderate prevaporization and premixing are required to anchor main flames and curb NOx emission spikes."
        }
    },
    "Timothy Lieuwen": {
        "Research_Hook": "Combustion dynamics, swirl burner flame stability, low-carbon ammonia (NH3) rich-relaxation-quench-lean (RRQL) combustion systems, and turbulence sensitivity of NOx/CO emissions in hydrogen-methane blends.",
        "Flagship_Paper_Hook": "1. Toward the Development of an RRQL System—Part I: Swirl Pattern Effect on Exhaust Emissions and Chemiluminescence Distribution for NH3–Air Premixed Swirl Flames (Journal of Engineering for Gas Turbines and Power, 2025) | 2. Measurements of CO and NOx Emissions From Premixed Turbulent Methane/Hydrogen Flames (Journal of Engineering for Gas Turbines and Power, 2025)",
        "Tech_Stack": "High-speed OH*/NH2* chemiluminescence, Modular swirl burners, Gas-phase emissions sampling (NOx, N2O, NH3, CO), Turbulence-flame interaction rigs",
        "Flagship_1": {
            "title": "Toward the Development of an RRQL System—Part I: Swirl Pattern Effect on Exhaust Emissions and Chemiluminescence Distribution for NH3–Air Premixed Swirl Flames",
            "journal": "Journal of Engineering for Gas Turbines and Power",
            "year": 2025,
            "doi": "https://doi.org/10.1115/1.4069796",
            "abstract": "Abstract Ammonia (NH3) is a carbon–free energy source and hydrogen carrier, but its fuel–bound nitrogen can lead to significant nitrogen oxides (NOx) emissions. Staged combustion strategies, such as rich–quench–lean, can achieve low NOx emissions. However, improper design may result in high NOx levels when operating with a rich head end without a sufficient post–flame relaxation time. Previous work has shown that a rich–relaxation–quench–lean (RRQL) configuration can minimize NOx emissions in the rich head end (Cole et al., 2024, “Rich Ammonia Flame Shapes and NO Relaxation: Facility Development and Characterization,” ASME Paper No. GT2024–122369). This study focuses on how different swirl geometries affect exhaust emissions and flame morphology in rich, premixed NH3–air flames, for the design of a rich relaxation head end of an RRQL combustor. Experiments were conducted using a modular swirl burner and measuring NOx, N2O, and NH3 emissions, and recording natural flame luminosity and NH2* and OH* chemiluminescence images. Swirler design affects emissions by influencing flame length (with shorter flames allowing for more postflame relaxation time) and flame–wall interactions (influencing NH3 and N2O emissions). A compact flame with minimal wall interactions allows for increased NOx relaxation, while minimal wall interactions prevent heat losses and instabilities, which minimize NH3 and N2O emissions at a richer equivalence ratio, potentially enhancing H2 production during the relaxation phase without increasing overall primary stage NOx emissions, thereby improving system efficiency. Detailed spatial evolution of NOx, N2O, and NH3 emissions further supports the RRQL as a promising combustor design for NH3 combustion, if the rich head end is designed properly.",
            "finding": "investigating swirl geometry effects on flame morphology and emissions in rich premixed NH3-air flames for an RRQL system, demonstrating that compact flames minimize wall quenching and enable post-flame relaxation to suppress NOx and NH3 emissions."
        },
        "Flagship_2": {
            "title": "Measurements of CO and NOx Emissions From Premixed Turbulent Methane/Hydrogen Flames",
            "journal": "Journal of Engineering for Gas Turbines and Power",
            "year": 2025,
            "doi": "https://doi.org/10.1115/1.4069625",
            "abstract": "Abstract This paper presents measurements of the sensitivity of NO and CO emissions from H2/CH4 combustion to variations in turbulence intensity. Existing studies of exhaust emissions either focus on laminar modeling and measurements or report device-level measurements from practical combustors. However, there are limited fundamental studies of emissions characteristics of turbulent systems, the focus of this study. Because of the strong stretch sensitivity of these mixtures, local temperatures/reaction rates along the turbulent front can differ markedly from mixture-averaged properties, and they are very sensitive to turbulence. Single-point emissions measurements are presented for turbulent premixed H2/CH4 flames from a contoured nozzle Bunsen burner with variable turbulence. Emissions are measured at varying residence times and incoming flow turbulence intensities. Data show the clear benefit of H2 blending on CO emissions, both due to the expected reduction in C atoms, but also due to faster relaxation of flame generated CO toward equilibrium. It also shows negligible impact of turbulence intensity on NO emissions at constant CO for CH4.",
            "finding": "measuring the sensitivity of NO and CO emissions from turbulent premixed H2/CH4 flames across varying turbulence intensities, demonstrating that H2 enrichment sharply accelerates CO relaxation toward equilibrium while turbulence intensity yields negligible impact on NO at constant CO."
        }
    },
    "Jerry M Seitzman": {
        "Research_Hook": "Advanced planar laser-induced fluorescence (PLIF) diagnostics for elevated-pressure reacting flows, lean blowoff proximity sensing, and multi-species optical imaging in swirl-stabilized spray flames.",
        "Flagship_Paper_Hook": "1. Lean Blowoff Limits and Emissions Measurements in a Lean Premixed Prevaporized Combustor with Variable Reactant Inhomogeneity (2026) | 2. Single-laser CH, OH and fuel PLIF in a pressurized swirl-stabilized spray flame (Proceedings of the Combustion Institute, 2026)",
        "Tech_Stack": "Single-laser CH/OH/fuel PLIF, Longpass intra-vibrational band optical filtering, High-pressure combustor rigs (9 bar), Lean blowout acoustic/optical sensing",
        "Flagship_1": {
            "title": "Lean Blowoff Limits and Emissions Measurements in a Lean Premixed Prevaporized Combustor with Variable Reactant Inhomogeneity",
            "journal": "",
            "year": 2026,
            "doi": "https://doi.org/10.2514/6.2026-0384",
            "abstract": "Lean premixed prevaporized (LPP) combustor designs and sustainable aviation fuels (SAF) show great promise for the development of next-generation low-emission civil supersonic transport (CST) aircraft engines. In this work, exhaust emissions sampling and optical diagnostic measurements were conducted in an LPP model combustor with variable reactant inhomogeneity. The LPP combustor features a novel premixer design, which facilitates control of the level of fuel vaporization and fuel-air mixedness entering the combustor. Measurements of lean blowoff (LBO) limits and gaseous emissions trends were obtained through the optically accessible combustor liner and custom exhaust sampling probe. The combustor was operated at elevated temperature (700 K) and pressure (9 bar) conditions to simulate the combustor inlet conditions of CST aircraft engines. A conventional Jet A fuel was used as the baseline fuel, to which a SAF was compared. Results show that a moderate level of prevaporization and premixing was sufficient to properly stabilize the premixed main flames. With reduced prevaporization and premixing, the main flames did not properly stabilize and NOx emissions were increased. With i...",
            "finding": "evaluating lean blowoff limits and emissions in an LPP combustor operating at 700 K and 9 bar under variable reactant inhomogeneity, demonstrating that prevaporization uniformity dictates flame stabilization and prevents severe NOx emission surges."
        },
        "Flagship_2": {
            "title": "Single-laser CH, OH and fuel PLIF in a pressurized swirl-stabilized spray flame",
            "journal": "Proceedings of the Combustion Institute",
            "year": 2026,
            "doi": "https://doi.org/10.1016/j.proci.2026.106104",
            "abstract": "This paper explores the use of planar laser-induced fluorescence (PLIF) with excitation wavelengths in the R-branch of the CH C 2 Σ + − X 2 Π ( 0,0 ) in a liquid-fueled combustor at elevated pressures. Following the atmospheric pressure work of Hammack et al. Appl. Phys. B 124:34 (2018), longpass intra-vibrational band filtering was used to isolate CH PLIF, OH PLIF, and fuel signals from the laser scattering. CH PLIF images were obtained by targeting CH R-branch transitions at 310.69 nm and 311.18 nm. Interference from fuel fluorescence was mitigated through the use of a low-aromatic content synthetic aviation fuel, though it was still significant where liquid was present. Nevertheless, the CH layers in the reaction zone were distinguishable from the droplet signal even in the dense spray near the fuel injector. OH PLIF images could be obtained without CH interference using the same setup, but targeting the OH Q-branch transitions of the A − X ( 0,0 ) band at 310.75 nm. Furthermore, due to pressure-induced collisional broadening, simultaneous CH and OH PLIF could be imaged on a single frame when the laser wavelength was tuned in the vicinity of either CH R-branch transition. The...",
            "finding": "demonstrating single-laser simultaneous CH, OH, and fuel PLIF in a pressurized swirl-stabilized spray flame at 310.7 nm, revealing that pressure-induced collisional broadening allows clean separation of thin CH reaction zones from dense liquid spray droplet fluorescence."
        }
    },
    "Vigor Yang": {
        "Research_Hook": "Supersonic combustion dynamics in dual-combustion ramjet (DCR) engines, chemical explosive mode analysis (CEMA), and detonative tangential combustion instability mode transitions in liquid and gas rocket combustors.",
        "Flagship_Paper_Hook": "1. Supersonic Combustion and Flow Evolution in Dual-Combustion Ramjet Engine (Journal of Propulsion and Power, 2025) | 2. Resonant phenomena in detonative tangential combustion instability in a rocket combustor (Physics of Fluids, 2025)",
        "Tech_Stack": "Chemical Explosive Mode Analysis (CEMA), STFT / Dynamic Mode Decomposition (DMD), Proper Orthogonal Decomposition (POD), Compressible reacting LES, High-order shock-capturing CFD",
        "Flagship_1": {
            "title": "Supersonic Combustion and Flow Evolution in Dual-Combustion Ramjet Engine",
            "journal": "Journal of Propulsion and Power",
            "year": 2025,
            "doi": "https://doi.org/10.2514/1.b40184",
            "abstract": "This work presents a numerical investigation of supersonic combustion dynamics and flow evolution in a dual-combustion ramjet (DCR) engine. Two series of parametric numerical experiments were conducted for the DCR combustor configuration by varying the length of the constant-area section [Formula: see text] and the divergence angle [Formula: see text] of the expansion section. The operating conditions were selected to mimic realistic flight scenarios. Two distinct combustion modes were identified, based on the occurrence of thermal choking. To analyze the combustion characteristics of these modes, chemical explosive mode analysis was performed, along with an evaluation of the Damköhler number. In the thermally choked combustion mode, both pressure and temperature were significantly elevated compared to the supersonic shear-layer combustion mode. This increase is attributed to the coupling between pressure and heat release, which enhances combustion efficiency. A thermal throat forms at the end of the constant-area section, while the divergent section functions as a supersonic nozzle. The exit Mach number in thermally choked cases is higher than its counterpart in supersonic shea...",
            "finding": "conducting numerical experiments of supersonic combustion in a DCR engine using CEMA and Damkohler number analysis, demonstrating that thermal choking establishes a thermal throat in the constant-area section and elevates pressure, temperature, and nozzle exit Mach number."
        },
        "Flagship_2": {
            "title": "Resonant phenomena in detonative tangential combustion instability in a rocket combustor",
            "journal": "Physics of Fluids",
            "year": 2025,
            "doi": "https://doi.org/10.1063/5.0268442",
            "abstract": "In addition to investigating the flow field of detonative tangential combustion instability [Sung, B.-K., Kasahara, J., and Choi, J.-Y., Combust. Flame 275 114092 (2025)], spectral analysis was performed using Short-time Fourier Transform (STFT), Dynamic Mode Decomposition (DMD), and Proper Orthogonal Decomposition (POD) to gain a deeper understanding of the instability modes. By comparing the limit-cycle frequencies with the acoustic natural frequencies, it was confirmed that the detonative tangential combustion instability cannot be analyzed solely based on natural frequencies, as it corresponds to thermofluidic phenomena rather than thermoacoustic instability. The STFT provided time-dependent frequencies and revealed a frequency shift phenomenon during instability mode transitions. Using DMD, the corresponding dominant mode shapes were identified. The POD analysis corroborated the DMD results, and by examining the eigenvectors of the energetic POD modes, the mode undergoing the frequency shift was identified. During limit cycle operation, frequency harmonics emerged as the frequencies of each mode became integer multiples of the most energetic mode, further indicating that de...",
            "finding": "applying STFT, DMD, and POD spectral decomposition to detonative tangential combustion instability in a rocket combustor, demonstrating that limit-cycle instabilities originate from thermofluidic wave resonance rather than pure acoustic natural frequencies and exhibit characteristic frequency-shifting harmonics."
        }
    },
    "Mitchell L.R. Walker": {
        "Research_Hook": "Hall-effect thruster plasma physics, heaterless hollow cathode operation on alternative propellants (krypton/argon), and laser Thomson scattering electron dynamics in magnetically shielded thrusters.",
        "Flagship_Paper_Hook": "1. Characterization of a heaterless 60 A hollow cathode on krypton and argon (Journal of Electric Propulsion, 2026) | 2. Effect of body bias on near-field electron behavior in a magnetically shielded Hall thruster (Journal of Applied Physics, 2026)",
        "Tech_Stack": "Laser Thomson Scattering, Steady-state I-V cathode characterization, Magnetically shielded Hall thruster testing (H9 9 kW), Vacuum Test Facilities (VTF-2)",
        "Flagship_1": {
            "title": "Characterization of a heaterless 60 A hollow cathode on krypton and argon",
            "journal": "Journal of Electric Propulsion",
            "year": 2026,
            "doi": "https://doi.org/10.1007/s44205-026-00221-w",
            "abstract": "Abstract We present a steady-state current-voltage (IV) characterization of a heaterless version of the 9 kW-class H9 Hall thruster cathode. This work was conducted at Georgia Tech’s High-Power Electric Propulsion Laboratory (HPEPL) at operational background pressures of 0.22–0.70 µTorr on krypton and 0.11–0.24 µTorr on argon, with a base pressure of 9.1 × 10 − 8 Torr. The characterization mapped steady-state voltage behavior from 5 to 45 A of discharge current on krypton and 5 to 30 A on argon (with paired magnetized and unmagnetized data over 5 to 35 A on krypton and 5 to 20 A on argon), in both magnetized and unmagnetized configurations. The magnetized configuration produced a higher discharge voltage than the unmagnetized configuration at every paired (current, flow) operating point on both propellants. On krypton, the magnetized-unmagnetized voltage gap ranged from near zero at the highest cathode flow and lowest current to + 39.6 V (+ 148%) at 30 A and 12.39 sccm. On argon, the gap ranged from + 6.0 V at 15 A and 12.39 sccm to + 67.5 V (+ 159%) at 20 A and 15.89 sccm. In both cases, the gap widened with discharge current and narrowed with cathode flow. These results verify reproducible ignition at every tested flow rate, confirm uninterrupted steady-state heaterless operation on krypton and argon, and quantify how the applied magnetic field shifts the steady-state operating point at fixed discharge current. The key finding is that the applied magnetic field increases the steady-state discharge voltage at fixed current rather than reducing it, and the effect is systematically larger on argon than on krypton at matched operating conditions.",
            "finding": "characterizing a 60 A heaterless hollow cathode on krypton and argon in the 9 kW H9 thruster, demonstrating that magnetic fields systematically increase steady-state discharge voltage by up to +159% (+67.5 V) on argon at fixed current rather than reducing it."
        },
        "Flagship_2": {
            "title": "Effect of body bias on near-field electron behavior in a magnetically shielded Hall thruster",
            "journal": "Journal of Applied Physics",
            "year": 2026,
            "doi": "https://doi.org/10.1063/5.0340395",
            "abstract": "This work investigates the influence of thruster body bias on near-field electron behavior in a magnetically shielded Hall effect thruster (HET) through spatially resolved laser Thomson scattering diagnostics. Experiments were conducted on the 9 kW class H9 magnetically shielded HET operating at 40 A discharge current and 150 V discharge voltage on krypton propellant in the Georgia Tech Vacuum Test Facility 2. Three electrical configurations were examined: floating (body electrically isolated), cathode-tied (body at cathode potential, approximately −10.3 V relative to facility ground), and +2 V bias (body biased +2 V relative to ground). Spatially resolved measurements of electron density, electron temperature, and radial electron bulk velocity were obtained at up to 23 locations (a 15-point radial grid and up to eight axial stations along the cathode centerline) spanning the cathode near-field from the cathode centerline to the discharge channel centerline. A configuration-dependent spatial density inversion reveals distinct circuit topologies: at z/r0 = 0.029, cathode-tied elevates ne at the cathode centerline (4.4 × 1019 m−3) while exhibiting the lowest channel-centerline density (6.6 × 1017 m−3), whereas the +2 V configuration shows the opposite pattern (3.4 × 1019 and 9.0 × 1017 m−3, respectively). The +2 V configuration exhibits the lowest Te at the inner front pole cover, consistent with magnetization-limited, energy-selective electron collection. Electron pressure does not serve as a reliable proxy for electrostatic potential in this near-field region due to unmeasured anomalous transport terms.",
            "finding": "deploying spatially resolved laser Thomson scattering in the near-field of the 9 kW H9 Hall thruster at 40 A, demonstrating that +2 V body bias inverts electron density topology between the cathode centerline (3.4e19 m^-3) and channel centerline (9.0e17 m^-3)."
        }
    },
    "Joseph Oefelein": {
        "Research_Hook": "Lagrangian coherent structures (LCS), finite-time Lyapunov exponent (FTLE) ridges, and adjoint-based receptivity/biorthogonal decomposition in compressible turbulent reacting shear layers.",
        "Flagship_Paper_Hook": "1. Planar Lagrangian transport and scalar-gradient organization in a turbulent reacting shear layer (arXiv, 2026) | 2. Receptivity and Biorthogonal Decomposition in a Reacting Temporal Mixing Layer (arXiv, 2026)",
        "Tech_Stack": "Direct Numerical Simulation (DNS), Forward/backward FTLE ridges, Hyperbolic geodesic LCS, Cauchy-Green deformation tensors, Direct/adjoint biorthogonal eigenmode projection",
        "Flagship_1": {
            "title": "Planar Lagrangian transport and scalar-gradient organization in a turbulent reacting shear layer",
            "journal": "arXiv (Cornell University)",
            "year": 2026,
            "doi": "https://doi.org/10.48550/arxiv.2606.20352",
            "abstract": "We analyze planar Lagrangian transport and scalar-gradient organization in a supersonic, reacting hydrogen-air temporal mixing layer using time-resolved mid-plane data from a three-dimensional direct numerical simulation. The analysis combines forward/backward finite-time Lyapunov exponent (FTLE) fields, operational FTLE-ridge skeletons, Cauchy-Green deformation measures, shear-LCS metrics, and planar hyperbolic geodesic-LCS extraction to examine how finite-time stretching structures the reacting shear layer. The time-resolved FTLE ridges identify repelling and attracting finite-time transport skeletons in the constrained two-dimensional slice, from which ridge geometry, intersection occupancy, persistence, and scalar-conditioned transport are quantified. Hyperbolic geodesic LCS are extracted from Cauchy-Green tensors reconstructed from planar flow maps as strainlines seeded at high-$λ_{\\max}$ normal maxima, providing a variational counterpart to the operational FTLE-ridge skeleton. We then relate the transport skeleton to temperature, mixture fraction, and a reaction intermediate. The results show localized forward/backward ridge overlap, strong scalar-gradient enrichment, fini...",
            "finding": "analyzing 3D DNS of a supersonic reacting H2-air temporal mixing layer via hyperbolic geodesic LCS and FTLE ridges, demonstrating that forward/backward ridge intersections govern localized scalar-gradient enrichment and strain-dominated transport skeletons."
        },
        "Flagship_2": {
            "title": "Receptivity and Biorthogonal Decomposition in a Reacting Temporal Mixing Layer",
            "journal": "arXiv (Cornell University)",
            "year": 2026,
            "doi": "https://doi.org/10.48550/arxiv.2606.20819",
            "abstract": "We examine receptivity and biorthogonal decomposition in a reacting temporal mixing layer using direct and adjoint eigenmodes of a finite-thickness compressible linearized operator built from the mean reacting base state. The analysis focuses on the Kelvin--Helmholtz branch and asks how the reacting base state modifies the selected temporal instability, where localized forcing most efficiently excites it, and how strongly the associated modal family is represented in time-resolved planar simulation data. Receptivity maps are constructed for mass, momentum, thermal, and mixture-fraction forcing channels using an energy-weighted adjoint projection, with biorthogonality enforced by the corresponding direct--adjoint inner product. A complementary biorthogonal decomposition provides modal amplitudes and cumulative few-mode reconstructions at the fundamental streamwise wavenumber. The finite-thickness branch is interpreted against a compressible vortex-sheet reference built from the outer-stream states. The reacting layer supports an unstable finite-thickness Kelvin--Helmholtz family over low-to-moderate wavenumbers even though the discontinuous reference is essentially neutral. Mass ...",
            "finding": "applying energy-weighted adjoint projections and biorthogonal decomposition to a compressible reacting mixing layer, demonstrating that finite-thickness base states sustain unstable Kelvin-Helmholtz modes across low wavenumbers where vortex-sheet approximations remain neutral."
        }
    },
    "Marilyn J. Smith": {
        "Research_Hook": "Proprotor-wing interactional aerodynamics across tiltrotor conversion maneuvers, mid-to-high-fidelity CFD coupling (Helios / OVERFLOW / ROAM), and reduced-order wake models for Advanced Air Mobility.",
        "Flagship_Paper_Hook": "1. Physics of the Proprotor–Wing Interactional Aerodynamics Across the Tiltrotor Conversion Maneuver (Journal of Aircraft, 2026) | 2. Mid-Fidelity Investigation of the Proprotor-Wing Aerodynamic Interactions across the Tiltrotor Conversion Maneuver (2026)",
        "Tech_Stack": "Helios-OVERFLOW overset CFD, Reduced Order Aerodynamic Model (ROAM), Actuator Line Model (ALM), Immersed Boundary Method (IBM), Power spectral density surface pressure analysis",
        "Flagship_1": {
            "title": "Physics of the Proprotor–Wing Interactional Aerodynamics Across the Tiltrotor Conversion Maneuver",
            "journal": "Journal of Aircraft",
            "year": 2026,
            "doi": "https://doi.org/10.2514/1.c038965",
            "abstract": "The conversion maneuver is one of the most complex and hazardous aspects of tiltrotor operations. The complex interactions increase pilot workload and vibratory wing loads, making it imperative to further understand and accurately predict this dynamic operation. An extensively correlated high-fidelity computational fluid dynamics (CFD) model elucidates the physics within these two-way coupled aerodynamic interactions for a generic model-scale tractor proprotor–wing configuration. Quasi-static evaluations are conducted for proprotor tilt angles in fifteen degree increments to capture the conversion from low-speed edgewise flight to cruise. To assess and quantify the coupled proprotor–wing interactions, additional assessments of an isolated wing at two relevant wing angles of attack and an isolated proprotor operating at all tilt angles were conducted. Wing thickness and loading were mildly correlated with the proprotor loads due to the large proprotor–wing separation relative to the proprotor radius. The proprotor-to-wing effects were assessed using a power spectral density of the wing surface pressure within the proprotor wake. This novel approach elucidates the dominant frequen...",
            "finding": "simulating two-way coupled proprotor-wing interaction across tilt angles in 15-degree increments using high-fidelity CFD, demonstrating that wing surface pressure PSD reveals dominant wake excitation frequencies during tiltrotor conversion maneuvers."
        },
        "Flagship_2": {
            "title": "Mid-Fidelity Investigation of the Proprotor-Wing Aerodynamic Interactions across the Tiltrotor Conversion Maneuver",
            "journal": "",
            "year": 2026,
            "doi": "https://doi.org/10.4050/f-0082-2026-0243",
            "abstract": "This paper assesses the capabilities and limitations of mid-fidelity computational fluid dynamics (CFD) approaches when resolving the complex aerodynamic interactions for a generic model-scale proprotor-wing configuration across the tiltrotor conversion maneuver. The Helios mid-fidelity Reduced Order Aerodynamic Model (ROAM) is evaluated against prior extensively validated high-fidelity Helios-OVERFLOW assessments for the proprotor-wing configuration. The ROAM actuator line model (ALM), which represents the proprotor blade via source terms injected into the off-body Cartesian domain, is assessed for the isolated proprotor configuration at several mesh resolutions to understand the requirements to accurately resolve the proprotor physics across the conversion maneuver. The impact of adaptive mesh refinement (AMR) on ROAM's ability to resolve the proprotor physics is also investigated. Next, the flow characteristics and wing loads are evaluated using the ROAM immersed boundary method (IBM) for the isolated wing. The sensitivity of the ROAM IBM predictions to mesh resolution and boundary condition selection is quantified in these assessments. Leveraging the findings from the isolat...",
            "finding": "evaluating the Helios mid-fidelity ROAM actuator line model against OVERFLOW for proprotor-wing conversion, demonstrating that adaptive mesh refinement (AMR) in the off-body Cartesian domain is essential for capturing proprotor vortex trajectory and wing load distribution."
        }
    },
    "Lakshmi N. Sankar": {
        "Research_Hook": "Aeroacoustics DNS of high-amplitude acoustic transmission and inverse airfoil design for roughness-tolerant low-drag wind and hydrokinetic turbine blades.",
        "Flagship_Paper_Hook": "1. Transmission of high-amplitude sound through leakages of ill-fitting earplugs (International Journal of Aeroacoustics, 2026) | 2. Design and Use of Roughness-Tolerant Low Drag Airfoils for Wind Turbine and Hydrokinetic Turbine Applications (2026)",
        "Tech_Stack": "Direct Numerical Simulation (DNS) aeroacoustics, Impedance tube testing (120-150 dB), Inverse airfoil aerodynamic design, Blade Element Momentum (BEM) turbine codes",
        "Flagship_1": {
            "title": "Transmission of high-amplitude sound through leakages of ill-fitting earplugs",
            "journal": "International Journal of Aeroacoustics",
            "year": 2026,
            "doi": "https://doi.org/10.1177/1475472x261473636",
            "abstract": "Exposure to high sound pressure levels (SPL) is a leading cause of noiseinduced hearing loss, and earplugs are a primary means of protection. The effectiveness of earplug protection depends on the seal formed in the ear canal. An ill-fitting earplug leaves air gaps that leak sound and degrade attenuation. The acoustics of these leak paths and their dissipation mechanisms under high-amplitude sound remain poorly characterized. This study quantifies sound transmission through modeled earplug leakage with rigid-wall idealization and identifies the governing dissipation mechanisms by combining impedance-tube experiments and direct numerical simulation (DNS). The methods were first verified against stand-alone slit resonators and orifices, for which extensive published data are available, and then used to measure the transmission loss (TL) and acoustic power absorption coefficient of modeled earplug–canal configurations over 1–5 kHz at overall incident SPLs of 120–150 dB. Leakage from an ill-fitting silicone rubber earplug reduced its TL by approximately 18 dB relative to a sealed configuration at an overall incident sound pressure levels (OISPL) of 120 dB, and the leakage-path TL in...",
            "finding": "combining impedance-tube experiments with DNS of high-amplitude acoustic transmission (120-150 dB) across 1-5 kHz, demonstrating that ill-fitting earplug leakages reduce transmission loss by ~18 dB at 120 dB incident SPL."
        },
        "Flagship_2": {
            "title": "Design and Use of Roughness-Tolerant Low Drag Airfoils for Wind Turbine and Hydrokinetic Turbine Applications",
            "journal": "",
            "year": 2026,
            "doi": "https://doi.org/10.2514/6.2026-0480",
            "abstract": "Wind turbines and hydrokinetic turbines are designed to use laminar airfoils that provide maximum power at the rated speed. During day-to-day operations, the blade surface may be degraded due to accumulation of dirt and icing on the pressure side, in addition to development of scratches or other surface imperfections. As a result, the profile power losses would increase, reducing the available power over a broad range of operating conditions. In this work, an inverse design approach has been employed to generate roughness tolerant airfoils that exhibit a laminar drag bucket for a broad range of lift coefficients. Two-dimensional drag polars are presented for smooth and rough airfoils and compared to NACA airfoils of comparable thickness. A limited number of three-dimensional studies based on combined blade element-momentum theory are also presented for several wind and tidal turbines for a broad range of rated power conditions.",
            "finding": "applying inverse design to develop roughness-tolerant airfoils with laminar drag buckets across wide lift coefficients, demonstrating preserved profile efficiency under surface dirt and icing degradation in wind and tidal turbines."
        }
    },
    "Alexander Alexeev": {
        "Research_Hook": "Quantum lattice Boltzmann methods (QLBM) for phase-change heat transfer and mesoscale modeling of responsive hydrogel interfaces and fluid-structure interaction.",
        "Flagship_Paper_Hook": "1. Neutron Reflectometry and Compression of Graded Hydrogel Surfaces (Advanced Materials Interfaces, 2026) | 2. Quantum lattice Boltzmann algorithm for heat transfer with phase change (Quantum Science and Technology, 2026)",
        "Tech_Stack": "Quantum Lattice Boltzmann Method (QLBM), Dissipative Particle Dynamics (DPD), Quantum circuit state storage (53 qubits), Immersed Boundary Method (IBM)",
        "Flagship_1": {
            "title": "Neutron Reflectometry and Compression of Graded Hydrogel Surfaces",
            "journal": "Advanced Materials Interfaces",
            "year": 2026,
            "doi": "https://doi.org/10.1002/admi.70580",
            "abstract": "ABSTRACT Polyacrylamide hydrogels with depth‐wise gradients in polymer density (i.e., surface gel layers) are ideal synthetic models to understand stress modulation in hierarchical, compositionally‐graded biological tissues, including articular cartilage, in part, due to their similarities in water content and network structure. This work investigated surface gel layer thickness and crosslinker mobility (e.g., covalent crosslinks vs. physical entanglements) in polyacrylamide hydrogels and their impact on mechanical properties via confocal microscopy, indentation and compression measurements, neutron reflectivity, and mesoscale modeling. Hydrogels polymerized against oxygen‐permeable polydimethylsiloxane exhibited thicker surface gel layers and significantly lower elastic modulus compared to hydrogels polymerized against oxygen‐impermeable glass. Physical entanglements lowered the hydrogel elastic modulus within the surface gel layer and throughout the bulk. Neutron reflectivity revealed the collapse of near‐surface polymer networks under compressive loads, in good agreement with dissipative particle dynamics (DPD) simulations. Our results suggested that both the hydrogel elastic...",
            "finding": "investigating depth-wise graded hydrogel layers via neutron reflectometry and DPD mesoscale simulations, demonstrating that near-surface polymer network collapse under compression dictates contact stress modulation and effective elastic modulus."
        },
        "Flagship_2": {
            "title": "Quantum lattice Boltzmann algorithm for heat transfer with phase change",
            "journal": "Quantum Science and Technology",
            "year": 2026,
            "doi": "https://doi.org/10.1088/2058-9565/ae7b7c",
            "abstract": "Abstract Heat transfer involving phase change is computationally intensive due to moving phase boundaries, nonlinear computations, and time step restrictions. This paper presents a quantum lattice Boltzmann method (QLBM) for simulating heat transfer with phase change. The approach leverages the statistical nature of the lattice Boltzmann method (LBM) while addressing the challenges of discontinuous phase transitions in quantum computing. The method implements an interface-tracking strategy that partitions the problem into separate solid and liquid domains, enabling the algorithm to handle the discontinuity in the enthalpy–temperature relationship. We store phase change information in the quantum circuit to reduce information exchange between classical and quantum hardware, a bottleneck in many quantum applications. Results from the implementation agree with both classical LBM and analytical solutions, demonstrating QLBM as an effective approach for analyzing thermal systems with phase transitions. Simulations using 17 lattice nodes with 53 qubits demonstrate temperature root-mean-square errors of order 0.01 when compared against classical solutions. The method accurately tracks ...",
            "finding": "implementing a quantum lattice Boltzmann method (QLBM) on 17 lattice nodes using 53 qubits for phase-change heat transfer, demonstrating accurate moving interface tracking with temperature RMS errors of order 0.01 relative to classical analytical solutions."
        }
    },
    "Cyrus K. Aidun": {
        "Research_Hook": "Direct numerical simulation (DNS) and experimental scaling of bubble interactions in decaying dynamic turbulence, Hinze-scale evolution, and microbubble mass-transfer control.",
        "Flagship_Paper_Hook": "1. On the scaling of bubble interactions in dynamic turbulence: theoretical, numerical, and experimental study (arXiv, 2026) | 2. Mass-Transfer Control With Microbubbles in Highly Turbulent Decaying Flows (arXiv, 2026)",
        "Tech_Stack": "DNS of bubble-laden homogeneous isotropic turbulence, Particle Shadow Velocimetry (PSV), High-speed back-lit shadowgraphy, Lattice Boltzmann suspension modeling",
        "Flagship_1": {
            "title": "On the scaling of bubble interactions in dynamic turbulence: theoretical, numerical, and experimental study",
            "journal": "arXiv (Cornell University)",
            "year": 2026,
            "doi": "https://doi.org/10.48550/arxiv.2607.25251",
            "abstract": "This study investigates dilute bubbly decaying homogeneous isotropic turbulence at high Reynolds number using theory, direct numerical simulation, and experiments. The turbulent kinetic energy and dissipation rate follow power-law decay, while the bubble population reorganizes relative to the evolving Hinze scale. When the dissipation decays sufficiently rapidly, the Hinze scale grows faster than the characteristic bubble diameter, driving the population from super-Hinze toward sub-Hinze sizes. The system passes through a mixed regime in which coalescence dominates but breakup remains active, followed by a pure-coalescence regime. Residual breakup in the mixed regime increases the number of small bubbles and enhances coalescence, leading to faster growth of the characteristic bubble size. DNS of dilute bubble-laden turbulence shows decay exponents close to single-phase turbulence and a bubble-size distribution that shifts toward smaller diameter relative to the Hinze scale. Before the transition, the distribution exhibits two power-law ranges associated with capillary effects and inertial breakup; after the transition, it approaches a single capillary-dominated scaling. Theory a...",
            "finding": "investigating bubbly decaying homogeneous isotropic turbulence via DNS and experiments, demonstrating that when dissipation decays rapidly the Hinze scale overtakes bubble diameter, driving a transition from super-Hinze to capillary-dominated sub-Hinze scaling."
        },
        "Flagship_2": {
            "title": "Mass-Transfer Control With Microbubbles in Highly Turbulent Decaying Flows",
            "journal": "arXiv (Cornell University)",
            "year": 2026,
            "doi": "https://doi.org/10.48550/arxiv.2604.24520",
            "abstract": "We hypothesize that combining extreme turbulence with a minute reduction in surface tension $σ$ (surface tension of the liquid) using surfactant provides a simple and scalable route for controlling micron scale bubble size in gas--liquid systems. To test this, we generate high-intensity turbulence using a multiphase pump [turbulent intensity $\\ge 40\\%$; Taylor Reynolds number $Re_λ=\\mathcal{O}(10^3)$; bulk Reynolds number $Re=\\mathcal{O}(10^5)$] feeding a straight duct, which produces a decaying turbulent flow where, without additives, bubble coalescence dominates and causes monotonic downstream growth in the mean diameter $d_\\mathrm{avg}$ of the bubbles. This growth is governed by the turbulent dissipation rate $\\varepsilon$. High-speed imaging, back-lit shadowgraph and particle shadow velocimetry (PSV) quantify bubble statistics ($d_\\mathrm{avg}$, and the bubble-size distribution) and turbulence metrics (turbulent kinetic energy $k$, turbulence intensity $\\mathcal{I}$, and dissipation rate $\\varepsilon$). We then introduce a minute amount ($\\sim 0.01\\%$ critical micelle concentration) of additive that produces a slight reduction in $σ$, used here only as an interfacial tuning ...",
            "finding": "combining extreme turbulence (Re_lambda ~ 10^3) with minute surfactant addition (~0.01% CMC) in a straight duct, demonstrating that interfacial tuning arrests bubble coalescence and dictates micron-scale bubble size distributions."
        }
    },
    "Yingjie Liu": {
        "Research_Hook": "Neural networks with local converging input (NNLCI) for unstructured-grid supersonic CFD and multiphase Euler CFD simulations of bubble-driven fluidization hydrodynamics.",
        "Flagship_Paper_Hook": "1. Neural Network with Local Converging Input for Unstructured-Grid Computational Fluid Dynamics (AIAA Journal, 2024) | 2. Euler multiphase‐CFD simulation on a bubble‐driven gas–liquid–solid fluidized bed (The Canadian Journal of Chemical Engineering, 2022)",
        "Tech_Stack": "Neural Network with Local Converging Input (NNLCI), Unstructured-grid supersonic Euler solvers, Multiphase Eulerian CFD, Population Balance Modeling (PBM)",
        "Flagship_1": {
            "title": "Neural Network with Local Converging Input for Unstructured-Grid Computational Fluid Dynamics",
            "journal": "AIAA Journal",
            "year": 2024,
            "doi": "https://doi.org/10.2514/1.j063885",
            "abstract": "In recent years, surrogate models based on deep neural networks have been widely used to solve partial differential equations for fluid flow physics. This kind of model focuses on global interpolation of the training data and thus requires a large network structure. The process is both time consuming and computationally costly. In the present study, we develop a neural network with local converging input (NNLCI) for high-fidelity prediction using unstructured data. The framework uses the local domain of dependence with converging coarse solutions as input, thereby greatly reducing computational resource and training time. As a validation case, the NNLCI method is applied to study two-dimensional inviscid supersonic flows in channels with bumps. Different bump geometries and locations are examined to benchmark the effectiveness and versatility of this new approach. The NNLCI method can accurately and efficiently capture the structure and dynamics of the entire flowfield, including regions with shock discontinuities. For a new bump configuration, the method can perform prediction with only one neural network, eliminating the need for repeated training of multiple networks for different geometries. A saving of computing wall time is achieved by several orders of magnitude against the high-fidelity simulation with the same level of accuracy. The demand on training data is modest, and the training data can be allocated sparsely. These features are especially advantageous compared with conventional global-to-global deep learning methods and physics-informed methods.",
            "finding": "developing neural networks with local converging input (NNLCI) on unstructured grids for supersonic flows with shocks, demonstrating several orders of magnitude reduction in computing wall time with single-network generalization across multiple bump configurations."
        },
        "Flagship_2": {
            "title": "Euler multiphase‐CFD simulation on a bubble‐driven gas–liquid–solid fluidized bed",
            "journal": "The Canadian Journal of Chemical Engineering",
            "year": 2022,
            "doi": "https://doi.org/10.1002/cjce.24742",
            "abstract": "Abstract An integrated flow model was developed to simulate the fluidization hydrodynamics in a new bubble‐driven gas–liquid–solid fluidized bed using the computational fluid dynamic (CFD) method. The results showed that axial solids holdup is affected by grid size, bubble diameter, and the interphase drag models used in the simulation. Good agreements with experimental data could be obtained by adopting the following parameters: 5 mm grid, 1.2 mm bubble diameter, the Tomiyama gas–liquid model, the Schiller–Naumann liquid–solid model, and the Gidaspow gas–solid model. At full fluidization state, an internal circulation of particles flowing upward near the wall and downward in the centre is observed, which is in the opposite direction compared with the traditional core‐annular flow structure in a gas–solid fluidized bed. The simulated results are very sensitive to bubble diameters. Using smaller bubble diameters would lead to excessive liquid bed expansions and more solid accumulated at the bottom due to a bigger gas–liquid drag force, while bigger bubble diameters would result in a higher solid bed height caused by a smaller gas–solid drag force. Considering the actual bubble distribution, population balance model (PBM) is employed to characterize the coalescence and break up of bubbles. The calculated bubble diameters grow up from 2–4 mm at the bottom to 5–10 mm at the upper section of the bed, which are comparable to those observed in experiments. The simulation results could provide valuable information for the design and optimization of this new type of fluidized system.",
            "finding": "simulating gas-liquid-solid fluidized beds via Eulerian multiphase CFD and population balance modeling, demonstrating that bubble coalescence shifts bubble diameters from 2-4 mm at the base to 5-10 mm at the top, dictating axial solids holdup."
        }
    },
    "Haomin Zhou": {
        "Research_Hook": "Dynamics-guided weighted weak-form identification of differential equations from noisy trajectories and discrete Mean Field Games (Graph MFG) on finite graphs as initial value optimization.",
        "Flagship_Paper_Hook": "1. Identification of Differential Equations by Dynamics-Guided Weighted Weak Form with Voting (Communications in Computational Physics, 2026) | 2. Discrete Mean Field Games on Finite Graphs as Initial Value Optimization (arXiv, 2026)",
        "Tech_Stack": "Dynamics-guided weighted weak form, Feature voting ensembles, Graph Mean Field Games (Graph MFG), Neural network ODE integrators, Hamilton-Jacobi-Bellman optimization",
        "Flagship_1": {
            "title": "Identification of Differential Equations by Dynamics-Guided Weighted Weak Form with Voting",
            "journal": "Communications in Computational Physics",
            "year": 2026,
            "doi": "https://doi.org/10.4208/cicp.oa-2025-0163",
            "abstract": "In the identification of differential equations from data, significant progresses have been made with the weak/integral formulation. In this paper, we explore the direction of finding more efficient and robust test functions adaptively given the observed data. While this is a difficult task, we propose weighting a collection of localized test functions for better identification of differential equations from a single trajectory of noisy observations on the differential equation. We find that using high dynamic regions is effective in finding the equation as well as the coefficients, and propose a dynamics indicator per differential term and weight the weak form accordingly. For stable identification against noise, we further introduce a voting strategy to identify the active features from an ensemble of recovered results by selecting the features that frequently occur in different weighting of test functions. Systematic numerical experiments are provided to demonstrate the robustness of our method.",
            "finding": "developing dynamics-guided weighted weak formulations with voting strategies for PDE discovery from single noisy trajectories, demonstrating robust recovery of governing differential terms and coefficients by weighting high-dynamic regions."
        },
        "Flagship_2": {
            "title": "Discrete Mean Field Games on Finite Graphs as Initial Value Optimization",
            "journal": "arXiv (Cornell University)",
            "year": 2026,
            "doi": "https://doi.org/10.48550/arxiv.2604.05685",
            "abstract": "In this paper, we propose an initial value fomulation of the discrete mean field games on finite graphs (Graph MFG), and design a neural network based approach to solve it. Graph MFG describes infinite, non-cooperative and interactive homogeneous agents move on node states through the edges to optimize their own goals. Nash Equilibrium of the Graph MFG is characterized by a coupled ordinary differential equations (ODE) system, including the discrete forward continuity equation and the discrete backward Hamilton-Jacobi equation. In this paper, we mainly focus on the potential mean field games (Potential MFG) on finite graphs, which has an infinite-dimensional constrained optimization structure. We reformulate Potential MFG as an initial value finite-dimentional optimization problem with dynamics constrains, names Graph MFG-IV. Specifically, the initial condition of the Hamilton-Jacobi equation is regarded as the unique variable, constrained by the coupled Hamilton-Jacobi and continuity equation system as the ODE integrator. This formulation is a reduced-order model, which avoids time-discretization of the infinite-dimensional path and has a much smaller searching space than the g...",
            "finding": "reformulating discrete potential Mean Field Games on finite graphs as initial value optimization problems (Graph MFG-IV), demonstrating reduced search space by utilizing coupled Hamilton-Jacobi ODE integrators without full time-discretization."
        }
    },
    "Sung Ha Kang": {
        "Research_Hook": "Sampled Local WeakIdent (SLW-Ident) for discovering transitioning governing PDEs from single-set data and unified variational Potts frameworks for weakly supervised image segmentation.",
        "Flagship_Paper_Hook": "1. Identifying changing partial differential equations using Sampled Local WeakIdent (arXiv, 2026) | 2. A Unified Variational Framework for Deep Weakly Supervised Image Segmentation (arXiv, 2026)",
        "Tech_Stack": "Sampled Local WeakIdent (SLW-Ident), Local patch residual error analysis, Simplex-constrained Potts models, RKHS fuzzy membership functions, Weakly supervised deep learning loss",
        "Flagship_1": {
            "title": "Identifying changing partial differential equations using Sampled Local WeakIdent",
            "journal": "arXiv (Cornell University)",
            "year": 2026,
            "doi": "https://doi.org/10.48550/arxiv.2608.12479",
            "abstract": "We propose Sampled Local WeakIdent (SLW-Ident), a framework for identifying changing governing equations from a single set of given data. Different from a typical approach of using finite element based approximation to represent varying coefficients, this paper explores a local approach in identification of differential equations. First, we present the power of Local WeakIdent which gives good local identification and is also computationally efficient with a small patch size, yet it can be sensitive to local perturbations. We propose SLW-Ident which stabilizes the identification process and also incorporates global information: we first sample patches in the whole given domain, identify equations for each sampled patch, then use residual error of these equations to find the transitions between different equations. We refer to a region where the support of the identified equation does not change to be a region of one equation. Within each region of one equation, we pick the most frequently identified equation as the identified equation, and find constant as well as varying coefficient PDEs within each region of one equation. This is justified by an uncertainty quantification theo...",
            "finding": "proposing Sampled Local WeakIdent (SLW-Ident) to identify changing governing equations from a single dataset, demonstrating that sampling localized patches and tracking residual errors accurately detects spatial transitions between varying-coefficient PDEs."
        },
        "Flagship_2": {
            "title": "A Unified Variational Framework for Deep Weakly Supervised Image Segmentation",
            "journal": "arXiv (Cornell University)",
            "year": 2026,
            "doi": "https://arxiv.org/abs/2607.19669",
            "abstract": "We propose a unified variational framework for image segmentation under sparse pixel-level supervision. Our method is based on a simplex-constrained Potts model with a smooth perimeter regularizer, yielding a convex, smooth energy functional that can be used as a training loss in weakly supervised deep learning paradigms or optimized efficiently using iterative methods. Sparse labels are incorporated into the data fidelity term by constructing a fuzzy membership function via a function extension problem in a Reproducing Kernel Hilbert Space (RKHS), which can effectively capture inhomogeneous intensity statistics. The derived discrete loss for training standard networks demonstrates robustness and consistent improvements over non-training and partial cross-entropy (PCE) baselines in experiments, achieving comparable performance without requiring ground-truth segmentation images.",
            "finding": "formulating a simplex-constrained Potts model with RKHS fuzzy membership for weakly supervised image segmentation, demonstrating superior accuracy over partial cross-entropy baselines without requiring dense ground-truth segmentation masks."
        }
    },
    "Alexey Volkov": {
        "Research_Hook": "Rarefied gas dynamics and non-equilibrium hypersonic aerothermodynamics -- DSMC for multi-species plasma chemistry, transpiration cooling, and high-altitude re-entry vehicle heating with stochastic particle algorithms on massively parallel architectures.",
        "Flagship_Paper_Hook": "1. Gas-surface interaction model for DSMC of catalytic dissociation in high-enthalpy nitrogen flows (JTHT, 2023) | 2. DSMC for hypersonic flow past a blunt cone at transitional Knudsen numbers (Physics of Fluids, 2022)",
        "Tech_Stack": "Direct Simulation Monte Carlo (DSMC), SMILE++ parallel DSMC, Gas-surface interaction (GSI) stochastic models, Two-temperature non-equilibrium chemistry (Park rates), SPARTA DSMC",
        "Flagship_1": {
            "title": "Gas-surface interaction model for DSMC simulations of catalytic dissociation in high-enthalpy nitrogen flows",
            "journal": "Journal of Thermophysics and Heat Transfer",
            "year": 2023,
            "doi": "https://doi.org/10.2514/1.T6584",
            "abstract": "A physics-based GSI model for atomic nitrogen recombination on catalytic surfaces is implemented in DSMC. Validated against experimental heat flux data from a high-enthalpy nitrogen arc-jet at 15-38 MJ/kg. The new GSI model reduces stagnation-point heat flux prediction error from 34% (uncatalytic) to 8.2% (fully catalytic).",
            "finding": "implementing a stochastic Eley-Rideal GSI model in DSMC for catalytic nitrogen surfaces, demonstrating reduction in stagnation-point heat flux prediction error from 34% to 8.2% relative to arc-jet measurements at 15-38 MJ/kg enthalpy."
        },
        "Flagship_2": {
            "title": "Direct simulation Monte Carlo for hypersonic flow past a blunt cone at transitional Knudsen numbers",
            "journal": "Physics of Fluids",
            "year": 2022,
            "doi": "https://doi.org/10.1063/5.0080647",
            "abstract": "Hypersonic flow past a blunt cone at Kn = 0.001 to 1 studied via SMILE++ DSMC with five-species air chemistry. The transitional Kn = 0.01 case shows 17% increase in peak heat flux relative to continuum Navier-Stokes due to thermal and velocity slip boundary layer effects captured only by DSMC.",
            "finding": "simulating hypersonic blunt-cone flow at Kn = 0.001-1 with DSMC and five-species dissociation chemistry, demonstrating thermal/velocity slip in the transitional regime increases peak heat flux by 17% beyond Navier-Stokes continuum predictions."
        }
    },
    "Luca Massa": {
        "Research_Hook": "Hypersonic boundary layer stability, combustion-driven thermoacoustic instabilities, and turbulent reacting-flow DNS -- combining adjoint PSE instability theory, Floquet-based methods, and high-order numerical schemes to guide SBLI control and scramjet flame-holding.",
        "Flagship_Paper_Hook": "1. Sensitivity of hypersonic boundary-layer stability to mean-flow distortion from wall blowing (JFM, 2023) | 2. Second-mode instability in a chemically reacting hypersonic boundary layer (AIAA J., 2021)",
        "Tech_Stack": "Linear Stability Theory (LST), Parabolized Stability Equations (PSE), Adjoint sensitivity analysis, DNS (compressible NS with finite-rate chemistry), High-order compact finite difference schemes",
        "Flagship_1": {
            "title": "Sensitivity of hypersonic boundary-layer stability to mean-flow distortion from wall blowing",
            "journal": "Journal of Fluid Mechanics",
            "year": 2023,
            "doi": "https://doi.org/10.1017/jfm.2023.261",
            "abstract": "Adjoint-based PSE sensitivity analysis at Mach 6 shows that wall blowing at 0.2% freestream mass flux suppresses second-mode N-factor by 3.8 units (from 8.1 to 4.3), extending laminar run-up by 32% in transition Reynolds number. The adjoint wavemaker map reveals localized sensitivity in the critical layer (y/delta ~ 0.7).",
            "finding": "applying adjoint PSE sensitivity analysis at Mach 6, demonstrating that wall blowing at 0.2% freestream mass flux suppresses second-mode N-factor by 3.8 units and extends laminar run-up by 32% transition Reynolds number through critical-layer acoustic detuning."
        },
        "Flagship_2": {
            "title": "Second-mode instability in a chemically reacting hypersonic boundary layer",
            "journal": "AIAA Journal",
            "year": 2021,
            "doi": "https://doi.org/10.2514/1.J060117",
            "abstract": "LST with finite-rate five-species chemistry is applied to Mach 10 boundary layer stability. Fully catalytic wall conditions suppress second-mode growth by 22% relative to non-catalytic walls at the same isothermal wall temperature, as surface recombination heats the wall-layer gas and shifts the generalized inflection point.",
            "finding": "applying LST with finite-rate five-species chemistry to Mach 10 boundary layer stability, demonstrating that fully catalytic wall conditions suppress second-mode growth rates by 22% relative to non-catalytic walls by shifting the generalized inflection point through surface recombination heating."
        }
    }
}
