# From quantum to classical modeling of radiation reaction: A focus on stochasticity effects

Original authors: F. Niel, C. Riconda, F. Amiranoff, R. Duclous, and M. Grech

Citation: Niel et al, Phys. Rev. E 97, 043209 (2018)

Link to paper: https://journals.aps.org/pre/abstract/10.1103/PhysRevE.97.043209

(Partially) reproduced by: [Óscar Amaro](https://github.com/OsAmaro)

The paper includes comparison between 3 regimes of radiation reaction: classical Landau-Lifschitz, Fokker-Planck and Boltzmann-Monte-Carlo.
In this notebook we only apply the Fokker-Planck pusher to reproduce figure 10 of the paper, where an electron beam loses energy as it interacts with a uniform-constant magnetic field.

Abstract: _Radiation reaction in the interaction of ultrarelativistic electrons with a strong external electromagnetic field is investigated using a kinetic approach in the nonlinear moderately quantum regime. Three complementary descriptions are discussed considering arbitrary geometries of interaction: a deterministic one relying on the quantum-corrected radiation reaction force in the Landau and Lifschitz (LL) form, a linear Boltzmann equation for the electron distribution function, and a Fokker-Planck (FP) expansion in the limit where the emitted photon energies are small with respect to that of the emitting electrons. The latter description is equivalent to a stochastic differential equation where the effect of the radiation reaction appears in the form of the deterministic term corresponding to the quantum-corrected LL friction force, and by a diffusion term accounting for the stochastic nature of photon emission. By studying the evolution of the energy moments of the electron distribution function with the three models, we are able to show that all three descriptions provide similar predictions on the temporal evolution of the average energy of an electron population in various physical situations of interest, even for large values of the quantum parameter χ. The FP and full linear Boltzmann descriptions also allow us to correctly describe the evolution of the energy variance (second-order moment) of the distribution function, while higher-order moments are in general correctly captured with the full linear Boltzmann description only. A general criterion for the limit of validity of each description is proposed, as well as a numerical scheme for the inclusion of the FP description in particle-in-cell codes. This work, not limited to the configuration of a monoenergetic electron beam colliding with a laser pulse, allows further insight into the relative importance of various effects of radiation reaction and in particular of the discrete and stochastic nature of high-energy photon emission and its back-reaction in the deformation of the particle distribution function._


__Notes__:

Evolution of energy moments of distribution. Normalization $\int f~d \gamma = 1$.

Vlasov-Fokker-Plank equation $d_t f = C[f] = \partial_\gamma [S f] + 0.5 \partial_{\gamma \gamma}[R f]$

Mean energy:

$$d_t \langle \gamma \rangle = \int ~\gamma ~d_t f ~d\gamma = \int \gamma \partial_\gamma [S f] + 0.5\gamma~ \partial_{\gamma \gamma}[R f]~d\gamma=$$

$$=(\gamma S f)| - \int S f d\gamma + 0.5(\gamma \partial_\gamma[R f])|-0.5 \int \partial_\gamma[R f] d\gamma=$$

$$= -\int S f d\gamma = -\langle S \rangle$$

Mean square energy:

$$d_t \langle \gamma^2 \rangle = \int \gamma^2 ~d_t f ~ d\gamma = \int \gamma^2 \partial_\gamma [S f] + 0.5\gamma^2~ \partial_{\gamma \gamma}[R f]~d\gamma =$$

$$=(\gamma^2 S f)| - 2\int \gamma ~S f d\gamma + 0.5(\gamma^2  \partial_\gamma[R f])|- \int \gamma~\partial_\gamma[R f] d\gamma=$$

$$=- 2\int \gamma ~S f d\gamma - (\gamma R f)| + \int R f d\gamma = -2 \langle \gamma S\rangle + \langle R \rangle$$

where $X| = X|_1^\infty$ and assuming $f(\gamma\rightarrow \infty) \rightarrow 0$
