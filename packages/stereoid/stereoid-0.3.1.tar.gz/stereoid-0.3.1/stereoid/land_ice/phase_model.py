from mpmath import hyp2f3, hyp2f1, hyp3f2, mpf
from scipy.special import loggamma
import numpy as np
import matplotlib.pyplot as plt

"""
Test:
L = 10
self = PhaseModel()
self.create_lookup_table(L)
self.plot(L)

coh_values = [0.1, 0.2, 0.3, 0.4]
cor_coh, std = self(coh_values, 2)
"""


class PhaseModel():


    def __init__(self, approx_steps=101, phase_steps=101):
        """
        This defines the uncertainty in the phase based on coherence and multilook values.

        """

        self.coherence = np.linspace(0, 1, approx_steps)
        self.lookup_coh_bias = dict()
        self.lookup_coh_std = dict()
        self.lookup_phase_std = dict()
        self.lookup_coh_biased = dict()
        self.lookup_phase_std_cramer_rao = dict()

        self.phase_steps = phase_steps
        self.approx_steps = approx_steps

    def create_lookup_table(self, n_looks):
        """
        Creates a lookup table for a defined number of looks.

        :param n_looks:
        :return:
        """

        self.create_coherence_lookup(n_looks)
        self.create_phase_lookup(n_looks)

    def interp_coh_real(self, n_looks, coherences):
        """
        Find the estimated standard deviation using a lookup table.

        :param n_looks:
        :param coherences:
        :return:
        """

        L = str(n_looks)

        coh_ids = np.floor(coherences * (len(self.coherence) - 1)).astype(np.int32)
        coh_ids[coh_ids > self.phase_steps - 2] = self.phase_steps - 2
        coh_rest = (coherences * (len(self.coherence) - 1) - coh_ids)
        std_phase = self.lookup_phase_std[L][coh_ids] * (1 - coh_rest) + self.lookup_phase_std[L][coh_ids + 1] * coh_rest

        std_phase[std_phase < 0.0001] = 0.0001

        return std_phase

    def interp_coh_estimated(self, n_looks, coherences, std_offset=0):
        # This function takes any array with coherence values and estimates the coherence value plus a std offset for
        # these points. Default is a std of 0

        L = str(n_looks)

        # Remove the bias
        coh_ids = np.floor(coherences * (len(self.coherence) - 1)).astype(np.int32)
        coh_ids[coh_ids > self.phase_steps - 2] = self.phase_steps - 2
        coh_rest = (coherences * (len(self.coherence) - 1) - coh_ids)
        coh_unbiased = coherences - (self.lookup_coh_bias[L][coh_ids] * (1 - coh_rest) + self.lookup_coh_bias[L][coh_ids + 1] * coh_rest)

        # Remove standard deviation
        coh_ids = np.floor(coh_unbiased * (len(self.coherence) - 1)).astype(np.int32)
        coh_ids[coh_ids > self.phase_steps - 2] = self.phase_steps - 2
        coh_rest = (coh_unbiased * (len(self.coherence) - 1) - coh_ids)
        coh_std_corrected = coh_unbiased - std_offset * (self.lookup_coh_std[L][coh_ids] * (1 - coh_rest) + self.lookup_coh_std[L][coh_ids + 1] * coh_rest)
        coh_std_corrected[coh_std_corrected < 0] = 0

        # Now get the standard deviation under this assumption
        std_corrected = self.interp_coh_real(n_looks, coh_std_corrected)

        return std_corrected, coh_std_corrected, coh_unbiased

    def create_phase_lookup(self, n_looks):
        """
        Based on the real coherence and number of looks we can approximate the phase using the analytical function.

        :param n_looks:
        :return:
        """

        L = str(n_looks)

        self.lookup_phase_std[L] = np.zeros(self.approx_steps)
        phases = np.pi * np.arange(-self.phase_steps + 1, self.phase_steps) / (self.phase_steps - 1)

        # Get the probability density density function for different real coherence values.
        for coh, id in zip(self.coherence, range(self.approx_steps)):

            if n_looks > (1 - coh) * 4000 + 150:
                fL = (1 - coh) * 4000 + 150
            else:
                fL = n_looks

            beta = coh * np.cos(phases)
            prob_curve = np.zeros(self.phase_steps * 2 - 1)

            if coh == 0:
                self.lookup_phase_std[L][id] = 2 * np.pi / np.sqrt(12)
            elif coh == 1:
                self.lookup_phase_std[L][id] = 0
            else:
                for b, i in zip(beta, np.arange(self.phase_steps * 2 - 1)):
                    prob_curve[i] = np.exp(loggamma(fL + 0.5) - loggamma(fL)) * (mpf(1 - coh**2)**fL * b) / (
                                    2 * np.sqrt(np.pi) * mpf(1 - b**2)**(fL + 0.5)) + (
                                    mpf(1 - coh**2)**fL / (2 * np.pi) * hyp2f1(fL, 1, 0.5, b**2))
                self.lookup_phase_std[L][id] = np.sqrt(np.trapz(phases**2 * prob_curve, phases))

    def create_coherence_lookup(self, n_looks):
        """
        Create lookup table using analytical functions.

        :param n_looks:
        :return:
        """

        L = str(n_looks)
        self.lookup_coh_biased[L] = np.zeros(self.approx_steps)
        self.lookup_coh_bias[L] = np.zeros(self.approx_steps)
        self.lookup_coh_std[L] = np.zeros(self.approx_steps)

        for coh, i in zip(self.coherence, range(self.approx_steps)):
            if coh == 1:
                self.lookup_coh_biased[L][i] = 1
                self.lookup_coh_std[L][i] = 0
            else:
                if n_looks > (1 - coh) * 3000 + 10:
                    fL = (1 - coh) * 3000 + 10
                else:
                    fL = n_looks

                self.lookup_coh_biased[L][i] = np.exp(loggamma(fL) + loggamma(1.5) - loggamma(fL + 0.5)) * hyp3f2(1.5, fL, fL, fL + 0.5, 1, coh**2) * mpf(1 - coh**2)**fL
                var = np.exp(loggamma(fL) + loggamma(2) - loggamma(fL + 1)) * hyp3f2(2, fL, fL, fL + 1, 1, coh**2) * mpf(1 - coh**2)**fL - self.lookup_coh_biased[L][i]**2
                if var < 0:
                    self.lookup_coh_std[L][i] = 0
                else:
                    self.lookup_coh_std[L][i] = np.sqrt(var)

        # Interpolate the coh_bias to a series where the biased values are an input.
        first_valid = np.where(self.coherence >= self.lookup_coh_biased[L][0])[0][0]
        self.lookup_coh_bias[L][first_valid:] = np.interp(self.coherence[first_valid:], self.lookup_coh_biased[L], self.coherence)
        self.lookup_coh_bias[L] = self.coherence - self.lookup_coh_bias[L]

    def create_lookup_cramer_rao_bound(self, n_looks):
        """
        Simple approximation using the cramer rao bound. Only holds for high coherences

        :return:
        """

        L = str(n_looks)

        # For now we just use the cramer rao bound instead of more complicated calculations.
        self.lookup_phase_std_cramer_rao[L] = 1 / np.sqrt(2 * n_looks) * (np.sqrt(1 - self.coherence**2) / self.coherence)

    def plot(self, n_looks):
        """


        :param n_looks:
        :return:
        """

        L = str(n_looks)

        plt.figure()
        plt.plot(self.coherence, self.coherence)
        plt.plot(self.coherence, self.lookup_coh_biased[L])
        plt.plot(self.coherence, self.lookup_coh_bias[L])
        plt.show()
        plt.figure()
        plt.plot(self.coherence, self.lookup_coh_std[L])
        plt.show()
        plt.figure()
        plt.plot(self.coherence, self.lookup_phase_std[L] / np.pi * 180)
        plt.show()
